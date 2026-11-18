# SECTOR MODELLING & 21-INDUSTRY SPECIFICATION GUIDE
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Supported Sector Taxonomy (21 Dedicated Modules)

The engine implements a plugin-style registry (`SectorRegistry`) supporting 21 specialized corporate and financial architectures:

| # | Sector Identifier | Business Model Archetype | Primary Operating Drivers | Primary Valuation |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `RETAIL_JEWELLERY` | Consumer Lifestyle (Titan) | SSSG, Store additions, Gold lease rate, DIO | **FCFF DCF** |
| **02** | `IT_SERVICES` | Tech Consulting (TCS) | Headcount, Billing rate, Attrition, Utilization | **FCFF DCF** |
| **03** | `BANKING` | Scheduled Commercial Banks (HDFC Bank) | Loan growth, NIM, CASA ratio, Credit cost | **DDM** |
| **04** | `NBFC` | Retail Lending (Bajaj Finance) | AUM growth, Spread, Cost of funds, Stage 3 | **Residual Income** |
| **05** | `LIFE_INSURANCE` | Life Insurance (SBI Life) | APE growth, VNB margin, 13M persistency | **Embedded Value** |
| **06** | `REIT` | Commercial Real Estate (Brookfield) | Occupancy, Rental escalation, WALE, Cap rate | **NAV / NDCF** |
| **07** | `CONGLOMERATE` | Multi-Industry Holdings (Reliance) | Segmental EBITDA, Holding company discount | **SOTP** |
| **08** | `FMCG` | Packaged Consumer Goods (HUL) | Volume growth, Realization, A&P spend | **FCFF DCF** |
| **09** | `OIL_AND_GAS` | Refining & Exploration (ONGC, IOC) | GRM ($/bbl), Crude benchmark, Lifting cost | **FCFF DCF** |
| **10** | `AUTOMOTIVE` | Auto OEMs (Tata Motors, M&M) | Volume dispatch, Realization/vehicle, Raw materials | **FCFF DCF** |
| **11** | `PHARMACEUTICALS` | Formulations & API (Sun Pharma) | US generic price erosion, Domestic chronic mix | **FCFF DCF** |
| **12** | `INFRASTRUCTURE` | EPC & Construction (L&T) | Order book-to-bill, Execution cycle, NWC days | **FCFF DCF** |
| **13** | `GENERAL_INSURANCE`| Non-Life (ICICI Lombard) | Combined ratio, Loss ratio, Underwriting profit | **P/B Comps** |
| **14** | `TELECOM` | Wireless Carriers (Bharti Airtel) | ARPU, Churn rate, Data volume, 5G CapEx | **FCFF DCF** |
| **15** | `METALS_AND_MINING`| Steel & Aluminium (Tata Steel, Hindalco)| LME spot prices, Coking coal, EBITDA/tonne | **FCFF DCF** |
| **16** | `POWER_AND_UTILITIES`| Generation & Grid (NTPC, PowerGrid) | Plant Load Factor (PLF), Regulated ROE (15.5%) | **DDM / DCF** |
| **17** | `CEMENT` | Building Materials (UltraTech) | Despatches (MT), EBITDA/tonne, Freight cost | **FCFF DCF** |
| **18** | `CHEMICALS` | Specialty Chemicals (Aarti, Deepak) | Feedstock spread, Export volume, ROCE | **FCFF DCF** |
| **19** | `HOSPITALS` | Healthcare Providers (Apollo) | ARPPB, Bed occupancy %, ALOS (days) | **FCFF DCF** |
| **20** | `REAL_ESTATE` | Developers (DLF, Godrej Properties) | Pre-sales booking, Collections, Pipeline | **NAV** |
| **21** | `ASSET_MANAGEMENT` | Mutual Funds (HDFC AMC) | Equity AUM mix, TER yield, Monthly SIP inflow | **P/AUM Comps** |
