# Contribution statement

**Central claim.** A compact, smooth, bounded, 1-Lipschitz scalar family of atomless conformal scores can suffer arbitrarily severe finite-sample coverage loss after calibration-data reuse; parameter count and raw smoothness alone do not justify that reuse.

**Why it matters.** This separates a mathematically defensible reason for reusing calibration data from an insufficient one, and pinpoints a gap in a published dimension-based argument.

**Difference from prior work.** Parameter dimension versus statistical complexity, adaptive overfitting, non-monotone conformal failures, beta order-statistic bounds, and covering-number arguments are established ideas. The specific contribution is an exact smooth split-conformal occupancy construction; its rank-cover separation; and an explicit link to classical fixed-family consistency. The consistency result follows from Newey and McFadden (1994), Lemma 2.4, under even weaker continuity conditions and is not a novelty claim. The novelty and significance of that package remain subject to expert judgment.

**Strongest evidence.** Constructive proofs, exact conditional and marginal coverage formulas, exhaustive small-case checks, and a frozen-protocol simulation suite. At n=99,K=10000,alpha=.1, 10,000 independent calibration samples give mean conditional coverage about .008863, compared with the exact .00886648. An independent million-test-point audit agrees. These numbers characterize the constructed example only.

**Principal limitation.** The scalar encodes one of 2^K subsets and requires increasing precision. Large-K experiments evaluate equivalent mask events, not an ordinary floating-point optimization of the smooth parameter. The positive certificate requires population CDF/regularity information; it is a theoretical result, not a ready-to-use calibration algorithm. There are no real-data or modern-network performance claims.
