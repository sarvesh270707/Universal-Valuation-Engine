"""
Universal Financial Valuation & DCF Engine - Sector Registry Module
Implements a plugin-style registry for all 21 sector-specific financial engines.
"""

from typing import Dict, Any, List, Type
from abc import ABC, abstractmethod
from pydantic import BaseModel
from backend.engine.classification.sector_classifier import SectorType

class SectorSpecification(BaseModel):
    sector_id: SectorType
    display_name: str
    operating_drivers: List[str]
    primary_valuation_method: str
    secondary_valuation_methods: List[str]
    balance_sheet_structure: str # INDUSTRIAL, BANKING_FINANCIAL, INSURANCE, REIT
    key_ratios: List[str]
    implementation_status: str = "PRODUCTION_READY" # PRODUCTION_READY or DOCUMENTED_SPEC

class BaseSectorForecaster(ABC):
    """Abstract base class for all sector forecasting modules."""
    
    @abstractmethod
    def get_specification(self) -> SectorSpecification:
        pass

    @abstractmethod
    def forecast(self, base_financials: Dict[str, float], custom_drivers: Dict[str, float]) -> Dict[str, Any]:
        pass

class SectorRegistry:
    """Plugin registry for sector-specific forecasting engines."""
    _registry: Dict[SectorType, BaseSectorForecaster] = {}

    @classmethod
    def register(cls, sector_type: SectorType):
        def decorator(forecaster_cls: Type[BaseSectorForecaster]):
            cls._registry[sector_type] = forecaster_cls()
            return forecaster_cls
        return decorator

    @classmethod
    def get(cls, sector_type: SectorType) -> BaseSectorForecaster:
        if sector_type not in cls._registry:
            raise KeyError(f"Sector forecaster for '{sector_type}' is not registered.")
        return cls._registry[sector_type]

    @classmethod
    def list_all_sectors(cls) -> List[SectorSpecification]:
        return [forecaster.get_specification() for forecaster in cls._registry.values()]
