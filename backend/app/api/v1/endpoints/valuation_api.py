from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from backend.engine.classification.sector_classifier import SectorClassifier, SectorType, BENCHMARK_COMPANIES_REGISTRY
from backend.engine.sectors.registry import SectorRegistry
import backend.engine.sectors.sector_modules
from backend.engine.three_statement.three_statement_model import ThreeStatementEngine, ScenarioAssumptions
from backend.engine.valuation.valuation_suite import UniversalValuationSuite
from backend.engine.cost_of_capital.wacc_engine import CostOfCapitalEngine
from backend.engine.sensitivity.sensitivity_engine import SensitivityEngine

router = APIRouter()
classifier = SectorClassifier()

# Mock historical financial baselines for benchmark universe
BENCHMARK_BASELINES: Dict[str, Dict[str, float]] = {
    "TITAN": {
        "operating_revenue": 51080.0,
        "cost_of_goods_sold": 38310.0,
        "ebitda": 5400.0,
        "ebit": 4600.0,
        "net_income": 3496.0,
        "cash_and_equivalents": 5423.0,
        "trade_receivables": 1150.0,
        "inventory": 42743.0,
        "property_plant_equipment": 4500.0,
        "other_assets": 8805.0,
        "trade_payables": 18500.0,
        "financial_debt": 30621.0,
        "shareholders_equity": 13500.0,
        "share_capital": 88.78
    },
    "TCS": {
        "operating_revenue": 240893.0,
        "cost_of_goods_sold": 142000.0,
        "ebitda": 64000.0,
        "ebit": 59000.0,
        "net_income": 45900.0,
        "cash_and_equivalents": 12000.0,
        "trade_receivables": 42000.0,
        "inventory": 0.0,
        "property_plant_equipment": 15000.0,
        "trade_payables": 18000.0,
        "financial_debt": 0.0,
        "shareholders_equity": 98000.0,
        "share_capital": 361.8
    },
    "HDFCBANK": {
        "operating_revenue": 280000.0,
        "ebit": 95000.0,
        "net_income": 60800.0,
        "gross_advances": 2500000.0,
        "customer_deposits": 2350000.0,
        "shareholders_equity": 440000.0,
        "share_capital": 760.0
    },
    "RELIANCE": {
        "operating_revenue": 900000.0,
        "ebitda": 178000.0,
        "net_income": 79000.0,
        "ebitda_o2c": 62000.0,
        "ebitda_retail": 24000.0,
        "ebitda_digital": 53000.0,
        "financial_debt": 320000.0,
        "cash_and_equivalents": 205000.0,
        "net_debt": 115000.0,
        "shareholders_equity": 790000.0,
        "share_capital": 676.0
    }
}

class ValuationRequest(BaseModel):
    methodology: str = "FCFF_DCF" # FCFF_DCF, DDM, SOTP, NAV
    terminal_growth_rate: float = 0.055
    exit_multiple: float = 35.0
    risk_free_rate: float = 0.070
    equity_risk_premium: float = 0.070
    beta: float = 1.15
    cost_of_debt: float = 0.075

class ForecastRequest(BaseModel):
    revenue_growth_rate: float = 0.15
    gross_margin: float = 0.28
    ebitda_margin: float = 0.12
    capex_pct_revenue: float = 0.025
    effective_tax_rate: float = 0.2517
    dividend_payout_ratio: float = 0.25
    forecast_years: int = 5

@router.get("/sectors")
def list_supported_sectors():
    """Lists all 21 registered sector specifications."""
    return {"total_sectors": 21, "sectors": SectorRegistry.list_all_sectors()}

@router.get("/companies/search")
def search_companies(query: Optional[str] = Query(None)):
    """Search registered companies by ticker or name."""
    results = []
    q = (query or "").upper().strip()
    for ticker, info in BENCHMARK_COMPANIES_REGISTRY.items():
        if not q or q in ticker or q in info["common_name"].upper():
            results.append({
                "ticker": ticker,
                "common_name": info["common_name"],
                "legal_name": info["legal_name"],
                "sector": info["primary_sector"],
                "exchange": info["exchange"]
            })
    return {"results": results}

@router.get("/companies/{ticker}")
def get_company_profile(ticker: str):
    """Retrieves full company profile, sector, segments, and valid valuation models."""
    profile = classifier.classify_company(ticker)
    return profile

@router.get("/companies/{ticker}/financials")
def get_company_financials(ticker: str):
    """Retrieves normalized financial baseline statement metrics."""
    t_clean = ticker.upper()
    if t_clean not in BENCHMARK_BASELINES:
        # Default synthetic baseline
        baseline = BENCHMARK_BASELINES["TITAN"]
    else:
        baseline = BENCHMARK_BASELINES[t_clean]
    return {"ticker": t_clean, "financial_baseline": baseline}

@router.post("/companies/{ticker}/forecast")
def run_forecast(ticker: str, request: ForecastRequest):
    """Executes integrated 5-year three-statement financial projections."""
    t_clean = ticker.upper()
    baseline = BENCHMARK_BASELINES.get(t_clean, BENCHMARK_BASELINES["TITAN"])
    
    assumptions = ScenarioAssumptions(
        revenue_growth_rate=request.revenue_growth_rate,
        gross_margin=request.gross_margin,
        ebitda_margin=request.ebitda_margin,
        capex_pct_revenue=request.capex_pct_revenue,
        effective_tax_rate=request.effective_tax_rate,
        dividend_payout_ratio=request.dividend_payout_ratio
    )
    
    forecast_out = ThreeStatementEngine.project_three_statements(
        base_year_data=baseline,
        assumptions=assumptions,
        forecast_years=request.forecast_years
    )
    return forecast_out

@router.post("/companies/{ticker}/valuation")
def run_valuation(ticker: str, request: ValuationRequest):
    """Executes sector-appropriate valuation engine."""
    t_clean = ticker.upper()
    profile = classifier.classify_company(t_clean)
    baseline = BENCHMARK_BASELINES.get(t_clean, BENCHMARK_BASELINES["TITAN"])

    # Enforce sector appropriateness
    UniversalValuationSuite.enforce_sector_appropriateness(profile.primary_sector, request.methodology)

    # Cost of Capital
    wacc_data = CostOfCapitalEngine.calculate_cost_of_capital(
        sector=profile.primary_sector,
        risk_free_rate=request.risk_free_rate,
        equity_risk_premium=request.equity_risk_premium,
        beta=request.beta,
        pre_tax_cost_of_debt=request.cost_of_debt,
        equity_market_value=baseline.get("operating_revenue", 10000.0) * 5.0,
        total_debt_value=baseline.get("financial_debt", 1000.0)
    )

    if profile.primary_sector == SectorType.BANKING or request.methodology == "DDM":
        res = UniversalValuationSuite.execute_ddm(
            forecast_dividends=[19.5, 22.5, 26.0, 30.0, 35.0],
            terminal_growth_rate=request.terminal_growth_rate,
            cost_of_equity=wacc_data["cost_of_equity"],
            shares_outstanding=baseline.get("share_capital", 100.0)
        )
    elif profile.primary_sector == SectorType.CONGLOMERATE or request.methodology == "SOTP":
        res = UniversalValuationSuite.execute_sotp(
            segments=[
                {"segment_name": "O2C", "metric": baseline.get("ebitda_o2c", 60000.0), "multiple": 6.5},
                {"segment_name": "Retail", "metric": baseline.get("ebitda_retail", 24000.0), "multiple": 28.0},
                {"segment_name": "Digital", "metric": baseline.get("ebitda_digital", 52000.0), "multiple": 18.0}
            ],
            net_debt=baseline.get("net_debt", 100000.0),
            holding_company_discount=0.15,
            shares_outstanding=baseline.get("share_capital", 676.0)
        )
    else:
        # Default FCFF DCF
        proj = ThreeStatementEngine.project_three_statements(
            base_year_data=baseline,
            assumptions=ScenarioAssumptions(),
            forecast_years=5
        )
        ufcfs = [proj["statements"][p]["ufcf"] for p in proj["forecast_periods"]]
        final_ebitda = proj["statements"][proj["forecast_periods"][-1]]["ebitda"]

        res = UniversalValuationSuite.execute_fcff_dcf(
            forecast_ufcfs=ufcfs,
            terminal_growth_rate=request.terminal_growth_rate,
            wacc=wacc_data["wacc"],
            final_ebitda=final_ebitda,
            exit_multiple=request.exit_multiple,
            total_debt=baseline.get("financial_debt", 30621.0),
            cash_and_equivalents=baseline.get("cash_and_equivalents", 5423.0),
            shares_outstanding=baseline.get("share_capital", 88.78)
        )

    return {
        "ticker": t_clean,
        "company_name": profile.common_name,
        "sector": profile.primary_sector,
        "cost_of_capital": wacc_data,
        "valuation_result": res
    }

@router.post("/companies/{ticker}/sensitivity")
def run_sensitivity(ticker: str):
    """Computes dynamic 5x5 WACC vs. Exit Multiple sensitivity matrix."""
    t_clean = ticker.upper()
    baseline = BENCHMARK_BASELINES.get(t_clean, BENCHMARK_BASELINES["TITAN"])

    proj = ThreeStatementEngine.project_three_statements(
        base_year_data=baseline,
        assumptions=ScenarioAssumptions(),
        forecast_years=5
    )
    ufcfs = [proj["statements"][p]["ufcf"] for p in proj["forecast_periods"]]
    final_ebitda = proj["statements"][proj["forecast_periods"][-1]]["ebitda"]

    matrix_out = SensitivityEngine.generate_wacc_vs_multiple_matrix(
        forecast_ufcfs=ufcfs,
        final_ebitda=final_ebitda,
        total_debt=baseline.get("financial_debt", 30621.0),
        cash_and_equivalents=baseline.get("cash_and_equivalents", 5423.0),
        shares_outstanding=baseline.get("share_capital", 88.78)
    )
    return matrix_out
