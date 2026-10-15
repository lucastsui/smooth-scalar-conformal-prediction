**Reviewer A additional source and search notes, September 28, 2026**

These are notes for the separate AI novelty/significance review. They are not edits to the manuscript or its existing evidence.

**Newey and McFadden (1994).** Full primary chapter downloaded from the University of Wisconsin-hosted copy; source URL, time, and SHA-256 are in additional_source_manifest.json. Read Section 2.3, Lemma 2.4, printed p. 2129, including footnote 17. The lemma assumes i.i.d. data, a compact parameter space, continuity at each parameter with probability one, and an integrable envelope. It yields uniform convergence in outer probability; a common samplewise continuity set is not required. This distinction matters for sublevel indicators.

Independent application to the manuscript: index the bounded indicator by \((\lambda,t)\). At a fixed pair, failure of indicator continuity can occur only if \(S_\lambda(Z)=t\), a null event under atomlessness. With \(S_\lambda(z)\) continuous in \(\lambda\), compactness and the unit envelope give uniform empirical-CDF convergence. At the selected order statistic, use both \(\widehat F(q)\ge k/n\) and \(\widehat F(q-)\le(k-1)/n\); population continuity identifies \(F(q-)=F(q)\). This handles sample ties created by adaptive parameter selection and proves Corollary 4 under weaker assumptions. This is a reviewer derivation from a standard theorem, not an assertion that an identical conformal corollary appears in that source.

**Kiyani, Pappas and Hassani (ICML 2024), Conformal Prediction with Learned Features.** Downloaded the published primary PDF and inspected Section 3.2, Definition 3.9 and Theorem 3.11, plus the surrounding conditional-CDF assumptions. It uses covering numbers for calibration-data learning but optimizes partitions/thresholds and conditional coverage. It does not appear to contain the manuscript's specific scalar occupancy counterexample. This is additional nearby work, not a decisive missing-citation objection; the manuscript already cites the authors' separate NeurIPS covering/CDF-regularity work.

**Shi et al. (September 2026), Occupancy-based Quantile Risk Control, arXiv:2609.03104v1.** Inspected the primary arXiv HTML setup and Section 3:
https://arxiv.org/html/2609.03104v1

Its occupancy is that of test losses in calibration order-statistic bins. Assumption 2.2 requires losses to be non-increasing and left-continuous in the tuning parameter. It therefore does not subsume the manuscript's non-monotone subset-selection counterexample. I did not verify its proofs or experiments. An attempted PDF download returned IncompleteRead; no successful PDF archive is claimed.

**Version checks.** The arXiv page for Zeng (2502.03023) lists v2, July 10, 2025, as its latest version at the review date; Aldirawi (2604.01502) lists v2, April 17, 2026; Angelopoulos (2602.20151) lists v1, February 23, 2026. The review's criticism of Zeng is anchored in the published PMLR PDF already archived by the project, not inferred from a search snippet.

**Additional search queries.** These were run through the web search tool; snippets were used for discovery rather than as evidence for theorem claims:

- "Limits of Smooth Scalar Tuning" conformal
- "Parametric Scaling Law" "tuning bias" counterexample
- conformal score selection smooth scalar Lipschitz covering probability integral transform
- conformal prediction adaptive calibration rank covering numbers anti concentration
- "conformal" "smooth" "tuning bias"
- "conformal" "occupancy" calibration selection
- "conformal prediction" "covering numbers" "score" selection
- "VC dimension" "one parameter" smooth function
- "Parametric Scaling Law of Tuning Bias" correction erratum
- "conformal" "score selection" "complexity" "covering"
- "conformal" "uniform" "Glivenko" "selection"
- "smooth" "one parameter" "VC" dimension Lipschitz
- "Conformal Prediction with Learned Features" Kiyani arxiv
- "conformal" "score" "rank" "entropy" selection
- "conformal" "tuning bias" "counterexample"
- "uniform convergence" "compact" "continuous" "Newey" McFadden Lemma 2.4
- Newey McFadden Large sample estimation hypothesis testing pdf berkeley
- "conformal" "smoothness" "calibration" "covering"
- "conformal" "non-monotone" "smooth" counterexample scalar

The searches did not locate an exact prior copy of the smooth atomless occupancy construction or an accessible published correction to Zeng. This is a limited search result, not evidence of priority or the nonexistence of a correction. Generic one-parameter infinite-VC examples appeared widely; secondary summaries were not used to establish a new technical claim.
