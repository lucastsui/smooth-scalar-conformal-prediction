"""Reproduce scientific outputs without overwriting the archived run."""
from pathlib import Path
import argparse, datetime, json, subprocess, sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def compare(candidate):
    reference=ROOT/'results/confirmatory'
    expected=sorted(p.name for p in reference.glob('*.npz'))
    actual=sorted(p.name for p in candidate.glob('*.npz'))
    assert expected==actual,'Different raw result file sets'
    maximum=0.
    for name in expected:
        with np.load(reference/name) as a,np.load(candidate/name) as b:
            assert a.files==b.files,(name,'keys')
            for key in a.files:
                assert a[key].shape==b[key].shape,(name,key,'shape')
                if a[key].dtype.kind in 'iuf':
                    assert np.allclose(a[key],b[key],rtol=0,atol=1e-12,equal_nan=True),(name,key)
                    finite=np.isfinite(a[key])&np.isfinite(b[key])
                    if finite.any(): maximum=max(maximum,float(np.max(np.abs(a[key][finite]-b[key][finite]))))
                else: assert np.array_equal(a[key],b[key]),(name,key)
    for name in ['occupancy_summary.csv','linear_summary.csv']:
        a=pd.read_csv(reference/name);b=pd.read_csv(candidate/name)
        cols=[c for c in a if c not in ['seconds','case_seconds']]
        pd.testing.assert_frame_equal(a[cols],b[cols],check_exact=False,rtol=0,atol=1e-12)
    assert json.loads((reference/'independent_test_audit.json').read_text())==json.loads((candidate/'independent_test_audit.json').read_text())
    return dict(raw_files_compared=len(expected),maximum_absolute_difference=maximum,scientific_results_match=True,tolerance=1e-12)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--compare-only');args=p.parse_args()
    if args.compare_only:
        out=ROOT/args.compare_only
    else:
        name=args.output or 'results/reproduction_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        out=ROOT/name;out.mkdir(parents=True,exist_ok=True)
        if (out/'run_manifest.json').exists():raise RuntimeError('Choose a new output path; completed runs are preserved.')
        with (out/'tests.txt').open('w') as stream:
            subprocess.run([sys.executable,'-m','pytest','-q','src/test_core.py'],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
        with (out/'execution.txt').open('w') as stream:
            subprocess.run([sys.executable,'src/experiments.py','--output',str(out)],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True)
    report=compare(out)
    (out/'comparison.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(output=str(out),**report),indent=2))

if __name__=='__main__':main()
