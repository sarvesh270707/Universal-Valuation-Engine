import pytest
from backend.engine.sensitivity.sensitivity_engine import SensitivityEngine

def test_scenario_generation():
    base_data = {
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

    scenarios = SensitivityEngine.generate_scenarios(base_data)
    assert "BEAR" in scenarios
    assert "BASE" in scenarios
    assert "BULL" in scenarios

    # Bull case revenue and EBITDA must exceed Base, which exceeds Bear
    assert scenarios["BULL"]["final_year_revenue"] > scenarios["BASE"]["final_year_revenue"]
    assert scenarios["BASE"]["final_year_revenue"] > scenarios["BEAR"]["final_year_revenue"]
    assert scenarios["BULL"]["final_year_ebitda"] > scenarios["BASE"]["final_year_ebitda"]

def test_sensitivity_matrix_monotonicity():
    res = SensitivityEngine.generate_wacc_vs_multiple_matrix(
        forecast_ufcfs=[2500.0, 3000.0, 3600.0, 4200.0, 5000.0],
        final_ebitda=8000.0,
        total_debt=20000.0,
        cash_and_equivalents=4000.0,
        shares_outstanding=88.78,
        wacc_range=[0.12, 0.14, 0.16],
        multiple_range=[25.0, 35.0, 45.0]
    )

    assert res["is_strictly_monotonic"] is True
    matrix = res["matrix"]
    # Check 3x3 dimensions
    assert len(matrix) == 3
    assert len(matrix[0]) == 3

    # Lowest WACC + Highest Multiple = Highest Valuation (top-right)
    # Highest WACC + Lowest Multiple = Lowest Valuation (bottom-left)
    assert matrix[0][2] > matrix[2][0]
