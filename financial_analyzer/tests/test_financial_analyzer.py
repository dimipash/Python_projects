import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch
from ..scraper import FinancialData, scrape_multiple_sources
from ..processor import DataProcessor
from ..database import DatabaseManager, FinancialRecord
from ..visualization import FinancialVisualizer
from ..cli import FinancialAnalyzerCLI

@pytest.fixture
def sample_financial_data():
    return [
        FinancialData(
            symbol="AAPL",
            price=150.0,
            volume=1000000,
            timestamp=datetime.now(),
            source="test"
        ),
        FinancialData(
            symbol="MSFT",
            price=250.0,
            volume=500000,
            timestamp=datetime.now(),
            source="test"
        )
    ]

@pytest.fixture
def sample_dataframe(sample_financial_data):
    return pd.DataFrame([d.__dict__ for d in sample_financial_data])

@pytest.fixture
def mock_db():
    with patch('financial_analyzer.database.DatabaseManager') as mock:
        yield mock

@pytest.fixture
def mock_visualizer():
    with patch('financial_analyzer.visualization.FinancialVisualizer') as mock:
        yield mock

@pytest.mark.asyncio
async def test_scrape_multiple_sources():
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(
            return_value="<html>...</html>"
        )
        result = await scrape_multiple_sources(["AAPL", "MSFT"])
        assert isinstance(result, dict)
        assert all(isinstance(v, list) for v in result.values())

def test_data_processor(sample_financial_data):
    processor = DataProcessor()
    processor.load_data({"test": sample_financial_data})
    
    assert isinstance(processor.df, pd.DataFrame)
    assert len(processor.df) == 2
    assert processor.get_correlation_matrix().shape == (2, 2)

def test_database_manager(mock_db, sample_financial_data):
    db = DatabaseManager("sqlite:///:memory:")
    db.save_batch(sample_financial_data)
    
    records = db.get_latest_records()
    assert len(records) > 0
    assert isinstance(records[0], FinancialRecord)

def test_visualizer(sample_dataframe, tmp_path):
    visualizer = FinancialVisualizer()
    output_path = tmp_path / "test.png"
    
    visualizer.plot_price_trend(sample_dataframe, str(output_path))
    assert output_path.exists()

@pytest.mark.asyncio
async def test_cli_integration(mock_db, mock_visualizer, tmp_path):
    cli = FinancialAnalyzerCLI()
    args = ["AAPL", "MSFT", "--output-dir", str(tmp_path)]
    
    with patch('financial_analyzer.scraper.scrape_multiple_sources') as mock_scrape:
        mock_scrape.return_value = {
            "AAPL": [FinancialData(
                symbol="AAPL",
                price=150.0,
                volume=1000000,
                timestamp=datetime.now(),
                source="test"
            )]
        }
        
        await cli.run(args)
        
        assert (tmp_path / "processed_data.csv").exists()
        mock_db.return_value.save_batch.assert_called_once()
        mock_visualizer.return_value.plot_price_trend.assert_called_once()
