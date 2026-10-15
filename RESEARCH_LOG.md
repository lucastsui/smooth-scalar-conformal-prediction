# Research log

## 2026-09-28 — Environment and scope

User requested a full autonomous research, manuscript, review and revision cycle. No research area, datasets, budget, or conference year was specified. Defaults: local CPU computation, public primary literature, synthetic data for a theoretical contribution, no paid services; target ICML 2027 subject to publication of its rules. No submissions, publications, purchases, or outreach authorized or attempted.

Environment: macOS arm64, Apple M4 Max, 16 CPU cores, 48 GB unified RAM; Python 3.12.12 in an isolated virtual environment. System LaTeX, BibTeX and Poppler are available. No inherited AGENTS.md was found at the workspace ancestors. Hardware identifiers and personal files are excluded from the research package.

The official ICML 2027 call could not be retrieved and no official 2027 call was found in the initial search. We provisionally use the official 2026 LaTeX template and eight-page main-body rule. The 2026 deadline has passed. Target-year compliance must be rechecked before any future submission.

Read official 2026 call, author and reviewer instructions. Criteria include soundness, presentation, significance and originality; reproducible evidence and an impact statement matter. This is a local draft, not a conference submission.

## Initial exploration

Searches covered conformal score selection, tuning bias, confidence quantization, risk–coverage metrics, finite-sample evaluation and parameter complexity. Search query history will be preserved in literature/search_history.json. Primary records identified Zeng et al. (ICML 2025), Yang and Kuchibhotla, Liang et al., and non-monotone conformal risk control as important nearby work.

Reading the **published PMLR PDF**, rather than only its abstract, revealed a concrete candidate: Zeng et al. Lemmas D.3/D.5 assert a VC dimension bound from bounded continuous parameterization; Proposition 4.6 uses those lemmas. Continuity by itself does not enforce that bound. This is an observed proof concern, not yet the final contribution. The authors' reported experiments are not invalidated by this observation. The classic distinction between parameter dimension and VC dimension is established knowledge, not our novelty claim.

Working hypothesis: a compact, smooth, uniformly Lipschitz scalar score family can exhibit severe same-sample conformal coverage loss if score anti-concentration is uncontrolled. A replacement result should reveal what quantitative structure is sufficient. Before investing in a manuscript, inspect nearby impossibility results and test a finite occupancy construction with an exactly calculable coverage law.

All further entries distinguish analytical derivations, exploratory runs, fixed-protocol checks, and unexecuted proposals.

## Pilot and continuation decision

Executed the fixed pilot (results/pilot.json). Mean adaptive conditional coverage 0.4859825, MC SE 0.0019953, exact target 0.4887125. Fixed-score mean 0.8966286 versus exact 0.9. All 20,000 direct test predictions matched the algebraic event; all eight three-label shattering patterns were recovered. The preregistered local go/no-go criterion passed. Continue with an exact theoretical claim, not an application-prevalence claim.

The closest-work audit found severe non-monotone CRC failures already in Angelopoulos et al. (2024), Proposition 2 in the proceedings (Proposition 1 in the updated arXiv version); Aldirawi et al. (2026 preprint) analyzes finite-grid behavior. Therefore broad failure under scalar adaptation is not treated as new. The precise distinction pursued here is smooth bounded score parameterization, continuous score distributions, an exact occupancy law, and a finite-sample versus fixed-family asymptotic distinction. Liang et al.'s current arXiv version is v4 (2026), with a revised title; Yang and Kuchibhotla's current title also differs from the early preprint.

## Verification before confirmatory execution

The first unit-test run had five passes and one implementation failure: scalar input to the convolution CDF returned a NumPy scalar that did not support indexed assignment. Fixed by retaining a zero-dimensional ndarray. This was found before confirmatory experiments; no outcomes or protocol settings were changed. Preserve the subsequent test output in logs/tests.txt. Confirmatory protocol and code were committed at af61a96 before any confirmatory data were generated; the implementation fix receives its own commit before execution.

## Confirmatory execution and manuscript

Ran the unchanged configuration at commit 02b4f3ef1a20e0f35e344a9b10eeef871bdbdb78. The original computation took 10.8828 seconds locally. Preserved 28 raw NPZ files: 21 occupancy settings (10,000 calibration samples each), six linear-family settings (1,000 each), and a separately seeded sampled-test audit. The run manifest records source, configuration and random-input hashes. No external dataset, paid compute or GPU was used.

At n=99, K=10,000, alpha=.1, adaptive coverage was 0.008863 versus exact 0.0088664818. Fixed and split controls were near their correct finite-sample targets; the split target is 0.9019608, not exactly 0.9. The independent sampled-test audit produced 0.008858, with calibration-level Monte Carlo interval [0.0086806, 0.0090354]. All occupancy/control rows passed the prespecified diagnostic tolerance.

The regular-family study found conservative certificates. Continuum bounds were sometimes stronger and sometimes weaker than finite-grid beta bounds; e.g. n=999, a=1 gives 0.85755 versus 0.86333. Their violation rates were only .001–.003 against a .05 tail level. This weakens any practical-tightness claim, which is not made. No held-out metric or configuration was altered after inspection. These are analytic verification experiments, not application benchmarks.

Derived the smooth interpolation, exact occupancy identity, fixed-class shattering, population-rank packing, beta-tail net certificate and anti-concentration transfer. The arguments state their assumptions and handle the k=n+1 infinite threshold separately. Finite tests supplement these proofs. Main limitations include combinatorial selection, exponential distinguishability, precision growth and unknown population quantities. These were placed in the abstract/main paper as well as the appendix.

Generated figures/tables from saved results and wrote the full manuscript in the official 2026 ICML template. Inspected all ten initial PDF pages, corrected a missing anonymous-template field, long URL overflow and equation overflow. References were checked against inspected primary documents. Explicit version clarification: the CRC non-monotone counterexample is Proposition 2, Section 2.3 in the 2024 proceedings, and Proposition 1, Section 2.4 in updated arXiv v4.

## Adversarial cycle 1

Froze v1 PDF/source with SHA-256 e8e9d171e386a08b1027bb598fae41c183976c4db9027e6fb85f0da90d264229. The v1 freeze omitted generated assets/style dependencies; reviewer C identified this real provenance gap. Preserve the historical snapshot unchanged and make the next snapshot complete.

Used the user's authorization for three separate AI review agents. A assessed novelty/significance, B proofs/implementation, C clarity/reproducibility. They received the frozen manuscript and evidence with no instruction to favor acceptance. These are separate AI passes, not external human validation. All complete reports, executed checks and scope exclusions are retained under reviews/.

A verified the published dimension-argument flaw but recommended weak rejection for a full ICML paper. The strongest new objection was that fixed-family consistency follows from Newey and McFadden (1994), Lemma 2.4, under weaker assumptions. Independently retrieved/read the lemma and its measurability qualification. Revised the abstract, contribution list, related work, corollary and conclusion; added a direct indicator-class reduction with the left-limit quantile sandwich to cover adaptive ties. Qualitative consistency is explicitly prior theory, not new. Remaining novelty/significance uncertainty is not resolved by this attribution fix.

B found no fatal proof error. It reproduced all 28 original raw files exactly and performed additional independent integrations, certificate inversions, direct scalar predictions and rank-transfer checks. It found two code edge cases outside the original grid: cancellation at tiny nonzero slopes and an unhandled infinite-threshold linear path. C also reproduced all 28 payloads exactly and identified missing reproduction instructions, incomplete snapshot dependencies, a plot based on expected rather than saved executed shattering values, and small clarity/layout issues. B/C's favorable recommendations were restricted to their review dimensions, not overall acceptance.

## Revision 1 and unchanged-protocol check

Replaced the cancellation-prone linear CDF with a piecewise uniform-convolution calculation. Handled k=n+1 consistently in continuum certificates, the linear runner and sampled-test audit. Added two substantive regression checks: tiny-slope limits/symmetry and end-to-end infinite-threshold execution. All eight tests pass. Reran the original confirmatory protocol and seeds into results/revision1_reproduction; all scientific outputs agree within 1e-12, with maximum raw difference 9.547918011776346e-15. Original results remain untouched, and original source bytes are preserved in provenance/reference_source/.

Added README install/run/compare/build instructions and safe output-path options. Figure 3 now reads saved pilot predictions and records input/generator hashes. Named the fixed control and analytic reference line explicitly, moved the obstructing legend, and unified linear-table units. No benchmark was added to manufacture significance; the original negative assessment remains visible. Issue-by-issue dispositions are in reviews/issue_resolution.md. The revised complete snapshot is the input to a second adversarial pass.


## Adversarial cycle 2 and final focused review

All three reviewers reassessed frozen v2. A marked the classical-attribution issue resolved but kept weak reject with moderate confidence because consequential originality remains unresolved. B confirmed the classical reduction and the numerical fixes; its technical recommendation remained 6/10, confidence 4/5. C installed all 31 locked distributions in a fresh isolated Python 3.12.12 environment on this host, ran all eight tests and reproduced all 28 payloads within 9.55e-15. It built a copied source snapshot with identical extracted text and all ten rendered pages, and regenerated all figures/tables from fresh results. Its favorable clarity/reproducibility recommendation remained unchanged. This is stronger local reproducibility evidence, not clean-machine or human validation.

B requested an explicit joint-measurability assumption. Added it in Setup and Appendix B; this makes the selected-score composition unambiguous. Also documented the stable equivalent CDF implementation and shortened the conclusion to remove a one-word orphan on page 7. No experiment, result, figure, table, configuration or reference changed. The exact final diff is saved in reviews/final_changes.md.

Froze the complete final manuscript with SHA-256 96b32fe1b039fbd590364027a2cf3858b71ce2f246c2afb444f7dde40a387b46. All three reviewers performed focused final checks. A found no attribution/novelty regression; B closed all B1–B4 concrete issues; C confirmed assets unchanged and the conclusion-layout fix. Their recommendations did not increase. A minor cross-column hyphenation remains a cosmetic limitation, not missing content.

Root rendered and visually inspected all ten final pages. Main body ends on page 6; impact/disclosure/references occupy page 7; appendices occupy pages 8–10. Programmatic checks verify all 84 occupancy summary rows, six linear rows, nine used references, generated severe-case macros, absence of unresolved references/template errors and the provisional file/page limits. The five official style files match the original archive byte-for-byte. The original two protocol commits are preserved in a verified Git bundle; experimental source bytes are separately archived.

The final package includes source, configurations, raw results, reproduction/build helpers, manifests, bibliography/closest-work audit, claim map, all reviews and issue dispositions. The release tool produces a per-file SHA-256 inventory and verifies every archived payload and ZIP CRC. Environments and third-party full documents are excluded. No paid resource, outreach, submission or publication occurred.

Final classification: complete executed research draft for external expert critique; not ICML-submission-ready. The unresolved issue is significance/originality of the strengthened correction and oracle specialization. No practical-method, optimality, first-result or acceptance claim is made. The fallback idea remains unexecuted rather than presented as completed research.
