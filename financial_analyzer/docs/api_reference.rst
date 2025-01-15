API Reference
=============

This document provides detailed API documentation for the Financial Analyzer package.

.. currentmodule:: financial_analyzer

Main Classes
------------

.. autoclass:: FinancialAnalyzer
   :members:
   :inherited-members:
   :show-inheritance:

   .. automethod:: __init__
   .. automethod:: scrape
   .. automethod:: process
   .. automethod:: save_to_csv
   .. automethod:: save_to_database
   .. automethod:: visualize

Scraper Module
--------------

.. automodule:: financial_analyzer.scraper
   :members:
   :show-inheritance:

   .. autoclass:: YahooFinanceScraper
      :members:
      :show-inheritance:

   .. autoclass:: MarketWatchScraper
      :members:
      :show-inheritance:

Processor Module
----------------

.. automodule:: financial_analyzer.processor
   :members:
   :show-inheritance:

   .. autoclass:: DataProcessor
      :members:
      :show-inheritance:

Database Module
---------------

.. automodule:: financial_analyzer.database
   :members:
   :show-inheritance:

   .. autoclass:: FinancialDatabase
      :members:
      :show-inheritance:

Visualization Module
--------------------

.. automodule:: financial_analyzer.visualization
   :members:
   :show-inheritance:

   .. autoclass:: FinancialVisualizer
      :members:
      :show-inheritance:

Technical Analysis Module
-------------------------

.. automodule:: financial_analyzer.technical
   :members:
   :show-inheritance:

   .. autofunction:: calculate_indicators

CLI Module
----------

.. automodule:: financial_analyzer.cli
   :members:
   :show-inheritance:

Exceptions
----------

.. automodule:: financial_analyzer.exceptions
   :members:
   :show-inheritance:

Utilities
---------

.. automodule:: financial_analyzer.utils
   :members:
   :show-inheritance:

For more information about using these classes and functions, see the :doc:`usage` guide.
