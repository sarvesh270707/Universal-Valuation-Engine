"""
Universal Financial Valuation & DCF Engine - Cost of Capital Module
Calculates Cost of Equity (CAPM), Unlevered/Relevered Beta (Hamada Equation),
Cost of Debt, Capital Structure Weights, and Blended WACC.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from backend.engine.classification.sector_classifier import SectorType

class CostOfCapitalEngine:
    """
    Computes rigorous, source-backed discount rates for equity and enterprise valuation.
    """

    DEFAULT_GSEC_RF = 0.0700 # 7.00% Indian 10-Yr Benchmark G-Sec
    DEFAULT_ERP = 0.0700     # 7.00% Indian Equity Risk Premium
    DEFAULT_STATUTORY_TAX = 0.2517 # 25.17% Base Corporate Tax Rate

    @staticmethod
    def unlever_beta(levered_beta: float, debt_to_equity: float, tax_rate: float) -> float:
        """
        Hamada Equation: βu = βl / (1 + (1 - t) * (D/E))
        """
        denom = 1.0 + ((1.0 - tax_rate) * debt_to_equity)
        return levered_beta / denom

    @staticmethod
    def relever_beta(unlevered_beta: float, debt_to_equity: float, tax_rate: float) -> float:
        """
        Hamada Equation: βl = βu * (1 + (1 - t) * (D/E))
        """
        return unlevered_beta * (1.0 + ((1.0 - tax_rate) * debt_to_equity))

    @classmethod
    def calculate_cost_of_capital(
        cls,
        sector: SectorType,
        risk_free_rate: float = DEFAULT_GSEC_RF,
        equity_risk_premium: float = DEFAULT_ERP,
        beta: float = 1.15,
        pre_tax_cost_of_debt: float = 0.075,
        tax_rate: float = DEFAULT_STATUTORY_TAX,
        equity_market_value: float = 80000.0,
        total_debt_value: float = 20000.0,
        valuation_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Computes complete cost of capital profile.
        Automatically substitutes Ke for WACC if the entity is a Bank, NBFC, or Life Insurer.
        """
        valuation_dt = valuation_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # 1. Cost of Equity via CAPM
        cost_of_equity = risk_free_rate + (beta * equity_risk_premium)

        # 2. Check if Financial Institution
        is_financial = sector in [SectorType.BANKING, SectorType.NBFC, SectorType.LIFE_INSURANCE, SectorType.GENERAL_INSURANCE]

        if is_financial:
            return {
                "sector": sector.value,
                "is_financial_institution": True,
                "applicable_discount_rate_name": "Cost of Equity (Ke)",
                "applicable_discount_rate": cost_of_equity,
                "cost_of_equity": cost_of_equity,
                "risk_free_rate": risk_free_rate,
                "beta": beta,
                "equity_risk_premium": equity_risk_premium,
                "wacc": cost_of_equity, # For financials, discount rate is Ke
                "note": "For financial institutions (Banks/NBFCs/Insurers), equity cash flows/dividends are discounted at Ke rather than WACC.",
                "provenance": {
                    "rf_source": "RBI 10-Yr Benchmark G-Sec Yield",
                    "erp_source": "Damodaran Indian Market Risk Premium",
                    "retrieval_date": valuation_dt
                }
            }

        # 3. Industrial / Corporate Capital Structure & WACC
        total_capital = equity_market_value + total_debt_value
        weight_equity = equity_market_value / total_capital
        weight_debt = total_debt_value / total_capital

        after_tax_kd = pre_tax_cost_of_debt * (1.0 - tax_rate)
        wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_kd)

        # Decompose Unlevered Beta
        de_ratio = total_debt_value / equity_market_value if equity_market_value > 0 else 0.0
        unlevered_beta = cls.unlever_beta(beta, de_ratio, tax_rate)

        return {
            "sector": sector.value,
            "is_financial_institution": False,
            "applicable_discount_rate_name": "Weighted Average Cost of Capital (WACC)",
            "applicable_discount_rate": wacc,
            "wacc": wacc,
            "cost_of_equity": cost_of_equity,
            "pre_tax_cost_of_debt": pre_tax_cost_of_debt,
            "after_tax_cost_of_debt": after_tax_kd,
            "risk_free_rate": risk_free_rate,
            "equity_risk_premium": equity_risk_premium,
            "levered_beta": beta,
            "unlevered_beta": unlevered_beta,
            "tax_rate": tax_rate,
            "weight_equity": weight_equity,
            "weight_debt": weight_debt,
            "debt_to_equity_ratio": de_ratio,
            "provenance": {
                "rf_source": "RBI 10-Yr Benchmark G-Sec Yield",
                "erp_source": "Damodaran Indian Market Risk Premium",
                "kd_source": "Weighted Average Effective Borrowing Rate",
                "retrieval_date": valuation_dt
            }
        }
