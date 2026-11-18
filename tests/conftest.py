import pytest
import os
import openpyxl

@pytest.fixture(scope="session")
def titan_model_path():
    path = os.path.abspath("Finance_FP&A_Portfolio/Project_01_Titan_Three_Statement_DCF/model/Titan_3Statement_DCF_Model.xlsx")
    assert os.path.exists(path), f"Titan model file not found at {path}"
    return path

@pytest.fixture(scope="session")
def titan_workbook(titan_model_path):
    wb = openpyxl.load_workbook(titan_model_path, data_only=True)
    return wb
