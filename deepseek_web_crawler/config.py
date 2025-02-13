import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "BASE_URL": "https://www.opencare.com/dentists/new-york-ny/",
    "CSS_SELECTOR": "div[data-test='search-result-card']",
    "REQUIRED_KEYS": [
        "name",
        "location",
        "description",
        "rating",
    ],
    "OPTIONAL_KEYS": [
        "phone",
        "website",
        "hours",
        "specialties",
        "reviews",
        "price",
    ],
    # Enhanced crawler settings
    "CRAWLER_CONFIG": {
        "MULTI_PAGE": True,
        "MAX_PAGES": 5,
        "DELAY_BETWEEN_PAGES": 2,
        "HEADLESS": True,
        "CACHE_ENABLED": True,
        "VERBOSE_LOGGING": True,
        "TIMEOUT": 30.0,
        "WAIT_TIME": 2.0,
        "RETRY_COUNT": 3,
        "RETRY_DELAY": 1.0,
        "RETRY_BACKOFF": 2.0,
        "BROWSER_TYPE": "chromium",
        "DEVICE_TYPE": "desktop",  # desktop, mobile, tablet
        "VIEWPORT": {"width": 1280, "height": 800},
        "RATE_LIMIT": {
            "REQUESTS_PER_SECOND": 2,
            "BURST_SIZE": 5
        }
    },
    # Enhanced LLM Configuration
    "LLM_CONFIG": {
        "PROVIDER": "groq/deepseek-r1-distill-llama-70b",
        "EXTRACTION_TYPE": "schema",
        "INPUT_FORMAT": "markdown",
        "INSTRUCTION": """
        Extract dental clinic information from the content. For each clinic, find:

        Required information:
        - Name: The full name of the dental clinic or dentist's practice
        - Location: The complete address of the clinic
        - Description: A brief description of the clinic, their services, or the dentist's expertise
        - Rating: The numerical rating (out of 5 stars) if available

        Additional information if present:
        - Phone number
        - Website URL
        - Operating hours
        - List of dental specialties or services offered
        - Number of reviews
        - Price range or insurance information

        Extract this information for each dental clinic card or listing found in the content.
        """,
    }
}

# Example configurations for different use cases
CONFIGS: Dict[str, Dict[str, Any]] = {
    # Test configuration for local development
    "test": {
        **DEFAULT_CONFIG,
        "BASE_URL": "file:///" + os.path.abspath("test.html").replace("\\", "/"),
        "CSS_SELECTOR": "div.item-card",
        "REQUIRED_KEYS": ["name", "description", "location", "rating"],
        "OPTIONAL_KEYS": ["phone", "website"],
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "MULTI_PAGE": False,
            "HEADLESS": False,
            "CACHE_ENABLED": True,
            "VERBOSE_LOGGING": True
        },
        "LLM_CONFIG": {
            **DEFAULT_CONFIG["LLM_CONFIG"],
            "INSTRUCTION": """
            Extract information from each item card. For each item, find:

            Required information:
            - Name: The title of the item (h2 text)
            - Description: The description text
            - Location: The location text
            - Rating: The numerical rating

            Additional information if present:
            - Phone number
            - Website URL

            Extract this information for each item card found in the content.
            """
        }
    },

    # E-commerce configuration
    "ecommerce": {
        **DEFAULT_CONFIG,
        "BASE_URL": "https://example-store.com/products",
        "CSS_SELECTOR": "div.product-card",
        "REQUIRED_KEYS": ["name", "price", "description"],
        "OPTIONAL_KEYS": [
            "sku",
            "category",
            "stock_status",
            "rating",
            "reviews_count",
            "image_url"
        ],
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "MULTI_PAGE": True,
            "MAX_PAGES": 10,
            "DEVICE_TYPE": "desktop"
        },
        "LLM_CONFIG": {
            **DEFAULT_CONFIG["LLM_CONFIG"],
            "INSTRUCTION": """
            Extract product information from each product card:
            - Name: Product title
            - Price: Current price (remove currency symbol)
            - Description: Product description
            - SKU: Product identifier
            - Category: Product category
            - Stock Status: In stock/Out of stock
            - Rating: Numerical rating
            - Reviews Count: Number of reviews
            - Image URL: Product image URL
            """
        }
    },

    # News article configuration
    "news": {
        **DEFAULT_CONFIG,
        "BASE_URL": "https://example-news.com",
        "CSS_SELECTOR": "article.news-item",
        "REQUIRED_KEYS": ["title", "content", "date_published"],
        "OPTIONAL_KEYS": [
            "author",
            "category",
            "tags",
            "image_url",
            "comments_count"
        ],
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "MULTI_PAGE": True,
            "MAX_PAGES": 5,
            "DELAY_BETWEEN_PAGES": 3,
            "DEVICE_TYPE": "desktop"
        }
    },

    # Job listing configuration
    "jobs": {
        **DEFAULT_CONFIG,
        "BASE_URL": "https://example-jobs.com/listings",
        "CSS_SELECTOR": "div.job-posting",
        "REQUIRED_KEYS": ["title", "company", "location", "description"],
        "OPTIONAL_KEYS": [
            "salary",
            "job_type",
            "experience_level",
            "posted_date",
            "benefits",
            "skills_required"
        ],
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "MULTI_PAGE": True,
            "MAX_PAGES": 10,
            "DEVICE_TYPE": "desktop"
        }
    },

    # Real estate configuration
    "real_estate": {
        **DEFAULT_CONFIG,
        "BASE_URL": "https://example-realty.com/listings",
        "CSS_SELECTOR": "div.property-listing",
        "REQUIRED_KEYS": [
            "address",
            "price",
            "bedrooms",
            "bathrooms",
            "square_feet"
        ],
        "OPTIONAL_KEYS": [
            "property_type",
            "year_built",
            "lot_size",
            "amenities",
            "agent_info",
            "images",
            "description"
        ],
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "MULTI_PAGE": True,
            "MAX_PAGES": 20,
            "DELAY_BETWEEN_PAGES": 3,
            "DEVICE_TYPE": "desktop"
        },
        "LLM_CONFIG": {
            **DEFAULT_CONFIG["LLM_CONFIG"],
            "INSTRUCTION": """
            Extract property information from each listing:
            - Address: Full property address
            - Price: Listing price (numbers only)
            - Bedrooms: Number of bedrooms
            - Bathrooms: Number of bathrooms
            - Square Feet: Property size
            - Property Type: House/Condo/etc.
            - Year Built: Construction year
            - Lot Size: Land area
            - Amenities: List of features
            - Agent Info: Contact information
            - Images: Property image URLs
            - Description: Property description
            """
        }
    },

    # Mobile-optimized configuration
    "mobile": {
        **DEFAULT_CONFIG,
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "DEVICE_TYPE": "mobile",
            "VIEWPORT": {"width": 375, "height": 812},  # iPhone X dimensions
            "HEADLESS": True
        }
    },

    # High-performance configuration
    "fast": {
        **DEFAULT_CONFIG,
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "CACHE_ENABLED": True,
            "HEADLESS": True,
            "RATE_LIMIT": {
                "REQUESTS_PER_SECOND": 5,
                "BURST_SIZE": 10
            }
        }
    },

    # Careful/respectful configuration
    "careful": {
        **DEFAULT_CONFIG,
        "CRAWLER_CONFIG": {
            **DEFAULT_CONFIG["CRAWLER_CONFIG"],
            "DELAY_BETWEEN_PAGES": 5,
            "RATE_LIMIT": {
                "REQUESTS_PER_SECOND": 1,
                "BURST_SIZE": 2
            },
            "RETRY_COUNT": 5,
            "RETRY_DELAY": 2.0
        }
    }
}
