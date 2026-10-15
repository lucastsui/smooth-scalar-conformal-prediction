import itertools
from fractions import Fraction
import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import beta, binom
from core import conformal_k, quantile, scalar_score, occupancy_theory, linear_cdf, finite_beta_lower

def test_quantile_boundaries():
    assert conformal_k(9,.1)==9
    assert conformal_k(19,.1)==18
    assert conformal_k(99,.1)==90
    assert np.isinf(quantile(np.arange(3.),.1))
    assert quantile(np.arange(9.),.1)==8

def test_all_masks():
    for K in range(1,7):
        M=2**K
        for mask in range(M):
            scores=scalar_score(mask/(M-1),np.full(K,.5),np.arange(K),K)
            pred=scores<=.5/(8*(M-1))
            assert np.array_equal(pred,[(mask>>j)&1 for j in range(K)])

def test_exact_occupancy_enumeration():
    for K in range(1,5):
        for n in range(1,5):
            esize=sum(Fraction(len(set(y)),K) for y in itertools.product(range(K),repeat=n))/K**n
            assert esize==1-Fraction(K-1,K)**n
            alpha=.5
            k=conformal_k(n,alpha)
            target=float(esize*Fraction(k,n+1))
            assert occupancy_theory(n,K,alpha)==pytest.approx(target)

def test_scalar_prediction_equivalence_and_scaling():
    rng=np.random.default_rng(404)
    for K in [3,6,12]:
        for _ in range(30):
            y=rng.integers(K,size=19);u=rng.random(19)
            A=np.unique(y);mask=sum(1<<int(j) for j in A)
            s=scalar_score(mask/(2**K-1),u,y,K)
            yt=rng.integers(K,size=101);ut=rng.random(101)
            st=scalar_score(mask/(2**K-1),ut,yt,K)
            q=quantile(s,.1)
            expected=np.isin(yt,A)&(ut<=quantile(u,.1))
            assert np.array_equal(st<=q,expected)
            for scale in [1e-12,1.,1e12]:
                assert np.array_equal(st*scale<=quantile(s*scale,.1),expected)

def test_cdf_by_quadrature():
    for slope in [-2,-.25,0,.25,2]:
        for q in np.linspace(-3,4,31):
            value,_=quad(lambda v:np.clip(q-slope*v,0,1)/2,-1,1,epsabs=1e-10,points=[-1,0,1],limit=200)
            assert float(linear_cdf(q,slope))==pytest.approx(value,abs=2e-8)

def test_beta_binomial_identity():
    for n in [9,19,99]:
        k=conformal_k(n,.1)
        for u in [.1,.5,.9,.99]:
            assert beta.cdf(u,k,n+1-k)==pytest.approx(binom.sf(k-1,n,u))
        for M in [1,8,257]:
            low=finite_beta_lower(n,.1,M)
            assert M*beta.cdf(low,k,n+1-k)==pytest.approx(.05)
