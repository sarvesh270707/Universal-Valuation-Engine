# ACCOUNTING NORMALISATION & MAPPING GUIDE
## Standardizing Indian Disclosures (Ind AS & IFRS)

---

## 1. Line Item Standardization Framework

Disclosures across Indian annual reports and MCA filings feature substantial variance in nomenclature. The Universal Normaliser maps reporting variations to standardized dictionary identifiers:

| Standard Concept | Common Reported Variations (MCA / Ind AS) | Statement Type | Sign Multiplier |
| :--- | :--- | :--- | :--- |
| `operating_revenue` | Revenue from operations, Gross Turnover, Sales of Products, Net Sales | Income Statement | +1 |
| `cost_of_goods_sold` | Cost of materials consumed, Purchases of stock-in-trade, Changes in inventory | Income Statement | +1 |
| `employee_benefit_expense` | Employee benefits expense, Salaries and wages, Staff welfare | Income Statement | +1 |
| `other_operating_expenses` | Other expenses, Manufacturing expenses, Administrative overheads | Income Statement | +1 |
| `depreciation_amortisation`| Depreciation and amortisation expense, D&A | Income Statement | +1 |
| `finance_cost` | Finance costs, Interest expense, Bank charges | Income Statement | +1 |
| `property_plant_equipment`| Property, plant and equipment, Fixed assets (gross block / net block) | Balance Sheet | +1 |
| `right_of_use_assets` | Right-of-use assets, Ind AS 116 Lease assets | Balance Sheet | +1 |
| `financial_debt` | Borrowings (current + non-current), Working capital demand loans, GML | Balance Sheet | +1 |
| `cash_and_equivalents` | Cash and cash equivalents, Balances with banks, Liquid mutual funds | Balance Sheet | +1 |

---

## 2. Unit Scaling Conventions
Financial reports in India report in Lakhs, Crores, or Millions. The engine scales all metrics to standard **₹ Crore**:
- `CRORE` -> Multiplier: `1.0`
- `LAKH` -> Multiplier: `0.01` (1 Lakh = 0.01 Crore)
- `MILLION` -> Multiplier: `0.1` (10 Lakhs = 0.1 Crore)
- `ABSOLUTE` -> Multiplier: `0.0000001`
