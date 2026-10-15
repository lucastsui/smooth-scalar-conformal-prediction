"""Second-pass independent technical checks; preserve all v1 artifacts."""
from pathlib import Path
import contextlib
import hashlib
import io
import itertools
import json
import math
import sys

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
import core
from experiments import linear, test_audit

report={}
manifest=json.loads((ROOT/'reviews/frozen_v2/manifest.json').read_text())
checks={}
for relative,digest in manifest['files'].items():
    checks['frozen_v2/'+relative]=hashlib.sha256((ROOT/'reviews/frozen_v2'/relative).read_bytes()).hexdigest()==digest
for relative,digest in manifest['external_evidence_sha256'].items():
    checks[relative]=hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest
assert all(checks.values())
report['manifest_checks']=checks
original_manifest=json.loads((ROOT/'results/confirmatory/run_manifest.json').read_text())
archive={name:hashlib.sha256((ROOT/'provenance/reference_source'/name).read_bytes()).hexdigest()==digest for name,digest in original_manifest['source_sha256'].items()}
assert all(archive.values())
report['original_source_archive_matches']=archive

def independent_cdf(q,b):
    b=abs(float(b));q=float(q)
    if b==0 or not math.isfinite(q):
        return float(np.clip(q,0,1))
    cuts=sorted(set([-1.,1.,float(np.clip(q/b,-1,1)),float(np.clip((q-1)/b,-1,1))]))
    # Midpoint integration is exact on every affine segment. Avoid evaluating
    # plateau endpoints via q-b*((q-1)/b), which can amplify cancellation.
    return float(sum((r-l)*np.clip(q-b*((l+r)/2),0,1)/2 for l,r in zip(cuts[:-1],cuts[1:])))

# Revisit every actual B1 counterexample.
b1=[]
for q in [.5,.9]:
    for b in [1e-12,1e-16,1e-20]:
        got=float(core.linear_cdf(q,b))
        expected=independent_cdf(q,b)
        assert abs(got-expected)<1e-15
        b1.append(dict(q=q,slope=b,revised=got,reference=expected))
report['B1_original_counterexamples']=b1

# Wider numerical domain includes support boundaries and both convolution regimes.
max_error=0.;count=0
for b in [0,1e-24,1e-20,1e-16,1e-12,1e-8,.001,.25,.5,1,2,1e6,1e12]:
    points=np.r_[np.linspace(-b,1+b,51),[-b,0,b,1-b,1,1+b],[-np.inf,np.inf],np.nextafter([-b,b,1-b,1+b],[-np.inf]*4),np.nextafter([-b,b,1-b,1+b],[np.inf]*4)]
    for sign in [-1,1]:
        for q in points:
            got=float(core.linear_cdf(q,sign*b))
            reference=independent_cdf(q,sign*b)
            max_error=max(max_error,abs(got-reference))
            count+=1
            assert np.isfinite(got) and 0<=got<=1
            assert abs(got-reference)<5e-12
report['piecewise_CDF_stress']={'evaluations':count,'max_error_against_independent_integral':max_error,'slope_magnitudes':[0,1e-24,1e-20,1e-16,1e-12,1e-8,.001,.25,.5,1,2,1e6,1e12]}

# Independently compare original and revised protocol payloads.
raw_diffs={};reference_error=0.
for path in sorted((ROOT/'results/confirmatory').glob('*.npz')):
    old=np.load(path);new=np.load(ROOT/'results/revision1_reproduction'/path.name)
    assert set(old.files)==set(new.files)
    maximum=0.
    for key in old.files:
        a,b=old[key],new[key]
        assert a.shape==b.shape
        if not np.issubdtype(a.dtype,np.number):
            assert np.array_equal(a,b)
        else:
            assert np.array_equal(np.isinf(a),np.isinf(b))
            finite=np.isfinite(a)&np.isfinite(b)
            maximum=max(maximum,float(np.max(np.abs(a[finite]-b[finite]))) if np.any(finite) else 0.)
            assert np.allclose(a,b,rtol=0,atol=1e-12,equal_nan=True)
    raw_diffs[path.name]=maximum
    if path.name.startswith('linear_'):
        x=new['values']
        reference=np.array([independent_cdf(q,slope) for _,_,slope,q in x])
        reference_error=max(reference_error,float(np.max(abs(reference-x[:,0]))))
report['original_to_revised_raw_max_differences']=raw_diffs
report['max_raw_difference']=max(raw_diffs.values())
report['max_revised_linear_CDF_reference_error']=reference_error

# Re-execute exactly the six linear settings affected by B1 into this review's directory.
cf=json.loads((ROOT/'configs/confirmatory.json').read_text())
rerun=OUT/'linear_rerun';rerun.mkdir(exist_ok=True)
with contextlib.redirect_stdout(io.StringIO()):
    linear(cf['linear'],cf['alpha'],rerun)
matching={}
for p in sorted(rerun.glob('*.npz')):
    got=np.load(p);saved=np.load(ROOT/'results/revision1_reproduction'/p.name)
    matching[p.name]=all(np.array_equal(got[key],saved[key]) for key in got.files)
assert all(matching.values())
report['reexecuted_linear_arrays_identical']=matching

# Execute B2 beyond the regression test's single sample size.
boundary=[]
for n in [1,3,19]:
    a=.01;out=OUT/f'infinite_n{n}';out.mkdir(exist_ok=True)
    config=dict(repetitions=5,grid_size=7,delta=.05,n_values=[n],a_values=[1.],seed=20260929+n)
    with contextlib.redirect_stdout(io.StringIO()):
        linear(config,a,out)
        test_audit(dict(seed=20260929+n,n=n,K=8,repetitions=5,test_points_per_repetition=17),a,out)
    vals=np.load(out/f'linear_n{n}_a1.npz')['values']
    audit=np.load(out/'independent_test_audit.npz')['values']
    summary=pd.read_csv(out/'linear_summary.csv')
    assert np.all(vals[:,:2]==1) and np.all(np.isposinf(vals[:,3]))
    assert np.all(audit[:,0]==1) and np.all(audit[:,1]==17) and np.all(audit[:,2]==1)
    assert np.all(summary[['finite_beta_lower','dkw_lower','continuum_lower']].to_numpy()==1)
    assert core.continuum_lower(n,a,1)['lower']==1
    boundary.append(dict(n=n,alpha=a,k=core.conformal_k(n,a),all_coverages_one=True,all_certificates_one=True))
report['B2_infinite_threshold_execution']=boundary

# Pure pathwise check of the new quantile sandwich, deliberately retaining ties.
# For continuous uniform F, the exact CDF discrepancy is attained at jumps/left limits.
arrays=quantiles=tied_arrays=0
slack=math.inf
for n in range(1,8):
    for values in itertools.combinations_with_replacement([0.,.25,.5,.75,1.],n):
        u=np.asarray(values)
        d=max(float(np.max(np.arange(1,n+1)/n-u)),float(np.max(u-np.arange(n)/n)))
        arrays+=1;tied_arrays+=int(len(set(values))<n)
        for k in range(1,n+1):
            q=u[k-1]
            lower=k/n-d;upper=(k-1)/n+d
            slack=min(slack,q-lower,upper-q)
            assert lower-2e-15<=q<=upper+2e-15
            quantiles+=1
report['quantile_sandwich_tie_stress']={'arrays':arrays,'arrays_with_ties':tied_arrays,'quantiles':quantiles,'minimum_slack':slack,'violations':0}

(OUT/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
