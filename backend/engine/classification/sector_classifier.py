"""
Universal Financial Valuation & DCF Engine - Sector Classification Module
Maps Indian listed companies (NSE/BSE) to 21 institutional sector models
with multi-segment detection and manual override support.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel

class SectorType(str, Enum):
    FMCG = "FMCG"
    RETAIL_JEWELLERY = "RETAIL_JEWELLERY"
    IT_SERVICES = "IT_SERVICES"
    OIL_AND_GAS = "OIL_AND_GAS"
    AUTOMOTIVE = "AUTOMOTIVE"
    PHARMACEUTICALS = "PHARMACEUTICALS"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    BANKING = "BANKING"
    NBFC = "NBFC"
    LIFE_INSURANCE = "LIFE_INSURANCE"
    GENERAL_INSURANCE = "GENERAL_INSURANCE"
    REIT = "REIT"
    TELECOM = "TELECOM"
    METALS_AND_MINING = "METALS_AND_MINING"
    POWER_AND_UTILITIES = "POWER_AND_UTILITIES"
    CEMENT = "CEMENT"
    CHEMICALS = "CHEMICALS"
    HOSPITALS = "HOSPITALS"
    REAL_ESTATE = "REAL_ESTATE"
    ASSET_MANAGEMENT = "ASSET_MANAGEMENT"
    CONGLOMERATE = "CONGLOMERATE"

class CompanyProfile(BaseModel):
    ticker: str
    exchange: str
    legal_name: str
    common_name: str
    primary_sector: SectorType
    segments: List[str] = []
    applicable_valuation_models: List[str]
    classification_confidence: float = 1.0
    manual_override: bool = False

# Benchmark Universe Taxonomy Directory
BENCHMARK_COMPANIES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "TITAN": {
        "ticker": "TITAN",
        "exchange": "NSE",
        "legal_name": "Titan Company Limited",
        "common_name": "Titan",
        "primary_sector": SectorType.RETAIL_JEWELLERY,
        "segments": ["Jewellery (Tanishq, Mia, Zoya)", "Watches & Wearables", "EyeCare", "Fragrances & Fashion Accessories"],
        "applicable_valuation_models": ["FCFF_DCF", "EXIT_MULTIPLE", "COMPS"],
        "classification_confidence": 1.0
    },
    "TCS": {
        "ticker": "TCS",
        "exchange": "NSE",
        "legal_name": "Tata Consultancy Services Limited",
        "common_name": "TCS",
        "primary_sector": SectorType.IT_SERVICES,
        "segments": ["BFSI", "Retail & CPG", "Communication & Media", "Manufacturing", "Life Sciences & Healthcare"],
        "applicable_valuation_models": ["FCFF_DCF", "EXIT_MULTIPLE", "FCFE_DCF"],
        "classification_confidence": 1.0
    },
    "HDFCBANK": {
        "ticker": "HDFCBANK",
        "exchange": "NSE",
        "legal_name": "HDFC Bank Limited",
        "common_name": "HDFC Bank",
        "primary_sector": SectorType.BANKING,
        "segments": ["Treasury", "Retail Banking", "Wholesale Banking", "Other Banking Operations"],
        "applicable_valuation_models": ["DDM", "RESIDUAL_INCOME", "PB_COMPS"],
        "classification_confidence": 1.0
    },
    "BAJFINANCE": {
        "ticker": "BAJFINANCE",
        "exchange": "NSE",
        "legal_name": "Bajaj Finance Limited",
        "common_name": "Bajaj Finance",
        "primary_sector": SectorType.NBFC,
        "segments": ["Consumer Lending", "SME Lending", "Commercial Lending", "Rural Lending"],
        "applicable_valuation_models": ["RESIDUAL_INCOME", "DDM", "PB_COMPS"],
        "classification_confidence": 1.0
    },
    "SBILIFE": {
        "ticker": "SBILIFE",
        "exchange": "NSE",
        "legal_name": "SBI Life Insurance Company Limited",
        "common_name": "SBI Life",
        "primary_sector": SectorType.LIFE_INSURANCE,
        "segments": ["Participating Life", "Non-Participating Life", "Unit Linked (ULIP)", "Annuity & Pension"],
        "applicable_valuation_models": ["EMBEDDED_VALUE", "VALUE_OF_NEW_BUSINESS", "P_EV_COMPS"],
        "classification_confidence": 1.0
    },
    "BIRET": {
        "ticker": "BIRET",
        "exchange": "NSE",
        "legal_name": "Brookfield India Real Estate Trust",
        "common_name": "Brookfield REIT",
        "primary_sector": SectorType.REIT,
        "segments": ["Commercial Grade-A Office Parks", "Hospitality & Ancillary Retail"],
        "applicable_valuation_models": ["NAV", "NDCF_DCF", "CAP_RATE_CAPITALIZATION"],
        "classification_confidence": 1.0
    },
    "RELIANCE": {
        "ticker": "RELIANCE",
        "exchange": "NSE",
        "legal_name": "Reliance Industries Limited",
        "common_name": "Reliance",
        "primary_sector": SectorType.CONGLOMERATE,
        "segments": ["Oil to Chemicals (O2C)", "Oil and Gas Exploration", "Retail (Reliance Retail)", "Digital Services (Jio Platforms)"],
        "applicable_valuation_models": ["SOTP", "FCFF_DCF", "NAV"],
        "classification_confidence": 1.0
    }
}

class SectorClassifier:
    """
    Automated company and industry classification engine.
    """

    def __init__(self, manual_overrides: Optional[Dict[str, SectorType]] = None):
        self.manual_overrides = manual_overrides or {}

    def classify_company(self, ticker: str, exchange: str = "NSE", description: str = "") -> CompanyProfile:
        ticker_clean = ticker.upper().strip()

        # Check manual analyst overrides first
        if ticker_clean in self.manual_overrides:
            override_sector = self.manual_overrides[ticker_clean]
            return CompanyProfile(
                ticker=ticker_clean,
                exchange=exchange,
                legal_name=f"{ticker_clean} (Overridden)",
                common_name=ticker_clean,
                primary_sector=override_sector,
                applicable_valuation_models=self._get_default_models(override_sector),
                classification_confidence=1.0,
                manual_override=True
            )

        # Check benchmark registry
        if ticker_clean in BENCHMARK_COMPANIES_REGISTRY:
            data = BENCHMARK_COMPANIES_REGISTRY[ticker_clean]
            return CompanyProfile(**data)

        # Keyword heuristics fallback
        desc_lower = description.lower()
        detected_sector = SectorType.CONGLOMERATE
        confidence = 0.6

        if any(w in desc_lower for w in ["bank", "deposits", "advances", "npa"]):
            detected_sector = SectorType.BANKING
            confidence = 0.85
        elif any(w in desc_lower for w in ["software", "technology", "consulting", "cloud"]):
            detected_sector = SectorType.IT_SERVICES
            confidence = 0.85
        elif any(w in desc_lower for w in ["reit", "real estate trust", "office park"]):
            detected_sector = SectorType.REIT
            confidence = 0.90
        elif any(w in desc_lower for w in ["insurance", "premium", "policyholder"]):
            detected_sector = SectorType.LIFE_INSURANCE
            confidence = 0.85
        elif any(w in desc_lower for w in ["lending", "nbfc", "microfinance"]):
            detected_sector = SectorType.NBFC
            confidence = 0.85
        elif any(w in desc_lower for w in ["jewellery", "watches", "retail"]):
            detected_sector = SectorType.RETAIL_JEWELLERY
            confidence = 0.85

        return CompanyProfile(
            ticker=ticker_clean,
            exchange=exchange,
            legal_name=ticker_clean,
            common_name=ticker_clean,
            primary_sector=detected_sector,
            applicable_valuation_models=self._get_default_models(detected_sector),
            classification_confidence=confidence,
            manual_override=False
        )

    def _get_default_models(self, sector: SectorType) -> List[str]:
        if sector == SectorType.BANKING:
            return ["DDM", "RESIDUAL_INCOME", "PB_COMPS"]
        elif sector == SectorType.NBFC:
            return ["RESIDUAL_INCOME", "DDM", "PB_COMPS"]
        elif sector == SectorType.LIFE_INSURANCE:
            return ["EMBEDDED_VALUE", "VALUE_OF_NEW_BUSINESS", "P_EV_COMPS"]
        elif sector == SectorType.REIT:
            return ["NAV", "NDCF_DCF", "CAP_RATE_CAPITALIZATION"]
        elif sector == SectorType.CONGLOMERATE:
            return ["SOTP", "FCFF_DCF", "NAV"]
        else:
            return ["FCFF_DCF", "EXIT_MULTIPLE", "FCFE_DCF"]
