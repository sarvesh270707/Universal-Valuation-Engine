from backend.app.core.database import engine, Base
from backend.app.models.db_models import (
    Company, Security, CompanySegment, FinancialPeriod, SourceDocument,
    FinancialFact, MappingRule, IndustryProfile, ForecastModel,
    ForecastAssumption, ValuationModel, ValuationResult, SensitivityResult,
    ValidationResult, AuditLog
)

def init_db():
    """Initializes all 15 database tables and indexes."""
    print("Initializing Universal DCF Engine database schema...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    init_db()
