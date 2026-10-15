"""Freeze a complete, buildable manuscript dependency tree without overwrites."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    source=ROOT/'paper';dest=ROOT/args.output
    dest.mkdir(parents=True,exist_ok=False)
    for name in ['main.tex','main.pdf','main.txt','references.bib','icml2026.sty',
                 'icml2026.bst','algorithm.sty','algorithmic.sty','fancyhdr.sty']:
        shutil.copy2(source/name,dest/name)
    for name in ['generated','figures']:
        shutil.copytree(source/name,dest/name)
    files={str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted(dest.rglob('*')) if p.is_file()}
    evidence=['configs/confirmatory.json','results/confirmatory/run_manifest.json',
              'results/revision1_reproduction/comparison.json','src/core.py',
              'src/experiments.py','src/test_core.py','src/make_artifacts.py']
    record=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=files,
        external_evidence_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in evidence},
        note='Complete manuscript dependency snapshot; external evidence is supplied in the parent research package. Manifest does not hash itself.')
    (dest/'manifest.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(dict(snapshot=str(dest),files=len(files),pdf_sha256=files['main.pdf']),indent=2))

if __name__=='__main__':main()
