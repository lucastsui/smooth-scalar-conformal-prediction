# Candidate assessment (exploratory, before the pilot)

Scores below are provisional judgments on a 1–5 scale, not calibrated probabilities of novelty or acceptance.

| Candidate | Significance | Plausible originality | Testability | Local feasibility |
|---|---:|---:|---:|---:|
| A. Regularity needed for low-dimensional conformal tuning | 4 | 3 | 5 | 5 |
| B. Tie-aware risk–coverage evaluation | 3 | 2 | 5 | 5 |
| C. Dependence-sensitive conformal model selection | 4 | 3 | 4 | 4 |
| D. Uncertainty of paired conformal coverage comparisons | 3 | 2 | 5 | 5 |
| E. Seed-selection optimism in small benchmark studies | 3 | 1 | 5 | 5 |

## A — Primary: parameter dimension versus probability-scale complexity

Question: Which regularity assumptions actually control coverage loss when a scalar score parameter is chosen on the calibration sample? Why it matters: low parameter count is used to justify data reuse, but the induced threshold class determines statistical complexity. Closest work: Zeng et al. (ICML 2025), especially Proposition 4.6 and Lemmas D.3/D.5; Yang and Kuchibhotla on finite-family selection; Angelopoulos et al. on non-monotone CRC. Proposed difference: an exactly analyzable split-conformal construction with a compact smooth 1-Lipschitz scalar parameter and atomless scores, plus a probability-scale covering argument that distinguishes no uniform finite-sample rate from consistency of each fixed family. The general warning that dimension is not VC dimension is old and is not claimed as new.

Evidence: a complete proof, explicit shattering examples, exact coverage calculations, simulations validating implementation, and a careful comparison with earlier CRC counterexamples. Cheapest pilot: enumerate eight masks on three labels and simulate an occupancy selector at n=9, K=12. Resources: minutes of CPU and no external data. Failure modes: an overlooked assumption in the published claim; a previous theorem already establishes the exact strengthened statement; a tie, quantile-index or independence error. Abandon or narrow if any of those arise. A technically correct correction may still lack ICML-level significance.

## B — Fallback: ties in risk–coverage summaries

Question: How much of a reported AURC improvement can arise solely from within-tie ordering after confidence quantization? Why it matters: confidence values may be discretized in deployment or saved at limited precision. Closest work: Traub et al., *Overcoming Common Flaws in the Evaluation of Selective Classification Systems* (NeurIPS 2024), inspected full paper; existing AURC implementations. Proposed difference: exact expected AURC and attainable range under random tie-breaking, followed by a reproducibility audit of quantized outputs. Evidence: combinatorial derivation and actual rank reversals in openly licensed model predictions. Pilot: exhaustive permutations for tied groups with at most eight examples. Resources: CPU; a real-data claim would need public predictions and implementation provenance. Failure modes: standard ranking theory already contains everything; negligible effect under realistic quantization. Abandon if no material ranking change is found in a preregistered audit. Retained as a fallback, not executed in this project.

## C — Correlation-sensitive finite candidate selection

Question: Can coverage-loss bounds reflect redundant score rankings instead of the raw number of candidate models? Why it matters: a dense hyperparameter grid may consist mostly of equivalent prediction sets. Closest work: Yang and Kuchibhotla; Liang, Zhu and Barber; Zeng et al. Proposed difference: finite-sample analysis using a metric on population ranks. Evidence: bound, redundant versus independent candidate stress tests, and comparison to valid post-selection methods. Pilot: correlated Gaussian-copula score arrays. Resources: modest CPU. Failure modes: standard covering-number arguments fully explain the result; estimating the relevant metric from the reused data invalidates a certificate. Abandon any claim of a usable data-driven certificate without a separate argument. A limited theoretical version is incorporated into A; no separate method-performance claim is made.

## D — Calibration variability in method comparisons

Question: How misleading are test-only error bars when two conformal methods share calibration data? Why it matters: an arbitrarily large test set cannot remove calibration variability. Closest work: Vovk (2012), *Conditional validity of inductive conformal predictors*, including its binomial/order-statistic analysis. Proposed difference: paired uncertainty decompositions for common calibration sets and a minimal evaluation protocol. Evidence: exact derivation and an audit of actual evaluation practice. Pilot: identical predictors with separate versus shared calibration splits. Resources: CPU. Failure modes: standard hierarchical variance calculations and existing conformal evaluation guidance suffice. Abandon as a standalone theory contribution unless a consequential empirical practice gap is established.

## E — Optimism from selecting random seeds

Question: How does selecting a seed before reporting benchmark averages interact with task-level uncertainty? Why it matters: small improvements can disappear after selection accounting. Closest work search target: Cawley and Talbot, *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation* (JMLR 2010). Proposed difference would have to be a specific auditable modern practice, not the known winner's curse. Evidence: a public benchmark selection log and a preregistered reanalysis. Pilot: order-statistic simulation with task/seed dependence. Resources: CPU, but meaningful public logs are not yet available. Failure modes: rediscovering established model-selection bias; unverifiable selection histories. Deprioritized; neither the paper nor its claims are cited as inspected evidence in our manuscript.

## Decision

Choose A because a concrete published proof step can be checked with a small decisive mathematical test. Retain B. Do not change to an empirical model-performance paper merely to obtain positive results. Continue A only after the pilot and closest-work audit support a precise, limited contribution.
