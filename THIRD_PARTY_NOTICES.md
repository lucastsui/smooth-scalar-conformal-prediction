# Third-party material

The files `paper/icml2026.sty`, `paper/icml2026.bst`, `paper/algorithm.sty`, `paper/algorithmic.sty` and `paper/fancyhdr.sty` come unchanged from the [official ICML 2026 style archive](https://media.icml.cc/Conferences/ICML2026/Styles/icml2026.zip). Their original notices and licenses remain in the files. Byte comparisons are recorded in `provenance/style_manifest.json`. Frozen manuscript snapshots contain copies of these same files.

Inspected research papers and official web pages are identified in `literature/source_manifest.json` and `paper/references.bib`. Their full downloaded PDFs/text and raw search-result excerpts are not redistributed in this repository or its portable archive. The local working directory retains the retrieved documents for auditing. To fetch the recorded sources into a new directory, run:

```bash
.venv/bin/python src/fetch_literature.py --output tmp/retrieved_sources
```

The downloader preserves the original audit manifest, requests the inspected arXiv versions, and records whether newly retrieved bytes match. Website changes or PDF metadata changes can alter hashes; a mismatch requires inspection and is not silently treated as the same source. This retrieval step is optional and is not required to reproduce the synthetic experiments.

Python dependencies are installed separately from the pinned lock file and retain their respective licenses. This project does not assert ownership of those dependencies, the official template, or cited research.
