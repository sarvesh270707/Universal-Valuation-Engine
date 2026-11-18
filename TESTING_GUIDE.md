# MASTER TESTING & QUALITY ASSURANCE GUIDE
## Universal Multi-Company Valuation & DCF Engine

---

## 1. Automated Test Execution

The automated regression suite is configured with `pytest` and runs across 44 verified test cases:

```bash
# Run all unit tests and integration tests
pytest tests/unit tests/integration -v

# Run with coverage report
pytest --cov=backend tests/
```

---

## 2. Granular Test Suites

1. **`tests/unit/test_core_financial_formulas.py`**:
   - Tests NOPAT, FCFF, FCFE, CAPM, WACC, and Equity Bridge.
   - Verifies division-by-zero defense and Gordon Growth singularity traps ($WACC \le g$).

2. **`tests/unit/test_accounting_dictionary.py`**:
   - Tests universal concept validation across Corporate, Banking, NBFC, Insurance, and REIT categories.

3. **`tests/unit/test_accounting_normaliser.py`**:
   - Tests regex pattern matching against real company disclosures and unit scaling.

4. **`tests/unit/test_sector_classifier.py`**:
   - Tests correct automated mapping of all 7 benchmark companies and manual overrides.

5. **`tests/unit/test_sector_modules.py`**:
   - Verifies registration of all 21 sectors in the `SectorRegistry`.

6. **`tests/unit/test_valuation_suite.py`**:
   - Tests FCFF DCF, DDM, NAV, SOTP, and the sector appropriateness defense gate.

7. **`tests/unit/test_sensitivity_engine.py`**:
   - Verifies 5x5 WACC vs. Multiple matrix strict monotonicity.

8. **`tests/integration/test_universal_api_e2e.py`**:
   - Tests end-to-end REST API pipeline from Company Search to Valuation.
