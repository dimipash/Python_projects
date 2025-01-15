Usage Guide
===========

This guide provides examples and instructions for using the Financial Analyzer tool.

Command Line Interface (CLI)
----------------------------

The primary interface for the Financial Analyzer is through the command line.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   financial-analyzer AAPL MSFT GOOGL --output-dir ./results

This command will:
1. Scrape financial data for Apple, Microsoft, and Alphabet
2. Process and analyze the data
3. Save results to CSV and database
4. Generate visualizations in the specified output directory

Advanced Options
~~~~~~~~~~~~~~~~

.. code-block:: bash

   financial-analyzer AAPL MSFT --start-date 2023-01-01 --end-date 2023-12-31 \
       --interval daily --output-format csv json --visualize

Available options:
- ``--start-date``: Start date for data collection (YYYY-MM-DD)
- ``--end-date``: End date for data collection (YYYY-MM-DD)
- ``--interval``: Data collection interval (daily, weekly, monthly)
- ``--output-format``: Output formats (csv, json, both)
- ``--visualize``: Generate visualizations
- ``--database``: Specify database connection string

Python API Usage
----------------

The Financial Analyzer can also be used as a Python package:

.. code-block:: python

   from financial_analyzer import FinancialAnalyzer

   analyzer = FinancialAnalyzer()
   
   # Scrape and process data
   data = analyzer.scrape(['AAPL', 'MSFT'])
   processed_data = analyzer.process(data)
   
   # Save results
   analyzer.save_to_csv(processed_data, 'output.csv')
   analyzer.save_to_database(processed_data)
   
   # Generate visualizations
   analyzer.visualize(processed_data, output_dir='visualizations')

Common Workflows
----------------

1. **Daily Market Analysis**

   .. code-block:: bash

      financial-analyzer SPY QQQ --interval daily --visualize

2. **Portfolio Analysis**

   .. code-block:: bash

      financial-analyzer AAPL MSFT GOOGL AMZN --start-date 2023-01-01 \
          --end-date 2023-12-31 --output-format csv

3. **Technical Indicators**

   .. code-block:: python

      from financial_analyzer.technical import calculate_indicators
      
      data = analyzer.scrape(['AAPL'])
      indicators = calculate_indicators(data, ['sma', 'rsi', 'macd'])

Troubleshooting
---------------

- If scraping fails, verify API keys and network connection
- For database issues, check connection string and permissions
- For visualization errors, ensure required dependencies are installed

For more advanced usage, see the :doc:`api_reference`.
