# Final clarification and layout edits

After cycle 2, the only manuscript changes were explicit joint measurability in Setup/Appendix B, a shorter conclusion to remove a one-word orphan, and a sentence documenting the stable equivalent CDF implementation. No result, configuration, figure, table, citation or experimental source changed. Full diff follows.

```diff
--- frozen_v2/main.tex
+++ frozen_final/main.tex
@@ -76,7 +76,7 @@
 
 \section{Setup}
 
-Let $Z_i=(X_i,Y_i)$, $i=1,\ldots,n+1$, be i.i.d. from $P$. The score family $\{S_\lambda:\lambda\in\Lambda\}$ is fixed before observing $D=(Z_1,\ldots,Z_n)$; independently trained models may be conditioned on. Write
+Let $Z_i=(X_i,Y_i)$, $i=1,\ldots,n+1$, be i.i.d. from $P$. The score family $\{S_\lambda:\lambda\in\Lambda\}$ is fixed before observing $D=(Z_1,\ldots,Z_n)$; independently trained models may be conditioned on. Assume $(z,\lambda)\mapsto S_\lambda(z)$ is jointly measurable. Write
 \begin{equation}
  k=\lceil(n+1)(1-\alpha)\rceil,\qquad c_n=\frac{k}{n+1}.
 \end{equation}
@@ -276,7 +276,7 @@
 
 \section{Conclusion}
 
-Smooth scalar score tuning can cause arbitrarily severe finite-sample split-conformal coverage loss across a class of families, with an exact occupancy law in a simple construction. Classical uniform convergence nevertheless ensures consistency for each fixed compact bounded continuous family with atomless scores. Probability-scale covers make this distinction explicit and combine with classical beta tails to give a finite-sample certificate. Establishing tractable, data-driven estimates of the relevant complexity remains open.
+Our construction gives an exact occupancy law showing arbitrarily severe finite-sample coverage loss under smooth scalar tuning. This is compatible with classical consistency for each fixed compact, bounded, continuous family with atomless scores. Population-rank covers combine with beta tails to provide a finite-sample certificate. Estimating the relevant complexity from data remains open.
 
 \section*{Impact Statement}
 This work concerns the reliability of uncertainty guarantees. A potential benefit is preventing unjustified calibration-data reuse. A potential misuse is to interpret a deliberately adversarial construction as evidence that all low-dimensional calibration fails, or to treat an oracle certificate with estimated constants as automatically valid. We explicitly limit both interpretations. Experiments use synthetic data only. No personal data, human participants, or deployed decision system is involved.
@@ -321,7 +321,7 @@
 Thus for any $r>0$, a sufficiently small parameter radius gives a rank net with error at most $r$. Its cardinality is finite and does not depend on $n$. For every center, the beta mean is $c_n\to1-\alpha$ and its variance is $k(n+1-k)/[(n+1)^2(n+2)]\to0$. A union bound over this fixed finite set gives convergence of both its maximum and minimum order statistics. This justifies the bracket argument without requiring a rate for the concentration modulus. It also shows why allowing $K$ and therefore the score family to change with $n$ falls outside the corollary.
 
 \paragraph{Direct classical reduction under weaker conditions.}
-Let $\Lambda\subset\R^d$ be compact, the scores bounded in $[0,1]$ and measurable, and suppose that at every fixed $\lambda$, $S_\mu(Z)\to S_\lambda(Z)$ almost surely as $\mu\to\lambda$. Assume $F_\lambda$ is continuous for every $\lambda$. On the compact index set $\Lambda\times[-1,2]$, consider $a(z,(\lambda,t))=\ind\{S_\lambda(z)\le t\}$. At each fixed $(\lambda,t)$ it is almost surely continuous in its index: the only possible obstruction is $S_\lambda(Z)=t$, which has probability zero. Its envelope is one. Lemma 2.4 of \citet{newey1994} therefore implies
+Let $\Lambda\subset\R^d$ be compact, the scores bounded in $[0,1]$ and jointly measurable in $(z,\lambda)$, and suppose that at every fixed $\lambda$, $S_\mu(Z)\to S_\lambda(Z)$ almost surely as $\mu\to\lambda$. Assume $F_\lambda$ is continuous for every $\lambda$. On the compact index set $\Lambda\times[-1,2]$, consider $a(z,(\lambda,t))=\ind\{S_\lambda(z)\le t\}$. At each fixed $(\lambda,t)$ it is almost surely continuous in its index: the only possible obstruction is $S_\lambda(Z)=t$, which has probability zero. Its envelope is one. Lemma 2.4 of \citet{newey1994} therefore implies
 \begin{equation}
  \Delta_n:=\sup_{\lambda,t}|F_{n,\lambda}(t)-F_\lambda(t)|\longrightarrow0
 \end{equation}
@@ -343,7 +343,7 @@
 \begin{equation}
  F_\beta(q)=\frac{(q+b)_+^2-(q-b)_+^2-(q+b-1)_+^2+(q-b-1)_+^2}{4b}.
 \end{equation}
-For $b=0$, it is $[q]_0^1$. This formula follows by integrating $[q-\beta x]_0^1/2$ over $x\in[-1,1]$; independent numerical quadrature is a verification test. The conditional prediction set is $\{y\in[0,1]:y\le q-\beta x\}$, so the CDF is precisely its coverage.
+For $b=0$, it is $[q]_0^1$. This formula follows by integrating $[q-\beta x]_0^1/2$ over $x\in[-1,1]$; independent quadrature is a verification test. The revised code uses an equivalent piecewise convolution formula to avoid cancellation for tiny $b$. The prediction set is $\{y\in[0,1]:y\le q-\beta x\}$, so the CDF is precisely its coverage.
 
 For $G=257$ candidates the finite-grid beta lower bound is $B_{n,k}^{-1}(\delta/G)$. The DKW lower bound reported in the figure is
 \begin{equation}
```
