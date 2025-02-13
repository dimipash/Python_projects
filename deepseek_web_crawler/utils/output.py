import csv
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

from utils.logger import logger

class OutputManager:
    """Manages data output in various formats with configurable options."""
    
    def __init__(
        self,
        output_dir: str = "output",
        filename_prefix: str = "scraped_data",
        timestamp: bool = True
    ):
        """
        Initialize the output manager.
        
        Args:
            output_dir: Directory to store output files
            filename_prefix: Prefix for output filenames
            timestamp: Whether to include timestamp in filenames
        """
        self.output_dir = Path(output_dir)
        self.filename_prefix = filename_prefix
        self.timestamp = timestamp
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_filename(self, extension: str) -> str:
        """Generate filename with optional timestamp."""
        if self.timestamp:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{self.filename_prefix}_{timestamp}.{extension}"
        return f"{self.filename_prefix}.{extension}"
    
    def save_csv(
        self,
        data: List[Dict],
        filename: Optional[str] = None,
        fieldnames: Optional[List[str]] = None,
        encoding: str = "utf-8",
        **csv_kwargs
    ) -> str:
        """
        Save data to CSV file.
        
        Args:
            data: List of dictionaries containing the data
            filename: Optional custom filename
            fieldnames: Optional list of field names for CSV columns
            encoding: File encoding
            csv_kwargs: Additional arguments for csv.DictWriter
            
        Returns:
            str: Path to the saved file
        """
        if not data:
            logger.warning("No data to save to CSV")
            return ""
        
        filepath = self.output_dir / (filename or self._get_filename("csv"))
        
        # Get fieldnames from data if not provided
        if not fieldnames:
            fieldnames = sorted(set().union(*(d.keys() for d in data)))
        
        try:
            with open(filepath, "w", newline="", encoding=encoding) as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, **csv_kwargs)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"Saved {len(data)} records to CSV: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving CSV file: {str(e)}")
            return ""
    
    def save_json(
        self,
        data: List[Dict],
        filename: Optional[str] = None,
        indent: int = 2,
        encoding: str = "utf-8",
        ensure_ascii: bool = False
    ) -> str:
        """
        Save data to JSON file.
        
        Args:
            data: List of dictionaries containing the data
            filename: Optional custom filename
            indent: Number of spaces for indentation
            encoding: File encoding
            ensure_ascii: Whether to escape non-ASCII characters
            
        Returns:
            str: Path to the saved file
        """
        if not data:
            logger.warning("No data to save to JSON")
            return ""
        
        filepath = self.output_dir / (filename or self._get_filename("json"))
        
        try:
            with open(filepath, "w", encoding=encoding) as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
            
            logger.info(f"Saved {len(data)} records to JSON: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving JSON file: {str(e)}")
            return ""
    
    def save_excel(
        self,
        data: List[Dict],
        filename: Optional[str] = None,
        sheet_name: str = "Sheet1",
        **excel_kwargs
    ) -> str:
        """
        Save data to Excel file.
        
        Args:
            data: List of dictionaries containing the data
            filename: Optional custom filename
            sheet_name: Name of the Excel sheet
            excel_kwargs: Additional arguments for pandas.DataFrame.to_excel
            
        Returns:
            str: Path to the saved file
        """
        if not data:
            logger.warning("No data to save to Excel")
            return ""
        
        filepath = self.output_dir / (filename or self._get_filename("xlsx"))
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(
                filepath,
                sheet_name=sheet_name,
                index=False,
                **excel_kwargs
            )
            
            logger.info(f"Saved {len(data)} records to Excel: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving Excel file: {str(e)}")
            return ""
    
    def save_all_formats(
        self,
        data: List[Dict],
        base_filename: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Save data to all supported formats.
        
        Args:
            data: List of dictionaries containing the data
            base_filename: Optional base filename without extension
            
        Returns:
            Dict[str, str]: Dictionary mapping format to saved filepath
        """
        results = {}
        
        if base_filename:
            self.filename_prefix = base_filename
        
        # Save in each format
        results["csv"] = self.save_csv(data)
        results["json"] = self.save_json(data)
        results["excel"] = self.save_excel(data)
        
        return {k: v for k, v in results.items() if v}  # Remove empty paths
    
    def clear_output_dir(self, pattern: Optional[str] = None):
        """
        Clear files from output directory.
        
        Args:
            pattern: Optional glob pattern to match files
        """
        try:
            if pattern:
                files = self.output_dir.glob(pattern)
            else:
                files = self.output_dir.iterdir()
            
            for file in files:
                if file.is_file():
                    file.unlink()
            
            logger.info(f"Cleared output directory: {self.output_dir}")
        except Exception as e:
            logger.error(f"Error clearing output directory: {str(e)}")