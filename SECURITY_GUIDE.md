# APPLICATION SECURITY & COMPLIANCE GUIDE
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Security Architecture & Controls

1. **SQL Injection Defense**: All database operations use SQLAlchemy ORM with strictly parameterized queries and bound variables. Zero raw SQL string concatenation.
2. **Defensive Financial Arithmetic**: Singularity guards on division operations and terminal value calculations prevent Denial of Service (DoS) from `ZeroDivisionError` or infinite loops.
3. **OWASP Input Validation**: All incoming REST payloads are validated via Pydantic v2 schemas with strict type and boundary constraints (e.g. tax rates must be within `0.0 <= t <= 1.0`).
4. **Secret Scanning**: 0 hardcoded credentials or API tokens across the entire codebase.
5. **Secure Headers**: Configured with CORS middleware and security headers preventing clickjacking and MIME-type sniffing.
