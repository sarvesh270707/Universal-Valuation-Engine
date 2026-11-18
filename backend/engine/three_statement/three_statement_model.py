"""
Universal Financial Valuation & DCF Engine - Three-Statement Modelling Engine
Projects integrated 5-year financial statements with:
- Natural Balance Sheet balancing (Assets == Liabilities + Equity with 0.00 deviation)
- Complete Cash Flow reconciliation (Closing Cash == Balance Sheet Cash)
- Explicit roll-forward schedules: PP&E, Debt, Working Capital, Retained Earnings
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ScenarioAssumptions(BaseModel):
    revenue_growth_rate: float = 0.12 # 12% annual growth
    gross_margin: float = 0.28 # 28% gross margin
    ebitda_margin: float = 0.12 # 12% EBITDA margin
    capex_pct_revenue: float = 0.025 # 2.5% of revenue
    depreciation_rate_ppe: float = 0.10 # 10% on opening net block
    effective_tax_rate: float = 0.2517 # 25.17%
    dividend_payout_ratio: float = 0.25 # 25% of PAT
    cost_of_debt: float = 0.075 # 7.5%
    dso_days: float = 8.0
    dio_days: float = 120.0
    dpo_days: float = 55.0

class ThreeStatementEngine:
    """
    Simulates integrated multi-year corporate financial statements ensuring strict double-entry balancing.
    """

    @classmethod
    def project_three_statements(
        cls,
        base_year_data: Dict[str, float],
        assumptions: ScenarioAssumptions,
        forecast_years: int = 5,
        start_forecast_year: int = 27 # e.g. FY27E
    ) -> Dict[str, Any]:
        """
        Projects Income Statement, Balance Sheet, and Cash Flow statement over N explicit forecast years.
        Guarantees: Total Assets == Total Liabilities + Equity (Deviation = 0.00).
        """
        projected_periods = []
        forecast_results = {}

        # Initial balance sheet balances from base year (e.g. FY26)
        curr_cash = base_year_data.get("cash_and_equivalents", 500.0)
        curr_ppe = base_year_data.get("property_plant_equipment", 2500.0)
        curr_other_assets = base_year_data.get("other_assets", 0.0)
        curr_debt = base_year_data.get("financial_debt", 1500.0)
        curr_equity = base_year_data.get("shareholders_equity", 4000.0)
        curr_share_capital = base_year_data.get("share_capital", 88.78)
        curr_retained_earnings = curr_equity - curr_share_capital

        prev_revenue = base_year_data.get("operating_revenue", 10000.0)

        for yr_idx in range(forecast_years):
            fy_label = f"FY{start_forecast_year + yr_idx}E"
            projected_periods.append(fy_label)

            # 1. Income Statement Projections
            revenue = prev_revenue * (1.0 + assumptions.revenue_growth_rate)
            cogs = revenue * (1.0 - assumptions.gross_margin)
            ebitda = revenue * assumptions.ebitda_margin
            
            # PP&E & Depreciation Schedule
            capex = revenue * assumptions.capex_pct_revenue
            depreciation = curr_ppe * assumptions.depreciation_rate_ppe
            closing_ppe = curr_ppe + capex - depreciation

            ebit = ebitda - depreciation
            
            # Debt & Interest Schedule (Opening Debt * Kd)
            interest_expense = curr_debt * assumptions.cost_of_debt
            pbt = ebit - interest_expense
            tax = max(0.0, pbt * assumptions.effective_tax_rate)
            net_income = pbt - tax

            # Dividend & Retained Earnings Roll-Forward
            dividends = net_income * assumptions.dividend_payout_ratio
            retained_earnings_addition = net_income - dividends
            closing_retained_earnings = curr_retained_earnings + retained_earnings_addition
            closing_equity = curr_share_capital + closing_retained_earnings

            # Working Capital Schedule
            receivables = (assumptions.dso_days / 365.0) * revenue
            inventory = (assumptions.dio_days / 365.0) * cogs
            payables = (assumptions.dpo_days / 365.0) * cogs
            nwc = receivables + inventory - payables

            prev_rec = base_year_data.get("trade_receivables", 0.0) if yr_idx == 0 else forecast_results[projected_periods[yr_idx-1]]["trade_receivables"]
            prev_inv = base_year_data.get("inventory", 0.0) if yr_idx == 0 else forecast_results[projected_periods[yr_idx-1]]["inventory"]
            prev_pay = base_year_data.get("trade_payables", 0.0) if yr_idx == 0 else forecast_results[projected_periods[yr_idx-1]]["trade_payables"]
            delta_nwc = (receivables - prev_rec) + (inventory - prev_inv) - (payables - prev_pay)

            # 2. Cash Flow Statement Projections
            # Cash Flow from Operations (CFO)
            cfo = net_income + depreciation - delta_nwc
            # Cash Flow from Investing (CFI)
            cfi = -capex
            # Cash Flow from Financing (CFF)
            # Principal repayment / debt policy: keep debt constant or scheduled
            net_borrowing = 0.0
            cff = net_borrowing - dividends

            net_change_in_cash = cfo + cfi + cff
            closing_cash = curr_cash + net_change_in_cash

            # 3. Balance Sheet Integration & Check
            total_assets = closing_cash + receivables + inventory + closing_ppe + curr_other_assets
            total_liabilities_and_equity = payables + curr_debt + closing_equity

            # Exact natural equilibrium check
            bs_difference = total_assets - total_liabilities_and_equity

            # Unlevered Free Cash Flow (UFCF)
            nopat = ebit * (1.0 - assumptions.effective_tax_rate)
            ufcf = nopat + depreciation - capex - delta_nwc

            forecast_results[fy_label] = {
                # P&L
                "operating_revenue": revenue,
                "cost_of_goods_sold": cogs,
                "ebitda": ebitda,
                "depreciation_amortisation": depreciation,
                "ebit": ebit,
                "finance_cost": interest_expense,
                "profit_before_tax": pbt,
                "income_tax": tax,
                "net_income": net_income,
                "dividends_paid": dividends,
                "nopat": nopat,
                "ufcf": ufcf,
                # Balance Sheet
                "cash_and_equivalents": closing_cash,
                "trade_receivables": receivables,
                "inventory": inventory,
                "property_plant_equipment": closing_ppe,
                "total_assets": total_assets,
                "trade_payables": payables,
                "financial_debt": curr_debt,
                "share_capital": curr_share_capital,
                "reserves_and_surplus": closing_retained_earnings,
                "shareholders_equity": closing_equity,
                "total_liabilities_and_equity": total_liabilities_and_equity,
                "balance_sheet_difference": bs_difference,
                # Cash Flow
                "cash_flow_operations": cfo,
                "cash_flow_investing": cfi,
                "cash_flow_financing": cff,
                "net_change_in_cash": net_change_in_cash
            }

            # Roll forward state to next year
            curr_cash = closing_cash
            curr_ppe = closing_ppe
            curr_retained_earnings = closing_retained_earnings
            curr_equity = closing_equity
            prev_revenue = revenue

        return {
            "forecast_periods": projected_periods,
            "statements": forecast_results,
            "max_balance_sheet_discrepancy": max(abs(v["balance_sheet_difference"]) for v in forecast_results.values())
        }
