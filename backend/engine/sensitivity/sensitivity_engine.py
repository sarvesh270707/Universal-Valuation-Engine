"""
Universal Financial Valuation & DCF Engine - Scenario & Sensitivity Engine
Generates:
1. Multi-scenario financial projections (Bear, Base, Bull)
2. Dynamic 2-dimensional sensitivity matrices:
   - WACC vs. Terminal Growth Rate
   - WACC vs. Exit Multiple
   - Revenue Growth vs. EBITDA Margin
   - Loan Growth vs. Net Interest Margin (Banking)
"""

from typing import Dict, Any, List, Optional, Tuple
from backend.engine.valuation.valuation_suite import UniversalValuationSuite
from backend.engine.three_statement.three_statement_model import ThreeStatementEngine, ScenarioAssumptions

class SensitivityEngine:
    """
    Computes rigorous multidimensional stress matrices and scenario comparisons.
    """

    @staticmethod
    def generate_scenarios(base_financials: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """
        Generates standard institutional Bear, Base, and Bull financial projections.
        """
        scenarios = {
            "BEAR": ScenarioAssumptions(
                revenue_growth_rate=0.08,
                gross_margin=0.25,
                ebitda_margin=0.09,
                capex_pct_revenue=0.035,
                effective_tax_rate=0.2517
            ),
            "BASE": ScenarioAssumptions(
                revenue_growth_rate=0.15,
                gross_margin=0.28,
                ebitda_margin=0.12,
                capex_pct_revenue=0.025,
                effective_tax_rate=0.2517
            ),
            "BULL": ScenarioAssumptions(
                revenue_growth_rate=0.22,
                gross_margin=0.31,
                ebitda_margin=0.15,
                capex_pct_revenue=0.020,
                effective_tax_rate=0.2517
            )
        }

        output = {}
        for sc_name, sc_assumptions in scenarios.items():
            proj = ThreeStatementEngine.project_three_statements(
                base_year_data=base_financials,
                assumptions=sc_assumptions,
                forecast_years=5
            )
            # Extract final year metrics
            final_p = proj["forecast_periods"][-1]
            final_stmt = proj["statements"][final_p]
            output[sc_name] = {
                "assumptions": sc_assumptions.dict(),
                "final_year_revenue": final_stmt["operating_revenue"],
                "final_year_ebitda": final_stmt["ebitda"],
                "final_year_nopat": final_stmt["nopat"],
                "forecast_ufcfs": [proj["statements"][p]["ufcf"] for p in proj["forecast_periods"]],
                "final_year_ebitda_val": final_stmt["ebitda"]
            }

        return output

    @staticmethod
    def generate_wacc_vs_multiple_matrix(
        forecast_ufcfs: List[float],
        final_ebitda: float,
        total_debt: float,
        cash_and_equivalents: float,
        shares_outstanding: float,
        wacc_range: List[float] = [0.12, 0.13, 0.1443, 0.16, 0.18],
        multiple_range: List[float] = [25.0, 30.0, 35.0, 40.0, 45.0]
    ) -> Dict[str, Any]:
        """
        Computes 5x5 WACC vs. Exit Multiple sensitivity matrix.
        Validates strict monotonic gradient (Higher Multiple = Higher Price; Higher WACC = Lower Price).
        """
        grid = []
        is_monotonic = True

        for w in wacc_range:
            row_vals = []
            for m in multiple_range:
                res = UniversalValuationSuite.execute_fcff_dcf(
                    forecast_ufcfs=forecast_ufcfs,
                    terminal_growth_rate=0.05,
                    wacc=w,
                    final_ebitda=final_ebitda,
                    exit_multiple=m,
                    total_debt=total_debt,
                    cash_and_equivalents=cash_and_equivalents,
                    shares_outstanding=shares_outstanding
                )
                price = round(res["exit_multiple_method"]["intrinsic_value_per_share"], 2)
                row_vals.append(price)
            grid.append(row_vals)

        # Monotonicity check
        # Along rows (increasing multiple): values must be strictly increasing
        for r in grid:
            for i in range(len(r) - 1):
                if r[i] >= r[i+1]:
                    is_monotonic = False

        # Along columns (increasing WACC): values must be strictly decreasing
        for c in range(len(grid[0])):
            for r in range(len(grid) - 1):
                if grid[r][c] <= grid[r+1][c]:
                    is_monotonic = False

        return {
            "row_variable": "WACC",
            "row_labels": [f"{w*100:.2f}%" for w in wacc_range],
            "row_values": wacc_range,
            "col_variable": "Exit Multiple",
            "col_labels": [f"{m:.1f}x" for m in multiple_range],
            "col_values": multiple_range,
            "matrix": grid,
            "is_strictly_monotonic": is_monotonic
        }

    @staticmethod
    def generate_wacc_vs_growth_matrix(
        forecast_ufcfs: List[float],
        final_ebitda: float,
        total_debt: float,
        cash_and_equivalents: float,
        shares_outstanding: float,
        wacc_range: List[float] = [0.12, 0.13, 0.1443, 0.16, 0.18],
        growth_range: List[float] = [0.03, 0.04, 0.05, 0.055, 0.06]
    ) -> Dict[str, Any]:
        """
        Computes 5x5 WACC vs. Perpetual Growth Rate sensitivity matrix.
        Defensively skips or flags any cell where WACC <= g.
        """
        grid = []
        is_monotonic = True

        for w in wacc_range:
            row_vals = []
            for g in growth_range:
                if w <= g:
                    row_vals.append(None) # Singularity trap
                    continue

                res = UniversalValuationSuite.execute_fcff_dcf(
                    forecast_ufcfs=forecast_ufcfs,
                    terminal_growth_rate=g,
                    wacc=w,
                    final_ebitda=final_ebitda,
                    exit_multiple=35.0,
                    total_debt=total_debt,
                    cash_and_equivalents=cash_and_equivalents,
                    shares_outstanding=shares_outstanding
                )
                price = round(res["gordon_growth_method"]["intrinsic_value_per_share"], 2)
                row_vals.append(price)
            grid.append(row_vals)

        return {
            "row_variable": "WACC",
            "row_labels": [f"{w*100:.2f}%" for w in wacc_range],
            "row_values": wacc_range,
            "col_variable": "Terminal Growth Rate",
            "col_labels": [f"{g*100:.2f}%" for g in growth_range],
            "col_values": growth_range,
            "matrix": grid
        }
