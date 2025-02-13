import csv
from typing import Dict, List, Set

from models.item import ScrapedItem


def is_duplicate_item(title: str, seen_titles: Set[str]) -> bool:
    """
    Check if an item with the given title has already been processed.
    
    Args:
        title: Title/name of the item to check
        seen_titles: Set of previously seen titles
    
    Returns:
        bool: True if the title has been seen before
    """
    return title in seen_titles


def is_complete_item(data: Dict, required_keys: List[str]) -> bool:
    """
    Check if the extracted data has all required fields.
    
    Args:
        data: Dictionary containing the extracted data
        required_keys: List of required field names
    
    Returns:
        bool: True if all required fields are present and non-empty
    """
    return all(
        key in data and data[key] is not None and str(data[key]).strip() != ""
        for key in required_keys
    )


def save_items_to_csv(data: List[Dict], filename: str):
    """
    Save extracted data to a CSV file.
    
    Args:
        data: List of dictionaries containing the extracted data
        filename: Name of the output CSV file
    """
    if not data:
        print("No data to save.")
        return

    # Get all possible field names from the data and model
    model_fields = set(ScrapedItem.model_fields.keys())
    data_fields = set().union(*(d.keys() for d in data))
    fieldnames = sorted(model_fields.union(data_fields))

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write each row, ensuring missing fields are handled
        for item in data:
            row = {field: item.get(field, "") for field in fieldnames}
            writer.writerow(row)
            
    print(f"Saved {len(data)} records to '{filename}'.")
