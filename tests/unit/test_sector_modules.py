import pytest
from backend.engine.classification.sector_classifier import SectorType
from backend.engine.sectors.registry import SectorRegistry
import backend.engine.sectors.sector_modules # loads all registrations

def test_all_21_sectors_registered():
    all_specs = SectorRegistry.list_all_sectors()
    assert len(all_specs) == 21, f"Expected 21 registered sectors, found {len(all_specs)}"
    
    # Verify each sector type has an entry
    registered_ids = {spec.sector_id for spec in all_specs}
    for st in SectorType:
        assert st in registered_ids, f"Sector {st} missing from registry"

def test_retail_jewellery_forecasting():
    forecaster = SectorRegistry.get(SectorType.RETAIL_JEWELLERY)
    res = forecaster.forecast(
        base_financials={"operating_revenue": 50000.0},
        custom_drivers={"revenue_growth": 0.15, "gross_margin": 0.25, "ebitda_margin": 0.11}
    )
    assert round(res["forecast_revenue"], 2) == 57500.0
    assert res["forecast_ebitda"] > 0
    assert res["primary_method"] == "FCFF_DCF"

def test_banking_ddm_forecasting():
    forecaster = SectorRegistry.get(SectorType.BANKING)
    res = forecaster.forecast(
        base_financials={"gross_advances": 2000000.0},
        custom_drivers={"loan_growth": 0.15, "net_interest_margin": 0.038, "credit_cost_bps": 40.0}
    )
    assert round(res["forecast_advances"], 2) == 2300000.0
    assert res["net_interest_income"] > 0
    assert res["primary_method"] == "DDM"

def test_insurance_embedded_value_forecasting():
    forecaster = SectorRegistry.get(SectorType.LIFE_INSURANCE)
    res = forecaster.forecast(
        base_financials={"annualized_premium_equivalent": 15000.0, "embedded_value": 50000.0},
        custom_drivers={"ape_growth": 0.20, "vnb_margin": 0.25}
    )
    assert round(res["forecast_ape"], 2) == 18000.0
    assert round(res["forecast_vnb"], 2) == 4500.0
    assert res["primary_method"] == "EMBEDDED_VALUE"

def test_reit_nav_forecasting():
    forecaster = SectorRegistry.get(SectorType.REIT)
    res = forecaster.forecast(
        base_financials={"net_operating_income": 1000.0, "net_debt_reit": 3000.0},
        custom_drivers={"rental_escalation": 0.06, "cap_rate": 0.08}
    )
    assert round(res["forecast_noi"], 2) == 1060.0
    assert round(res["gross_asset_value"], 2) == 13250.0
    assert round(res["net_asset_value"], 2) == 10250.0
    assert res["primary_method"] == "NAV"

def test_conglomerate_sotp_forecasting():
    forecaster = SectorRegistry.get(SectorType.CONGLOMERATE)
    res = forecaster.forecast(
        base_financials={"ebitda_o2c": 50000.0, "ebitda_retail": 20000.0, "ebitda_digital": 40000.0, "net_debt": 100000.0},
        custom_drivers={}
    )
    assert res["consolidated_ev"] > 1000000.0
    assert res["equity_value"] > 0
    assert res["primary_method"] == "SOTP"
