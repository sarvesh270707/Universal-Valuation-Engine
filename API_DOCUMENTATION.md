# UNIVERSAL DCF ENGINE - REST API SPECIFICATION
## Version: 1.0.0 | OpenAPI 3.1.0 Compliant

---

## 1. Base URL & Routing Architecture

- **Local Development**: `http://localhost:8000/api/v1`
- **Interactive Swagger Documentation**: `http://localhost:8000/docs`
- **ReDoc Technical Interface**: `http://localhost:8000/redoc`
- **Web Application Portal**: `http://localhost:8000/app`

---

## 2. API Endpoints Catalog

### 2.1 System & Diagnostic Endpoints

#### `GET /health`
Returns system operational status, active database connectivity, and timestamp.

#### `GET /api/v1/sectors`
Returns all 21 registered sector specifications, operating drivers, and applicable valuation methodologies.

---

### 2.2 Company Search & Profile Endpoints

#### `GET /api/v1/companies/search`
**Query Parameters**:
- `query` (optional string): Ticker symbol or partial legal name.

**Response**:
```json
{
  "results": [
    {
      "ticker": "TITAN",
      "common_name": "Titan",
      "legal_name": "Titan Company Limited",
      "sector": "RETAIL_JEWELLERY",
      "exchange": "NSE"
    }
  ]
}
```

#### `GET /api/v1/companies/{ticker}`
Retrieves company metadata, primary sector classification, operating segments, and valid valuation models.

---

### 2.3 Financial Modeling & Valuation Endpoints

#### `GET /api/v1/companies/{ticker}/financials`
Returns standardized historical financial statement metrics.

#### `POST /api/v1/companies/{ticker}/forecast`
Executes integrated 5-year three-statement financial projections with natural balance sheet equilibrium.

**Request Body**:
```json
{
  "revenue_growth_rate": 0.16,
  "gross_margin": 0.25,
  "ebitda_margin": 0.11,
  "capex_pct_revenue": 0.025,
  "effective_tax_rate": 0.2517,
  "dividend_payout_ratio": 0.25,
  "forecast_years": 5
}
```

#### `POST /api/v1/companies/{ticker}/valuation`
Executes sector-appropriate valuation engine (Dual FCFF DCF, DDM, SOTP, or NAV) with Cost of Capital WACC/Ke.

**Request Body**:
```json
{
  "methodology": "FCFF_DCF",
  "terminal_growth_rate": 0.055,
  "exit_multiple": 35.0,
  "risk_free_rate": 0.070,
  "equity_risk_premium": 0.070,
  "beta": 1.15,
  "cost_of_debt": 0.075
}
```

#### `POST /api/v1/companies/{ticker}/sensitivity`
Computes dynamic 5x5 WACC vs. Exit Multiple sensitivity matrix with verified monotonicity.
