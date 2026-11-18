from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, 
    Text, UniqueConstraint, Index, Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

# 1. Companies
class Company(Base):
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    cin = Column(String(21), unique=True, index=True, nullable=True) # Corporate Identification Number
    legal_name = Column(String(255), nullable=False)
    common_name = Column(String(255), index=True, nullable=False)
    primary_sector = Column(String(100), index=True, nullable=False)
    sub_industry = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    securities = relationship("Security", back_populates="company", cascade="all, delete-orphan")
    segments = relationship("CompanySegment", back_populates="company", cascade="all, delete-orphan")
    periods = relationship("FinancialPeriod", back_populates="company", cascade="all, delete-orphan")
    source_documents = relationship("SourceDocument", back_populates="company", cascade="all, delete-orphan")
    forecast_models = relationship("ForecastModel", back_populates="company", cascade="all, delete-orphan")
    valuation_models = relationship("ValuationModel", back_populates="company", cascade="all, delete-orphan")


# 2. Securities
class Security(Base):
    __tablename__ = "securities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    ticker = Column(String(20), index=True, nullable=False)
    exchange = Column(String(20), index=True, nullable=False) # NSE, BSE
    isin = Column(String(12), unique=True, index=True, nullable=True)
    currency = Column(String(10), default="INR")
    shares_outstanding = Column(Float, nullable=True) # in Crores or units
    current_market_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="securities")

    __table_args__ = (
        UniqueConstraint("ticker", "exchange", name="uq_ticker_exchange"),
    )


# 3. Company Segments
class CompanySegment(Base):
    __tablename__ = "company_segments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    segment_name = Column(String(150), nullable=False)
    industry_type = Column(String(100), nullable=True)
    revenue_contribution_pct = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="segments")


# 4. Financial Periods
class FinancialPeriod(Base):
    __tablename__ = "financial_periods"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year = Column(String(10), nullable=False, index=True) # e.g. FY24, FY25
    period_type = Column(String(20), default="ANNUAL") # ANNUAL, Q1, Q2, Q3, Q4, TTM
    period_scope = Column(String(20), default="CONSOLIDATED") # CONSOLIDATED, STANDALONE
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_audited = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="periods")
    facts = relationship("FinancialFact", back_populates="period", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "fiscal_year", "period_type", "period_scope", name="uq_company_period"),
    )


# 5. Source Documents
class SourceDocument(Base):
    __tablename__ = "source_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    document_title = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False) # ANNUAL_REPORT, XBRL_INSTANCE, PRESS_RELEASE, INVESTOR_PRESENTATION
    filing_date = Column(DateTime, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_hash_sha256 = Column(String(64), nullable=True)
    extracted_metadata = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="source_documents")
    facts = relationship("FinancialFact", back_populates="source_document")


# 6. Financial Facts (Standardised Universal Line Items)
class FinancialFact(Base):
    __tablename__ = "financial_facts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    period_id = Column(String(36), ForeignKey("financial_periods.id", ondelete="CASCADE"), nullable=False, index=True)
    source_doc_id = Column(String(36), ForeignKey("source_documents.id", ondelete="SET NULL"), nullable=True, index=True)
    
    statement_type = Column(String(30), nullable=False) # INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW
    standard_concept = Column(String(100), nullable=False, index=True) # Universal Dictionary ID
    raw_label = Column(String(255), nullable=True) # As reported by company
    numeric_value = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    unit_scale = Column(String(20), default="CRORE") # CRORE, LAKH, ABSOLUTE
    
    mapping_confidence = Column(Float, default=1.0) # 0.0 to 1.0
    verification_status = Column(String(30), default="VERIFIED") # VERIFIED, PENDING_REVIEW, MANUALLY_OVERRIDDEN
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    period = relationship("FinancialPeriod", back_populates="facts")
    source_document = relationship("SourceDocument", back_populates="facts")

    __table_args__ = (
        Index("ix_fact_period_concept", "period_id", "standard_concept"),
    )


# 7. Mapping Rules
class MappingRule(Base):
    __tablename__ = "mapping_rules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sector = Column(String(100), index=True, nullable=True)
    raw_pattern = Column(String(255), nullable=False, index=True)
    standard_concept = Column(String(100), nullable=False, index=True)
    statement_type = Column(String(30), nullable=False)
    sign_multiplier = Column(Integer, default=1) # 1 or -1
    priority = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)


# 8. Industry Profiles
class IndustryProfile(Base):
    __tablename__ = "industry_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    sector_name = Column(String(100), unique=True, index=True, nullable=False)
    standard_valuation_methods = Column(Text, nullable=False) # JSON list: ["FCFF_DCF", "EXIT_MULTIPLE"]
    default_unlevered_beta = Column(Float, nullable=True)
    default_operating_metrics = Column(Text, nullable=True) # JSON list
    created_at = Column(DateTime, default=datetime.utcnow)


# 9. Forecast Models
class ForecastModel(Base):
    __tablename__ = "forecast_models"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    model_name = Column(String(150), nullable=False)
    scenario_type = Column(String(20), default="BASE") # BEAR, BASE, BULL
    forecast_horizon_years = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="forecast_models")
    assumptions = relationship("ForecastAssumption", back_populates="forecast_model", cascade="all, delete-orphan")
    valuation_models = relationship("ValuationModel", back_populates="forecast_model", cascade="all, delete-orphan")


# 10. Forecast Assumptions
class ForecastAssumption(Base):
    __tablename__ = "forecast_assumptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    forecast_model_id = Column(String(36), ForeignKey("forecast_models.id", ondelete="CASCADE"), nullable=False, index=True)
    parameter_name = Column(String(100), nullable=False) # e.g. revenue_growth_rate, ebitda_margin
    forecast_year = Column(String(10), nullable=False) # FY27E, FY28E...
    parameter_value = Column(Float, nullable=False)
    unit = Column(String(20), default="PERCENT") # PERCENT, DAYS, CRORE
    rationale = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    forecast_model = relationship("ForecastModel", back_populates="assumptions")


# 11. Valuation Models
class ValuationModel(Base):
    __tablename__ = "valuation_models"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    forecast_model_id = Column(String(36), ForeignKey("forecast_models.id", ondelete="CASCADE"), nullable=False, index=True)
    methodology = Column(String(50), nullable=False) # FCFF_DCF, FCFE_DCF, DDM, SOTP, NAV, COMPS
    risk_free_rate = Column(Float, nullable=False)
    equity_risk_premium = Column(Float, nullable=False)
    beta = Column(Float, nullable=False)
    cost_of_equity = Column(Float, nullable=False)
    cost_of_debt = Column(Float, nullable=True)
    tax_rate = Column(Float, nullable=False)
    wacc = Column(Float, nullable=False)
    terminal_growth_rate = Column(Float, nullable=True)
    exit_multiple = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="valuation_models")
    forecast_model = relationship("ForecastModel", back_populates="valuation_models")
    results = relationship("ValuationResult", back_populates="valuation_model", cascade="all, delete-orphan")
    sensitivities = relationship("SensitivityResult", back_populates="valuation_model", cascade="all, delete-orphan")


# 12. Valuation Results
class ValuationResult(Base):
    __tablename__ = "valuation_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    valuation_model_id = Column(String(36), ForeignKey("valuation_models.id", ondelete="CASCADE"), nullable=False, index=True)
    enterprise_value = Column(Float, nullable=True)
    net_debt = Column(Float, nullable=True)
    equity_value = Column(Float, nullable=False)
    shares_outstanding = Column(Float, nullable=False)
    intrinsic_value_per_share = Column(Float, nullable=False)
    current_market_price = Column(Float, nullable=True)
    upside_downside_pct = Column(Float, nullable=True)
    valuation_timestamp = Column(DateTime, default=datetime.utcnow)

    valuation_model = relationship("ValuationModel", back_populates="results")


# 13. Sensitivity Results
class SensitivityResult(Base):
    __tablename__ = "sensitivity_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    valuation_model_id = Column(String(36), ForeignKey("valuation_models.id", ondelete="CASCADE"), nullable=False, index=True)
    row_variable = Column(String(50), nullable=False) # e.g. WACC
    row_value = Column(Float, nullable=False)
    col_variable = Column(String(50), nullable=False) # e.g. Terminal Growth or Multiple
    col_value = Column(Float, nullable=False)
    calculated_share_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    valuation_model = relationship("ValuationModel", back_populates="sensitivities")

    __table_args__ = (
        Index("ix_sens_model_grid", "valuation_model_id", "row_value", "col_value"),
    )


# 14. Validation Results
class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    target_id = Column(String(36), index=True, nullable=False) # Period ID or Model ID
    target_type = Column(String(50), nullable=False) # FINANCIAL_PERIOD, FORECAST_MODEL, VALUATION_MODEL
    rule_name = Column(String(100), nullable=False) # e.g. BALANCE_SHEET_EQUALITY, CASH_RECONCILIATION
    is_valid = Column(Boolean, nullable=False)
    discrepancy_value = Column(Float, default=0.0)
    details = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow)


# 15. Audit Logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_name = Column(String(100), nullable=False, index=True)
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(50), nullable=False) # CREATE, UPDATE, DELETE, OVERRIDE
    changed_by = Column(String(100), default="SYSTEM_ENGINE")
    previous_state = Column(Text, nullable=True) # JSON
    new_state = Column(Text, nullable=True) # JSON
    timestamp = Column(DateTime, default=datetime.utcnow)
