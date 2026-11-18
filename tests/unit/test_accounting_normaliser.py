import pytest
from backend.engine.normalisation.accounting_normaliser import AccountingNormaliser
from backend.engine.dictionary.accounting_dict import StatementType

def test_line_item_mapping():
    norm = AccountingNormaliser()

    c1, conf1, s1 = norm.map_line_item("Revenue from operations", StatementType.INCOME_STATEMENT)
    assert c1 == "operating_revenue"
    assert conf1 == 1.0

    c2, conf2, s2 = norm.map_line_item("Property, plant and equipment", StatementType.BALANCE_SHEET)
    assert c2 == "property_plant_equipment"

    c3, conf3, s3 = norm.map_line_item("Employee benefits expense", StatementType.INCOME_STATEMENT)
    assert c3 == "employee_benefit_expense"

    c4, conf4, s4 = norm.map_line_item("Random Unknown Unrelated Header", StatementType.INCOME_STATEMENT)
    assert c4 is None
    assert conf4 == 0.0

def test_unit_and_sign_scaling():
    norm = AccountingNormaliser()
    raw_facts = [
        {"raw_label": "Revenue from operations", "numeric_value": 500000.0, "statement_type": "INCOME_STATEMENT", "reporting_period": "FY25"},
        {"raw_label": "Profit for the period", "numeric_value": 35000.0, "statement_type": "INCOME_STATEMENT", "reporting_period": "FY25"}
    ]

    # Suppose values were reported in Lakhs -> multiplier to Crore is 0.01
    res = norm.normalise_dataset(raw_facts, unit_multiplier_to_crore=0.01)
    assert res["mapped_count"] == 2
    assert res["normalised_facts"][0]["numeric_value"] == 5000.0 # 500,000 Lakhs = 5,000 Crores
    assert res["normalised_facts"][1]["numeric_value"] == 350.0  # 35,000 Lakhs = 350 Crores
