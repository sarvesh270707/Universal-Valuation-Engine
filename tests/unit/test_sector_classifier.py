import pytest
from backend.engine.classification.sector_classifier import SectorClassifier, SectorType

def test_benchmark_companies_classification():
    classifier = SectorClassifier()

    # 1. Titan -> RETAIL_JEWELLERY
    titan = classifier.classify_company("TITAN")
    assert titan.primary_sector == SectorType.RETAIL_JEWELLERY
    assert "FCFF_DCF" in titan.applicable_valuation_models

    # 2. TCS -> IT_SERVICES
    tcs = classifier.classify_company("TCS")
    assert tcs.primary_sector == SectorType.IT_SERVICES

    # 3. HDFC Bank -> BANKING (must NOT select FCFF DCF!)
    hdfc = classifier.classify_company("HDFCBANK")
    assert hdfc.primary_sector == SectorType.BANKING
    assert "DDM" in hdfc.applicable_valuation_models
    assert "FCFF_DCF" not in hdfc.applicable_valuation_models

    # 4. Bajaj Finance -> NBFC
    bajaj = classifier.classify_company("BAJFINANCE")
    assert bajaj.primary_sector == SectorType.NBFC
    assert "RESIDUAL_INCOME" in bajaj.applicable_valuation_models

    # 5. SBI Life -> LIFE_INSURANCE
    sbi = classifier.classify_company("SBILIFE")
    assert sbi.primary_sector == SectorType.LIFE_INSURANCE
    assert "EMBEDDED_VALUE" in sbi.applicable_valuation_models

    # 6. Brookfield REIT -> REIT
    biret = classifier.classify_company("BIRET")
    assert biret.primary_sector == SectorType.REIT
    assert "NAV" in biret.applicable_valuation_models

    # 7. Reliance -> CONGLOMERATE (SOTP)
    ril = classifier.classify_company("RELIANCE")
    assert ril.primary_sector == SectorType.CONGLOMERATE
    assert "SOTP" in ril.applicable_valuation_models

def test_manual_override_functionality():
    classifier = SectorClassifier(manual_overrides={"RELIANCE": SectorType.OIL_AND_GAS})
    res = classifier.classify_company("RELIANCE")
    assert res.primary_sector == SectorType.OIL_AND_GAS
    assert res.manual_override is True
