"""Retrieve inspected public sources into a NEW directory; retain audit hashes."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
VERSIONS={'yang':'2104.13871v3','liang':'2408.07066v4','crc':'2208.02814v4',
          'aldirawi2026':'2604.01502v2','vovk2012':'1209.2673v2','angelopoulos2026':'2602.20151v1'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--key',action='append');args=p.parse_args()
    dest=ROOT/args.output;dest.mkdir(parents=True,exist_ok=False)
    records=[]
    for original in json.loads((ROOT/'literature/source_manifest.json').read_text()):
        key=original['key']
        if not original.get('sha256') or (args.key and key not in args.key):continue
        url='https://arxiv.org/pdf/'+VERSIONS[key] if key in VERSIONS else original['url']
        row=dict(key=key,url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),expected_sha256=original['sha256'])
        try:
            response=requests.get(url,timeout=50);response.raise_for_status()
            ext='.pdf' if response.content.startswith(b'%PDF') else '.html'
            file=dest/(key+ext);file.write_bytes(response.content)
            digest=hashlib.sha256(response.content).hexdigest()
            row.update(status=response.status_code,file=file.name,sha256=digest,original_bytes_match=digest==original['sha256'])
            if ext=='.pdf':subprocess.run(['pdftotext','-layout',str(file),str(file.with_suffix('.txt'))],check=True)
            else:file.with_suffix('.txt').write_text(BeautifulSoup(response.text,'html.parser').get_text('\n',strip=True))
        except Exception as exc:row['error']=str(exc)
        records.append(row);print(json.dumps(row),flush=True)
    (dest/'retrieval_manifest.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
