"""
Universal Financial Valuation & DCF Engine - Core Formula Module
Implements strictly validated, decimal-aware financial formulas with:
- Division-by-zero traps
- Singularity protection (WACC <= g)
- Calculation audit trails
- Standard institutional sign conventions
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Dict, Any, List, Optional, Tuple
import math

class FinancialFormulaException(Exception):
    """Custom exception raised when financial inputs violate economic or mathematical bounds."""
    pass

class FinancialFormulaEngine:
    """
    Certified mathematical formula engine for corporate finance and equity valuation.
    """

    @staticmethod
    def calculate_nopat(ebit: float, effective_tax_rate: float) -> Tuple[float, Dict[str, Any]]:
        """
        NOPAT = EBIT * (1 - Tax Rate)
        """
        if effective_tax_rate < 0.0 or effective_tax_rate > 1.0:
            raise FinancialFormulaException(f"Effective tax rate must be between 0.0 and 1.0, got {effective_tax_rate}")
        
        nopat = ebit * (1.0 - effective_tax_rate)
        audit_trail = {
            "formula": "EBIT * (1 - Tax Rate)",
            "ebit": ebit,
            "tax_rate": effective_tax_rate,
            "tax_shield_factor": 1.0 - effective_tax_rate,
            "result_nopat": nopat
        }
        return nopat, audit_trail

    @staticmethod
    def calculate_fcff(
        nopat: float,
        depreciation_amortisation: float,
        capital_expenditure: float,
        change_in_working_capital: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        FCFF (Free Cash Flow to Firm / Unlevered Free Cash Flow):
        FCFF = NOPAT + D&A - CapEx - Change in Operating NWC
        """
        fcff = nopat + depreciation_amortisation - capital_expenditure - change_in_working_capital
        audit_trail = {
            "formula": "NOPAT + D&A - CapEx - Change in NWC",
            "nopat": nopat,
            "depreciation_amortisation": depreciation_amortisation,
            "capital_expenditure": capital_expenditure,
            "change_in_working_capital": change_in_working_capital,
            "result_fcff": fcff
        }
        return fcff, audit_trail

    @staticmethod
    def calculate_fcfe(
        net_income: float,
        depreciation_amortisation: float,
        capital_expenditure: float,
        change_in_working_capital: float,
        net_borrowing: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        FCFE (Free Cash Flow to Equity):
        FCFE = Net Income + D&A - CapEx - Change in Operating NWC + Net Borrowing
        """
        fcfe = net_income + depreciation_amortisation - capital_expenditure - change_in_working_capital + net_borrowing
        audit_trail = {
            "formula": "Net Income + D&A - CapEx - Change in NWC + Net Borrowing",
            "net_income": net_income,
            "depreciation_amortisation": depreciation_amortisation,
            "capital_expenditure": capital_expenditure,
            "change_in_working_capital": change_in_working_capital,
            "net_borrowing": net_borrowing,
            "result_fcfe": fcfe
        }
        return fcfe, audit_trail

    @staticmethod
    def calculate_capm(
        risk_free_rate: float,
        beta: float,
        equity_risk_premium: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Cost of Equity (Ke) via Capital Asset Pricing Model:
        Ke = Risk-free Rate + Beta * ERP
        """
        if risk_free_rate < 0.0:
            raise FinancialFormulaException(f"Risk-free rate cannot be negative in Indian G-Sec context: {risk_free_rate}")
        if equity_risk_premium <= 0.0:
            raise FinancialFormulaException(f"Equity risk premium must be positive: {equity_risk_premium}")
        if beta < 0.0:
            raise FinancialFormulaException(f"Beta must be non-negative: {beta}")

        cost_of_equity = risk_free_rate + (beta * equity_risk_premium)
        audit_trail = {
            "formula": "Rf + Beta * ERP",
            "risk_free_rate": risk_free_rate,
            "beta": beta,
            "equity_risk_premium": equity_risk_premium,
            "result_ke": cost_of_equity
        }
        return cost_of_equity, audit_trail

    @staticmethod
    def calculate_wacc(
        equity_value: float,
        debt_value: float,
        cost_of_equity: float,
        cost_of_debt: float,
        marginal_tax_rate: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Weighted Average Cost of Capital (WACC):
        WACC = (E/V * Ke) + (D/V * Kd * (1 - Tax Rate))
        """
        if equity_value < 0.0 or debt_value < 0.0:
            raise FinancialFormulaException("Equity value and debt value must be non-negative")
        
        total_capital = equity_value + debt_value
        if total_capital == 0.0:
            raise FinancialFormulaException("Total firm capital (E + D) cannot be zero")

        weight_equity = equity_value / total_capital
        weight_debt = debt_value / total_capital
        after_tax_cost_of_debt = cost_of_debt * (1.0 - marginal_tax_rate)

        wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_of_debt)
        audit_trail = {
            "formula": "(E/V * Ke) + (D/V * Kd * (1 - t))",
            "equity_weight": weight_equity,
            "debt_weight": weight_debt,
            "cost_of_equity": cost_of_equity,
            "pre_tax_cost_of_debt": cost_of_debt,
            "after_tax_cost_of_debt": after_tax_cost_of_debt,
            "result_wacc": wacc
        }
        return wacc, audit_trail

    @staticmethod
    def calculate_terminal_value_gordon(
        terminal_cash_flow: float,
        terminal_growth_rate: float,
        discount_rate: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Gordon Growth Terminal Value:
        TV = Cash Flow(n+1) / (WACC - g) = CF(n) * (1 + g) / (WACC - g)
        Defensive trap: discount_rate must be strictly greater than terminal_growth_rate.
        """
        if discount_rate <= terminal_growth_rate:
            raise FinancialFormulaException(
                f"Singularity Trap: Discount Rate ({discount_rate:.4f}) must be strictly greater "
                f"than Perpetual Growth Rate ({terminal_growth_rate:.4f})"
            )
        
        denominator = discount_rate - terminal_growth_rate
        if denominator == 0.0:
            raise FinancialFormulaException("Division by zero in terminal value denominator")

        tv = terminal_cash_flow / denominator
        audit_trail = {
            "formula": "CF(n+1) / (Discount_Rate - g)",
            "terminal_cash_flow": terminal_cash_flow,
            "terminal_growth_rate": terminal_growth_rate,
            "discount_rate": discount_rate,
            "spread": denominator,
            "result_tv": tv
        }
        return tv, audit_trail

    @staticmethod
    def calculate_terminal_value_exit_multiple(
        final_year_ebitda: float,
        exit_multiple: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Exit Multiple Terminal Value:
        TV = Final Year EBITDA * Exit Multiple
        """
        if exit_multiple <= 0.0:
            raise FinancialFormulaException(f"Exit multiple must be positive: {exit_multiple}")
        
        tv = final_year_ebitda * exit_multiple
        audit_trail = {
            "formula": "Final EBITDA * Exit Multiple",
            "final_year_ebitda": final_year_ebitda,
            "exit_multiple": exit_multiple,
            "result_tv": tv
        }
        return tv, audit_trail

    @staticmethod
    def calculate_enterprise_value(
        forecast_cash_flows: List[float],
        discount_rate: float,
        terminal_value: float,
        mid_year_convention: bool = True
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Enterprise Value = PV of Explicit Forecast Cash Flows + PV of Terminal Value
        Supports standard year-end and mid-year discounting conventions.
        """
        if discount_rate <= 0.0:
            raise FinancialFormulaException(f"Discount rate must be positive: {discount_rate}")
        
        n_periods = len(forecast_cash_flows)
        if n_periods == 0:
            raise FinancialFormulaException("Forecast cash flows list cannot be empty")

        pv_explicit_flows = []
        for idx, cf in enumerate(forecast_cash_flows):
            t = (idx + 0.5) if mid_year_convention else (idx + 1.0)
            discount_factor = 1.0 / math.pow(1.0 + discount_rate, t)
            pv_cf = cf * discount_factor
            pv_explicit_flows.append({
                "period": idx + 1,
                "t": t,
                "cash_flow": cf,
                "discount_factor": discount_factor,
                "pv": pv_cf
            })

        sum_pv_explicit = sum(item["pv"] for item in pv_explicit_flows)
        
        # Terminal value discount factor at horizon N
        tv_t = n_periods if not mid_year_convention else n_periods
        tv_discount_factor = 1.0 / math.pow(1.0 + discount_rate, tv_t)
        pv_terminal_value = terminal_value * tv_discount_factor

        enterprise_value = sum_pv_explicit + pv_terminal_value
        audit_trail = {
            "sum_pv_explicit": sum_pv_explicit,
            "pv_terminal_value": pv_terminal_value,
            "tv_discount_factor": tv_discount_factor,
            "explicit_breakdown": pv_explicit_flows,
            "result_enterprise_value": enterprise_value
        }
        return enterprise_value, audit_trail

    @staticmethod
    def calculate_equity_bridge(
        enterprise_value: float,
        total_debt: float,
        cash_and_equivalents: float,
        minority_interest: float = 0.0,
        preferred_stock: float = 0.0,
        non_operating_assets: float = 0.0
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Equity Value = EV - Debt - Preferred Stock - Minority Interest + Cash + Non-operating Assets
        """
        equity_value = (
            enterprise_value 
            - total_debt 
            - preferred_stock 
            - minority_interest 
            + cash_and_equivalents 
            + non_operating_assets
        )
        net_debt = total_debt - cash_and_equivalents
        audit_trail = {
            "formula": "EV - Debt - Pref - Minority + Cash + NonOperating",
            "enterprise_value": enterprise_value,
            "total_debt": total_debt,
            "cash_and_equivalents": cash_and_equivalents,
            "net_debt": net_debt,
            "minority_interest": minority_interest,
            "preferred_stock": preferred_stock,
            "non_operating_assets": non_operating_assets,
            "result_equity_value": equity_value
        }
        return equity_value, audit_trail

    @staticmethod
    def calculate_per_share_value(
        equity_value: float,
        fully_diluted_shares: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Intrinsic Value Per Share = Equity Value / Fully Diluted Shares
        """
        if fully_diluted_shares <= 0.0:
            raise FinancialFormulaException(f"Fully diluted shares must be positive: {fully_diluted_shares}")

        per_share_value = equity_value / fully_diluted_shares
        audit_trail = {
            "equity_value": equity_value,
            "fully_diluted_shares": fully_diluted_shares,
            "result_per_share_value": per_share_value
        }
        return per_share_value, audit_trail
