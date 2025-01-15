import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FinancialVisualizer:
    def __init__(self):
        sns.set(style="whitegrid")
        plt.style.use('seaborn')
        self.figsize = (12, 6)
        
    def plot_price_trend(self, df: pd.DataFrame, output_path: Optional[str] = None) -> None:
        """Plot price trends for multiple symbols."""
        try:
            plt.figure(figsize=self.figsize)
            ax = sns.lineplot(
                x='timestamp',
                y='price',
                hue='symbol',
                data=df,
                palette='tab10'
            )
            ax.set_title('Price Trends Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            plt.xticks(rotation=45)
            self._save_or_show(output_path)
        except Exception as e:
            logger.error(f"Error plotting price trend: {str(e)}")
            raise

    def plot_volume_distribution(self, df: pd.DataFrame, output_path: Optional[str] = None) -> None:
        """Plot volume distribution using violin plots."""
        try:
            plt.figure(figsize=self.figsize)
            ax = sns.violinplot(
                x='symbol',
                y='volume',
                data=df,
                palette='Set2'
            )
            ax.set_title('Volume Distribution by Symbol')
            ax.set_xlabel('Symbol')
            ax.set_ylabel('Volume')
            self._save_or_show(output_path)
        except Exception as e:
            logger.error(f"Error plotting volume distribution: {str(e)}")
            raise

    def plot_correlation_heatmap(self, correlation_matrix: pd.DataFrame, output_path: Optional[str] = None) -> None:
        """Plot correlation heatmap between symbols."""
        try:
            plt.figure(figsize=(10, 8))
            ax = sns.heatmap(
                correlation_matrix,
                annot=True,
                cmap='coolwarm',
                vmin=-1,
                vmax=1
            )
            ax.set_title('Price Correlation Between Symbols')
            self._save_or_show(output_path)
        except Exception as e:
            logger.error(f"Error plotting correlation heatmap: {str(e)}")
            raise

    def plot_moving_average(self, df: pd.DataFrame, output_path: Optional[str] = None) -> None:
        """Plot moving average for prices."""
        try:
            plt.figure(figsize=self.figsize)
            ax = sns.lineplot(
                x='timestamp',
                y='price',
                hue='symbol',
                data=df,
                palette='tab10',
                legend=False
            )
            ax.set_title('Moving Average (5 periods)')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            plt.xticks(rotation=45)
            self._save_or_show(output_path)
        except Exception as e:
            logger.error(f"Error plotting moving average: {str(e)}")
            raise

    def _save_or_show(self, output_path: Optional[str] = None) -> None:
        """Save plot to file or show it."""
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            logger.info(f"Plot saved to {output_path}")
        else:
            plt.show()
            plt.close()
