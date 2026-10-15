# Confirmatory implementation-check protocol

Frozen after the pilot and before generating any confirmatory data. This is a locally time-stamped protocol, not an external preregistration. Config: configs/confirmatory.json; seeds differ from the pilot. These simulations check specific proved calculations; they are not a benchmark estimating prevalence in applications.

## Questions and outcomes

1. Does the exact occupancy law match independent calibration repetitions across small and large n/K? Main outcome: mean conditional coverage; uncertainty unit: independent calibration sample. Report Monte Carlo SE and pointwise 95% intervals. Use analytic test probabilities to remove avoidable finite-test noise. Preserve each repetition's outcomes.
2. Do fixed-score, strictly monotone transformation, and disjoint tuning/recalibration controls retain their known coverage? All-data fixed and monotone controls use n observations. The matched-budget split uses floor(n/2) for selecting A and the remainder for calibration. Report its actual order-statistic target; do not pretend all targets equal exactly 0.9. Cases where k>n use an infinite threshold and coverage one.
3. Does a fixed label universe recover as n grows, unlike a sequence where K grows with n? Include fixed K=16 and 128 alongside K=n,10n,100n. The constructed family changes when K changes. No fixed-family asymptotic impossibility is claimed.
4. Do oracle finite-family and continuum lower bounds hold in a regular family? Take U~Unif[0,1], V~Unif[-1,1], score U+beta V, beta in [-a,a], and select the smallest empirical conformal quantile among 257 fixed slopes. Evaluate exact conditional coverage with the convolution CDF. Compare uncorrected selection to fixed beta=0, the exact beta-tail union certificate, the DKW union certificate, and the Lipschitz/anti-concentration continuum certificate. These are guarantee comparisons, not new prediction algorithms. The selector sees calibration data only; known population CDFs are used for evaluation and oracle certificate constants, not selection.
5. Independently audit the severe n=99,K=10000 case with sampled test points. Compare test indicators to exact conditional coverage, preserving per-repetition counts.

No tuning on confirmatory outcomes. Record all settings, including failures and loose bounds. A discrepancy >5 SE + 0.001 between the occupancy simulation and theory triggers investigation, not a new metric. Since many checks are correlated and not adjusted hypothesis tests, do not interpret isolated 95% misses as scientific falsification. The theorem proofs remain the primary evidence.

## Implementation verification

Tests must cover all masks up to K=6, finite-score versus algebraic predictions, k=n+1, K=1, exact rational occupancy calculations for small n,K, convolution CDF versus independent numerical integration, scale invariance, and small-sample beta-tail identities. No practical claim will rely on an unimplemented huge scalar floating-point parameter: larger K experiments evaluate its mathematically equivalent knot representation, and that limitation must be prominent.

## Scope and costs

Synthetic i.i.d. data only; no datasets, training, hyperparameter fitting, GPU jobs, paid compute, or human subjects. Runtime includes experimental computation and is recorded separately from literature, rendering and writing time. No claim of computational efficiency or state-of-the-art predictive performance.
