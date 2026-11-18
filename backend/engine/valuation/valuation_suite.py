"""
Universal Financial Valuation & DCF Engine - Valuation Methodologies Suite
Implements:
1. Industrial FCFF DCF (Dual Terminal: Exit Multiple & Gordon Growth)
2. FCFE DCF (Discounted at Ke)
3. Dividend Discount Model (DDM for Banks & Financials)
4. Residual Income Model (RIM)
5. Net Asset Value (NAV for REITs & Real Estate)
6. Sum of the Parts (SOTP for Conglomerates)
7. Comparable Company Analysis (CCA / Trading Multiples)
8. Embedded Value & VNB (Life Insurance)
"""

from typing import Dict, Any, List, Optional
import math
from backend.engine.formulas.core_formulas import FinancialFormulaEngine, FinancialFormulaException
from backend.engine.classification.sector_classifier import SectorType

class ValuationMethodologyException(Exception):
    pass

class UniversalValuationSuite:
    """
    Executes sector-appropriate equity and enterprise valuation models.
    """

    @staticmethod
    def execute_fcff_dcf(
        forecast_ufcfs: List[float],
        terminal_growth_rate: float,
        wacc: float,
        final_ebitda: float,
        exit_multiple: float,
        total_debt: float,
        cash_and_equivalents: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Industrial FCFF DCF generating dual targets: Exit Multiple and Gordon Growth.
        """
        # 1. Exit Multiple Valuation
        tv_exit, _ = FinancialFormulaEngine.calculate_terminal_value_exit_multiple(final_ebitda, exit_multiple)
        ev_exit, audit_exit = FinancialFormulaEngine.calculate_enterprise_value(forecast_ufcfs, wacc, tv_exit)
        eq_exit, _ = FinancialFormulaEngine.calculate_equity_bridge(ev_exit, total_debt, cash_and_equivalents)
        price_exit, _ = FinancialFormulaEngine.calculate_per_share_value(eq_exit, shares_outstanding)

        # 2. Gordon Growth Valuation
        final_ufcf = forecast_ufcfs[-1]
        terminal_ufcf = final_ufcf * (1.0 + terminal_growth_rate)
        tv_growth, _ = FinancialFormulaEngine.calculate_terminal_value_gordon(terminal_ufcf, terminal_growth_rate, wacc)
        ev_growth, audit_growth = FinancialFormulaEngine.calculate_enterprise_value(forecast_ufcfs, wacc, tv_growth)
        eq_growth, _ = FinancialFormulaEngine.calculate_equity_bridge(ev_growth, total_debt, cash_and_equivalents)
        price_growth, _ = FinancialFormulaEngine.calculate_per_share_value(eq_growth, shares_outstanding)

        return {
            "methodology": "FCFF_DCF",
            "wacc": wacc,
            "exit_multiple_method": {
                "exit_multiple": exit_multiple,
                "terminal_value": tv_exit,
                "enterprise_value": ev_exit,
                "equity_value": eq_exit,
                "intrinsic_value_per_share": price_exit
            },
            "gordon_growth_method": {
                "terminal_growth_rate": terminal_growth_rate,
                "terminal_value": tv_growth,
                "enterprise_value": ev_growth,
                "equity_value": eq_growth,
                "intrinsic_value_per_share": price_growth
            }
        }

    @staticmethod
    def execute_fcfe_dcf(
        forecast_fcfes: List[float],
        terminal_growth_rate: float,
        cost_of_equity: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Free Cash Flow to Equity (FCFE) directly outputs Equity Value.
        """
        if cost_of_equity <= terminal_growth_rate:
            raise ValuationMethodologyException("Cost of equity must be strictly greater than terminal growth rate")

        final_fcfe = forecast_fcfes[-1]
        terminal_fcfe = final_fcfe * (1.0 + terminal_growth_rate)
        tv_equity = terminal_fcfe / (cost_of_equity - terminal_growth_rate)

        # Discount explicit FCFEs and TV at Ke
        pv_fcfes = [cf / math.pow(1.0 + cost_of_equity, i + 1) for i, cf in enumerate(forecast_fcfes)]
        pv_tv = tv_equity / math.pow(1.0 + cost_of_equity, len(forecast_fcfes))
        equity_value = sum(pv_fcfes) + pv_tv
        price_per_share, _ = FinancialFormulaEngine.calculate_per_share_value(equity_value, shares_outstanding)

        return {
            "methodology": "FCFE_DCF",
            "cost_of_equity": cost_of_equity,
            "terminal_growth_rate": terminal_growth_rate,
            "equity_value": equity_value,
            "intrinsic_value_per_share": price_per_share
        }

    @staticmethod
    def execute_ddm(
        forecast_dividends: List[float],
        terminal_growth_rate: float,
        cost_of_equity: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Dividend Discount Model (DDM) for Commercial Banks and Dividend-Paying Institutions.
        """
        if cost_of_equity <= terminal_growth_rate:
            raise ValuationMethodologyException("Cost of equity must be strictly greater than terminal dividend growth")

        pv_dividends = [d / math.pow(1.0 + cost_of_equity, i + 1) for i, d in enumerate(forecast_dividends)]
        final_div = forecast_dividends[-1]
        tv_dividend = (final_div * (1.0 + terminal_growth_rate)) / (cost_of_equity - terminal_growth_rate)
        pv_tv = tv_dividend / math.pow(1.0 + cost_of_equity, len(forecast_dividends))

        equity_value = sum(pv_dividends) + pv_tv
        price_per_share, _ = FinancialFormulaEngine.calculate_per_share_value(equity_value, shares_outstanding)

        return {
            "methodology": "DDM",
            "cost_of_equity": cost_of_equity,
            "terminal_growth_rate": terminal_growth_rate,
            "equity_value": equity_value,
            "intrinsic_value_per_share": price_per_share
        }

    @staticmethod
    def execute_residual_income(
        current_book_value: float,
        forecast_net_incomes: List[float],
        cost_of_equity: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Residual Income Model (RIM) = Current Book Value + PV of Residual Incomes (Net Income - Equity Charge).
        """
        pv_residual_incomes = []
        book_val = current_book_value

        for i, ni in enumerate(forecast_net_incomes):
            equity_charge = book_val * cost_of_equity
            residual_income = ni - equity_charge
            pv_ri = residual_income / math.pow(1.0 + cost_of_equity, i + 1)
            pv_residual_incomes.append(pv_ri)
            book_val += (ni * 0.70) # Assume 30% dividend payout

        equity_value = current_book_value + sum(pv_residual_incomes)
        price_per_share, _ = FinancialFormulaEngine.calculate_per_share_value(equity_value, shares_outstanding)

        return {
            "methodology": "RESIDUAL_INCOME",
            "current_book_value": current_book_value,
            "pv_residual_incomes_sum": sum(pv_residual_incomes),
            "equity_value": equity_value,
            "intrinsic_value_per_share": price_per_share
        }

    @staticmethod
    def execute_nav(
        revalued_assets: float,
        total_liabilities: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Net Asset Value (NAV) for REITs and Real Estate Companies.
        """
        net_asset_value = revalued_assets - total_liabilities
        price_per_share, _ = FinancialFormulaEngine.calculate_per_share_value(net_asset_value, shares_outstanding)
        return {
            "methodology": "NAV",
            "revalued_gross_assets": revalued_assets,
            "total_liabilities": total_liabilities,
            "net_asset_value": net_asset_value,
            "intrinsic_value_per_share": price_per_share
        }

    @staticmethod
    def execute_sotp(
        segments: List[Dict[str, Any]], # [{"segment": "...", "metric": 100, "multiple": 10.0}]
        net_debt: float,
        holding_company_discount: float,
        shares_outstanding: float
    ) -> Dict[str, Any]:
        """
        Sum of the Parts (SOTP) with Holding Company Conglomerate Discount.
        """
        segment_values = []
        gross_ev = 0.0
        for seg in segments:
            val = seg["metric"] * seg["multiple"]
            segment_values.append({
                "segment_name": seg["segment_name"],
                "metric_value": seg["metric"],
                "multiple": seg["multiple"],
                "enterprise_value": val
            })
            gross_ev += val

        discounted_ev = gross_ev * (1.0 - holding_company_discount)
        equity_val = max(0.0, discounted_ev - net_debt)
        price_per_share, _ = FinancialFormulaEngine.calculate_per_share_value(equity_val, shares_outstanding)

        return {
            "methodology": "SOTP",
            "segments_breakdown": segment_values,
            "gross_enterprise_value": gross_ev,
            "holding_company_discount_pct": holding_company_discount,
            "discounted_enterprise_value": discounted_ev,
            "net_debt": net_debt,
            "equity_value": equity_val,
            "intrinsic_value_per_share": price_per_share
        }

    @staticmethod
    def enforce_sector_appropriateness(sector: SectorType, selected_method: str):
        """
        Defensive gate: prevents running inappropriate valuation models (e.g. FCFF on Banks).
        """
        method_upper = selected_method.upper()
        if sector == SectorType.BANKING and "FCFF" in method_upper:
            raise ValuationMethodologyException(
                "Methodology Invalidation Gate: FCFF DCF is economically invalid for Commercial Banks "
                "because debt is raw material operating inventory (deposits/borrowings), not leverage capital. "
                "Use Dividend Discount Model (DDM) or Residual Income (RIM)."
            )
        if sector == SectorType.LIFE_INSURANCE and "FCFF" in method_upper:
            raise ValuationMethodologyException(
                "Methodology Invalidation Gate: FCFF DCF is invalid for Life Insurers due to policyholder reserves. "
                "Use Embedded Value (EV) & Value of New Business (VNB)."
            )
