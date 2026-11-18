# VALUATION METHODOLOGY & SECTOR APPROPRIATENESS GUIDE
## Institutional DCF, DDM, NAV, SOTP, and Comps

---

## 1. Valuation Method Selection Matrix

Not all corporate valuation methodologies apply universally. The engine enforces sector appropriateness:

```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│       VALUATION METHODOLOGY     │      APPLICABLE INDUSTRIES      │        INVALID INDUSTRIES       │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ FCFF DCF (Enterprise Value)     │ Manufacturing, Retail, IT, Auto,│ Commercial Banks, NBFCs, Life   │
│                                 │ Pharma, Telecom, FMCG, Metals   │ Insurers (Debt is not leverage) │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Dividend Discount Model (DDM)   │ Commercial Banks, Regulated     │ High-growth tech reinvesting    │
│                                 │ Utilities, Asset Managers       │ 100% of cash flows (0 dividends)│
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Net Asset Value (NAV)           │ Real Estate Investment Trusts   │ Asset-light IT consulting,      │
│                                 │ (REITs), Real Estate Developers │ Software-as-a-Service (SaaS)    │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Sum of the Parts (SOTP)         │ Diversified Conglomerates, Multi│ Single-segment pure-play        │
│                                 │ business Holding Companies      │ operating companies             │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ Embedded Value & VNB            │ Life Insurance Underwriters     │ Industrial manufacturing        │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

---

## 2. Defensive Methodology Enforcement

If an analyst attempts to run an inappropriate valuation method (e.g. executing an industrial FCFF DCF on a Commercial Bank), the engine throws a `ValuationMethodologyException`:

> *"Methodology Invalidation Gate: FCFF DCF is economically invalid for Commercial Banks because debt is raw material operating inventory (deposits/borrowings), not leverage capital. Use Dividend Discount Model (DDM) or Residual Income (RIM)."*
