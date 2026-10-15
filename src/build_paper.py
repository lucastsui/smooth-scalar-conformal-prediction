"""Compile the official-template manuscript with checked sequential commands."""
from pathlib import Path
import argparse, shutil, subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--paper-dir',default='paper');p.add_argument('--output',default='output/pdf/manuscript.pdf');args=p.parse_args()
    paper=ROOT/args.paper_dir;logdir=ROOT/'logs';logdir.mkdir(exist_ok=True)
    commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],['bibtex','main'],
        ['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex']]
    for i,cmd in enumerate(commands):
        log=logdir/f'build_{i}_{cmd[0]}.txt'
        with log.open('w') as stream:
            subprocess.run(cmd,cwd=paper,stdout=stream,stderr=subprocess.STDOUT,check=True)
    text=(paper/'main.log').read_text(errors='replace')
    errors=[x for x in ['Overfull \\hbox','undefined references','undefined citations','AUTHORERR'] if x in text]
    if errors:raise RuntimeError('Layout/citation issues require inspection: '+str(errors))
    output=ROOT/args.output;output.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(paper/'main.pdf',output)
    subprocess.run(['pdftotext','-layout',str(output),str(paper/'main.txt')],check=True)
    print(output)

if __name__=='__main__':main()
