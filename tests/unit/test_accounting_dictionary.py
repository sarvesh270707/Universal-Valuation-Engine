import pytest
from backend.engine.dictionary.accounting_dict import (
    UniversalAccountingDictionary,
    MissingValueState,
    StandardFinancialFact,
    StatementType
)

def test_universal_concepts_validation():
    assert UniversalAccountingDictionary.validate_concept("operating_revenue") is True
    assert UniversalAccountingDictionary.validate_concept("ebitda") is True
    assert UniversalAccountingDictionary.validate_concept("property_plant_equipment") is True
    assert UniversalAccountingDictionary.validate_concept("cash_flow_operations") is True
    assert UniversalAccountingDictionary.validate_concept("non_existent_fake_concept") is False

def test_sector_specific_concepts():
    # Banking
    assert UniversalAccountingDictionary.validate_concept("gross_npa") is True
    assert UniversalAccountingDictionary.validate_concept("net_interest_income") is True
    bank_concepts = UniversalAccountingDictionary.get_all_concepts_for_sector("BANKING")
    assert "gross_advances" in bank_concepts
    assert "casa_deposits" in bank_concepts

    # NBFC
    assert UniversalAccountingDictionary.validate_concept("assets_under_management") is True

    # Insurance
    assert UniversalAccountingDictionary.validate_concept("embedded_value") is True
    assert UniversalAccountingDictionary.validate_concept("value_of_new_business") is True

    # REIT
    assert UniversalAccountingDictionary.validate_concept("net_operating_income") is True
    assert UniversalAccountingDictionary.validate_concept("ndcf_reit_level") is True

def test_missing_value_states():
    fact = StandardFinancialFact(
        standard_concept="other_income",
        statement_type=StatementType.INCOME_STATEMENT,
        missing_state=MissingValueState.NOT_DISCLOSED,
        mapping_confidence=0.95
    )
    assert fact.missing_state == MissingValueState.NOT_DISCLOSED
    assert fact.numeric_value is None
    assert fact.currency == "INR"
