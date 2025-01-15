from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from datetime import datetime
import logging
from .scraper import FinancialData

logger = logging.getLogger(__name__)

Base = declarative_base()

class FinancialRecord(Base):
    """SQLAlchemy model for financial data."""
    __tablename__ = 'financial_data'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String(50), nullable=False)

class DatabaseManager:
    def __init__(self, connection_string: str):
        """Initialize database connection."""
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()
        
    def _create_tables(self) -> None:
        """Create database tables if they don't exist."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created/verified")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise

    def save_record(self, data: FinancialData) -> None:
        """Save a single financial record to the database."""
        session = self.Session()
        try:
            record = FinancialRecord(
                symbol=data.symbol,
                price=data.price,
                volume=data.volume,
                timestamp=data.timestamp,
                source=data.source
            )
            session.add(record)
            session.commit()
            logger.info(f"Saved record for {data.symbol}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving record: {str(e)}")
            raise
        finally:
            session.close()

    def save_batch(self, data: list[FinancialData]) -> None:
        """Save multiple financial records to the database."""
        session = self.Session()
        try:
            records = [
                FinancialRecord(
                    symbol=d.symbol,
                    price=d.price,
                    volume=d.volume,
                    timestamp=d.timestamp,
                    source=d.source
                )
                for d in data
            ]
            session.bulk_save_objects(records)
            session.commit()
            logger.info(f"Saved {len(records)} records")
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving batch: {str(e)}")
            raise
        finally:
            session.close()

    def get_latest_records(self, symbol: Optional[str] = None) -> list[FinancialRecord]:
        """Retrieve latest records from the database."""
        session = self.Session()
        try:
            query = session.query(FinancialRecord)\
                .order_by(FinancialRecord.timestamp.desc())
                
            if symbol:
                query = query.filter(FinancialRecord.symbol == symbol)
                
            return query.limit(100).all()
        except Exception as e:
            logger.error(f"Error retrieving records: {str(e)}")
            raise
        finally:
            session.close()
