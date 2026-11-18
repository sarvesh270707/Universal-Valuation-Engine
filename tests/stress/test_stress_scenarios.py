import pytest
import numpy as np

def test_wacc_stress_121_combinations():
    wacc_range = np.linspace(0.11, 0.18, 11)
    multiple_range = np.linspace(20, 50, 11)
    
    ebitda_31 = 17089.5747
    pv_ufcf = 9561.8330
    debt = 30621.0
    cash = 1917.0
    inv = 3506.0
    shares = 88.78
    
    prices = []
    for w in wacc_range:
        df5 = 1.0 / ((1.0 + w) ** 5)
        for m in multiple_range:
            ev = pv_ufcf + (ebitda_31 * m) * df5
            eq = ev - debt + cash + inv
            p = eq / shares
            assert p > 0, f"Negative equity value observed at WACC={w}, Mult={m}"
            prices.append((w, m, p))
            
    assert len(prices) == 121
    
    # Test monotonicity for fixed multiple 35x
    fixed_35 = [p[2] for p in prices if p[1] == 35.0]
    for i in range(len(fixed_35) - 1):
        assert fixed_35[i] > fixed_35[i+1], "Higher WACC failed to reduce valuation monotonically"
