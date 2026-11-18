import pytest
import os
from backend.engine.ingestion.data_ingestion import DataIngestionEngine
from backend.engine.dictionary.accounting_dict import StatementType

def test_unit_detection():
    u1, m1 = DataIngestionEngine.detect_units("All figures are stated in INR Crores unless specified")
    assert u1 == "CRORE"
    assert m1 == 1.0

    u2, m2 = DataIngestionEngine.detect_units("Standalone results in Lakhs (INR)")
    assert u2 == "LAKH"
    assert m2 == 0.01

    u3, m3 = DataIngestionEngine.detect_units("Consolidated balance sheet in Millions")
    assert u3 == "MILLION"
    assert m3 == 0.1

def test_csv_ingestion_with_real_filing():
    csv_path = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/income_statement_standardized.csv"
    assert os.path.exists(csv_path), "Target CSV must exist"

    result = DataIngestionEngine.ingest_csv_statement(
        file_path=csv_path,
        statement_type=StatementType.INCOME_STATEMENT
    )

    assert result["total_facts_extracted"] > 50
    assert len(result["sha256"]) == 64
    assert "FY26" in result["periods_detected"]
    assert any(f["raw_label"] in ["Total Revenue", "Revenue from Operations"] for f in result["facts"])

def test_xbrl_xml_ingestion():
    sample_xbrl = """<?xml version="1.0" encoding="UTF-8"?>
    <xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:in-gaap="http://www.icai.org/xbrl/in-gaap">
        <in-gaap:RevenueFromOperations contextRef="FY2025" unitRef="INR" decimals="-7">510800000000</in-gaap:RevenueFromOperations>
        <in-gaap:ProfitBeforeTax contextRef="FY2025" unitRef="INR" decimals="-7">46720000000</in-gaap:ProfitBeforeTax>
        <in-gaap:NetProfit contextRef="FY2025" unitRef="INR" decimals="-7">34960000000</in-gaap:NetProfit>
    </xbrli:xbrl>
    """
    res = DataIngestionEngine.ingest_xbrl_instance(sample_xbrl)
    assert res["total_facts"] == 3
    assert res["facts"][0]["concept"] == "RevenueFromOperations"
    assert res["facts"][0]["numeric_value"] == 510800000000.0
    assert res["facts"][2]["numeric_value"] == 34960000000.0
