# Cashflows

A Django-based application for managing financial flows.

## Requirements

- Python >= 3.13
- Django 5.1
- Other dependencies as listed in `pyproject.toml` or `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/effedib/cashflows.git
cd cashflows
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Or using uv (recommended)
uv venv
```

3. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install .
```

## Features

- Bootstrap 5 integration via crispy-bootstrap5
- Form handling with django-crispy-forms
- Table management with django-tables2
- Filtering capabilities with django-filter
- Excel file support through openpyxl
- Data import/export functionality with tablib

## Development

This project uses [ruff](https://github.com/astral-sh/ruff) for code formatting and linting. To set up the development environment:

```bash
uv pip install --dev .
```

## Project Structure

The project follows standard Django project structure:

```
cashflows/
├── manage.py          # Django command-line utility
├── config/            # Project configuration
├── pyproject.toml     # Project metadata and dependencies
└── requirements.txt   # Pin-pointed dependencies
```

## License

GNU General Public License (GPL)
