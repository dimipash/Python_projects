def format_code_snippet(code_snippet):
    """Format the given code snippet for better readability."""
    return "\n".join(line.strip() for line in code_snippet.splitlines() if line.strip())

def calculate_code_metrics(code_snippet):
    """Calculate and return metrics for the given code snippet."""
    lines = code_snippet.splitlines()
    num_lines = len(lines)
    num_chars = sum(len(line) for line in lines)
    return {
        "num_lines": num_lines,
        "num_chars": num_chars,
    }