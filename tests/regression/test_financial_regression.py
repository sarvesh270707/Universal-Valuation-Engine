import pytest
import pandas as pd
from pathlib import Path

SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "resources" / "sample_data" / "titan" / "data"

def test_titan_valuation_regression(titan_workbook):
    ws_cover = titan_workbook['01_Cover']
    wacc = ws_cover.cell(row=16, column=3).value
    exit_price = ws_cover.cell(row=18, column=3).value
    gordon_price = ws_cover.cell(row=19, column=3).value
    
    assert round(wacc, 4) == 0.1443, f"WACC drifted from 14.43%: {wacc}"
    assert round(exit_price, 2) == 3257.67, f"Exit Multiple Price drifted from 3257.67: {exit_price}"
    assert round(gordon_price, 2) == 368.40, f"Gordon Growth Price drifted from 368.40: {gordon_price}"

def test_titan_historical_performance_regression():
    p_is = SAMPLE_DATA_DIR / "processed" / "income_statement_standardized.csv"
    assert p_is.exists(), f"Historical standardized income statement missing at {p_is}"
    df = pd.read_csv(p_is)
    row_rev = df[df.iloc[:, 0].str.contains("Total Revenue|Revenue from Operations", case=False, na=False)]
    assert not row_rev.empty
    val_fy26 = float(row_rev["FY26"].values[0])
    assert val_fy26 > 50000, f"FY26 Revenue should exceed 50,000 Cr, got {val_fy26}"
