import pytest
from backend.engine.historical.financial_analyser import HistoricalFinancialAnalyser

def test_cagr_calculation():
    # 100 to 200 in 3 years -> 2^(1/3) - 1 = 25.99%
    cagr = HistoricalFinancialAnalyser.calculate_cagr(100.0, 200.0, 3)
    assert round(cagr, 4) == 0.2599

    # Zero or negative handling
    assert HistoricalFinancialAnalyser.calculate_cagr(-50.0, 100.0, 3) is None
    assert HistoricalFinancialAnalyser.calculate_cagr(100.0, 100.0, 0) is None

def test_historical_series_analysis():
    statements = {
        "FY24": {
            "operating_revenue": 10000.0,
            "cost_of_goods_sold": 7000.0,
            "ebitda": 1500.0,
            "ebit": 1200.0,
            "net_income": 800.0,
            "finance_cost": 100.0,
            "total_assets": 12000.0,
            "shareholders_equity": 5000.0,
            "financial_debt": 2000.0,
            "cash_and_equivalents": 500.0,
            "trade_receivables": 1000.0,
            "inventory": 2500.0,
            "trade_payables": 1500.0,
            "total_current_assets": 4500.0,
            "total_current_liabilities": 2500.0
        },
        "FY25": {
            "operating_revenue": 12000.0,
            "cost_of_goods_sold": 8400.0,
            "ebitda": 1800.0,
            "ebit": 1500.0,
            "net_income": 1050.0,
            "finance_cost": 120.0,
            "total_assets": 14000.0,
            "shareholders_equity": 6000.0,
            "financial_debt": 2200.0,
            "cash_and_equivalents": 600.0,
            "trade_receivables": 1200.0,
            "inventory": 3000.0,
            "trade_payables": 1800.0,
            "total_current_assets": 5500.0,
            "total_current_liabilities": 3000.0
        }
    }

    res = HistoricalFinancialAnalyser.analyse_historical_series(statements, ["FY24", "FY25"])
    m_fy25 = res["period_metrics"]["FY25"]

    # YoY growth = (12000 - 10000)/10000 = 20.0%
    assert round(m_fy25["yoy_revenue_growth"], 4) == 0.2000
    # EBITDA margin = 1800 / 12000 = 15.0%
    assert round(m_fy25["ebitda_margin"], 4) == 0.1500
    # ROE = 1050 / 6000 = 17.5%
    assert round(m_fy25["roe"], 4) == 0.1750
    # Current ratio = 5500 / 3000 = 1.83
    assert round(m_fy25["current_ratio"], 2) == 1.83
    # Interest coverage = 1500 / 120 = 12.5x
    assert round(m_fy25["interest_coverage"], 1) == 12.5
