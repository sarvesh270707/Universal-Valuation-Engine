# DATABASE SCHEMA & ENTITY ARCHITECTURE
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Relational Entity Inventory (15 Core Tables)

1. `companies`: Primary entity tracking legal name, common name, CIN, primary sector, and country.
2. `securities`: Ticker symbols, exchanges (NSE/BSE), ISIN, and shares outstanding.
3. `company_segments`: Operating business divisions (e.g. Jewellery vs. Watches).
4. `financial_periods`: Fiscal years (FY24, FY25), reporting types (Annual, Quarterly), and audit statuses.
5. `source_documents`: Filing archives, SHA-256 hashes, and document types (Annual Report, XBRL).
6. `financial_facts`: Line items mapped to the Universal Accounting Dictionary with unit scaling.
7. `mapping_rules`: Regular expressions and priorities mapping company labels to concepts.
8. `industry_profiles`: Sector metadata, default unlevered betas, and valuation rules.
9. `forecast_models`: Scenarios (Bear, Base, Bull) and forecast horizons.
10. `forecast_assumptions`: Parameter values (growth, margin, CapEx) per forecast year.
11. `valuation_models`: Methodology configurations (WACC, terminal growth, multiple).
12. `valuation_results`: Enterprise values, net debts, and per-share intrinsic targets.
13. `sensitivity_results`: 2D sensitivity matrix cell outputs.
14. `validation_results`: Automated balance sheet equality and reconciliation check records.
15. `audit_logs`: Immutable tracking of model modifications and overrides.

---

## 2. Integrity Constraints & Foreign Key Rules
- `companies.cin`: Unique index.
- `securities`: Unique constraint on `(ticker, exchange)`.
- `financial_periods`: Unique constraint on `(company_id, fiscal_year, period_type, period_scope)`.
- Foreign key cascade: Deleting a company cascades safely to securities, periods, facts, and models.
- SQLite Pragmas: Foreign keys strictly enforced via `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL;`.
