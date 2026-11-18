import pytest
from backend.engine.valuation.valuation_suite import UniversalValuationSuite, ValuationMethodologyException
from backend.engine.classification.sector_classifier import SectorType

def test_fcff_dcf_dual_valuation():
    # Titan-like test parameters
    res = UniversalValuationSuite.execute_fcff_dcf(
        forecast_ufcfs=[3000.0, 3600.0, 4300.0, 5100.0, 6000.0],
        terminal_growth_rate=0.055,
        wacc=0.1443,
        final_ebitda=9000.0,
        exit_multiple=35.0,
        total_debt=30000.0,
        cash_and_equivalents=5000.0,
        shares_outstanding=88.78
    )

    assert "exit_multiple_method" in res
    assert "gordon_growth_method" in res
    assert res["exit_multiple_method"]["intrinsic_value_per_share"] > 0
    assert res["gordon_growth_method"]["intrinsic_value_per_share"] > 0
    # Exit multiple price is substantially higher due to multiple disparity
    assert res["exit_multiple_method"]["intrinsic_value_per_share"] > res["gordon_growth_method"]["intrinsic_value_per_share"]

def test_ddm_banking_valuation():
    # HDFC Bank-like dividend stream
    res = UniversalValuationSuite.execute_ddm(
        forecast_dividends=[19.5, 22.5, 26.0, 30.0, 34.5],
        terminal_growth_rate=0.06,
        cost_of_equity=0.13,
        shares_outstanding=760.0
    )
    assert res["equity_value"] > 0
    assert res["intrinsic_value_per_share"] > 0

def test_sector_appropriateness_enforcement():
    # Attempting to run FCFF on Banking must fail
    with pytest.raises(ValuationMethodologyException, match="Methodology Invalidation Gate"):
        UniversalValuationSuite.enforce_sector_appropriateness(SectorType.BANKING, "FCFF_DCF")

    # FCFF on Retail/Jewellery must succeed
    UniversalValuationSuite.enforce_sector_appropriateness(SectorType.RETAIL_JEWELLERY, "FCFF_DCF")

def test_sotp_conglomerate_valuation():
    segments = [
        {"segment_name": "O2C", "metric": 50000.0, "multiple": 6.5},
        {"segment_name": "Retail", "metric": 20000.0, "multiple": 25.0},
        {"segment_name": "Digital Services", "metric": 40000.0, "multiple": 18.0}
    ]
    res = UniversalValuationSuite.execute_sotp(
        segments=segments,
        net_debt=100000.0,
        holding_company_discount=0.15,
        shares_outstanding=670.0
    )
    assert res["gross_enterprise_value"] == 1545000.0
    assert res["discounted_enterprise_value"] == 1545000.0 * 0.85
    assert res["intrinsic_value_per_share"] > 0

def test_nav_reit_valuation():
    res = UniversalValuationSuite.execute_nav(
        revalued_assets=15000.0,
        total_liabilities=5000.0,
        shares_outstanding=35.0 # units
    )
    assert res["net_asset_value"] == 10000.0
    assert round(res["intrinsic_value_per_share"], 2) == 285.71
