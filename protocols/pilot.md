# Pilot protocol — fixed before execution

Central claim: compact smooth scalar score parameterization, even with a uniform Lipschitz bound, does not by itself ensure small same-sample split-conformal coverage loss.

Let Y be uniform on K labels and U uniform on [0,1], independently. Enumerate all label subsets A at scalar knots. At a knot, use the normalized score 1{Y not in A}+U/4. Choose A to contain precisely the labels observed in the calibration sample; use the ordinary k=ceil((n+1)(1-alpha)) order statistic. A common positive scaling embeds these scores in a smooth bounded 1-Lipschitz scalar family. Proposed exact conditional coverage is |A| U_(k)/K and marginal coverage is k/(n+1) * (1-(1-1/K)^n), for k<=n. For k=n+1, the threshold is infinity and coverage is one.

Smallest decisive checks:
1. Exhaustively exhibit all 8 binary labelings for K=3 using the explicit smooth scalar score and a common threshold.
2. Compare direct score predictions to the algebraic event Y in A and U<=U_(k), at K=12,n=9,alpha=.1.
3. Use 2,000 independent calibration repetitions, seed 20260928. Estimate conditional coverage and verify agreement with the exact formula within 5 Monte Carlo standard errors plus .001; fixed-score coverage should agree with k/(n+1). Adaptive coverage below .65 is a useful signal at this setting.

Falsification: any mismatch in the algebraic event or exact calculation; inability to satisfy smoothness and atomless-score assumptions; a relevant prior result that subsumes the proposed strengthened statement. Competing explanations to exclude: ties, an incorrect order statistic, an off-by-one label mask, finite-precision collapse, and data leakage into the supposedly fixed baseline.

The pilot is exploratory. The untouched confirmatory seeds and broader settings will be committed only after the pilot decision. A numerical check cannot establish the theorem; it only checks the construction and implementation.
