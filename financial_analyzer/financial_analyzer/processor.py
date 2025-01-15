import pandas as pd
import numpy as np
from typing import List, Dict
from dataclasses import asdict
from .scraper import FinancialData
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_data(self, data: Dict[str, List[FinancialData]]) -> None:
        """Load scraped data into a pandas DataFrame."""
        try:
            records = []
            for symbol, data_points in data.items():
                for point in data_points:
                    records.append(asdict(point))
            
            self.df = pd.DataFrame(records)
            self._clean_data()
            logger.info(f"Loaded {len(self.df)} records")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def _clean_data(self) -> None:
        """Clean and preprocess the data."""
        if self.df.empty:
            return
            
        # Handle missing values
        self.df['price'].replace(0, np.nan, inplace=True)
        self.df['volume'].replace(0, np.nan, inplace=True)
        
        # Fill missing prices with mean of same symbol
        self.df['price'] = self.df.groupby('symbol')['price']\
            .transform(lambda x: x.fillna(x.mean()))
            
        # Fill missing volumes with median of same symbol
        self.df['volume'] = self.df.groupby('symbol')['volume']\
            .transform(lambda x: x.fillna(x.median()))
            
        # Drop any remaining null values
        self.df.dropna(inplace=True)
        
        # Convert timestamp to datetime
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        logger.info("Data cleaning completed")

    def calculate_moving_average(self, window: int = 5) -> pd.DataFrame:
        """Calculate moving average for prices."""
        if self.df.empty:
            return pd.DataFrame()
            
        return self.df.groupby('symbol')['price']\
            .rolling(window=window, min_periods=1)\
            .mean()\
            .reset_index()

    def get_volume_statistics(self) -> pd.DataFrame:
        """Calculate volume statistics per symbol."""
        if self.df.empty:
            return pd.DataFrame()
            
        return self.df.groupby('symbol')['volume']\
            .agg(['mean', 'median', 'std', 'min', 'max'])\
            .reset_index()

    def get_correlation_matrix(self) -> pd.DataFrame:
        """Calculate correlation between symbols."""
        if self.df.empty:
            return pd.DataFrame()
            
        pivot = self.df.pivot(index='timestamp', columns='symbol', values='price')
        return pivot.corr()

    def save_to_csv(self, path: str) -> None:
        """Save processed data to CSV."""
        try:
            self.df.to_csv(path, index=False)
            logger.info(f"Data saved to {path}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            raise
