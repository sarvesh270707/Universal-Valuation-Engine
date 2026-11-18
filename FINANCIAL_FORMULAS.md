# INSTITUTIONAL FINANCIAL FORMULAS & MATHEMATICAL EQUATIONS
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Operating Profitability & Cash Flow Equations

### Net Operating Profit After Tax (NOPAT)
$$\text{NOPAT} = \text{EBIT} \times (1 - t)$$
*Where $t$ is the effective marginal corporate tax rate (25.17% standard).*

### Free Cash Flow to Firm (FCFF / Unlevered Free Cash Flow)
$$\text{FCFF} = \text{NOPAT} + \text{D&A} - \text{CapEx} - \Delta\text{Operating NWC}$$
*Where $\Delta\text{Operating NWC} = \Delta\text{Receivables} + \Delta\text{Inventory} - \Delta\text{Payables}$.*

### Free Cash Flow to Equity (FCFE)
$$\text{FCFE} = \text{Net Income} + \text{D&A} - \text{CapEx} - \Delta\text{Operating NWC} + \text{Net Borrowing}$$

---

## 2. Cost of Capital Equations

### Capital Asset Pricing Model (CAPM)
$$K_e = R_f + \beta_L \times \text{ERP}$$
*Where $R_f$ is the 10-Yr Indian G-Sec Yield (7.00%), $\beta_L$ is the levered equity beta, and $\text{ERP}$ is the Equity Risk Premium (7.00%).*

### Hamada Equation (Beta Unlevering & Relevering)
$$\beta_U = \frac{\beta_L}{1 + (1 - t) \times \left(\frac{D}{E}\right)}$$
$$\beta_L = \beta_U \times \left[1 + (1 - t) \times \left(\frac{D}{E}\right)\right]$$

### Weighted Average Cost of Capital (WACC)
$$\text{WACC} = \left(\frac{E}{V} \times K_e\right) + \left(\frac{D}{V} \times K_d \times (1 - t)\right)$$
*Where $V = E + D$, and $K_d$ is the pre-tax weighted borrowing cost.*

---

## 3. Valuation & Equity Bridge Equations

### Gordon Growth Terminal Value
$$\text{TV}_{\text{Gordon}} = \frac{\text{FCFF}_{n+1}}{\text{WACC} - g} = \frac{\text{FCFF}_n \times (1 + g)}{\text{WACC} - g}$$
*Singularity Guard: $\text{WACC} > g$ is strictly enforced; raises `FinancialFormulaException` if $\text{WACC} \le g$.*

### Exit Multiple Terminal Value
$$\text{TV}_{\text{Exit}} = \text{EBITDA}_n \times \text{Exit Multiple}$$

### Enterprise Value
$$\text{Enterprise Value} = \sum_{t=1}^n \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{Terminal Value}}{(1 + \text{WACC})^n}$$

### Equity Value & Intrinsic Price Per Share
$$\text{Equity Value} = \text{Enterprise Value} - \text{Total Debt} + \text{Cash & Equivalents} - \text{Minority Interest} + \text{Non-Operating Assets}$$
$$\text{Intrinsic Value Per Share} = \frac{\text{Equity Value}}{\text{Fully Diluted Shares Outstanding}}$$
