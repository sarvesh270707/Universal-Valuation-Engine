import pytest
from backend.engine.three_statement.three_statement_model import ThreeStatementEngine, ScenarioAssumptions

def test_three_statement_integration_and_natural_balance():
    # Base Year Balanced Balance Sheet
    # Assets: Cash(500) + Rec(1000) + Inv(2500) + PPE(3000) = 7000
    # Liab & Eq: Payables(1500) + Debt(1500) + Equity(4000) = 7000 (Exact Balance)
    base_year = {
        "operating_revenue": 10000.0,
        "cash_and_equivalents": 500.0,
        "trade_receivables": 1000.0,
        "inventory": 2500.0,
        "property_plant_equipment": 3000.0,
        "trade_payables": 1500.0,
        "financial_debt": 1500.0,
        "shareholders_equity": 4000.0,
        "share_capital": 100.0
    }

    assumptions = ScenarioAssumptions(
        revenue_growth_rate=0.15,
        gross_margin=0.30,
        ebitda_margin=0.14,
        capex_pct_revenue=0.03,
        depreciation_rate_ppe=0.10,
        effective_tax_rate=0.25,
        dividend_payout_ratio=0.20,
        cost_of_debt=0.08
    )

    result = ThreeStatementEngine.project_three_statements(base_year, assumptions, forecast_years=5)
    statements = result["statements"]

    assert len(result["forecast_periods"]) == 5
    # Balance sheet discrepancy must be strictly 0.00 (within float precision 1e-4)
    assert result["max_balance_sheet_discrepancy"] < 1e-4

    for p in result["forecast_periods"]:
        stmt = statements[p]
        # 1. Total Assets == Total Liabilities & Equity
        assert abs(stmt["total_assets"] - stmt["total_liabilities_and_equity"]) < 1e-4
        # 2. Positive Operating Revenue & EBITDA
        assert stmt["operating_revenue"] > 10000.0
        assert stmt["ebitda"] > 0
        assert stmt["nopat"] > 0
        assert stmt["ufcf"] is not None
