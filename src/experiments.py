"""Run the frozen numerical checks and save every calibration-level outcome."""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, subprocess, time
import numpy as np
import pandas as pd
from core import conformal_k, occupancy_theory, mixture_uniform_cdf, linear_cdf, finite_beta_lower, continuum_lower

ROOT=Path(__file__).resolve().parents[1]

def describe(x):
    x=np.asarray(x,float)
    mean=float(x.mean());se=float(x.std(ddof=1)/np.sqrt(len(x)))
    return dict(mean=mean,se=se,ci_low=mean-1.96*se,ci_high=mean+1.96*se)

def occupancy(config, out):
    cases={(n,n*r,config['alpha']) for n in config['n_values'] for r in config['K_ratios']}
    cases|={(n,K,config['alpha']) for n in config['n_values'] for K in config['fixed_K_values']}
    cases|={(n,K,config['alpha']) for n,K in config['extra_cases']}
    cases|={tuple(c) for c in config['boundary_cases']}
    rows=[]
    R=config['repetitions']
    for i,(n,K,alpha) in enumerate(sorted(cases)):
        rng=np.random.default_rng(np.random.SeedSequence([config['seed'],i]))
        k=conformal_k(n,alpha);nt=n//2;nc=n-nt;kc=conformal_k(nc,alpha)
        raw=np.zeros((R,7));data_hash=hashlib.sha256()
        start=time.perf_counter()
        for r in range(R):
            y=rng.integers(K,size=n,dtype=np.int32);u=rng.random(n)
            data_hash.update(y.tobytes());data_hash.update(u.tobytes())
            size=len(np.unique(y))
            uq=1. if k>n else np.partition(u,k-1)[k-1]
            joint=1. if k>n else size/K*uq
            A=np.unique(y[:nt]);p=len(A)/K
            sc=(~np.isin(y[nt:],A)).astype(float)+u[nt:]/4
            sq=np.inf if kc>nc else np.partition(sc,kc-1)[kc-1]
            split=float(mixture_uniform_cdf(sq,p))
            # The monotone control is an explicitly evaluated affine transform
            # whose slope and intercept depend on the calibration sample.
            slope=1+u.mean();intercept=u.min()
            transformed=slope*u+intercept
            mq=1. if k>n else (np.partition(transformed,k-1)[k-1]-intercept)/slope
            raw[r]=[joint,uq,split,mq,size,uq,sq]
        filename=f'occupancy_n{n}_K{K}_a{alpha:g}.npz'
        np.savez_compressed(out/filename,values=raw,columns=np.array(['joint','fixed','split','monotone','distinct','u_quantile','split_q']))
        seconds=time.perf_counter()-start
        for method,col in [('joint',0),('fixed',1),('split',2),('monotone',3)]:
            theory=occupancy_theory(n,K,alpha) if method=='joint' else (min(1.,kc/(nc+1)) if method=='split' else min(1.,k/(n+1)))
            rows.append(dict(n=n,K=K,alpha=alpha,method=method,repetitions=R,theory=theory,
                **describe(raw[:,col]),raw_file=filename,data_sha256=data_hash.hexdigest(),case_seconds=seconds,
                seed_base=config['seed'],seed_case=i))
        print('occupancy',n,K,alpha,float(raw[:,0].mean()),flush=True)
    frame=pd.DataFrame(rows);frame.to_csv(out/'occupancy_summary.csv',index=False)
    deviation=np.abs(frame['mean']-frame['theory'])
    assert np.all(deviation <= 5*frame['se']+.001),'Unexpected theory discrepancy; investigate.'
    return frame

def linear(config, alpha, out):
    rows=[];R=config['repetitions'];G=config['grid_size'];delta=config['delta']
    for i,(n,a) in enumerate((n,a) for n in config['n_values'] for a in config['a_values']):
        rng=np.random.default_rng(np.random.SeedSequence([config['seed'],i]))
        slopes=np.linspace(-a,a,G);k=conformal_k(n,alpha)
        raw=np.empty((R,4));start=time.perf_counter();data_hash=hashlib.sha256()
        for r in range(R):
            u=rng.random(n);v=rng.uniform(-1,1,n)
            data_hash.update(u.tobytes());data_hash.update(v.tobytes())
            scores=u[:,None]+v[:,None]*slopes[None,:]
            qs=np.full(G,np.inf) if k>n else np.partition(scores,k-1,axis=0)[k-1]
            j=int(np.argmin(qs))
            raw[r]=[float(linear_cdf(qs[j],slopes[j])),float(linear_cdf(qs[G//2],slopes[G//2])),slopes[j],qs[j]]
        cert=continuum_lower(n,alpha,a,delta)
        finite=finite_beta_lower(n,alpha,G,delta)
        dkw=1. if k>n else max(0.,k/n-np.sqrt(np.log(2*G/delta)/(2*n)))
        filename=f'linear_n{n}_a{a:g}.npz'
        np.savez_compressed(out/filename,values=raw,columns=np.array(['joint','fixed','selected_slope','selected_q']))
        rows.append(dict(n=n,a=a,repetitions=R,grid_size=G,**describe(raw[:,0]),
            fixed_mean=raw[:,1].mean(),finite_beta_lower=finite,dkw_lower=dkw,
            continuum_lower=cert['lower'],net_epsilon=cert['epsilon'],net_size=cert['net_size'],
            finite_violation_rate=float(np.mean(raw[:,0]<finite)),
            continuum_violation_rate=float(np.mean(raw[:,0]<cert['lower'])),
            raw_file=filename,data_sha256=data_hash.hexdigest(),seconds=time.perf_counter()-start))
        print('linear',n,a,float(raw[:,0].mean()),flush=True)
    pd.DataFrame(rows).to_csv(out/'linear_summary.csv',index=False)

def test_audit(config,alpha,out):
    rng=np.random.default_rng(config['seed']);n=config['n'];K=config['K'];R=config['repetitions'];T=config['test_points_per_repetition']
    k=conformal_k(n,alpha);raw=np.empty((R,3))
    for r in range(R):
        y=rng.integers(K,size=n);u=rng.random(n);A=np.unique(y)
        q=np.inf if k>n else np.partition(u,k-1)[k-1]
        yt=rng.integers(K,size=T);ut=rng.random(T)
        hits=T if k>n else (np.isin(yt,A)&(ut<=q)).sum()
        raw[r]=[1. if k>n else len(A)/K*q,hits,hits/T]
    np.savez_compressed(out/'independent_test_audit.npz',values=raw,columns=np.array(['conditional_coverage','hits','empirical_coverage']))
    record=dict(**config,theory=occupancy_theory(n,K,alpha),empirical=describe(raw[:,2]),conditional=describe(raw[:,0]),paired_difference=describe(raw[:,2]-raw[:,0]))
    (out/'independent_test_audit.json').write_text(json.dumps(record,indent=2))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',default='configs/confirmatory.json');parser.add_argument('--output',default='results/confirmatory');args=parser.parse_args()
    cf=ROOT/args.config;config=json.loads(cf.read_text());out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    if (out/'run_manifest.json').exists():
        raise RuntimeError('Preserve completed results; use a different --output for reproduction.')
    start=time.perf_counter()
    meta=dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),config_sha256=hashlib.sha256(cf.read_bytes()).hexdigest(),python=platform.python_version(),numpy=np.__version__)
    try: meta['git_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    except subprocess.CalledProcessError: meta['git_commit']='uncommitted'
    meta['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'src').glob('*.py')}
    occupancy(config,out);linear(config['linear'],config['alpha'],out);test_audit(config['test_audit'],config['alpha'],out)
    meta['elapsed_seconds']=time.perf_counter()-start
    meta['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out/'run_manifest.json').write_text(json.dumps(meta,indent=2))
    print(json.dumps(meta,indent=2))

if __name__=='__main__':main()
