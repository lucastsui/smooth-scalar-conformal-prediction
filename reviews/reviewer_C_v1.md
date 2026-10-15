# Separate AI review C: clarity and reproducibility

Review date: 2026-09-28. This is an AI-generated review, separate from the other requested passes. It is not external human peer review or independent expert validation. I reviewed the frozen v1 manuscript and the project files present at the start of this pass; planned packaging changes do not erase the findings below.

Frozen PDF: `reviews/frozen_v1/main.pdf`, SHA-256 `e8e9d171e386a08b1027bb598fae41c183976c4db9027e6fb85f0da90d264229`. All four hashes in the frozen manifest matched. I did not edit the manuscript, experiment code, or original results.

**Neutral summary.** The paper constructs a smooth scalar conformal-score family whose adaptive coverage has an exact occupancy formula. It uses this example to distinguish a lack of uniform finite-sample guarantees across families from consistency of each fixed compact, atomless, Lipschitz family. A population-rank covering argument gives sufficient beta-tail certificates. The experiments check exact identities and illustrate conservative oracle bounds; they are not application benchmarks or evaluations of a practical replacement method.

The paper makes these distinctions unusually explicit. A reader can reconstruct the main score construction, selector, quantile convention, and conditional-coverage calculation from the manuscript. The numerical headline is reproducible in the supplied environment. The principal remaining problems concern a portable reproduction route and the provenance of one plotted check.

**Merits.**

- The setup separates calibration-conditional coverage from marginal coverage and states the `k = n + 1` convention. This prevents several common ambiguities in conformal simulations.
- The increasing-precision requirement, exponential number of alternatives, exact mask implementation, discontinuous selection objective, and distinction between fixed and changing families are prominent in the abstract, main text, and appendix. I found no claim that ordinary temperature scaling exhibits the severe failure.
- The manuscript distinguishes Monte Carlo uncertainty from theorem validity, uses calibration samples as the uncertainty unit, reports the disjoint control's actual order-statistic target, and separates pointwise certificate confidence from confidence across all settings.
- The complete confirmatory execution succeeded. All 28 NPZ payloads reproduced exactly: 21 occupancy settings, six linear settings, and the independent-test audit. All scientific CSV fields, random-input hashes, and the audit JSON matched the original results. Runtime was 10.64 seconds, compared with 10.88 seconds for the original run, on the supplied environment.
- All six existing tests passed. Independent recalculation of saved raw means and standard errors agreed with the summary CSVs to at most `1.11e-16`. All 21 full occupancy table rows and six linear table rows agree with those summaries to their stated rounding. The fixed and monotone control outcomes differ by at most `2.22e-16`.

**Rejection concerns and required revisions.** I found no failed quantitative headline or experimental discrepancy that by itself justifies rejection. The following issues would nevertheless weaken an artifact or reproducibility assessment if left in the released package.

1. **Moderate: the frozen source is not a self-contained reconstruction of the frozen PDF.** `reviews/frozen_v1/main.tex` imports `generated/values`, three generated tables, and three figures, and uses the ICML class/style dependencies. The frozen directory and its four-file manifest do not contain or hash these dependencies. They exist under the mutable `paper/` directory. Consequently, possession of the frozen source snapshot alone is insufficient to rebuild it, and the snapshot does not establish which asset bytes produced the reviewed PDF. Freeze the complete source dependency tree and record recursive hashes. A source-and-assets snapshot is needed in addition to a PDF hash.

2. **Moderate: numerical reproduction currently depends on knowing an undocumented entrypoint and an already working environment.** At the start of the review there was no project README or reproduction/build entrypoint. The Python lock file and manuscript's Python version are useful, but they do not give a complete install/run/compare/build sequence or describe the external TeX/Poppler dependencies. I could execute the code because the review task supplied the command and a populated `.venv`. Moreover, `src/make_artifacts.py` reads `results/confirmatory` and writes `paper/` through hard-coded paths, so a reader cannot simply point it at a fresh reproduction directory. Supply explicit clean-environment instructions, non-overwriting output handling, a scientific-results comparison command, and a documented route from fresh results to tables/figures/PDF. The exact local rerun establishes same-environment repeatability, not clean-machine portability.

3. **Moderate but localized: Figure 3's caption overstates the provenance of the plotted data.** The caption calls it an “Executed exhaustive check.” In `src/make_artifacts.py`, the matrix is constructed directly from `[(mask >> y) & 1 ...]`; it does not read the executed pilot's `shattering` values or call `scalar_score`. The saved pilot and the passing exhaustive test independently confirm this matrix, so I found no incorrect mathematical value. Nevertheless, the figure is currently a drawing of the expected truth table, not a plot of the executed check. Read the saved pilot results (and verify their expected shape/content), or label the figure as an illustration and cite the separately executed check.

4. **Minor: define the fixed control explicitly.** Section 6.1 calls it “a fixed score,” while the code saves the uniform order statistic as its conditional coverage. State `S(U,Y)=U`, or the equivalent full-label knot after positive rescaling. This makes the particular paired control reproducible without inspecting the implementation. The linear fixed control is saved in the raw data and summary but omitted from the full linear results table; either show it or state plainly that the dashed reference is the analytic fixed-score target.

5. **Minor: improve figure and unit readability.** In the rendered Figure 1B, the legend overlaps the `K=n` curve. Move it into clear space or outside the plotting area. Table 3 mixes percent coverage with probability-valued certificates; its caption does disclose this, but using one unit throughout would make the comparisons less error-prone. I found no clipping or unreadable table entries in the ten rendered pages.

These are concrete reproducibility/presentation concerns, not evidence that the occupancy identity or certificates are false. The paper's contribution may still be too narrow for a full conference paper; this pass did not independently audit the literature sufficiently to settle that question.

**Questions that could change my assessment.**

- Can a reader install the declared environment, execute all checks into a new directory, and rebuild the complete frozen source without undocumented local dependencies or replacing original results?
- Will the released snapshot include immutable figure/table inputs and generator hashes, as well as the result-producing code and configuration?
- Can Figure 3 be traced directly to stored or freshly evaluated scalar-score predictions? The current saved pilot suggests this is a straightforward correction.
- Is the contribution intended principally as a correction/counterexample plus a consistency clarification, or as a broadly useful new guarantee? The current evidence supports the former framing. An attempt to claim the latter would need substantially more than the oracle examples presented here.

**Tentative recommendation and confidence.** Weak accept on the clarity and reproducibility evidence reviewed here, with the above artifact revisions required before release; moderate confidence. The main construction and scope are understandable, and the entire quantitative suite repeated exactly. This recommendation does not certify mathematical originality, a complete proof audit, clean-machine portability, or ICML acceptance.

**What I actually checked.**

- Read the frozen TeX, PDF, configuration, confirmatory protocol, core implementation, experiment runner, tests, pilot implementation/results, artifact generator, generated tables, result manifests, contribution statement, research log, and closest-work matrix.
- Rendered and visually inspected all ten frozen PDF pages using Poppler.
- Executed `.venv/bin/python -m pytest -q src/test_core.py`: six passed in 0.41 seconds.
- Executed `.venv/bin/python src/experiments.py --output reviews/C_reproduction`: all settings completed, without changing original results.
- Compared all NPZ arrays and column names, both CSVs excluding timing fields, the audit JSON, source/configuration hashes, and the frozen manifest. Details are preserved in `reviews/C_reproduction/reviewer_comparison.json`.
- Recomputed raw means/standard errors and checked generated full-table values against the summaries. Details are preserved in `reviews/C_reproduction/reviewer_table_audit.json`.
- Inspected selection/evaluation separation in code: the synthetic test audit and population CDF evaluation are not used to select the score; the split control uses disjoint tuning/calibration subsets.

**Unverified.** I did not install dependencies in a clean environment, rebuild the PDF, rerun the pilot (which writes to original paths), run a new independent implementation or new-seed replication, audit every literature claim against external sources, reproduce a practical model benchmark, or formally verify the proofs. The fresh execution uses the same code, seeds, and supplied environment, and must not be described as an independent scientific replication.
