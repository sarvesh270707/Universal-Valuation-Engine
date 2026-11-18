"""
Universal Accounting Dictionary & Standard Financial Taxonomy
Enforces strict accounting concepts across corporate, manufacturing,
banking, NBFC, insurance, and REIT financial reporting.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class MissingValueState(str, Enum):
    ZERO = "ZERO"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_DISCLOSED = "NOT_DISCLOSED"
    NOT_EXTRACTED = "NOT_EXTRACTED"
    AWAITING_VERIFICATION = "AWAITING_VERIFICATION"

class StatementType(str, Enum):
    INCOME_STATEMENT = "INCOME_STATEMENT"
    BALANCE_SHEET = "BALANCE_SHEET"
    CASH_FLOW = "CASH_FLOW"
    SPECIALIZED_DISCLOSURE = "SPECIALIZED_DISCLOSURE"

class StandardFinancialFact(BaseModel):
    standard_concept: str
    statement_type: StatementType
    numeric_value: Optional[float] = None
    missing_state: MissingValueState = MissingValueState.AWAITING_VERIFICATION
    raw_label: Optional[str] = None
    currency: str = "INR"
    unit_scale: str = "CRORE"
    source_reference: Optional[str] = None
    reporting_period: Optional[str] = None
    mapping_confidence: float = 1.0

# Universal Corporate Concepts
UNIVERSAL_INCOME_STATEMENT_CONCEPTS = [
    "operating_revenue",
    "other_operating_income",
    "total_revenue",
    "cost_of_goods_sold",
    "gross_profit",
    "employee_benefit_expense",
    "other_operating_expenses",
    "total_operating_expenses",
    "ebitda",
    "depreciation_amortisation",
    "ebit",
    "finance_cost",
    "other_income",
    "profit_before_tax",
    "income_tax",
    "net_income"
]

UNIVERSAL_BALANCE_SHEET_CONCEPTS = [
    # Assets
    "cash_and_equivalents",
    "short_term_investments",
    "trade_receivables",
    "inventory",
    "other_current_assets",
    "total_current_assets",
    "property_plant_equipment",
    "right_of_use_assets",
    "capital_work_in_progress",
    "goodwill",
    "intangible_assets",
    "non_current_investments",
    "other_non_current_assets",
    "total_assets",
    # Liabilities & Equity
    "trade_payables",
    "short_term_borrowings",
    "lease_liabilities_current",
    "other_current_liabilities",
    "total_current_liabilities",
    "long_term_borrowings",
    "financial_debt",
    "lease_liabilities_non_current",
    "total_non_current_liabilities",
    "total_liabilities",
    "share_capital",
    "reserves_and_surplus",
    "shareholders_equity",
    "minority_interest",
    "total_equity_and_liabilities"
]

UNIVERSAL_CASH_FLOW_CONCEPTS = [
    "cash_flow_operations",
    "change_in_working_capital",
    "tax_paid",
    "capital_expenditure",
    "cash_flow_investing",
    "net_borrowing",
    "dividends_paid",
    "finance_cost_paid",
    "cash_flow_financing",
    "net_change_in_cash",
    "opening_cash_balance",
    "closing_cash_balance"
]

# Specialized Banking Concepts
BANKING_CONCEPTS = [
    "interest_earned",
    "interest_expended",
    "net_interest_income",
    "other_operating_income",
    "operating_expenses",
    "operating_profit_before_provisions",
    "provisions_and_contingencies",
    "profit_before_tax",
    "net_profit",
    # Balance Sheet
    "customer_deposits",
    "casa_deposits",
    "term_deposits",
    "gross_advances",
    "net_advances",
    "investments_slr",
    "borrowings",
    "capital_adequacy_ratio",
    "gross_npa",
    "net_npa",
    "gross_npa_ratio",
    "net_npa_ratio",
    "provision_coverage_ratio"
]

# Specialized NBFC Concepts
NBFC_CONCEPTS = [
    "revenue_from_operations",
    "finance_costs",
    "net_interest_income",
    "impairment_on_financial_instruments",
    "operating_expenses",
    "profit_before_tax",
    "profit_after_tax",
    "assets_under_management",
    "loan_assets",
    "borrowings_nbfc",
    "stage_3_assets_ratio",
    "capital_adequacy_ratio_nbfc"
]

# Specialized Life Insurance Concepts
INSURANCE_CONCEPTS = [
    "gross_written_premium",
    "net_premium_earned",
    "investment_income",
    "claims_and_benefits_paid",
    "commission_expenses",
    "operating_expenses_insurance",
    "change_in_mathematical_reserves",
    "profit_after_tax",
    "embedded_value",
    "value_of_new_business",
    "vnb_margin",
    "solvency_ratio",
    "13th_month_persistency_ratio",
    "61st_month_persistency_ratio"
]

# Specialized REIT Concepts
REIT_CONCEPTS = [
    "gross_rental_revenue",
    "property_operating_expenses",
    "net_operating_income",
    "ndcf_spv_level",
    "ndcf_reit_level",
    "distribution_per_unit",
    "portfolio_occupancy_pct",
    "weighted_average_lease_expiry_years",
    "gross_asset_value",
    "net_debt_reit",
    "capitalization_rate"
]

class UniversalAccountingDictionary:
    """
    Standard registry and validator for universal and sector-specific financial metrics.
    """

    @classmethod
    def get_all_concepts_for_sector(cls, sector: str) -> List[str]:
        sector_upper = sector.upper()
        if "BANK" in sector_upper:
            return UNIVERSAL_INCOME_STATEMENT_CONCEPTS + UNIVERSAL_BALANCE_SHEET_CONCEPTS + BANKING_CONCEPTS
        elif "NBFC" in sector_upper or "FINANCE" in sector_upper:
            return UNIVERSAL_INCOME_STATEMENT_CONCEPTS + UNIVERSAL_BALANCE_SHEET_CONCEPTS + NBFC_CONCEPTS
        elif "INSURANCE" in sector_upper:
            return UNIVERSAL_INCOME_STATEMENT_CONCEPTS + UNIVERSAL_BALANCE_SHEET_CONCEPTS + INSURANCE_CONCEPTS
        elif "REIT" in sector_upper or "REAL ESTATE" in sector_upper:
            return UNIVERSAL_INCOME_STATEMENT_CONCEPTS + UNIVERSAL_BALANCE_SHEET_CONCEPTS + REIT_CONCEPTS
        else:
            return UNIVERSAL_INCOME_STATEMENT_CONCEPTS + UNIVERSAL_BALANCE_SHEET_CONCEPTS + UNIVERSAL_CASH_FLOW_CONCEPTS

    @classmethod
    def validate_concept(cls, concept_name: str) -> bool:
        all_concepts = set(
            UNIVERSAL_INCOME_STATEMENT_CONCEPTS +
            UNIVERSAL_BALANCE_SHEET_CONCEPTS +
            UNIVERSAL_CASH_FLOW_CONCEPTS +
            BANKING_CONCEPTS +
            NBFC_CONCEPTS +
            INSURANCE_CONCEPTS +
            REIT_CONCEPTS
        )
        return concept_name in all_concepts
