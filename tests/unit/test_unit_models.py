import pytest

def test_wacc_formula():
    rf = 0.07
    erp = 0.07
    beta = 1.15
    ke = rf + beta * erp
    assert round(ke, 4) == 0.1505
    
    kd = 0.075
    tax = 0.2517
    kd_after_tax = kd * (1 - tax)
    assert round(kd_after_tax, 5) == 0.05612
    
    e = 435909.8
    d = 30621.0
    tot = e + d
    we = e / tot
    wd = d / tot
    wacc = we * ke + wd * kd_after_tax
    assert round(wacc, 4) == 0.1443

def test_gordon_growth_formula():
    nopat_31 = 11074.675296
    g = 0.055
    roic = 0.20
    wacc = 0.14430548202283752
    rr = g / roic # 0.275
    terminal_fcf = nopat_31 * (1 + g) * (1 - rr)
    tv = terminal_fcf / (wacc - g)
    assert abs(tv - 94851.31) < 1.0

def test_exit_multiple_formula():
    ebitda_31 = 17089.5747
    multiple = 35.0
    tv = ebitda_31 * multiple
    assert round(tv, 0) == 598135.0

def test_equity_bridge():
    ev = 314414.08
    debt = 30621.0
    cash = 1917.0
    inv = 3506.0
    eq = ev - debt + cash + inv
    shares = 88.78
    price = eq / shares
    assert round(price, 2) == 3257.67

def test_dax_variance_logic():
    actual_rev = 6047961200.0
    budget_rev = 5931976900.0
    var = actual_rev - budget_rev
    pct = var / budget_rev
    assert round(var, 0) == 115984300.0
    assert round(pct * 100, 2) == 1.96
