"""Immutable evidence storage, claim validation and readiness rules."""
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
import sqlite3
import re
from urllib.parse import urlsplit

FIELDS = {'registration_deadline', 'submission_deadline', 'prize', 'eligibility', 'automation', 'license'}


def validate_claim(field,value,quote,body):
    if not isinstance(field,str) or field not in FIELDS or not isinstance(quote,str) or not quote or not isinstance(value,str) or not value.strip():
        raise ValueError('Invalid claim')
    if not isinstance(body,str) or quote not in body:
        raise ValueError('Claim must cite an exact source passage')
    if value not in quote:
        raise ValueError('Value must be a verbatim substring of its source quote; interpretation needs review')
    if field.endswith('_deadline'):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?[+-]\d{2}:\d{2}',value):
            raise ValueError('Deadline needs full ISO date, time and explicit numeric UTC offset')
        dt.datetime.fromisoformat(value)

class EvidenceStore:
    def __init__(self, path=':memory:'):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self._atomic_depth = 0
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,url TEXT NOT NULL,body TEXT NOT NULL,observed_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS extraction_sets(source_id TEXT PRIMARY KEY,digest TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS claims(id INTEGER PRIMARY KEY,source_id TEXT NOT NULL,field TEXT NOT NULL,value TEXT NOT NULL,quote TEXT NOT NULL,start INTEGER NOT NULL,end INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY,source_id TEXT NOT NULL,decision TEXT NOT NULL,reviewer TEXT NOT NULL,at TEXT NOT NULL);
        ''')
    def _commit(self):
        if not self._atomic_depth:self.db.commit()
    @contextmanager
    def atomic(self):
        if self._atomic_depth:raise ValueError('Nested evidence transaction not supported')
        self.db.execute('BEGIN IMMEDIATE')
        self._atomic_depth=1
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        finally:self._atomic_depth=0
    def snapshot(self, url, body, observed_at=None):
        if not isinstance(url,str) or not isinstance(body,str):
            raise ValueError('Source URL and body must be text')
        if any(ord(ch)<33 or ch in '"<>`' for ch in url):
            raise ValueError('Invalid characters in source URL')
        parts=urlsplit(url)
        if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password:

            raise ValueError('HTTPS source URL required')
        source_id = hashlib.sha256((url+'\0'+body).encode()).hexdigest()
        self.db.execute('INSERT OR IGNORE INTO sources VALUES(?,?,?,?)', (source_id,url,body,observed_at or dt.datetime.now(dt.timezone.utc).isoformat()))
        self._commit()
        return source_id
    def claim(self, source_id, field, value, quote):
        row = self.db.execute('SELECT body FROM sources WHERE id=?', (source_id,)).fetchone()
        if row is None:raise ValueError('Unknown source')
        validate_claim(field,value,quote,row['body'])
        start = row['body'].index(quote)
        self.db.execute('INSERT INTO claims(source_id,field,value,quote,start,end) VALUES(?,?,?,?,?,?)',(source_id,field,value,quote,start,start+len(quote)))
        self._commit()
    def source(self, source_id):
        row=self.db.execute('SELECT * FROM sources WHERE id=?',(source_id,)).fetchone()
        if row is None:raise ValueError('Unknown source')
        return dict(row)
    def reviews(self, source_id):
        return [dict(r) for r in self.db.execute('SELECT * FROM reviews WHERE source_id=? ORDER BY id',(source_id,))]
    def claims(self, source_id):
        return [dict(r) for r in self.db.execute('SELECT * FROM claims WHERE source_id=? ORDER BY field,id',(source_id,))]
    def diff(self, before, after):
        a,b = self.claims(before),self.claims(after)
        values = lambda rs,k: sorted({r['value'] for r in rs if r['field']==k})
        return [{'field':k,'before':values(a,k),'after':values(b,k),'evidence':[r for r in b if r['field']==k],'previous_evidence':[r for r in a if r['field']==k]} for k in sorted(FIELDS) if values(a,k)!=values(b,k)]
    def readiness(self, source_id):
        claims = self.claims(source_id)
        missing = sorted(FIELDS-{r['field'] for r in claims})
        conflicts = sorted(k for k in FIELDS if len({r['value'] for r in claims if r['field']==k})>1)
        # Quoted source text can support facts but can never approve participation.
        return {'state':'REVIEW REQUIRED','missing':missing,'conflicts':conflicts,'can_submit':False,'evidence_status':'Quoted, not independently verified','checklist':['Check eligibility and original licenses','Review full legal terms','Confirm AI/automation scope','Human review before any external action']}
    def review(self, source_id, decision, reviewer):
        if not isinstance(decision,str) or decision not in {'reviewed','needs_changes'} or not isinstance(reviewer,str) or not reviewer.strip() or len(reviewer)>100:
            raise ValueError('Review identity and valid decision required')
        if not isinstance(source_id,str) or not self.db.execute('SELECT id FROM sources WHERE id=?',(source_id,)).fetchone():
            raise ValueError('Unknown source')
        self.db.execute('INSERT INTO reviews(source_id,decision,reviewer,at) VALUES(?,?,?,?)',(source_id,decision,reviewer,dt.datetime.now(dt.timezone.utc).isoformat()))
        self._commit()
        return {'recorded':True,'external_action':False}

def normalize_time(iso, zone):
    from zoneinfo import ZoneInfo
    t=dt.datetime.fromisoformat(iso)
    if t.tzinfo is None:
        raise ValueError('Explicit source offset required')
    return t.astimezone(ZoneInfo(zone)).isoformat()
