"""
Universal Financial Valuation & DCF Engine - Historical Financial Analysis Module
Calculates historical financial growth, profitability margins, return on capital,
liquidity, leverage, and working capital cycles across 5 to 10 historical years.
"""

from typing import Dict, Any, List, Optional
import math
import pandas as pd

class HistoricalFinancialAnalyser:
    """
    Computes comprehensive institutional ratio analytics from normalized statement series.
    """

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, n_years: int) -> Optional[float]:
        """Calculates Compound Annual Growth Rate (CAGR) with defensive domain traps."""
        if start_value <= 0.0 or end_value <= 0.0 or n_years <= 0:
            return None
        return math.pow(end_value / start_value, 1.0 / n_years) - 1.0

    @classmethod
    def analyse_historical_series(
        cls,
        financial_statements: Dict[str, Dict[str, float]], # {period: {concept: value}}
        periods_chronological: List[str]
    ) -> Dict[str, Any]:
        """
        Executes ratio analysis across chronological operating periods (e.g. FY17-FY26).
        """
        period_metrics = {}
        prev_period_data = None

        for p in periods_chronological:
            curr = financial_statements.get(p, {})
            rev = curr.get("operating_revenue", 0.0)
            cogs = curr.get("cost_of_goods_sold", 0.0)
            ebitda = curr.get("ebitda", 0.0)
            ebit = curr.get("ebit", 0.0)
            pat = curr.get("net_income", 0.0)
            int_exp = curr.get("finance_cost", 0.0)

            # Balance sheet
            assets = curr.get("total_assets", 0.0)
            equity = curr.get("shareholders_equity", 0.0)
            debt = curr.get("financial_debt", curr.get("short_term_borrowings", 0.0) + curr.get("long_term_borrowings", 0.0))
            cash = curr.get("cash_and_equivalents", 0.0)
            rec = curr.get("trade_receivables", 0.0)
            inv = curr.get("inventory", 0.0)
            pay = curr.get("trade_payables", 0.0)
            ca = curr.get("total_current_assets", 0.0)
            cl = curr.get("total_current_liabilities", 0.0)

            # Margins
            gross_margin = ((rev - cogs) / rev) if rev > 0 else 0.0
            ebitda_margin = (ebitda / rev) if rev > 0 else 0.0
            ebit_margin = (ebit / rev) if rev > 0 else 0.0
            net_margin = (pat / rev) if rev > 0 else 0.0

            # Returns
            roe = (pat / equity) if equity > 0 else 0.0
            roa = (pat / assets) if assets > 0 else 0.0
            
            # Invested Capital = Total Debt + Equity - Cash
            invested_capital = max(0.0, debt + equity - cash)
            nopat = ebit * (1.0 - 0.2517)
            roic = (nopat / invested_capital) if invested_capital > 0 else 0.0

            # Liquidity & Leverage
            current_ratio = (ca / cl) if cl > 0 else None
            debt_to_equity = (debt / equity) if equity > 0 else None
            debt_to_ebitda = (debt / ebitda) if ebitda > 0 else None
            interest_coverage = (ebit / int_exp) if int_exp > 0 else None

            # Working Capital Cycles (in days)
            dso = (rec / rev * 365.0) if rev > 0 else 0.0
            dio = (inv / cogs * 365.0) if cogs > 0 else 0.0
            dpo = (pay / cogs * 365.0) if cogs > 0 else 0.0
            ccc = dso + dio - dpo

            # YoY Growth
            yoy_growth = None
            if prev_period_data and prev_period_data.get("operating_revenue", 0.0) > 0:
                yoy_growth = (rev - prev_period_data["operating_revenue"]) / prev_period_data["operating_revenue"]

            period_metrics[p] = {
                "revenue": rev,
                "ebitda": ebitda,
                "net_income": pat,
                "yoy_revenue_growth": yoy_growth,
                "gross_margin": gross_margin,
                "ebitda_margin": ebitda_margin,
                "ebit_margin": ebit_margin,
                "net_margin": net_margin,
                "roe": roe,
                "roa": roa,
                "roic": roic,
                "current_ratio": current_ratio,
                "debt_to_equity": debt_to_equity,
                "debt_to_ebitda": debt_to_ebitda,
                "interest_coverage": interest_coverage,
                "dso": dso,
                "dio": dio,
                "dpo": dpo,
                "cash_conversion_cycle": ccc
            }
            prev_period_data = curr

        # Multi-Year CAGRs
        n_periods = len(periods_chronological)
        revenue_cagr_3yr = None
        revenue_cagr_5yr = None
        
        if n_periods >= 4:
            revenue_cagr_3yr = cls.calculate_cagr(
                start_value=period_metrics[periods_chronological[-4]]["revenue"],
                end_value=period_metrics[periods_chronological[-1]]["revenue"],
                n_years=3
            )
        if n_periods >= 6:
            revenue_cagr_5yr = cls.calculate_cagr(
                start_value=period_metrics[periods_chronological[-6]]["revenue"],
                end_value=period_metrics[periods_chronological[-1]]["revenue"],
                n_years=5
            )

        return {
            "period_metrics": period_metrics,
            "cagr_summary": {
                "revenue_3yr_cagr": revenue_cagr_3yr,
                "revenue_5yr_cagr": revenue_cagr_5yr
            }
        }
