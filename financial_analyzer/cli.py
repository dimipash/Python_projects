import argparse
import asyncio
import logging
from typing import List
from pathlib import Path
from .scraper import scrape_multiple_sources
from .processor import DataProcessor
from .database import DatabaseManager
from .visualization import FinancialVisualizer

logger = logging.getLogger(__name__)

class FinancialAnalyzerCLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.visualizer = FinancialVisualizer()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        parser = argparse.ArgumentParser(
            description="Financial Data Analysis Tool"
        )
        
        parser.add_argument(
            'symbols',
            nargs='+',
            help="Stock symbols to analyze (e.g. AAPL MSFT GOOG)"
        )
        
        parser.add_argument(
            '--db',
            type=str,
            default='sqlite:///financial_data.db',
            help="Database connection string"
        )
        
        parser.add_argument(
            '--output-dir',
            type=str,
            default='output',
            help="Directory to save output files"
        )
        
        parser.add_argument(
            '--log-level',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            default='INFO',
            help="Set logging level"
        )
        
        return parser

    async def run(self, args: List[str]) -> None:
        """Run the financial analyzer."""
        parsed_args = self.parser.parse_args(args)
        
        # Configure logging
        logging.basicConfig(
            level=parsed_args.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create output directory
        output_dir = Path(parsed_args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Step 1: Scrape data
            logger.info("Starting data scraping...")
            scraped_data = await scrape_multiple_sources(parsed_args.symbols)
            
            # Step 2: Process data
            logger.info("Processing data...")
            processor = DataProcessor()
            processor.load_data(scraped_data)
            
            # Step 3: Save to database
            logger.info("Saving to database...")
            db_manager = DatabaseManager(parsed_args.db)
            all_records = [item for sublist in scraped_data.values() for item in sublist]
            db_manager.save_batch(all_records)
            
            # Step 4: Generate visualizations
            logger.info("Generating visualizations...")
            self._generate_visualizations(processor, output_dir)
            
            # Step 5: Save processed data to CSV
            csv_path = output_dir / 'processed_data.csv'
            processor.save_to_csv(str(csv_path))
            
            logger.info(f"Analysis complete! Results saved to {output_dir}")
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise

    def _generate_visualizations(self, processor: DataProcessor, output_dir: Path) -> None:
        """Generate and save all visualizations."""
        # Price trends
        price_trend_path = output_dir / 'price_trends.png'
        self.visualizer.plot_price_trend(
            processor.df,
            str(price_trend_path)
        )
        
        # Volume distribution
        volume_path = output_dir / 'volume_distribution.png'
        self.visualizer.plot_volume_distribution(
            processor.df,
            str(volume_path)
        )
        
        # Correlation heatmap
        correlation_matrix = processor.get_correlation_matrix()
        if not correlation_matrix.empty:
            correlation_path = output_dir / 'correlation_heatmap.png'
            self.visualizer.plot_correlation_heatmap(
                correlation_matrix,
                str(correlation_path)
            )
        
        # Moving average
        moving_avg_df = processor.calculate_moving_average()
        if not moving_avg_df.empty:
            moving_avg_path = output_dir / 'moving_average.png'
            self.visualizer.plot_moving_average(
                moving_avg_df,
                str(moving_avg_path)
            )

def main():
    import sys
    cli = FinancialAnalyzerCLI()
    asyncio.run(cli.run(sys.argv[1:]))

if __name__ == '__main__':
    main()
