Installation
============

The Financial Analyzer package requires Python 3.9 or higher. We recommend using a virtual environment for installation.

Prerequisites
-------------

- Python 3.9+
- pip
- virtualenv (optional but recommended)

Installation Steps
------------------

1. Clone this repository.


2. Create and activate a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies:

   .. code-block:: bash

      pip install -r financial_analyzer/requirements.txt

4. Configure environment variables:

   Create a `.env` file in the project root with the following content:

   .. code-block:: bash

      # Database configuration
      DATABASE_URL=sqlite:///financial_data.db

      # API Keys (if needed)
      YAHOO_FINANCE_API_KEY=your_api_key
      MARKETWATCH_API_KEY=your_api_key

5. Verify installation:

   .. code-block:: bash

      python -m pytest financial_analyzer/tests/

Database Setup
--------------

The application uses SQLAlchemy for database operations. To initialize the database:

.. code-block:: bash

   python -m financial_analyzer.database init

This will create the necessary database tables.

Troubleshooting
---------------

If you encounter any issues during installation:

1. Ensure all dependencies are installed correctly
2. Verify Python version meets requirements
3. Check database connection settings
4. Review error logs for specific issues

For additional help, please refer to the :doc:`usage` guide or open an issue on GitHub.
