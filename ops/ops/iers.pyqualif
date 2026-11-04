"""Deterministic advisory for monetary qualifiers omitted from an extracted value.

Pure functions only: no state, no I/O, no network. Advisories never modify the
claim's value or quote; they only point a reviewer back at the full quote.
"""
import bisect
import re

ADVISORY_TYPE = 'omitted_qualifier'
MESSAGE = ('Extracted value omits the qualifier "{qualifier}" that appears in the same '
           'sentence of its source quote. Review the full quote; the value was not changed.')

# Longest phrases first so "prize pool" wins over "pool" and "approximately" over "approx".
# Plain "guaranteed" is deliberately absent: only the negated phrase is material.
VOCABULARY = sorted([
    'total', 'prize pool', 'pool', 'per winner', 'per team', 'per person', 'each',
    'up to', 'split', 'shared', 'conditional', 'conditionally', 'pilot',
    'not guaranteed', 'in credits', 'approx', 'approximately',
], key=lambda t: (-len(t), t))

_QUALIFIER_RE = re.compile(
    r'\b(?:' + '|'.join(r'\s+'.join(map(re.escape, t.split())) for t in VOCABULARY) + r')\b',
    re.IGNORECASE)

_CODES = r'USD|US\$|EUR|GBP|INR|JPY|CNY|CAD|AUD|CHF|SGD|Rs\.?'
_SYMBOLS = r'[$€£₹¥]'
_MONEY_RE = re.compile(
    r'(?:(?<![A-Za-z])(?:' + _CODES + r')\s?|' + _SYMBOLS + r'\s?)\d'
    r'|\d[\d,.]*\s?(?:' + _CODES + r')(?![A-Za-z])',
    re.IGNORECASE)

# Sentence ends at . ! ? followed by whitespace or end of text (so 1,000.50 is not split),
# except after a few common abbreviations used around amounts.
_BOUNDARY_RE = re.compile(r'[.!?]+(?=\s|$)')
_ABBREVIATIONS = {'rs', 'approx', 'e.g', 'i.e', 'vs', 'incl'}


def _norm(text):
    return ' '.join(text.lower().split())


def is_monetary(field, value):
    return field == 'prize' or bool(_MONEY_RE.search(value))


_WORD_BEFORE_RE = re.compile(r'[A-Za-z.]+$')


def _boundaries(quote):
    """Sorted (start, end) spans of sentence-ending punctuation."""
    spans = []
    for m in _BOUNDARY_RE.finditer(quote):
        # Bounded look-behind window keeps this linear in the quote length.
        word = _WORD_BEFORE_RE.search(quote[max(0, m.start() - 10):m.start()])
        if m.group() == '.' and word and word.group().lower().strip('.') in _ABBREVIATIONS:
            continue
        spans.append((m.start(), m.end()))
    return spans


def _sentence_span(start, end, quote_len, starts, ends):
    """Span of the sentence containing quote[start:end]; boundaries inside the value are ignored."""
    i = bisect.bisect_right(ends, start)
    lo = ends[i - 1] if i else 0
    j = bisect.bisect_left(starts, end)
    hi = ends[j] if j < len(starts) else quote_len
    return lo, hi


def detect_omitted_qualifiers(claim):
    """Return advisory dicts for qualifiers in the value's sentence but absent from the value."""
    if not isinstance(claim, dict):
        return []
    field, value, quote = claim.get('field'), claim.get('value'), claim.get('quote')
    if not all(isinstance(x, str) for x in (field, value, quote)) or not value.strip():
        return []
    if not is_monetary(field, value) or value not in quote:
        return []
    retained = {_norm(m.group()) for m in _QUALIFIER_RE.finditer(value)}
    spans = _boundaries(quote)
    starts, ends = [s for s, _ in spans], [e for _, e in spans]
    occurrences, i = [], quote.find(value)
    while i != -1:
        occurrences.append((i, i + len(value)))
        i = quote.find(value, i + 1)
    sentences = {}
    for vs, ve in occurrences:
        sentences.setdefault(_sentence_span(vs, ve, len(quote), starts, ends), []).append((vs, ve))
    seen, found = set(), []
    for (lo, hi), inside in sorted(sentences.items()):
        for m in _QUALIFIER_RE.finditer(quote, lo, hi):
            if any(m.start() < ve and m.end() > vs for vs, ve in inside):
                continue  # inside the value itself
            key = _norm(m.group())
            if key in retained or key in seen:
                continue
            seen.add(key)
            found.append((m.start(), m.group()))
    return [{'type': ADVISORY_TYPE, 'qualifier': q, 'message': MESSAGE.format(qualifier=q)}
            for _, q in sorted(found)]


def annotate_claims(claims):
    """New claim dicts, each with an 'advisories' list; inputs are not mutated."""
    return [{**c, 'advisories': detect_omitted_qualifiers(c)} for c in claims]
