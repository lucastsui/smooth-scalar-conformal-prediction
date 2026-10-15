"""Exact score construction and distribution calculations; no learned models."""
import math
import numpy as np
from scipy.special import expit
from scipy.stats import beta

def conformal_k(n, alpha):
    # Decimal string conversion prevents binary-roundoff at integral ranks.
    from decimal import Decimal, ROUND_CEILING
    return int(((Decimal(n)+1)*(1-Decimal(str(alpha)))).to_integral_value(rounding=ROUND_CEILING))

def quantile(scores, alpha):
    k = conformal_k(len(scores), alpha)
    return np.inf if k > len(scores) else np.partition(scores, k-1)[k-1]

def smooth_step(t):
    t = np.asarray(t, dtype=float)
    out = np.zeros_like(t)
    out[t >= 1] = 1
    mid = (t > 0) & (t < 1)
    out[mid] = expit(1/(1-t[mid])-1/t[mid])
    return out

def scalar_score(lam, u, y, K):
    """C-infinity family on [0,1], constant outside; intended for small K.

    Mask j represents A by its set bits. The positive scale is 1/(8*(2**K-1)).
    Large K experiments use exact algebra at the knots, NOT floating lambda.
    """
    if K > 20:
        raise ValueError('Direct floating scalar evaluation restricted to K<=20')
    M = 2**K
    pos = np.clip(float(lam), 0, 1)*(M-1)
    j = min(int(np.floor(pos)), M-2)
    t = pos-j
    y = np.asarray(y, dtype=np.int64)
    left = 1-((j >> y) & 1)
    right = 1-(((j+1) >> y) & 1)
    f = left+(right-left)*smooth_step(t)
    return (f+np.asarray(u)/4)/(8*(M-1))

def occupancy_theory(n, K, alpha):
    k = conformal_k(n, alpha)
    if k > n:
        return 1.
    return k/(n+1)*(-np.expm1(n*np.log1p(-1/K))) if K > 1 else k/(n+1)

def mixture_uniform_cdf(q, proportion):
    """CDF of 1{Y not in A}+U/4, with P(Y in A)=proportion."""
    return proportion*np.clip(4*q, 0, 1)+(1-proportion)*np.clip(4*(q-1), 0, 1)

def linear_cdf(q, slope):
    """Exact CDF of U+slope*V, U~Unif[0,1], V~Unif[-1,1]."""
    q, b = np.broadcast_arrays(np.asarray(q, float), np.abs(np.asarray(slope, float)))
    out = np.array(np.clip(q, 0, 1), copy=True)
    nz = b > 0
    x, a = q[nz], b[nz]
    # Convolution of uniforms of widths 1 and 2*a. Evaluate each piece
    # without subtracting nearly equal squares when a is close to zero.
    z=x+a;small=np.minimum(1.,2*a);large=np.maximum(1.,2*a)
    val=np.zeros_like(z)
    rising=(z>0)&(z<small)
    middle=(z>=small)&(z<=large)
    falling=(z>large)&(z<small+large)
    val[rising]=.5*(z[rising]/small[rising])*(z[rising]/large[rising])
    val[middle]=(z[middle]-small[middle]/2)/large[middle]
    tail=small[falling]+large[falling]-z[falling]
    val[falling]=1-.5*(tail/small[falling])*(tail/large[falling])
    val[z>=small+large]=1
    out[nz] = np.clip(val, 0, 1)
    return out

def finite_beta_lower(n, alpha, M, delta=.05):
    k=conformal_k(n,alpha)
    return 1. if k>n else float(beta.ppf(delta/M,k,n+1-k))

def continuum_lower(n, alpha, a, delta=.05):
    """Oracle continuum certificate for slopes in [-a,a], L=B=1.

    Grid mesh <=2*epsilon supplies a sup-norm epsilon cover. For a deterministic
    choice of epsilon, rank distance <=2*epsilon. Optimizing analytic constants
    before observing calibration data requires no multiplicity adjustment.
    """
    k=conformal_k(n,alpha)
    if k>n:
        return dict(lower=1.,epsilon=0.,net_size=1)
    eps = np.geomspace(1e-5, .25, 2000)
    numbers = np.ceil(a/eps).astype(int)+1
    lows = beta.ppf(delta/numbers,k,n+1-k)-2*eps
    i=int(np.argmax(lows))
    return dict(lower=max(0.,float(lows[i])),epsilon=float(eps[i]),net_size=int(numbers[i]))
