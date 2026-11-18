import pytest
from backend.engine.formulas.core_formulas import FinancialFormulaEngine, FinancialFormulaException

def test_nopat_calculation():
    # EBIT = 1000, Tax = 25% -> NOPAT = 750
    nopat, audit = FinancialFormulaEngine.calculate_nopat(ebit=1000.0, effective_tax_rate=0.25)
    assert nopat == 750.0
    assert audit["tax_shield_factor"] == 0.75

    # Invalid tax rate trap
    with pytest.raises(FinancialFormulaException):
        FinancialFormulaEngine.calculate_nopat(ebit=1000.0, effective_tax_rate=1.2)

def test_fcff_calculation():
    # NOPAT = 750, D&A = 150, CapEx = 200, ΔNWC = 100 -> FCFF = 600
    fcff, audit = FinancialFormulaEngine.calculate_fcff(
        nopat=750.0,
        depreciation_amortisation=150.0,
        capital_expenditure=200.0,
        change_in_working_capital=100.0
    )
    assert fcff == 600.0
    assert audit["result_fcff"] == 600.0

def test_fcfe_calculation():
    # Net Income = 500, D&A = 150, CapEx = 200, ΔNWC = 100, Net Borrowing = 50 -> FCFE = 400
    fcfe, audit = FinancialFormulaEngine.calculate_fcfe(
        net_income=500.0,
        depreciation_amortisation=150.0,
        capital_expenditure=200.0,
        change_in_working_capital=100.0,
        net_borrowing=50.0
    )
    assert fcfe == 400.0

def test_capm_calculation():
    # Rf = 7.0%, Beta = 1.15, ERP = 7.0% -> Ke = 7.0 + 1.15*7.0 = 15.05%
    ke, audit = FinancialFormulaEngine.calculate_capm(
        risk_free_rate=0.07,
        beta=1.15,
        equity_risk_premium=0.07
    )
    assert round(ke, 4) == 0.1505

    # Negative Rf error
    with pytest.raises(FinancialFormulaException):
        FinancialFormulaEngine.calculate_capm(risk_free_rate=-0.02, beta=1.0, equity_risk_premium=0.07)

def test_wacc_calculation():
    # E = 800, D = 200, Ke = 15%, Kd = 8%, Tax = 25% -> E/V = 0.8, D/V = 0.2
    # Kd*(1-t) = 6.0% -> WACC = 0.8*15% + 0.2*6% = 12.0% + 1.2% = 13.2%
    wacc, audit = FinancialFormulaEngine.calculate_wacc(
        equity_value=800.0,
        debt_value=200.0,
        cost_of_equity=0.15,
        cost_of_debt=0.08,
        marginal_tax_rate=0.25
    )
    assert round(wacc, 4) == 0.1320

def test_gordon_growth_and_singularity_trap():
    # CF(n+1) = 100, WACC = 12%, g = 5% -> TV = 100 / (0.12 - 0.05) = 1428.57
    tv, audit = FinancialFormulaEngine.calculate_terminal_value_gordon(
        terminal_cash_flow=100.0,
        terminal_growth_rate=0.05,
        discount_rate=0.12
    )
    assert round(tv, 2) == 1428.57

    # Singularity trap: WACC <= g MUST raise FinancialFormulaException
    with pytest.raises(FinancialFormulaException, match="Singularity Trap"):
        FinancialFormulaEngine.calculate_terminal_value_gordon(
            terminal_cash_flow=100.0,
            terminal_growth_rate=0.12,
            discount_rate=0.10
        )

def test_equity_bridge_and_per_share():
    # EV = 10000, Debt = 2000, Cash = 500 -> Net Debt = 1500 -> Equity Value = 8500
    equity_val, audit = FinancialFormulaEngine.calculate_equity_bridge(
        enterprise_value=10000.0,
        total_debt=2000.0,
        cash_and_equivalents=500.0
    )
    assert equity_val == 8500.0

    # Shares = 100 -> Per Share = 85.0
    per_share, _ = FinancialFormulaEngine.calculate_per_share_value(
        equity_value=equity_val,
        fully_diluted_shares=100.0
    )
    assert per_share == 85.0

    # Zero shares trap
    with pytest.raises(FinancialFormulaException):
        FinancialFormulaEngine.calculate_per_share_value(equity_value=8500.0, fully_diluted_shares=0.0)
