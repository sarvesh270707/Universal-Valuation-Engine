import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="module")
def api_client():
    return TestClient(app)

def test_full_e2e_pipeline_titan(api_client):
    # 1. Search Company
    r_search = api_client.get("/api/v1/companies/search?query=TITAN")
    assert r_search.status_code == 200
    results = r_search.json()["results"]
    assert any(r["ticker"] == "TITAN" for r in results)

    # 2. Company Profile & Sector Classification
    r_prof = api_client.get("/api/v1/companies/TITAN")
    assert r_prof.status_code == 200
    prof = r_prof.json()
    assert prof["primary_sector"] == "RETAIL_JEWELLERY"
    assert "FCFF_DCF" in prof["applicable_valuation_models"]

    # 3. Normalized Statement Baseline
    r_fin = api_client.get("/api/v1/companies/TITAN/financials")
    assert r_fin.status_code == 200
    base = r_fin.json()["financial_baseline"]
    assert base["operating_revenue"] > 50000.0

    # 4. Integrated 5-Year Three-Statement Forecast
    r_fc = api_client.post("/api/v1/companies/TITAN/forecast", json={
        "revenue_growth_rate": 0.16,
        "gross_margin": 0.25,
        "ebitda_margin": 0.11,
        "forecast_years": 5
    })
    assert r_fc.status_code == 200
    fc = r_fc.json()
    assert len(fc["forecast_periods"]) == 5
    assert fc["max_balance_sheet_discrepancy"] < 1e-4

    # 5. Dual Valuation (Exit Multiple & Gordon Growth)
    r_val = api_client.post("/api/v1/companies/TITAN/valuation", json={
        "methodology": "FCFF_DCF",
        "terminal_growth_rate": 0.055,
        "exit_multiple": 35.0,
        "risk_free_rate": 0.07,
        "equity_risk_premium": 0.07,
        "beta": 1.15
    })
    assert r_val.status_code == 200
    val_out = r_val.json()
    assert val_out["cost_of_capital"]["wacc"] > 0.14
    vr = val_out["valuation_result"]
    assert vr["exit_multiple_method"]["intrinsic_value_per_share"] > 0
    assert vr["gordon_growth_method"]["intrinsic_value_per_share"] > 0

    # 6. Dynamic 5x5 Sensitivity Matrix
    r_sens = api_client.post("/api/v1/companies/TITAN/sensitivity")
    assert r_sens.status_code == 200
    sens = r_sens.json()
    assert sens["is_strictly_monotonic"] is True
    assert len(sens["matrix"]) == 5
    assert len(sens["matrix"][0]) == 5

def test_full_e2e_pipeline_hdfc_bank(api_client):
    # DDM Valuation for Bank
    r_val = api_client.post("/api/v1/companies/HDFCBANK/valuation", json={
        "methodology": "DDM",
        "terminal_growth_rate": 0.06,
        "risk_free_rate": 0.07,
        "equity_risk_premium": 0.07,
        "beta": 1.10
    })
    assert r_val.status_code == 200
    val_out = r_val.json()
    assert val_out["sector"] == "BANKING"
    assert val_out["cost_of_capital"]["is_financial_institution"] is True
    assert val_out["valuation_result"]["methodology"] == "DDM"
    assert val_out["valuation_result"]["intrinsic_value_per_share"] > 0
