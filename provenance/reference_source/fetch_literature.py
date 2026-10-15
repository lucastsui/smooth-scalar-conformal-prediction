"""Archive public research sources, recording byte hashes and retrieval times."""
from pathlib import Path
import datetime, hashlib, json, subprocess
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'zeng2025': 'https://raw.githubusercontent.com/mlresearch/v267/main/assets/zeng25e/zeng25e.pdf',
    'yang': 'https://arxiv.org/pdf/2104.13871',
    'liang': 'https://arxiv.org/pdf/2408.07066',
    'crc': 'https://arxiv.org/pdf/2208.02814',
    'aldirawi2026': 'https://arxiv.org/pdf/2604.01502',
    'vovk2012': 'https://arxiv.org/pdf/1209.2673',
    'traub2024': 'https://proceedings.neurips.cc/paper_files/paper/2024/file/047c84ec50bd8ea29349b996fc64af4b-Paper-Conference.pdf',
    'icml2026_call': 'https://icml.cc/Conferences/2026/CallForPapers',
    'icml2026_authors': 'https://icml.cc/Conferences/2026/AuthorInstructions',
    'icml2026_reviewers': 'https://icml.cc/Conferences/2026/ReviewerInstructions',
    'icml2027_call_check': 'https://icml.cc/Conferences/2027/CallForPapers',
    'zeng_repo': 'https://raw.githubusercontent.com/ml-stat-Sustech/Parametric-Scaling-Law-CP-Tuning/main/README.md',
}

def main():
    records = []
    for key, url in SOURCES.items():
        record = dict(key=key, url=url, retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        try:
            r = requests.get(url, timeout=50)
            record.update(status=r.status_code, final_url=r.url)
            r.raise_for_status()
            ext = '.pdf' if r.content.startswith(b'%PDF') else '.html'
            p = ROOT / 'literature' / (key + ext)
            p.write_bytes(r.content)
            record.update(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(r.content).hexdigest())
            if ext == '.pdf':
                subprocess.run(['pdftotext', '-layout', str(p), str(p.with_suffix('.txt'))], check=True)
            else:
                p.with_suffix('.txt').write_text(BeautifulSoup(r.text, 'html.parser').get_text('\n', strip=True))
            print(key, r.status_code, len(r.content), flush=True)
        except Exception as e:
            record['error'] = str(e)
            print(key, 'ERROR', str(e), flush=True)
        records.append(record)
    (ROOT / 'literature' / 'source_manifest.json').write_text(json.dumps(records, indent=2))

if __name__ == '__main__':
    main()
