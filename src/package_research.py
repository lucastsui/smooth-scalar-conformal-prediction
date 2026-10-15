"""Create a portable research archive and verify every archived byte hash."""
from pathlib import Path
import datetime,hashlib,json,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'.md','.py','.json','.txt','.csv','.npz','.tex','.bib','.sty','.bst','.pdf','.png','.log','.bundle'}
FOLDERS={'src','configs','protocols','results','paper','reviews','literature','provenance','logs'}

def included(path):
    rel=path.relative_to(ROOT);parts=rel.parts
    if any(x in {'.venv','.git','__pycache__','.pytest_cache','tmp'} for x in parts):return False
    if len(parts)==1:return path.suffix=='.md' or path.name in {'requirements.lock.txt','.gitignore'}
    if rel.as_posix()=='output/pdf/manuscript.pdf':return True
    if parts[0] not in FOLDERS or path.suffix not in ALLOWED:return False
    if parts[0]=='literature':return path.suffix in {'.md','.json'}
    if parts[:2]==('reviews','A_sources'):return path.suffix in {'.md','.json'}
    if parts[:2]==('reviews','B_checks') and path.suffix=='.png':return False
    if path.name=='example_paper.tex':return False
    if path.name in {'main.log','main.aux','main.out','main.bbl','main.blg'}:return False
    if parts[0]=='logs' and path.name=='archive_verification.json':return False
    return True

def main():
    out=ROOT/'output/research-package.zip';out.parent.mkdir(exist_ok=True)
    if out.exists():raise RuntimeError('Archive exists; preserve or explicitly relocate it before making a new release.')
    # Prune virtual environments before traversal; they are never read or archived.
    import os
    files=[]
    for directory,dirs,names in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in {'.venv','.git','__pycache__','.pytest_cache','tmp'}]
        for name in names:
            path=Path(directory)/name
            if included(path):files.append(path)
    files.sort()
    records={p.relative_to(ROOT).as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files}
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),local_git_commit=commit,
        files=records,note='Includes the public research snapshot and available supporting evidence. The original protocol Git bundle remains in the local archive. Excludes environments, caches, third-party full papers and regenerable reviewer page renders. Does not include or hash itself.')
    manifest_text=json.dumps(manifest,indent=2)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in files:z.write(path,'research-package/'+path.relative_to(ROOT).as_posix())
        z.writestr('research-package/PACKAGE_MANIFEST.json',manifest_text)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for name,row in records.items():
            content=z.read('research-package/'+name)
            assert len(content)==row['bytes'] and hashlib.sha256(content).hexdigest()==row['sha256'],name
        assert all('/.venv/' not in n and '/.git/' not in n for n in z.namelist())
    digest=hashlib.sha256(out.read_bytes()).hexdigest()
    out.with_suffix('.zip.sha256').write_text(digest+'  '+out.name+'\n')
    (ROOT/'output/PACKAGE_MANIFEST.json').write_text(manifest_text)
    report=dict(archive=str(out.relative_to(ROOT)),files_checked=len(records),bytes=out.stat().st_size,sha256=digest,crc_and_all_hashes_pass=True)
    (ROOT/'logs/archive_verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
