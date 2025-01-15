Contributing Guide
==================

We welcome contributions to the Financial Analyzer project! Please follow these guidelines when contributing.

Getting Started
---------------

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature/bugfix
4. Set up development environment (see :doc:`installation`)
5. Install development dependencies:

   .. code-block:: bash

      pip install -r requirements-dev.txt

Coding Standards
----------------

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings following Google style
- Keep functions small and focused
- Use descriptive variable names
- Write unit tests for new features
- Maintain 100% test coverage

Pull Request Process
--------------------

1. Create a new branch from main
2. Implement your changes
3. Write tests for your changes
4. Run all tests and verify coverage:

   .. code-block:: bash

      pytest --cov=financial_analyzer --cov-report=html

5. Update documentation if needed
6. Push your branch and create a pull request
7. Address any review comments
8. Ensure all CI checks pass

Testing Requirements
--------------------

- Write unit tests using pytest
- Use pytest fixtures for test setup
- Mock external API calls
- Test edge cases and error conditions
- Maintain 100% code coverage
- Run tests before submitting PR:

   .. code-block:: bash

      pytest --cov=financial_analyzer --cov-report=term-missing

Documentation
-------------

- Update relevant documentation when adding features
- Follow Sphinx documentation style
- Add examples to docstrings
- Update README.md if needed
- Add new documentation files to index.rst

Code Review Process
-------------------

- All PRs require at least one approval
- Reviewers will check for:
  - Code quality and style
  - Test coverage
  - Documentation updates
  - Security considerations
  - Performance impact

Issue Reporting
---------------

- Use GitHub issues to report bugs
- Include steps to reproduce
- Provide error logs
- Include system information
- For feature requests, describe the use case

Thank you for contributing!
