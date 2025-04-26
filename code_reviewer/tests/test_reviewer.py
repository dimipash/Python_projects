import pytest
from src.reviewer import Reviewer

def test_analyze_code():
    reviewer = Reviewer()
    code_snippet = "def example_function():\n    return True"
    analysis_result = reviewer.analyze_code(code_snippet)
    assert analysis_result is not None
    assert isinstance(analysis_result, dict)

def test_provide_feedback():
    reviewer = Reviewer()
    code_snippet = "def example_function():\n    return True"
    feedback = reviewer.provide_feedback(code_snippet)
    assert isinstance(feedback, str)
    assert len(feedback) > 0

def test_generate_report():
    reviewer = Reviewer()
    code_snippet = "def example_function():\n    return True"
    report = reviewer.generate_report(code_snippet)
    assert isinstance(report, str)
    assert "Report" in report