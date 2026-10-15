# Limits of Smooth Scalar Tuning in Split Conformal Prediction

**Ming Leong Tsui — Boston University**

[Read the paper (PDF)](output/pdf/manuscript.pdf) · [LaTeX source](paper/main.tex) · [Claim and evidence map](claim_evidence.md)

Research draft and reproducibility materials, publicly shared on October 15, 2026. The study was developed on September 28, 2026; the current manuscript includes the author's October 2 revision. It has not been submitted to a conference or externally peer reviewed. The original assessment identifies significance relative to established theory as an unresolved concern; see [READINESS.md](READINESS.md).

This repository includes proofs, synthetic experiments, code, frozen protocols, and AI review records. The reviews concern the historical snapshots preserved in `reviews/`; the current manuscript is a later revision. See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the publication scope.

The central result is an exact counterexample: a smooth bounded 1-Lipschitz scalar score family can have arbitrarily low finite-sample coverage after using the calibration data for selection. A population-rank covering argument gives sufficient conditions for coverage. Fixed-family consistency is explicitly attributed to classical uniform convergence, not claimed as new. The scalar hides a large discrete search, and no practical neural-network failure or new state-of-the-art method is claimed.

## Start here

- `output/pdf/manuscript.pdf`: current authored manuscript.
- `paper/main.tex`, `paper/references.bib`, `paper/figures/`, `paper/generated/`: editable manuscript and assets.
- `CONTRIBUTION.md`: concise claim, significance, evidence and principal limitation.
- `claim_evidence.md`: map from every major claim to proof/code/results.
- `literature/closest_work.md`, `literature/bibliography_audit.md`: positioning and reference verification.
- `reviews/`: frozen drafts, separate review passes and issue resolution.
- `RESEARCH_LOG.md`, `protocols/`, `configs/`: decisions and fixed experimental specifications.
- `results/confirmatory/`: raw calibration-level outputs, CSV summaries, independent test audit and run manifest.

## Reproduce the results

No external dataset, network access after dependency installation, trained model, GPU or API key is needed. The recorded environment uses Python 3.12.12, NumPy 2.5.3, SciPy 1.18.1 and an Apple M4 Max. Exact dependencies are in `requirements.lock.txt`.

From the package root, with [uv](https://docs.astral.sh/uv/) installed:

```bash
uv venv --python 3.12.12 .venv
uv pip sync --python .venv/bin/python requirements.lock.txt
.venv/bin/python src/reproduce.py
```

The runner executes eight verification tests, creates a new timestamped results directory, runs the frozen configuration, and compares all 28 raw result payloads and scientific summary columns to the archived run. It never overwrites completed reference results. Floating-point comparisons allow absolute error up to 1e-12; runtime is intentionally excluded. The recorded confirmatory computation took 10.88 seconds; dependency setup and writing were separate. Review fixes for tiny slopes and infinite thresholds changed the original numerical results by at most 9.55e-15. Original source bytes are preserved under `provenance/reference_source/` for exact same-environment replay.

To compare an existing reproduction without rerunning it:

```bash
.venv/bin/python src/reproduce.py --compare-only results/revision1_reproduction
```

To inspect or rerun only a component:

```bash
.venv/bin/python -m pytest -q src/test_core.py
.venv/bin/python src/experiments.py --output results/my_fresh_run
```

The exploratory pilot is separately reproducible with `src/pilot.py`; it overwrites only the pilot artifacts and is not part of confirmatory evaluation. Keep the archived copy if auditing the original pilot.

## Rebuild the manuscript

LaTeX with the usual ICML dependencies, BibTeX and Poppler (`pdftotext`, `pdftoppm`, `pdfinfo`) are needed. The official ICML 2026 style files are included unchanged; the source changes only the local-draft notice. The eight-page main-body rule is provisional because the target ICML 2027 rules were unavailable when checked.

```bash
.venv/bin/python src/make_artifacts.py
.venv/bin/python src/build_paper.py
.venv/bin/python src/verify_package.py
mkdir -p tmp/pdfs
pdftoppm -r 110 -png output/pdf/manuscript.pdf tmp/pdfs/review
```

The figures and tables are generated from saved results; numerical claims are not entered from memory. Programmatic checks do not substitute for visually inspecting the rendered pages. PDF bytes may vary with timestamps and TeX versions even when scientific results match.

To rebuild from a fresh numerical run without changing the archived manuscript, substitute its output directory below:

```bash
mkdir -p tmp
cp -R paper tmp/regenerated_paper
.venv/bin/python src/make_artifacts.py --results-dir results/my_fresh_run --paper-dir tmp/regenerated_paper
.venv/bin/python src/build_paper.py --paper-dir tmp/regenerated_paper --output tmp/regenerated.pdf
```

`reviews/frozen_final/` contains the final September 28 reviewed source-and-assets snapshot and a recursive SHA-256 manifest; `frozen_v2/` preserves the second review input. These historical snapshots predate the October 2 author revision in `paper/` and `output/pdf/manuscript.pdf`. Copy a snapshot to a fresh directory before rebuilding. `src/build_paper.py --paper-dir <copy> --output <new.pdf>` compiles it without regenerating assets. The v1 snapshot lacked dependencies; this is retained as a documented review finding rather than retroactively overwritten.

Reviewer C installed all 31 locked distributions into a fresh isolated Python 3.12.12 environment on the same host, passed all eight checks, reproduced the scientific outputs within 9.55e-15, and rebuilt a snapshot with identical extracted text and rendered pages. This verifies same-host environment reconstruction, not cross-platform or clean-machine portability. Details are in `reviews/C_v2/`.

## Data and statistical interpretation

Twenty-one occupancy settings use 10,000 independent calibration samples each; six regular-family settings use 1,000 each. A separate severe-case audit uses 1,000 calibration samples with 1,000 fresh test points each. The unit for reported uncertainty is an independent calibration sample. Pointwise intervals are mean ±1.96 Monte Carlo standard errors. Conditional coverage is integrated analytically where possible, with an independent sampled-test audit as a check.

Large-label experiments use an exact mask representation of the scalar construction. They do not numerically optimize a huge-precision smooth scalar. Disjoint recalibration uses the same total sample budget and therefore a smaller calibration subset. Its finite-sample target is reported correctly. Fixed-family convergence and sequences of different families are kept distinct.

## Provenance and boundaries

The protocol was frozen in local Git before confirmatory data generation; the reference run records commit `02b4f3ef1a20e0f35e344a9b10eeef871bdbdb78`, source hashes, configuration hash and input hashes. This was a local protocol commitment, not a registry preregistration. The original protocol Git bundle is retained in the local research archive and is not redistributed here because it embeds raw third-party search-result text. The original commit identifiers remain in the audit records; this public repository starts with a new snapshot commit. The source manifest gives URLs, versions, retrieval dates and hashes for inspected literature. Third-party research PDFs are retained locally but excluded from the portable archive; `THIRD_PARTY_NOTICES.md` describes safe retrieval.

Running the packaging command creates a portable ZIP with `PACKAGE_MANIFEST.json` and per-file SHA-256 hashes. The ZIP's separate `.sha256` file identifies the generated archive bytes. `src/package_research.py` creates and verifies a new archive; it refuses to replace an existing one. Environments, caches, downloaded third-party papers and regenerable reviewer page images are excluded. Original results, revised rerun evidence, review reports and checks remain included.

The project used AI assistance throughout, including three separate AI reviewers. Those passes do not constitute external expert validation. No paid compute, outreach, publication or submission took place during the original research cycle. This repository publicly shares the draft and supporting materials; it is not a conference submission or a peer-reviewed publication. Responsible human authorship, external novelty/technical review and target-year compliance remain necessary before any submission.
