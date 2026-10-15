"""Create publication figures, tables and numeric macros only from saved results."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core import occupancy_theory

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--results-dir',default='results/confirmatory')
parser.add_argument('--paper-dir',default='paper')
parser.add_argument('--pilot-path',default='results/pilot.json')
args=parser.parse_args()
RESULTS=ROOT/args.results_dir
P=ROOT/args.paper_dir;P.mkdir(parents=True,exist_ok=True)
G=P/'generated';G.mkdir(exist_ok=True)
F=P/'figures';F.mkdir(exist_ok=True)
occ=pd.read_csv(RESULTS/'occupancy_summary.csv')
lin=pd.read_csv(RESULTS/'linear_summary.csv')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,
    'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'axes.labelsize':8,
    'legend.fontsize':7,'xtick.labelsize':7,'ytick.labelsize':7})
colors=['#0072B2','#D55E00','#009E73']

def save(fig,name):
    fig.savefig(F/(name+'.pdf'),bbox_inches='tight')
    fig.savefig(F/(name+'.png'),dpi=180,bbox_inches='tight')
    plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(6.7,2.35),layout='constrained')
ns=np.unique(np.round(np.geomspace(10,800,250)).astype(int))
for K,c in zip([16,128],colors):
    d=occ[(occ.method=='joint')&(occ.K==K)&(occ.alpha==.1)]
    axes[0].plot(ns,[occupancy_theory(int(n),K,.1) for n in ns],color=c,lw=1.2,label=f'K = {K}')
    axes[0].errorbar(d.n,d['mean'],yerr=1.96*d.se,fmt='o',color=c,ms=4,capsize=2)
for ratio,c in zip([1,10,100],colors):
    d=occ[(occ.method=='joint')&(occ.K==occ.n*ratio)&(occ.alpha==.1)]
    axes[1].plot(ns,[occupancy_theory(int(n),int(n)*ratio,.1) for n in ns],color=c,lw=1.2,label=f'K = {ratio}n')
    axes[1].errorbar(d.n,d['mean'],yerr=1.96*d.se,fmt='o',color=c,ms=4,capsize=2)
for ax,title in zip(axes,['A. One family: fixed label universe','B. Different families: K grows with n']):
    ax.axhline(.9,color='0.45',ls='--',lw=.8,label='Nominal 0.9')
    ax.set(xscale='log',xlabel='Calibration sample size n',ylabel='Marginal coverage',ylim=(-.035,1.02),title=title)
    if ax is axes[0]: ax.legend(loc='lower right',frameon=False)
    else: ax.legend(loc='upper right',bbox_to_anchor=(1,.84),ncol=2,frameon=False,columnspacing=.7)
    ax.grid(alpha=.15)
save(fig,'occupancy')

fig,axes=plt.subplots(1,2,figsize=(6.7,2.25),layout='constrained')
for ax,a in zip(axes,[.25,1.]):
    d=lin[lin.a==a].sort_values('n')
    ax.errorbar(d.n,d['mean'],yerr=1.96*d.se,fmt='o-',c=colors[0],label='Observed mean',capsize=2)
    for col,label,c,marker in [('finite_beta_lower','Finite-grid beta',colors[1],'s'),('continuum_lower','Continuum net',colors[2],'^'),('dkw_lower','Finite-grid DKW','0.45','x')]:
        ax.plot(d.n,d[col],marker=marker,color=c,label=label,lw=1)
    ax.axhline(.9,color='0.6',ls='--',lw=.8)
    ax.set(xscale='log',xlabel='Calibration sample size n',ylabel='Coverage / lower bound',ylim=(.58,.93),title=f'Slope range [-{a:g}, {a:g}]')
    ax.grid(alpha=.15)
axes[0].legend(frameon=False,loc='lower right')
save(fig,'certificates')

fig,ax=plt.subplots(figsize=(3.2,1.5),layout='constrained')
pilot=json.loads((ROOT/args.pilot_path).read_text())
matrix=np.asarray(pilot['shattering'],dtype=int).T
assert matrix.shape==(3,8)
ax.imshow(matrix,cmap='Blues',vmin=0,vmax=1,aspect='auto')
for y in range(3):
    for j in range(8): ax.text(j,y,str(matrix[y,j]),ha='center',va='center',color='white' if matrix[y,j] else 'black',fontsize=8)
ax.set(xticks=range(8),xticklabels=[f'{j}/7' for j in range(8)],yticks=range(3),yticklabels=['y=0','y=1','y=2'],xlabel='Scalar parameter knot',title='All eight labelings at one score threshold')
save(fig,'shattering')

def pm(row):return f"{100*row['mean']:.4f} $\\pm$ {196*row['se']:.4f}"
selected=[(99,16,.1),(99,128,.1),(99,990,.1),(99,10000,.1),(499,128,.1)]
table=[]
for n,K,a in selected:
    z=occ[(occ.n==n)&(occ.K==K)&(occ.alpha==a)].set_index('method')
    table.append(f"{n} & {K:,} & {100*z.loc['joint','theory']:.4f} & {pm(z.loc['joint'])} & {pm(z.loc['split'])} "+chr(92)*2)
(G/'occupancy_table.tex').write_text('\n'.join(table)+'\n')
table=[]
for _,r in occ[occ.method=='joint'].iterrows():
    z=occ[(occ.n==r.n)&(occ.K==r.K)&(occ.alpha==r.alpha)].set_index('method')
    table.append(f"{int(r.n)} & {int(r.K):,} & {r.alpha:g} & {100*r.theory:.4f} & {pm(r)} & {pm(z.loc['fixed'])} & {pm(z.loc['split'])} "+chr(92)*2)
(G/'all_occupancy_table.tex').write_text('\n'.join(table)+'\n')
table=[]
for _,r in lin.iterrows():
    table.append(f"{int(r.n)} & {r.a:g} & {pm(r)} & {100*r.finite_beta_lower:.4f} & {100*r.continuum_lower:.4f} & {100*r.dkw_lower:.4f} & {int(round(r.continuum_violation_rate*r.repetitions))} "+chr(92)*2)
(G/'linear_table.tex').write_text('\n'.join(table)+'\n')
s=occ[(occ.n==99)&(occ.K==10000)&(occ.alpha==.1)].set_index('method')
manifest=json.loads((RESULTS/'run_manifest.json').read_text())
values={
 'SevereMean':f"{100*s.loc['joint','mean']:.4f}",
 'SevereTheory':f"{100*s.loc['joint','theory']:.4f}",
 'SevereCI':f"{196*s.loc['joint','se']:.4f}",
 'SevereFixed':f"{100*s.loc['fixed','mean']:.4f}",
 'SevereSplit':f"{100*s.loc['split','mean']:.4f}",
 'NumOccupancyCases':str(len(occ[occ.method=='joint'])),
 'RunSeconds':f"{manifest['elapsed_seconds']:.2f}"
}
(G/'values.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in values.items())+'\n')
(G/'values.json').write_text(json.dumps(values,indent=2))
inputs=[RESULTS/'occupancy_summary.csv',RESULTS/'linear_summary.csv',RESULTS/'run_manifest.json',ROOT/args.pilot_path,Path(__file__).resolve(),ROOT/'src/core.py']
(G/'figure_sources.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
print(json.dumps(values,indent=2))
