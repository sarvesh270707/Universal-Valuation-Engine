import pytest
from backend.engine.cost_of_capital.wacc_engine import CostOfCapitalEngine
from backend.engine.classification.sector_classifier import SectorType

def test_industrial_wacc_and_hamada_equation():
    # Test Titan-like capital structure
    res = CostOfCapitalEngine.calculate_cost_of_capital(
        sector=SectorType.RETAIL_JEWELLERY,
        risk_free_rate=0.07,
        equity_risk_premium=0.07,
        beta=1.15,
        pre_tax_cost_of_debt=0.075,
        tax_rate=0.2517,
        equity_market_value=280000.0,
        total_debt_value=20000.0
    )

    assert res["is_financial_institution"] is False
    assert round(res["cost_of_equity"], 4) == 0.1505
    assert round(res["after_tax_cost_of_debt"], 4) == 0.0561
    assert res["wacc"] > 0.14 and res["wacc"] < 0.15
    assert res["unlevered_beta"] < res["levered_beta"] # Unlevered beta must be lower than levered beta

    # Relevering round-trip verification
    relevered = CostOfCapitalEngine.relever_beta(
        unlevered_beta=res["unlevered_beta"],
        debt_to_equity=res["debt_to_equity_ratio"],
        tax_rate=res["tax_rate"]
    )
    assert round(relevered, 2) == 1.15

def test_financial_institution_ke_substitution():
    # Banking (HDFC Bank): Must return Ke as applicable discount rate
    res = CostOfCapitalEngine.calculate_cost_of_capital(
        sector=SectorType.BANKING,
        risk_free_rate=0.07,
        equity_risk_premium=0.07,
        beta=1.10
    )
    assert res["is_financial_institution"] is True
    assert res["applicable_discount_rate_name"] == "Cost of Equity (Ke)"
    assert res["applicable_discount_rate"] == 0.07 + (1.10 * 0.07)
