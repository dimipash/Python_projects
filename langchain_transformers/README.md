# Local LLM Text Processing System

A Python application for document summarization and question-answering using local Hugging Face models.

## Features

- Configurable model management via YAML
- Error handling and logging
- Interactive Q&A mode
- Input validation and safety checks
- Type hints and PEP8 compliance
- CLI interface with argparse

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Usage

Basic summarization:
```bash
python main.py --text "Your long text here" --length medium
```

Interactive mode:
```bash
python main.py --text @input.txt --length long --interactive
```

## Configuration

Edit `config.yml` to:
- Change models
- Adjust input/output limits
- Configure logging
- Set default parameters

Example config:
```yaml
models:
  summarization:
    base_model: "facebook/bart-large-cnn"
    refinement_model: "facebook/bart-large"
    # ... other settings
```

## Notes

- First run will download models (5-10GB disk space required)
- Use device: -1 for CPU-only mode
- Models cached in `./model_cache`

## License
MIT License