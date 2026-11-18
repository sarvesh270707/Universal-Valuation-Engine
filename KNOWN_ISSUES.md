# KNOWN ISSUES & TECHNICAL DEBT REGISTER

**System**: Universal Multi-Company Financial Valuation & DCF Engine  
**Last Updated**: November 17, 2026  

---

## Active Issues Register

| Issue ID | Severity | Stage Identified | Description | Current Status / Workaround | Target Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISSUE-001** | Low | Stage 1 | Native PostgreSQL CLI (`psql`) is not installed on the system PATH. | SQLite embedded engine configured as primary local driver via SQLAlchemy; PostgreSQL connection strings fully supported for remote/cloud deployment. | Stage 2 |
| **ISSUE-002** | Medium | Stage 1 | System memory has ~900 MB free under active workloads. | Enforce lightweight batching and aggressive memory deallocation in data ingestion pipelines. | Stage 5 |
