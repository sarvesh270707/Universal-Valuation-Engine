import pytest
import os
import openpyxl
from backend.engine.reporting.report_generator import ReportGeneratorEngine

def test_excel_model_generation():
    out_path = "output/test_generated_model.xlsx"
    forecast_data = {
        "forecast_periods": ["FY27E", "FY28E", "FY29E"],
        "statements": {
            "FY27E": {"operating_revenue": 58000.0, "ebitda": 6200.0, "ebit": 5300.0, "net_income": 3900.0, "ufcf": 3500.0, "total_assets": 50000.0, "total_liabilities_and_equity": 50000.0, "balance_sheet_difference": 0.0},
            "FY28E": {"operating_revenue": 66000.0, "ebitda": 7100.0, "ebit": 6100.0, "net_income": 4500.0, "ufcf": 4100.0, "total_assets": 58000.0, "total_liabilities_and_equity": 58000.0, "balance_sheet_difference": 0.0},
            "FY29E": {"operating_revenue": 75000.0, "ebitda": 8200.0, "ebit": 7000.0, "net_income": 5200.0, "ufcf": 4800.0, "total_assets": 67000.0, "total_liabilities_and_equity": 67000.0, "balance_sheet_difference": 0.0}
        }
    }
    valuation_data = {
        "valuation_result": {
            "exit_multiple_method": {"exit_multiple": 35.0, "terminal_value": 287000.0, "enterprise_value": 290000.0, "intrinsic_value_per_share": 3257.67},
            "gordon_growth_method": {"terminal_growth_rate": 0.055, "terminal_value": 85000.0, "enterprise_value": 60000.0, "intrinsic_value_per_share": 368.40}
        }
    }

    res_path = ReportGeneratorEngine.generate_excel_model(
        ticker="TITAN",
        company_name="Titan Company Limited",
        sector="RETAIL_JEWELLERY",
        forecast_data=forecast_data,
        valuation_data=valuation_data,
        output_path=out_path
    )

    assert os.path.exists(res_path)
    wb = openpyxl.load_workbook(res_path, data_only=False)
    assert "Valuation_Summary" in wb.sheetnames
    assert "Financial_Projections" in wb.sheetnames
    ws_val = wb["Valuation_Summary"]
    # Check that live Excel formulas are preserved
    assert ws_val["B9"].value == "=B7-B8"
    assert ws_val["B11"].value == "=B9/B10"
    wb.close()

def test_markdown_report_generation():
    out_path = "output/test_research_report.md"
    valuation_data = {
        "valuation_result": {
            "exit_multiple_method": {"intrinsic_value_per_share": 3257.67},
            "gordon_growth_method": {"intrinsic_value_per_share": 368.40}
        },
        "cost_of_capital": {"wacc": 0.1443}
    }

    res_path = ReportGeneratorEngine.generate_markdown_report(
        ticker="TITAN",
        company_name="Titan Company Limited",
        sector="RETAIL_JEWELLERY",
        valuation_data=valuation_data,
        output_path=out_path
    )

    assert os.path.exists(res_path)
    with open(res_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "INSTITUTIONAL EQUITY VALUATION & RESEARCH REPORT" in content
    assert "₹3257.67" in content
