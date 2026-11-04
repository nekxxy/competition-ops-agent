"""Conservative offline parser, not an LLM. Only explicit ISO dates and labeled lines.

It makes no legal/eligibility judgments. A matched passage is still unverified.
Natural-language dates are intentionally left for review, never guessed.
"""
import re
from .core import validate_claim

DATE=r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?[+-]\d{2}:\d{2}'
LABELS={'registration_deadline':'Registration closes','submission_deadline':'Final submissions close','prize':'Prizes:','eligibility':'Eligibility:','automation':'AI policy:','license':'Code license:'}

def extract_explicit(body):
    claims=[]
    for line in body.splitlines():
        quote=line.strip()
        for field,label in LABELS.items():
            if not quote.startswith(label):continue
            value=quote[len(label):].strip().rstrip('.')
            if field.endswith('_deadline'):
                if not re.fullmatch(DATE,value):continue
            if not value:continue
            try:validate_claim(field,value,quote,body)
            except ValueError:continue
            claims.append({'field':field,'value':value,'quote':quote})
    return claims
