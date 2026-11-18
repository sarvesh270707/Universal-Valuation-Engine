# SYSTEM ARCHITECTURE & INTEGRATION SPECIFICATION
## Universal Multi-Company Financial Valuation & DCF Engine

---

## 1. System Architectural Overview

The Universal Valuation Engine is designed as a decoupled, modular, enterprise-grade financial engineering platform:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND CLIENT LAYER                           │
│  Next.js / React / TypeScript / Tailwind CSS Institutional Portal       │
│  - Financial Statement Tables   - Interactive Scenario Toggles         │
│  - 2D Sensitivity Heatmaps      - Real-time Valuation Bridges          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST / JSON (HTTP/2)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND API LAYER (FastAPI)                     │
│  - Versioned Endpoints (/api/v1) - Pydantic Validation & Serialization │
│  - Dependency Injection         - CORS & Security Middleware           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴────────────────────────────────┐
    │                                                                │
    ▼                                                                ▼
┌─────────────────────────────────────────┐  ┌─────────────────────────────────────────┐
│       FINANCIAL ENGINEERING ENGINE      │  │        DATA INGESTION & PIPELINE        │
│  - Core Formula Engine (NOPAT, WACC)    │  │  - XBRL/XML Parser                      │
│  - Universal Accounting Dictionary      │  │  - PDF Tabular Extractor                │
│  - 21 Sector-Specific Modules (Registry)│  │  - CSV / Excel Importers                │
│  - Dual-DCF, DDM, NAV, SOTP, Comps      │  │  - Provenance & Metadata Tracker        │
│  - Dynamic Three-Statement Forecaster   │  │  - Accounting Normaliser & Ind AS 116   │
└───────────────────┬─────────────────────┘  └────────────────────┬────────────────────┘
                    │                                             │
                    └──────────────────────┬──────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA PERSISTENCE LAYER                          │
│  SQLAlchemy 2.0 ORM with 15 Relational Entities                        │
│  - SQLite (ACID Local Embedded Engine) / PostgreSQL (Cloud Production)  │
│  - Companies, Securities, Facts, Assumptions, Models, Valuations       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Entity Relationship Architecture (15 Core Entities)

```mermaid
erDiagram
    COMPANIES ||--o{ SECURITIES : "issues"
    COMPANIES ||--o{ COMPANY_SEGMENTS : "operates"
    COMPANIES ||--o{ FINANCIAL_PERIODS : "reports"
    COMPANIES ||--o{ SOURCE_DOCUMENTS : "files"
    COMPANIES ||--o{ FORECAST_MODELS : "has"
    COMPANIES ||--o{ VALUATION_MODELS : "values"

    FINANCIAL_PERIODS ||--o{ FINANCIAL_FACTS : "contains"
    SOURCE_DOCUMENTS ||--o{ FINANCIAL_FACTS : "proves"
    
    FORECAST_MODELS ||--o{ FORECAST_ASSUMPTIONS : "defines"
    FORECAST_MODELS ||--o{ VALUATION_MODELS : "feeds"

    VALUATION_MODELS ||--o{ VALUATION_RESULTS : "outputs"
    VALUATION_MODELS ||--o{ SENSITIVITY_RESULTS : "generates"
    VALUATION_MODELS ||--o{ VALIDATION_RESULTS : "validates"

    COMPANIES {
        string id PK
        string cin UK
        string legal_name
        string common_name
        string primary_sector
        string country
    }

    SECURITIES {
        string id PK
        string company_id FK
        string ticker
        string exchange
        string isin
    }

    FINANCIAL_PERIODS {
        string id PK
        string company_id FK
        string fiscal_year
        string period_type
        date start_date
        date end_date
        boolean is_audited
    }

    FINANCIAL_FACTS {
        string id PK
        string period_id FK
        string source_doc_id FK
        string standard_concept
        string raw_label
        decimal numeric_value
        string currency
        string unit_scale
        string restatement_status
    }
```

---

## 3. Universal Module Interfaces

Every sector-specific valuation engine implements a strict interface contract (`ISectorEngine`):

```python
class ISectorEngine(ABC):
    @abstractmethod
    def get_operating_drivers(self) -> List[DriverDefinition]:
        """Returns standard operational drivers for the sector."""
        pass

    @abstractmethod
    def forecast_statements(self, historicals: FinancialDataset, assumptions: ScenarioAssumptions) -> ForecastOutput:
        """Projects integrated 5-year financial statements."""
        pass

    @abstractmethod
    def select_valuation_methodologies(self) -> List[ValuationMethod]:
        """Returns ordered list of applicable valuation techniques."""
        pass

    @abstractmethod
    def compute_valuation(self, forecast: ForecastOutput, wacc: CostOfCapital) -> ValuationOutput:
        """Executes sector-appropriate valuation (e.g. DDM for Banks, SOTP for Holding Co)."""
        pass
```

This ensures zero coupling between the API layer and the individual mathematical models.
