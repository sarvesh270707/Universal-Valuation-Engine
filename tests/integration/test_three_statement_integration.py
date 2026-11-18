import pytest
import openpyxl

def test_balance_sheet_equality(titan_workbook):
    ws_bs = titan_workbook['10_Balance_Sheet']
    # Forecast columns D to H (FY27E to FY31E)
    for col in range(4, 9):
        col_letter = openpyxl.utils.get_column_letter(col)
        period = ws_bs.cell(row=4, column=col).value
        assets = ws_bs.cell(row=13, column=col).value
        liab_eq = ws_bs.cell(row=22, column=col).value
        diff = round((assets or 0.0) - (liab_eq or 0.0), 2)
        assert diff == 0.0, f"Balance Sheet does not balance in {period} ({col_letter}): Diff = {diff}"

def test_cash_flow_closing_cash(titan_workbook):
    ws_bs = titan_workbook['10_Balance_Sheet']
    ws_cf = titan_workbook['09_Cash_Flow']
    for col in range(4, 9):
        period = ws_bs.cell(row=4, column=col).value
        bs_cash = ws_bs.cell(row=6, column=col).value
        cf_cash = ws_cf.cell(row=26, column=col).value
        diff = round((bs_cash or 0.0) - (cf_cash or 0.0), 2)
        assert diff == 0.0, f"Cash Flow Closing Cash mismatch in {period}: Diff = {diff}"

def test_ppe_roll_forward(titan_workbook):
    ws_ppe = titan_workbook['07_PP&E_Schedule']
    for col in range(4, 9):
        period = ws_ppe.cell(row=4, column=col).value
        opening = ws_ppe.cell(row=5, column=col).value or 0.0
        capex = ws_ppe.cell(row=6, column=col).value or 0.0
        depr = ws_ppe.cell(row=7, column=col).value or 0.0
        closing = ws_ppe.cell(row=9, column=col).value or 0.0
        calc_closing = opening + capex - depr
        diff = round(calc_closing - closing, 2)
        assert diff == 0.0, f"PP&E roll-forward mismatch in {period}: Diff = {diff}"

def test_debt_roll_forward(titan_workbook):
    ws_debt = titan_workbook['08_Debt_Schedule']
    for col in range(4, 9):
        period = ws_debt.cell(row=4, column=col).value
        opening = ws_debt.cell(row=5, column=col).value or 0.0
        borrow = ws_debt.cell(row=6, column=col).value or 0.0
        repay = ws_debt.cell(row=7, column=col).value or 0.0
        closing = ws_debt.cell(row=8, column=col).value or 0.0
        calc_closing = opening + borrow - repay
        diff = round(calc_closing - closing, 2)
        assert diff == 0.0, f"Debt roll-forward mismatch in {period}: Diff = {diff}"

def test_retained_earnings_roll_forward(titan_workbook):
    ws_bs = titan_workbook['10_Balance_Sheet']
    ws_is = titan_workbook['05_Income_Statement']
    for col in range(4, 9):
        period = ws_bs.cell(row=4, column=col).value
        opening = ws_bs.cell(row=20, column=col-1).value or 0.0
        re_addition = ws_is.cell(row=24, column=col).value or 0.0
        closing = ws_bs.cell(row=20, column=col).value or 0.0
        calc_closing = opening + re_addition
        diff = round(calc_closing - closing, 2)
        assert diff == 0.0, f"Retained Earnings roll-forward mismatch in {period}: Diff = {diff}"

def test_no_external_corruptions(titan_workbook):
    for s in titan_workbook.sheetnames:
        ws = titan_workbook[s]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                val = str(ws.cell(row=r, column=c).value or '')
                assert not ('ash_Flow' in val and '09_Cash_Flow' not in val), f"Corrupted formula in {s}!R{r}C{c}: {val}"
