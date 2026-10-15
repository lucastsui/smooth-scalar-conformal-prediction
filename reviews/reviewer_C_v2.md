# Separate AI review C, cycle 2: clarity and reproducibility

Review date: 2026-09-28. This is a second AI review of the revised artifact, not external human peer review or independent expert validation. I reassessed the evidence rather than increasing the recommendation automatically after revisions.

Reviewed frozen PDF: `reviews/frozen_v2/main.pdf`, SHA-256 `af9c88d9acfcac97d3663b442a7abd358fb9fc4f2d6f20d9d5e3618fb78bf004`. The frozen manuscript, source, and original experimental results were not edited. All review outputs are under `reviews/C_v2/`.

**Neutral summary.** The manuscript retains the smooth scalar occupancy counterexample, population-rank covering certificate, and a careful distinction between fixed-family consistency and lack of uniform rates across families. The revision explicitly attributes qualitative consistency to classical uniform-convergence theory. Its numerical evidence remains a set of synthetic implementation checks and conservative oracle examples. The substantive contribution has been narrowed, while the reproduction package has become materially more complete.

**Merits and verified resolution of cycle-1 issues.**

| Issue | Cycle-2 evidence | Assessment |
|---|---|---|
| C1: incomplete source freeze | All 21 files in the recursive manifest matched their hashes, as did the seven external evidence hashes and six figure-source hashes. I copied the snapshot and the unmodified build helper into a separate review project and built it successfully. Extracted text was byte-identical, and all ten rendered pages were pixel-identical at 100 dpi to the frozen PDF. | Resolved for reconstruction on this host. |
| C2: missing documented reproduction route | The README now gives install, run, comparison, fresh-output artifact generation, and PDF build commands. A fresh isolated Python 3.12.12 environment installed all 31 locked distributions. System site packages were disabled. The documented reproduction runner passed eight tests and reproduced all 28 raw payloads and scientific summaries within `9.547918011776346e-15`, below the stated `1e-12` tolerance. | Resolved for a fresh Python environment on this host; this is not clean-machine validation. |
| C3: Figure 3 provenance | The generator now reads the pilot's saved `shattering` values. The saved array is binary, has shape `(8, 3)`, and contains all eight distinct rows. Input and generator hashes are recorded. Regeneration from fresh results produced a shattering PNG pixel-identical to the frozen one. | Resolved. The figure now follows the executed-data chain. |
| C4: unspecified fixed control/reference | Section 6.1 names `S(U,Y)=U`, and Figure 2 identifies the dashed line as the analytic fixed-score target 0.9. | Resolved. |
| C5: overlapping legend and mixed units | Figure 1B's legend occupies clear space. Table 3 reports coverage and all certificates in percent. All three regenerated table files were byte-identical to frozen v2, and all three regenerated figure PNGs were pixel-identical. | Resolved. |

The new README describes the mathematical and computational scope accurately. It documents the Python environment and required system tools, the distinction between the original run and numerical fixes, and the limitation of large-K mask evaluation. The original five source files are preserved under `provenance/reference_source/`; I checked their hashes against the original run manifest and all matched.

The fresh confirmatory computation took 10.74 seconds. The eight tests took 25.56 seconds in this newly populated environment. Regeneration changed only the runtime macro from `10.88` to `10.74`; the scientific numerical macros and all table strings were unchanged. I did not treat PDF-byte differences caused by build metadata as a failure: extracted text and rendered pages agreed exactly.

**Remaining rejection reasons and limitations.**

I found no remaining clarity or local-reproducibility failure that would independently justify rejection. The earlier artifact problems have been addressed with executable evidence, not merely statements of intent. The following matters remain:

1. **Conference significance remains unresolved.** The consistency result is now explicitly classical, and the beta-cover certificate is presented as a synthesis without a demonstrated tightness, practical, or algorithmic advantage. The surviving contribution is chiefly the strengthened smooth/atomless, recalibrated-score construction and its exact occupancy law. That may be valuable as a correction or focused theoretical note, but successful reproduction does not establish that it clears the significance threshold for a full ICML paper. The issue-resolution table correctly keeps this concern open. I did not independently settle it in this pass.

2. **Portability is bounded by the scope of the executed check.** The fresh environment shared this host's Python installation, package cache, system libraries, fonts, TeX distribution, and Poppler tools. The 31 locked distributions installed successfully into an isolated site-packages directory, but I did not test a cold-cache download, another operating system/architecture, or a machine without the existing system tools. These are unverified dimensions, not observed failures. No broader portability claim is warranted by this check.

3. **Minor release provenance improvement.** The frozen v2 manifest covers manuscript dependencies and selected external scientific evidence, but does not itself hash `requirements.lock.txt`, the README, or the new reproduction/build helpers. A final research-archive manifest should include those files so that the successful procedure is tied to an immutable release. My build audit separately records the exact copied build-helper hash. This is not a blocker for understanding or reproducing the current local package.

4. **Minor layout defect.** The final word of the conclusion, “open.”, appears alone at the top of page 7. It is legible but should be brought back into its paragraph before final release. The remaining pages, figures, equations, and tables were readable in the complete visual inspection. I reviewed frozen v2 as it stands and did not modify this defect.

These observations do not imply a new empirical contradiction. No practical benchmark has been added, and none is needed merely to make the synthetic implementation checks reproducible. Stronger scientific claims would require stronger evidence than the current examples.

**Questions that could change the assessment.**

- Does external domain-expert review regard the exact smooth/atomless occupancy construction as a consequential correction or sufficient theoretical advance beyond prior non-monotone conformal counterexamples?
- Will the final portable archive include and hash the full environment specification, entrypoints, reviewed evidence, and source history needed to reconstruct this precise research state?
- Does the documented pipeline work on a second host with declared system dependencies? Such a result would increase confidence in portability; it would not by itself improve the scientific novelty assessment.

**Tentative recommendation and confidence.** Weak accept on the clarity and reproducibility remit, unchanged from cycle 1; moderate confidence. The local artifact evidence is stronger, and all five original C issues are resolved. The conference-level significance concern remains, so this is not an endorsement of ICML readiness or acceptance. I would not reject this version for inability to repeat its reported synthetic experiments on the tested host.

**Checked scope and audit records.**

- Read the revised frozen TeX and all manuscript changes, `reviews/issue_resolution.md`, README, new reproduction/build/verification helpers, revised artifact generator, numerical-code changes, tests, manifests, and source provenance.
- Created `reviews/C_v2/.venv` using `uv venv --python 3.12.12`; installed `requirements.lock.txt` using `uv pip sync`. Verified 31 installed versions against all 31 lock entries after normalizing package-name aliases. Evidence: `environment_audit.json`.
- Executed `reviews/C_v2/.venv/bin/python src/reproduce.py --output reviews/C_v2/fresh_results`. This ran the eight tests, unchanged confirmatory configuration, and comparisons of raw arrays, scientific CSV fields, and the sampled-test audit JSON. Evidence: `fresh_results/tests.txt`, `execution.txt`, `run_manifest.json`, and `comparison.json`.
- Verified recursive frozen hashes and external evidence hashes. Evidence: `snapshot_audit.json`. Verified the archived original source bytes against their recorded hashes: `original_source_audit.json`.
- Copied frozen v2 into `build_project/paper`, copied the build helper unchanged into `build_project/src`, and compiled there with the fresh environment. Build logs are preserved under `build_project/logs`. Evidence: `build_audit.json`; rebuilt PDF: `build_project/output/rebuilt.pdf`.
- Rendered and visually inspected all ten frozen pages. Compared all ten rebuilt page images with the frozen render; every page was pixel-identical at the checked resolution.
- Regenerated figures and tables using `--results-dir reviews/C_v2/fresh_results --paper-dir reviews/C_v2/regenerated_paper --pilot-path results/pilot.json`. Compared all three tables, three figure PNGs, numerical macros, and recorded input hashes. Evidence: `artifact_audit.json` and `artifact_generation.txt`.

**Unverified scope.** No clean-machine or cross-platform installation, independent reimplementation, new-seed scientific replication, rerun of the original pilot, practical neural-network experiment, exhaustive literature novelty audit, or formal proof verification was performed. I read the new classical reduction for clarity but did not independently validate its cited source in this pass. The frozen-source rebuild and the fresh-results artifact regeneration were tested separately; I did not compile the regenerated-assets copy into a second PDF. No claim of external human validation follows from any of these checks.
