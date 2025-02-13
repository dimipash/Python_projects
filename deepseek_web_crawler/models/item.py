from typing import Optional
from pydantic import BaseModel

class ScrapedItem(BaseModel):
    """
    Base model for scraped items with common fields.
    All fields are optional since different scraping configurations
    may require different subsets of fields.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    price: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[str] = None
    reviews_count: Optional[int] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    date_posted: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[str] = None
    additional_info: Optional[str] = None
