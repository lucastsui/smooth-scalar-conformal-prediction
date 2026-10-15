"""Audit raw-to-table agreement, paper macros, citations and PDF boundaries."""
from pathlib import Path
import hashlib,json,re
import numpy as np
import pandas as pd
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]

def main():
    d=ROOT/'results/confirmatory';occ=pd.read_csv(d/'occupancy_summary.csv');lin=pd.read_csv(d/'linear_summary.csv')
    for _,r in occ.iterrows():
        with np.load(d/r.raw_file) as z:
            c=list(z['columns']).index(r.method);v=z['values'][:,c]
        assert abs(v.mean()-r['mean'])<1e-14
        assert abs(v.std(ddof=1)/np.sqrt(len(v))-r.se)<1e-14
        assert abs(r.ci_low-(r['mean']-1.96*r.se))<1e-14
        assert abs(r.ci_high-(r['mean']+1.96*r.se))<1e-14
    for _,r in lin.iterrows():
        with np.load(d/r.raw_file) as z:v=z['values'][:,0]
        assert abs(v.mean()-r['mean'])<1e-14
        assert abs(v.std(ddof=1)/np.sqrt(len(v))-r.se)<1e-14
        assert np.isclose((v<r.continuum_lower).mean(),r.continuum_violation_rate)
    vals=json.loads((ROOT/'paper/generated/values.json').read_text())
    severe=occ[(occ.n==99)&(occ.K==10000)&(occ.alpha==.1)&(occ.method=='joint')].iloc[0]
    assert vals['SevereMean']==f'{100*severe["mean"]:.4f}'
    assert vals['SevereTheory']==f'{100*severe.theory:.4f}'
    tex=(ROOT/'paper/main.tex').read_text();bib=(ROOT/'paper/references.bib').read_text()
    cites={k.strip() for m in re.findall(r'\\cite(?:p|t)?(?:\[[^\]]*\])*\{([^}]+)\}',tex) for k in m.split(',')}
    keys=set(re.findall(r'@\w+\{([^,]+),',bib));assert cites==keys,(cites,keys)
    pdf=ROOT/'output/pdf/manuscript.pdf'
    if not pdf.exists():pdf=ROOT/'paper/main.pdf'
    reader=PdfReader(pdf);texts=[p.extract_text() for p in reader.pages];joined='\n'.join(texts)
    assert 'AUTHORERR' not in joined
    assert '??' not in joined
    impact_page=next(i+1 for i,t in enumerate(texts) if 'Impact Statement' in t)
    assert impact_page<=8,'Main body over provisional page limit'
    assert pdf.stat().st_size<50_000_000
    report=dict(occupancy_rows_checked=len(occ),linear_rows_checked=len(lin),references_checked=len(keys),
        pdf_pages=len(reader.pages),main_body_page_upper_bound=impact_page,impact_statement_page=impact_page,pdf_bytes=pdf.stat().st_size,
        pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),numeric_and_citation_checks_pass=True,
        note='Programmatic verification supplements visual page inspection; it does not verify mathematical novelty or proofs.')
    (ROOT/'logs/package_verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
