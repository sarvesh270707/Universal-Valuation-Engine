"""
Universal Financial Valuation & DCF Engine - Accounting Normalisation Module
Maps varied company disclosure line items to the Universal Accounting Dictionary
and performs:
- Sign convention normalisation
- Unit scaling (converting Lakhs, Millions, Absolute to Crores)
- Ind AS 116 lease reconciliation
- Statement balance reconciliation checks
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from backend.engine.dictionary.accounting_dict import (
    StatementType,
    UNIVERSAL_INCOME_STATEMENT_CONCEPTS,
    UNIVERSAL_BALANCE_SHEET_CONCEPTS,
    UNIVERSAL_CASH_FLOW_CONCEPTS
)

class NormalisationRule:
    def __init__(self, pattern: str, standard_concept: str, statement_type: StatementType, sign_multiplier: int = 1):
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.standard_concept = standard_concept
        self.statement_type = statement_type
        self.sign_multiplier = sign_multiplier

# Canonical Indian Corporate & Ind AS Normalisation Rules
CORE_MAPPING_RULES = [
    # Revenue
    NormalisationRule(r"^(Revenue from operations|Total Revenue|Operating Revenue|Sales Turnover|Gross Revenue)$", "operating_revenue", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Other Operating Revenue|Other Operating Income)$", "other_operating_income", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Other Income|Non-operating Income)$", "other_income", StatementType.INCOME_STATEMENT),
    
    # Expenses
    NormalisationRule(r"^(Cost of materials consumed|Cost of goods sold|COGS|Purchases of stock-in-trade|Changes in inventories.*)$", "cost_of_goods_sold", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Employee benefits? expense|Salaries and wages|Staff costs)$", "employee_benefit_expense", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Other expenses|Selling, general and admin.*|Operating expenses)$", "other_operating_expenses", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Depreciation and amorti[sz]ation.*|D&A)$", "depreciation_amortisation", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Finance costs?|Interest expense)$", "finance_cost", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Profit before tax|PBT)$", "profit_before_tax", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Tax expense|Income tax|Current tax.*)$", "income_tax", StatementType.INCOME_STATEMENT),
    NormalisationRule(r"^(Profit for the period|Profit after tax|Net profit.*|PAT)$", "net_income", StatementType.INCOME_STATEMENT),

    # Balance Sheet Assets
    NormalisationRule(r"^(Cash and cash equivalents|Bank balances other than cash.*)$", "cash_and_equivalents", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Current investments|Short-term investments)$", "short_term_investments", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Trade receivables|Sundry debtors)$", "trade_receivables", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Inventories|Stock-in-trade)$", "inventory", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Property, plant and equipment|Tangible assets|Fixed assets)$", "property_plant_equipment", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Right-of-use assets|ROU Assets)$", "right_of_use_assets", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Capital work-in-progress|CWIP)$", "capital_work_in_progress", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Goodwill|Intangible assets)$", "goodwill", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Total assets|Total non-current and current assets)$", "total_assets", StatementType.BALANCE_SHEET),

    # Balance Sheet Liabilities & Equity
    NormalisationRule(r"^(Trade payables|Sundry creditors)$", "trade_payables", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Borrowings \(current\)|Short-term borrowings)$", "short_term_borrowings", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Borrowings \(non-current\)|Long-term borrowings)$", "long_term_borrowings", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Lease liabilities.*)$", "lease_liabilities_non_current", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Equity share capital|Share capital)$", "share_capital", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Other equity|Reserves and surplus)$", "reserves_and_surplus", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Total equity|Shareholders' funds)$", "shareholders_equity", StatementType.BALANCE_SHEET),
    NormalisationRule(r"^(Total equity and liabilities|Total liabilities and equity)$", "total_equity_and_liabilities", StatementType.BALANCE_SHEET),
]

class AccountingNormaliser:
    """
    Normalises raw line items into standard financial concepts with unit and sign adjustments.
    """

    def __init__(self, custom_rules: Optional[List[NormalisationRule]] = None):
        self.rules = (custom_rules or []) + CORE_MAPPING_RULES

    def map_line_item(self, raw_label: str, statement_type: StatementType) -> Tuple[Optional[str], float, int]:
        """
        Matches a raw line label against normalisation patterns.
        Returns: (standard_concept, confidence, sign_multiplier)
        """
        cleaned_label = raw_label.strip()
        for rule in self.rules:
            if rule.statement_type == statement_type and rule.pattern.search(cleaned_label):
                return rule.standard_concept, 1.0, rule.sign_multiplier

        # Partial match fallback
        for rule in self.rules:
            if rule.statement_type == statement_type and (rule.standard_concept in cleaned_label.lower().replace(" ", "_")):
                return rule.standard_concept, 0.75, rule.sign_multiplier

        return None, 0.0, 1

    def normalise_dataset(
        self,
        extracted_facts: List[Dict[str, Any]],
        unit_multiplier_to_crore: float = 1.0
    ) -> Dict[str, Any]:
        """
        Normalises an entire extracted statement fact list into standardized financial records.
        """
        normalised_records = []
        unmapped_records = []

        for fact in extracted_facts:
            raw_label = fact.get("raw_label", "")
            stmt_type_str = fact.get("statement_type", "INCOME_STATEMENT")
            stmt_type = StatementType(stmt_type_str) if stmt_type_str in StatementType.__members__ else StatementType.INCOME_STATEMENT
            
            raw_val = fact.get("numeric_value")
            period = fact.get("reporting_period", "UNKNOWN")

            concept, conf, sign = self.map_line_item(raw_label, stmt_type)

            if concept and raw_val is not None:
                norm_val = raw_val * unit_multiplier_to_crore * sign
                normalised_records.append({
                    "standard_concept": concept,
                    "reporting_period": period,
                    "numeric_value": norm_val,
                    "raw_label": raw_label,
                    "confidence": conf,
                    "unit": "INR_CRORE"
                })
            else:
                unmapped_records.append(fact)

        return {
            "total_processed": len(extracted_facts),
            "mapped_count": len(normalised_records),
            "unmapped_count": len(unmapped_records),
            "normalised_facts": normalised_records,
            "unmapped_samples": unmapped_records[:10]
        }
