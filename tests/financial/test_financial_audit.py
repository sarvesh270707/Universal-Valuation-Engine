import pytest

def test_historical_audit_completeness(titan_workbook):
    ws_hist = titan_workbook['02_Historical_Data']
    # Check 10 historical years FY17 (col 3) to FY26 (col 12)
    for col in range(3, 13):
        year = ws_hist.cell(row=4, column=col).value
        rev = ws_hist.cell(row=6, column=col).value
        pat = ws_hist.cell(row=21, column=col).value
        assets = ws_hist.cell(row=38, column=col).value
        liab_eq = ws_hist.cell(row=30, column=col).value
        
        assert rev is not None and rev > 0, f"Missing revenue in {year}"
        assert pat is not None and pat > 0, f"Missing net income in {year}"
        assert assets is not None and assets > 0, f"Missing assets in {year}"
        assert round(assets - liab_eq, 2) == 0.0, f"Historical balance mismatch in {year}"

def test_dcf_ufcf_components(titan_workbook):
    ws_dcf = titan_workbook['13_DCF_Valuation']
    # FY27E to FY31E (cols C to G, indices 3 to 7)
    for col in range(3, 8):
        ebit = ws_dcf.cell(row=5, column=col).value or 0.0
        tax = ws_dcf.cell(row=6, column=col).value or 0.0
        nopat = ws_dcf.cell(row=7, column=col).value or 0.0
        depr = ws_dcf.cell(row=8, column=col).value or 0.0
        capex = ws_dcf.cell(row=9, column=col).value or 0.0
        delta_wc = ws_dcf.cell(row=10, column=col).value or 0.0
        ufcf = ws_dcf.cell(row=11, column=col).value or 0.0
        
        calc_nopat = ebit - tax
        assert round(calc_nopat - nopat, 2) == 0.0
        calc_ufcf = nopat + depr - capex - delta_wc
        assert round(calc_ufcf - ufcf, 2) == 0.0
