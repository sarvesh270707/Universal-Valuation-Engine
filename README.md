# Universal Multi-Company Financial Valuation & DCF Engine
## 🛠️ Status: IN ACTIVE DEVELOPMENT — Multi-Function Financial Valuation Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](http://localhost:8000/docs)
[![Python 3.12](https://img.shields.io/badge/Python-3.12.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Sectors Supported](https://img.shields.io/badge/Sectors-21_Registered_Industries-635BFF?style=for-the-badge)](SECTOR_MODELLING_GUIDE.md)
[![Valuation Models](https://img.shields.io/badge/Valuation-Dual_DCF%20%7C%20DDM%20%7C%20NAV%20%7C%20SOTP-FF6F00?style=for-the-badge)](VALUATION_METHODOLOGY.md)
[![Regression Tests](https://img.shields.io/badge/Automated_QA-50%2F50_PASS_(100%25)-00C853?style=for-the-badge)](TEST_RESULTS.md)
[![Development Roadmap](https://img.shields.io/badge/Roadmap-Phase_2_In_Progress-orange?style=for-the-badge)](resources/ROADMAP.md)

An institutional-grade, multi-function financial engineering and quantitative equity valuation platform designed to dynamically model, forecast, and value companies across **21 distinct industry sectors**. 

Engineered with strict accounting fidelity (natural balance sheet roll-forward with ₹0.00 Cr deviation), sector-specific operational drivers, division-by-zero defense gates, dynamic 2D sensitivity matrices, an interactive institutional research portal (`/app`), and automated live-formula Excel export generation.

---

## 🌟 Platform Architectural Highlights

```mermaid
flowchart TD
    subgraph IngestionLayer["1. Ingestion & Normalisation"]
        Raw[Filing Data: CSV / XBRL / API] --> Ingest[Data Ingestion Engine]
        Ingest --> Dict[Universal Accounting Dictionary]
        Dict --> Norm[Ind AS Accounting Normaliser]
    end

    subgraph CoreLayer["2. Classification & Financial Analysis"]
        Norm --> Class[21-Sector Classifier & Override]
        Class --> Hist[Historical Ratio & CAGR Analyser]
        Hist --> ThreeStmt[Integrated 3-Statement Model<br/>(Assets = Liabilities + Equity)]
    end

    subgraph SectorLayer["3. Operational Forecasting & Valuation"]
        ThreeStmt --> Sectors[21 Sector Forecasting Modules]
        Sectors --> CostOfCap[Cost of Capital Engine (WACC / CAPM / Hamada)]
        CostOfCap --> ValSuite[Valuation Methodology Suite<br/>(FCFF / FCFE / DDM / RIM / NAV / SOTP)]
        ValSuite --> Gate{Methodology Invalidation Gate}
    end

    subgraph DeliveryLayer["4. Analytics, UI & Artifact Generation"]
        Gate --> Sens[5x5 Sensitivity & Scenario Engine]
        Sens --> WebUI[Interactive Web Research Portal (/app)]
        Sens --> API[FastAPI High-Performance REST Endpoints]
        Sens --> Excel[Live-Formula Excel Model Export (OpenPyXL)]
    end
```

---

## 🏛️ Benchmark Coverage & Methodological Gates

The engine enforces strict sector-specific valuation logic. For instance, **Industrial FCFF DCF is prohibited for commercial banks and NBFCs** because debt and deposits represent operating raw materials rather than capital leverage.

| Company Archetype | Ticker | Primary Sector | Implemented Valuation Framework | Target / Key Output | Methodology Guard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Titan Company Ltd.** | `TITAN` | `RETAIL_JEWELLERY` | **FCFF DCF (Dual Terminal)** | Exit Multiple: **₹3,257.67** / Gordon: **₹368.40** | High working capital intensity |
| **Tata Consultancy Services** | `TCS` | `IT_SERVICES` | **FCFF DCF & Exit Multiple** | 88% FCF conversion, 24.5% EBIT margin | Negative net debt, asset-light |
| **HDFC Bank Limited** | `HDFCBANK` | `BANKING` | **Dividend Discount Model (DDM)** | 14.70% Ke Discount Rate | **WACC Blocked** (Debt is inventory) |
| **Bajaj Finance Limited** | `BAJFINANCE`| `NBFC` | **Residual Income Model (RIM)** | Spread-based net interest income & credit costs | Equity capital adequacy focus |
| **SBI Life Insurance** | `SBILIFE` | `LIFE_INSURANCE` | **Embedded Value (EV) & VNB** | APE growth, 28% VNB margin, persistency | Solvency II / Ind AS 117 aligned |
| **Brookfield India REIT** | `BIRET` | `REIT` | **Net Asset Value (NAV) & NDCF** | 8.0% Capitalization Rate, Grade-A Office Parks | Cap rate capitalization |
| **Reliance Industries Ltd.**| `RELIANCE` | `CONGLOMERATE` | **Sum of the Parts (SOTP)** | O2C (6.5x), Retail (28x), Jio (18x) | 15% Conglomerate HoldCo discount |

---

## 📚 Technical Documentation & Developer Resources

Complete engineering specifications, mathematical proofs, and development logs:

- [📘 Development Roadmap](resources/ROADMAP.md) — Multi-phase milestones (Phase 1 Complete, Phase 2 Active Development).
- [📊 21-Sector Taxonomy Specification](resources/sector_taxonomy.json) — Comprehensive JSON schema defining drivers and valuation models.
- [🏛️ System Architecture](ARCHITECTURE.md) — 18-stage modular microservice design and data flow.
- [📐 Financial Formulas & Mathematical Proofs](FINANCIAL_FORMULAS.md) — NOPAT, UFCF, WACC, Hamada beta un-levering, and Gordon Growth singularity proofs.
- [🔌 API Specification](API_DOCUMENTATION.md) — FastAPI interactive endpoints, request schemas, and responses.
- [🗄️ Database Schema](DATABASE_SCHEMA.md) — 15 relational entities for financial facts, audit logs, and valuation runs.
- [🏭 Sector Modelling Guide](SECTOR_MODELLING_GUIDE.md) — Implementation guide across all 21 industry sectors.
- [⚖️ Valuation Methodology Guide](VALUATION_METHODOLOGY.md) — Dual terminal DCF, DDM, NAV, and SOTP methodologies.
- [🧪 Testing & QA Guide](TESTING_GUIDE.md) — Regression testing, accounting integrity assertions, and audit rules.

---

## 🚀 Quickstart & Server Launch

### 1. Launch the Engine & Web Portal
```bash
# Install core dependencies
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy scipy python-multipart httpx openpyxl pandas numpy

# Start the production server
python run_server.py
```
- **Interactive Web Portal**: [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app)
- **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Diagnostic**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 2. Run the Full Automated QA Suite
```bash
python -m pytest tests/unit tests/integration -v
```
*(All 50 tests pass with 100% coverage across accounting reconciliations, formula accuracy, and API endpoints).*
