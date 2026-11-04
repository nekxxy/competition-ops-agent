"""Deterministic review prompts. Never a legal or eligibility decision."""
from .core import normalize_time

def review_plan(claims,readiness,zone='Asia/Kolkata'):
    deadlines=[]
    for c in claims:
        if c['field'].endswith('_deadline'):
            deadlines.append({'field':c['field'],'source_value':c['value'],'local_value':normalize_time(c['value'],zone),'zone':zone,'conflicting':c['field'] in readiness['conflicts']})
    tasks=[]
    for field in readiness['missing']:
        tasks.append({'priority':'BLOCKED','field':field,'task':'Find an explicit current source passage; do not guess.'})
    for field in readiness['conflicts']:
        tasks.append({'priority':'BLOCKED','field':field,'task':'Compare conflicting passages with the organizer source; do not choose automatically.'})
    for field,instruction in [('eligibility','Check your eligibility against the full rules.'),('automation','Review the exact AI/automation policy before any tool-driven participation.'),('license','Audit code, data and model licenses separately.'),('prize','Check the full reward passage: total pool versus per-winner amount, split, conditions, cash versus credits or a pilot. A shorter extracted amount can lose qualifiers even when its quote is valid.')]:
        if any(c['field']==field for c in claims):tasks.append({'priority':'REVIEW','field':field,'task':instruction})
    return {'zone':zone,'deadlines':deadlines,'tasks':tasks,'can_submit':False,'disclaimer':'Planning prompts, not permission or legal advice.'}
