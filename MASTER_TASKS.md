# MASTER TASKS & STAGE EXIT CRITERIA TRACKER

**System**: Universal Multi-Company Financial Valuation & DCF Engine  
**Execution Standard**: 100% Executable Code, Zero Fabricated Data, Strict Accounting Fidelity  

---

## Stage-by-Stage Tasks & Exit Criteria

### Stage 1: Architecture and Environment
- [x] Inspect hardware, operating system, and software runtimes.
- [x] Verify Python 3.12, Node.js 24, Git, Excel COM availability.
- [x] Define multi-layer architectural design and module separation.
- [x] Establish data models, entity relationships, and API specifications.
- [ ] Document contracts and complete Stage 1 exit criteria.

### Stage 2: Project Scaffolding and Database
- [ ] Initialize backend structure (`backend/app`).
- [ ] Implement SQLAlchemy 2.0 database engine with connection pooling.
- [ ] Define 15 core database entities (companies, securities, financial_facts, etc.).
- [ ] Implement database initialization and migration logic.
- [ ] Create FastAPI application with versioned routes (`/api/v1`) and health check endpoints.
- [ ] Verify database connectivity and CRUD transaction integrity.

### Stage 3: Core Financial Formula Engine
- [ ] Implement NOPAT, FCFF, FCFE, CAPM, WACC, Terminal Value, Enterprise Value, Equity Value.
- [ ] Build decimal-aware arithmetic safeguards and division-by-zero traps.
- [ ] Build singularity defense ($WACC \le g$).
- [ ] Write independent PyTest suite for all mathematical formulas with manually proven test cases.

### Stage 4: Universal Accounting Dictionary
- [ ] Define standardized line items across Income Statement, Balance Sheet, Cash Flow.
- [ ] Define specialized financial dictionaries for Banks, NBFCs, Insurance, REITs.
- [ ] Implement missing-value states (Zero, Missing, Not Applicable, Not Disclosed).
- [ ] Write tests verifying cross-statement linkage contracts.

### Stage 5: Financial Data Ingestion
- [ ] Implement XBRL/XML ingestion parser.
- [ ] Implement structured Excel/CSV statement parser.
- [ ] Implement PDF tabular statement extractor with fallback.
- [ ] Implement document metadata and source provenance tracking.

### Stage 6: Accounting Normalisation
- [ ] Build mapping rules from original company disclosures to universal dictionary.
- [ ] Implement sign normalization and unit scaling (₹ Cr, ₹ Lakhs, Millions).
- [ ] Implement Ind AS 116 lease accounting adjustments and restatement handling.

### Stage 7: Automated Company & Sector Classification
- [ ] Implement sector classification engine mapping NSE/BSE tickers to 21 industries.
- [ ] Support segment identification and conglomerate multi-business tagging.
- [ ] Implement manual analyst override functionality.

### Stage 8: Historical Financial Analysis
- [ ] Implement CAGR calculations (3-Yr, 5-Yr, 10-Yr).
- [ ] Implement financial ratio engine (Gross/EBITDA/Net Margins, ROE, ROIC, CCC).
- [ ] Implement specialized banking & insurance metrics (NIM, GNPA, VNB margin).

### Stage 9: Three-Statement Financial Modelling
- [ ] Implement dynamic forecast engine linking P&L, Balance Sheet, and Cash Flow.
- [ ] Implement working capital, PP&E, debt, and equity roll-forward schedules.
- [ ] Ensure natural balance sheet equilibrium with ₹0.00 plug deviation.

### Stage 10: Sector-Specific Forecasting Engines
- [ ] Build plugin-style sector registry.
- [ ] Implement dedicated forecast modules for all 21 sectors (FMCG, Retail, IT, Banks, NBFC, Insurance, REIT, Conglomerates, etc.).
- [ ] Verify benchmark implementations for the 7 primary business archetypes.

### Stage 11: Valuation Methodologies
- [ ] Implement Industrial FCFF DCF.
- [ ] Implement FCFE DCF.
- [ ] Implement Dividend Discount Model (DDM).
- [ ] Implement Residual Income Model (RIM).
- [ ] Implement Net Asset Value (NAV).
- [ ] Implement Sum of the Parts (SOTP).
- [ ] Implement Comparable Company Analysis (CCA).
- [ ] Implement Embedded Value (EV) & Value of New Business (VNB).

### Stage 12: Cost of Capital Engine
- [ ] Implement G-Sec risk-free rate lookup & ERP module.
- [ ] Implement Hamada equation for unlevered / relevered beta.
- [ ] Implement after-tax cost of debt and capital-weighted WACC.

### Stage 13: Scenario and Sensitivity Engine
- [ ] Implement Bear, Base, Bull scenario toggle.
- [ ] Generate dynamic 2D sensitivity matrices (WACC vs. Growth, Growth vs. Margin).

### Stage 14: Frontend and Workflow Integration
- [ ] Develop institutional financial web interface with Tailwind styling.
- [ ] Connect company search, financial tables, charts, assumptions, and valuation views.

### Stage 15: Reporting and Exports
- [ ] Implement structured Excel export preserving formulas.
- [ ] Implement executive PDF valuation report generator.

### Stage 16: Master QA and Regression Testing
- [ ] Run full automated test suite (Unit, Integration, Sector, Accounting, Stress).
- [ ] Fix all reproducible defects.

### Stage 17: Security, Performance and Deployment
- [ ] Perform security review, OWASP input sanitization, and performance profiling.
- [ ] Configure deployment scripts and verify production readiness.

### Stage 18: Final Acceptance and Documentation
- [ ] Produce complete 14-manual technical documentation suite.
- [ ] Sign off on universal equity valuation engine.
