import pytest
import os
from pathlib import Path
import openpyxl

REPO_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture(scope="session")
def titan_model_path():
    candidate_paths = [
        REPO_ROOT / "resources" / "sample_data" / "titan" / "model" / "Titan_3Statement_DCF_Model.xlsx",
        REPO_ROOT / "Finance_FP&A_Portfolio" / "Project_01_Titan_Three_Statement_DCF" / "model" / "Titan_3Statement_DCF_Model.xlsx",
        Path("C:/Users/DELL/Desktop/DCF-Valuation-Model/Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/model/Titan_3Statement_DCF_Model.xlsx")
    ]
    for p in candidate_paths:
        if p.exists():
            return str(p)
    raise FileNotFoundError("Titan model file not found in any expected location.")

@pytest.fixture(scope="session")
def titan_workbook(titan_model_path):
    wb = openpyxl.load_workbook(titan_model_path, data_only=True)
    return wb
