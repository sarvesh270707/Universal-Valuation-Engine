import pytest
import os
import pandas as pd
from pathlib import Path

SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "resources" / "sample_data" / "titan" / "data"

def test_historical_statements_presence():
    p_is = SAMPLE_DATA_DIR / "processed" / "income_statement_standardized.csv"
    p_bs = SAMPLE_DATA_DIR / "processed" / "balance_sheet_standardized.csv"
    p_cf = SAMPLE_DATA_DIR / "processed" / "cash_flow_historical.csv"
    assert p_is.exists(), f"Income statement standardized CSV must exist at {p_is}"
    assert p_bs.exists(), f"Balance sheet standardized CSV must exist at {p_bs}"
    assert p_cf.exists(), f"Cash flow historical CSV must exist at {p_cf}"

def test_source_register_coverage():
    p_sr = SAMPLE_DATA_DIR / "source_register" / "source_register.csv"
    assert p_sr.exists(), f"Source register must exist at {p_sr}"
    df = pd.read_csv(p_sr)
    assert len(df) >= 300, f"Source register must track at least 300 line items, got {len(df)}"

def test_historical_years_continuity():
    p_is = SAMPLE_DATA_DIR / "processed" / "income_statement_standardized.csv"
    df = pd.read_csv(p_is)
    expected_years = [f"FY{yy}" for yy in range(17, 27)]
    for y in expected_years:
        assert y in df.columns, f"Column {y} missing from historical income statement"

def test_standardized_balance_sheet_balance():
    p_bs = SAMPLE_DATA_DIR / "processed" / "balance_sheet_standardized.csv"
    df = pd.read_csv(p_bs)
    total_assets = df[df.iloc[:, 0].str.contains("Total Assets", case=False, na=False)]
    total_liab_eq = df[df.iloc[:, 0].str.contains("Total Equity and Liabilities|Total Liabilities and Equity", case=False, na=False)]
    assert not total_assets.empty, "Total Assets line item must exist in standardized BS"
    assert not total_liab_eq.empty, "Total Liabilities & Equity line item must exist in standardized BS"

def test_model_output_artifacts():
    model_path = SAMPLE_DATA_DIR.parent / "model" / "Titan_3Statement_DCF_Model.xlsx"
    assert model_path.exists(), f"Sample model Excel artifact must exist at {model_path}"
    assert model_path.stat().st_size > 50000, "Model workbook must be non-empty institutional artifact"
