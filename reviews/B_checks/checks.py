"""Separate AI reviewer B checks; does not modify the reviewed implementation."""
from pathlib import Path
from fractions import Fraction
import hashlib
import itertools
import json
import math
import sys
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import beta, binom

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
import core

report = {}

def rank(n, alpha):
    x = (n + 1) * (1 - Fraction(str(alpha)))
    return (x.numerator + x.denominator - 1) // x.denominator

def independent_linear_cdf(q, b):
    """Integrate the clipped affine function by its breakpoints, no cancellation."""
    b = abs(float(b))
    if b == 0:
        return float(np.clip(q, 0, 1))
    knots = [-1., 1.]
    knots += [float(np.clip(q / b, -1, 1)), float(np.clip((q - 1) / b, -1, 1))]
    knots = sorted(set(knots))
    return sum((r - l) * (np.clip(q - b*l, 0, 1) + np.clip(q - b*r, 0, 1)) / 4
               for l, r in zip(knots[:-1], knots[1:]))

frozen = json.loads((ROOT / "reviews/frozen_v1/manifest.json").read_text())
run = json.loads((ROOT / "results/confirmatory/run_manifest.json").read_text())
report["frozen_hashes_match"] = {
    name: hashlib.sha256((ROOT / "reviews/frozen_v1" / name).read_bytes()).hexdigest() == digest
    for name, digest in frozen.items()
}
report["source_hashes_match_run"] = {
    name: hashlib.sha256((ROOT / "src" / name).read_bytes()).hexdigest() == digest
    for name, digest in run["source_sha256"].items()
}
report["config_hash_matches_run"] = hashlib.sha256((ROOT / "configs/confirmatory.json").read_bytes()).hexdigest() == run["config_sha256"]
assert all(report["frozen_hashes_match"].values())
assert all(report["source_hashes_match_run"].values())
assert report["config_hash_matches_run"]

# All frozen calibration outcomes and tabulated means/SEs, using an independent rank calculation.
occ = pd.read_csv(ROOT / "results/confirmatory/occupancy_summary.csv")
lin = pd.read_csv(ROOT / "results/confirmatory/linear_summary.csv")
max_mean_err = max_se_err = max_occ_event_err = 0.
for _, row in occ.iterrows():
    n, K, a = int(row.n), int(row.K), float(row.alpha)
    arr = np.load(ROOT / "results/confirmatory" / row.raw_file)["values"]
    col = {"joint": 0, "fixed": 1, "split": 2, "monotone": 3}[row.method]
    x = arr[:, col]
    max_mean_err = max(max_mean_err, abs(float(x.mean()) - row["mean"]))
    max_se_err = max(max_se_err, abs(float(x.std(ddof=1)/np.sqrt(len(x))) - row.se))
    k = rank(n, a)
    expected = np.ones(len(arr)) if k > n else arr[:, 4] / K * arr[:, 5]
    max_occ_event_err = max(max_occ_event_err, float(np.max(abs(expected-arr[:, 0]))))
    target = 1. if k > n else float(Fraction(k,n+1)*(1-Fraction(K-1,K)**n))
    if row.method == "joint":
        assert abs(target - row.theory) < 1e-14
    elif row.method == "split":
        nc = n - n//2
        assert abs(min(1., rank(nc,a)/(nc+1)) - row.theory) < 1e-14
    else:
        assert abs(min(1., k/(n+1)) - row.theory) < 1e-14
    assert np.max(abs(arr[:,1]-arr[:,3])) < 1e-14
assert max_mean_err < 1e-14 and max_se_err < 1e-14 and max_occ_event_err < 1e-14

linear_errors = []
cert_errors = []
for _, row in lin.iterrows():
    n, a, G = int(row.n), float(row.a), int(row.grid_size)
    arr = np.load(ROOT / "results/confirmatory" / row.raw_file)["values"]
    independent = np.array([independent_linear_cdf(q,b) for _,_,b,q in arr])
    err = float(np.max(abs(independent-arr[:,0])))
    linear_errors.append(err)
    assert err < 2e-12
    assert abs(arr[:,0].mean()-row["mean"]) < 1e-14
    assert abs(arr[:,0].std(ddof=1)/np.sqrt(len(arr))-row.se) < 1e-14
    k = rank(n,.1)
    # Invert the binomial tail, without using the implementation's beta PPF.
    fin = brentq(lambda u:binom.sf(k-1,n,u)-.05/G,0,1,xtol=1e-14)
    eps = np.geomspace(1e-5,.25,2000)
    sizes = np.ceil(a/eps).astype(int)+1
    ppf_by_size = {int(m):brentq(lambda u:binom.sf(k-1,n,u)-.05/m,0,1,xtol=1e-14) for m in set(sizes)}
    lows = np.array([ppf_by_size[int(m)]-2*e for m,e in zip(sizes,eps)])
    cont = max(0., float(lows.max()))
    cert_errors.append(max(abs(fin-row.finite_beta_lower),abs(cont-row.continuum_lower)))
    assert cert_errors[-1] < 1e-12
    assert np.mean(arr[:,0] < cont) == row.continuum_violation_rate
report["frozen_results_audit"] = {
    "occupancy_settings": len(occ)//4,
    "occupancy_calibration_rows": int(occ[occ.method == "joint"].repetitions.sum()),
    "linear_calibration_rows": int(lin.repetitions.sum()),
    "max_mean_error": max_mean_err,
    "max_se_error": max_se_err,
    "max_occupancy_identity_error": max_occ_event_err,
    "max_linear_cdf_error_via_piecewise_integral": max(linear_errors),
    "max_certificate_error_via_binomial_root": max(cert_errors),
}

# Re-execution audit: ignore compressed-file metadata and runtime differences.
reproduced = OUT / "reproduced"
same_npz = {}
for original in sorted((ROOT / "results/confirmatory").glob("*.npz")):
    x, y = np.load(original), np.load(reproduced / original.name)
    same_npz[original.name] = set(x.files) == set(y.files) and all(np.array_equal(x[key],y[key],equal_nan=True) if np.issubdtype(x[key].dtype,np.number) else np.array_equal(x[key],y[key]) for key in x.files)
assert all(same_npz.values())
report["reproduction_npz_arrays_identical"] = same_npz

# Exhaustive direct-score prediction checks over every label sequence in small cases.
rng = np.random.default_rng(28190173)
direct_trials = direct_events = 0
for K in range(1,5):
    for n in range(1,5):
        for ys in itertools.product(range(K),repeat=n):
            y = np.array(ys)
            u = rng.random(n)
            mask = sum(1 << int(j) for j in set(ys))
            lam = mask/(2**K-1)
            st_u = np.linspace(0,1,21)
            ut = np.repeat(st_u,K)
            yt = np.tile(np.arange(K),len(st_u))
            train = core.scalar_score(lam,u,y,K)
            test = core.scalar_score(lam,ut,yt,K)
            for alpha in [.01,.1,.5,.9]:
                k = rank(n,alpha)
                q = math.inf if k > n else sorted(train)[k-1]
                expected = np.ones(len(ut),bool) if k > n else np.isin(yt,y) & (ut <= sorted(u)[k-1])
                assert np.array_equal(test <= q,expected)
                direct_trials += 1
                direct_events += len(ut)
report["direct_scalar_vs_membership"] = {"calibration_case_level_combinations":direct_trials,"test_events":direct_events,"disagreements":0}

# Exact PIT CDF for every interpolation parameter: score is a uniform mixture.
def offsets(lam,K):
    return core.scalar_score(lam,np.zeros(K),np.arange(K),K)

def mixture_cdf(q,off,width):
    return np.clip((np.asarray(q)[...,None]-off)/width,0,1).mean(axis=-1)

def concentration_at(off,width,w):
    knots = np.r_[off,off+width,off-w,off+width-w]
    return float(np.max(mixture_cdf(knots+w,off,width)-mixture_cdf(knots,off,width)))

transfer_trials = 0
transfer_min_slack = math.inf
for K in [2,3,5,8,12]:
    width = 1/(32*(2**K-1))
    for trial in range(160):
        lam = rng.random()
        mu = float(np.clip(lam+rng.normal()*10**rng.uniform(-10,-1),0,1))
        left,right = offsets(lam,K),offsets(mu,K)
        h = float(np.max(abs(left-right)))
        # CDFs are piecewise linear; their difference attains its extrema at these knots.
        dist = 0.
        for y in range(K):
            knots = np.clip(np.r_[0,1,(left-left[y])/width,(left+width-left[y])/width,(right-right[y])/width,(right+width-right[y])/width],0,1)
            x = mixture_cdf(left[y]+width*knots,left,width)
            z = mixture_cdf(right[y]+width*knots,right,width)
            dist = max(dist,float(np.max(abs(x-z))))
        r = concentration_at(right,width,2*h)
        assert dist <= r + 2e-12
        transfer_min_slack = min(transfer_min_slack,r-dist)
        transfer_trials += 1
report["rank_transfer_stress"] = {"parameter_pairs":transfer_trials,"min_bound_minus_rank_distance":transfer_min_slack,"violations_above_2e_minus_12":0}

packing=[]
for K in range(2,9):
    m=K//2;p=m/K
    masks=[sum(1<<j for j in A) for A in itertools.combinations(range(K),m)]
    funcs=[]
    for mask in masks:
        member=np.array([(mask>>j)&1 for j in range(K)],bool)
        funcs.append(np.r_[np.where(member,0,p),np.where(member,p,1)])
    distances=[float(np.max(abs(funcs[i]-funcs[j]))) for i in range(len(funcs)) for j in range(i)]
    minimum=min(distances)
    assert minimum >= p-1e-14
    packing.append({"K":K,"equal_size_masks":len(masks),"proven_claim_separation":p,"observed_exact_separation":minimum})
report["packing_endpoint_enumeration"] = packing

# Adversarial measurable selector minimizing/maximizing the rank order statistic
# over all K=5 knots. Dependence among candidates is deliberately retained.
K,n,R=5,19,30000
M=2**K;k=rank(n,.1)
members=np.array([[(mask>>j)&1 for j in range(K)] for mask in range(M)],bool)
p=members.mean(axis=1)
low=brentq(lambda u:binom.sf(k-1,n,u)-.05/M,0,1,xtol=1e-14)
high=brentq(lambda u:binom.sf(k-1,n,u)-(1-.05/M),0,1,xtol=1e-14)
lower_hits=upper_hits=0
for start in range(0,R,500):
    y=rng.integers(K,size=(500,n));u=rng.random((500,n))
    inc=members[:,y].transpose(1,2,0)
    ranks=np.where(inc,p*u[:,:,None],p+(1-p)*u[:,:,None])
    kth=np.partition(ranks,k-1,axis=1)[:,k-1,:]
    lower_hits+=int(np.sum(kth.min(axis=1)<low))
    upper_hits+=int(np.sum(kth.max(axis=1)>high))
report["adversarial_rank_selector_simulation"]={"K":K,"n":n,"candidates":M,"calibrations":R,"lower":low,"upper":high,"lower_tail_rate":lower_hits/R,"upper_tail_rate":upper_hits/R,"theoretical_each_tail_upper_bound":.05}

# Probe code outside the frozen numerical settings; do not conflate these with paper errors.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    boundary = core.continuum_lower(3,.1,1)
tiny = [{"q":q,"slope":b,"implementation":float(core.linear_cdf(q,b)),"reference":independent_linear_cdf(q,b)} for q in [.5,.9] for b in [1e-12,1e-16,1e-20]]
report["out_of_experiment_domain_probes"]={"infinite_threshold_continuum_result":boundary,"infinite_threshold_correct_coverage":1.,"tiny_slope_cdf":tiny}

(OUT/"check_results.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
