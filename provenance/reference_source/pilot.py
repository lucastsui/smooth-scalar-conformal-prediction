from pathlib import Path
import json, datetime
import numpy as np
from core import scalar_score, occupancy_theory, conformal_k

root=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20260928)
K,n,alpha,R=12,9,.1,2000
k=conformal_k(n,alpha)
shattering=[]
for mask in range(8):
    s=scalar_score(mask/7,np.full(3,.5),np.arange(3),3)
    got=(s <= 1/(8*7)*.5).astype(int)
    expected=np.array([(mask >> j)&1 for j in range(3)])
    assert np.array_equal(got,expected)
    shattering.append(got.tolist())
cover=[]
fixed=[]
direct_mismatches=0
for r in range(R):
    y=rng.integers(K,size=n)
    u=rng.random(n)
    A=np.unique(y)
    mask=sum(1<<int(j) for j in A)
    q=np.partition(u,k-1)[k-1]
    cover.append(len(A)/K*q)
    fixed.append(q)
    if r<100:
        yt=rng.integers(K,size=200)
        ut=rng.random(200)
        scores=scalar_score(mask/(2**K-1),u,y,K)
        direct=scalar_score(mask/(2**K-1),ut,yt,K)<=np.partition(scores,k-1)[k-1]
        algebra=np.isin(yt,A)&(ut<=q)
        direct_mismatches+=int(np.sum(direct!=algebra))
cover=np.array(cover)
fixed=np.array(fixed)
se=float(cover.std(ddof=1)/np.sqrt(R))
theory=occupancy_theory(n,K,alpha)
passed=(abs(cover.mean()-theory)<5*se+.001 and cover.mean()<.65 and direct_mismatches==0)
record=dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    seed=20260928,n=n,K=K,alpha=alpha,repetitions=R,mean=float(cover.mean()),se=se,
    theory=theory,fixed_mean=float(fixed.mean()),fixed_theory=k/(n+1),
    direct_mismatches=direct_mismatches,shattering=shattering,pilot_passed=bool(passed))
(root/'results/pilot.json').write_text(json.dumps(record,indent=2))
np.savez_compressed(root/'results/pilot_raw.npz',coverage=cover,fixed=fixed)
print(json.dumps(record,indent=2))
assert passed
