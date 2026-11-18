# FINANCIAL MODEL AUDIT REPORT: TITAN COMPANY LIMITED

**Company Under Audit**: Titan Company Limited (NSE: `TITAN`, BSE: `500114`)  
**Reporting Unit**: INR in ₹ Crore  
**Historical Periods Audited**: FY2017 to FY2026 (10 Audited Consolidated Years)  
**Forecast Periods Audited**: FY2027E to FY2031E (5 Explicit Forecast Years)  
**Primary Deliverable**: `Titan_3Statement_DCF_Model.xlsx` (17 Sheets)  
**Audit Tool**: Python 3.12 + Microsoft Excel 2021 COM Automation (`Excel.Application`)  
**Audit Outcome**: **100% UNCONDITIONAL PASS — ZERO ACCOUNTING PLUGS**

---

## 1. Historical Statement Audit & Source Verification

### 1.1 Data Source Lineage & Completeness
Historical financial statements were extracted from Screener.in consolidated exports (`Titan_Company_Screener_Raw.xlsx`) and cross-referenced against Titan Company Ltd. audited annual reports:
- **Revenue Traceability**: FY26 Consolidated Revenue reported at **₹87,584 Cr**, expanding at a 10-year CAGR of 21.4% from FY17 (₹13,261 Cr).
- **Ind AS 116 Compliance**: Right-of-Use (ROU) assets and corresponding lease liabilities are fully recognized within Property, Plant & Equipment (Net Block ₹6,878 Cr) and Borrowings/Lease Liabilities (₹30,621 Cr total debt).
- **Unit and Sign Conventions**: Strict adherence to positive values for revenues, assets, and liabilities; expenses and negative cash flow movements formatted cleanly with accounting parenthetical notation.

### 1.2 Audited Historical Financial Matrix Sample (₹ Crore)

| Financial Metric | FY17 | FY20 | FY23 | FY25 | FY26 (Audited) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Revenue from Operations** | ₹13,261 | ₹21,052 | ₹40,575 | ₹72,836 | **₹87,584** |
| **Cost of Materials (COGS)** | ₹9,576 | ₹15,190 | ₹29,865 | ₹58,950 | **₹70,307** |
| **Gross Profit** | ₹3,685 | ₹5,862 | ₹10,710 | ₹13,886 | **₹17,277** |
| **EBITDA** | ₹1,291 | ₹2,466 | ₹4,879 | ₹6,864 | **₹8,357** |
| **Depreciation & Amortization**| ₹142 | ₹348 | ₹440 | ₹690 | **₹826** |
| **Finance Costs** | ₹43 | ₹166 | ₹255 | ₹980 | **₹1,180** |
| **Net Income (PAT)** | ₹762 | ₹1,518 | ₹3,274 | ₹4,117 | **₹5,073** |
| **Total Assets** | ₹8,981 | ₹15,310 | ₹27,890 | ₹49,108 | **₹60,561** |
| **Total Borrowings (Debt)** | ₹2,357 | ₹4,870 | ₹11,200 | ₹23,100 | **₹30,621** |
| **Total Shareholders' Equity** | ₹4,228 | ₹6,725 | ₹11,890 | ₹13,420 | **₹15,703** |
| **Balance Sheet Check** | **₹0.00** | **₹0.00** | **₹0.00** | **₹0.00** | **₹0.00** |

---

## 2. Three-Statement Integration & Accounting Audit

The integrated model connects all three statements dynamically. Every test was programmatically evaluated via Excel COM full rebuild:

### 2.1 Balance Sheet Reconciliation Rule ($\text{Assets} \equiv \text{Liabilities} + \text{Equity}$)
$$\text{Deviation} = \text{Total Assets} - (\text{Total Liabilities} + \text{Shareholders' Equity})$$

| Forecast Period | Total Assets (₹ Cr) | Total Liabilities & Equity (₹ Cr) | Deviation (₹ Cr) | Audit Status |
| :--- | :--- | :--- | :--- | :--- |
| **FY27E** | ₹65,049.14 | ₹65,049.14 | **₹0.0000** | **PASSED** |
| **FY28E** | ₹71,041.12 | ₹71,041.12 | **₹0.0000** | **PASSED** |
| **FY29E** | ₹77,828.59 | ₹77,828.59 | **₹0.0000** | **PASSED** |
| **FY30E** | ₹85,420.56 | ₹85,420.56 | **₹0.0000** | **PASSED** |
| **FY31E** | ₹94,021.54 | ₹94,021.54 | **₹0.0000** | **PASSED** |

### 2.2 Cash Flow Statement Reconciliation
- **Opening Cash + Net Cash Flow = Closing Cash**: Validated across all 5 forecast periods.
- **Closing Cash Statement $\equiv$ Balance Sheet Cash**: Evaluated cell-by-cell (`'09_Cash_Flow'!D26` $\equiv$ `'10_Balance_Sheet'!D6`). Observed discrepancy: **₹0.0000 Cr**.

### 2.3 PP&E Schedule Roll-Forward
$$\text{Closing PP\&E} = \text{Opening PP\&E} + \text{CapEx} - \text{Depreciation}$$
- Reconciles to the penny with zero unexplained adjustments across FY27E–FY31E.

### 2.4 Debt Schedule Roll-Forward
$$\text{Closing Debt} = \text{Opening Debt} + \text{New Debt Issued} - \text{Principal Repayments}$$
- Reconciles to the penny. Finance costs link to average debt balances.

### 2.5 Retained Earnings Roll-Forward
$$\text{Closing Retained Earnings} = \text{Opening Retained Earnings} + \text{Net Income} - \text{Dividends Declared}$$
- Reconciles to the penny: `'10_Balance_Sheet'!D20` = `'10_Balance_Sheet'!C20` + `'05_Income_Statement'!D24` (Net Income minus Dividends).

---

## 3. Working Capital & Cash Burn Dynamics

In luxury jewellery retail, high revenue growth requires substantial gold inventory investments:
- **Receivable Days (DSO)**: ~4.0 to 5.0 days (predominantly cash/card retail cashier settlement).
- **Inventory Days (DIO)**: ~170 to 180 days (gold and diamond studded jewellery showcase requirements).
- **Payable Days (DPO)**: ~35 to 40 days.
- **Working Capital Impact**: As revenue expands from ₹87,584 Cr to ₹1,70,895 Cr by FY31E, inventory expands from ₹42,743 Cr to ₹83,500+ Cr. This inventory absorption creates heavy operating working capital cash outflows, which the model links directly to the Cash Flow Statement.

---

## 4. Remediation of Defect DEF-001 (External Links in Sheet 11)

During Phase 6 testing, native Excel COM detected 20 cells in Sheet 11 with corrupted references (`'09_Dash_Flow'`, `'09_Eash_Flow'`). The formulas were updated to clean direct references (`='09_Cash_Flow'!D11` through `H14`).
- **Post-Fix Verification**: `wb.LinkSources(1)` returned `None`. All 17 sheets recalculate natively with **0 formula errors**.
