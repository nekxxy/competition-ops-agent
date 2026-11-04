"""Portable review report, never an entry or authorization."""
import json

def export_report(result):
    allowed={'plan','title','mode','live_meta_inference','before_id','after_id','sources','changes','claims','readiness','reviews','local_deadline','note','fixture','recorded_meta'}
    r={k:v for k,v in result.items() if k in allowed}
    r['report_type']='Evidence review, not an entry'
    r['limitations']=['Saved text, not a current website check','Quote matching does not prove semantic truth or source authenticity','Reviews are self-reported and do not authorize external action','No live Meta inference in this report','Qualifier advisories are deterministic heuristics for review, not corrections']
    r['external_action']=False
    return json.dumps(r,indent=2,ensure_ascii=False)
