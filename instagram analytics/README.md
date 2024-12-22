# Instagram Analytics Application

## Overview

This Python application retrieves and analyzes Instagram account insights using the Facebook Graph API. It provides comprehensive metrics including follower growth, post engagement, reach, and more.

## Prerequisites

-   Python 3.8+
-   Facebook Developer Account
-   Instagram Business/Creator Account
-   Facebook Graph API Access Token

## Setup Instructions

### 1. API Credentials

1. Create a Facebook Developer Account
2. Create a Facebook App
3. Generate a Long-Lived Access Token
4. Find your Instagram Account ID and Page ID

### 2. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
FACEBOOK_ACCESS_TOKEN=your_long_lived_access_token
FACEBOOK_PAGE_ID=your_page_id
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
```

## Output

The application generates:

-   Console output with key metrics
-   `follower_growth.png`: Visualization of follower growth
-   `instagram_analytics_report.json`: Detailed JSON report
-   `instagram_analytics.log`: Logging information

## Features

-   Retrieve account-level insights
-   Analyze top-performing posts
-   Generate follower growth visualization
-   Secure credential management
-   Comprehensive error handling

## Important Notes

-   Requires Facebook Graph API permissions
-   Metrics depend on account type and API access
-   Refresh access token periodically

## Troubleshooting

-   Ensure all credentials are correct
-   Check API permissions
-   Verify Python and package versions
