import pytest
import os
import pandas as pd

def test_historical_statements_presence():
    p_is = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/income_statement_standardized.csv"
    p_bs = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/balance_sheet_standardized.csv"
    p_cf = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/cash_flow_historical.csv"
    assert os.path.exists(p_is), "Income statement standardized CSV must exist"
    assert os.path.exists(p_bs), "Balance sheet standardized CSV must exist"
    assert os.path.exists(p_cf), "Cash flow historical CSV must exist"

def test_source_register_coverage():
    p_sr = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/source_register/source_register.csv"
    assert os.path.exists(p_sr), "Source register must exist"
    df = pd.read_csv(p_sr)
    assert len(df) >= 300, f"Source register must track at least 300 line items, got {len(df)}"

def test_historical_years_continuity():
    p_is = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/income_statement_standardized.csv"
    df = pd.read_csv(p_is)
    expected_years = [f"FY{yy}" for yy in range(17, 27)]
    for y in expected_years:
        assert y in df.columns, f"Column {y} missing from historical income statement"

def test_standardized_balance_sheet_balance():
    p_bs = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/data/processed/balance_sheet_standardized.csv"
    df = pd.read_csv(p_bs)
    total_assets = df[df.iloc[:, 0].str.contains("Total Assets", case=False, na=False)]
    total_liab_eq = df[df.iloc[:, 0].str.contains("Total Equity and Liabilities|Total Liabilities and Equity", case=False, na=False)]
    assert not total_assets.empty, "Total Assets line item must exist in standardized BS"
    assert not total_liab_eq.empty, "Total Liabilities & Equity line item must exist in standardized BS"

def test_model_output_artifacts():
    out_val = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/outputs/valuation_summary.csv"
    out_sens = "Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/outputs/sensitivity_matrix_exit_multiple.csv"
    assert os.path.exists(out_val), "Valuation summary CSV must exist"
    assert os.path.exists(out_sens), "Sensitivity matrix CSV must exist"
