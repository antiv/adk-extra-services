# Contributing to ADK Extra Services

We welcome contributions from the community! Here's how you can help improve this project.


## Contribution Workflow

### Finding Issues to Work On

- Look for issues labeled `good first issue` for beginner-friendly tasks
- Check `help wanted` for general contributions
- If you want to work on something not listed, please open an issue first to discuss

### Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation when adding new features
- Ensure all tests pass before submitting
- Include a clear description of changes in your PR

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/edu010101/adk-extra-services.git
   cd adk-extra-services
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests:**
   ```bash
   pip install -e ".[test]"
   pytest
   ```

5. **Code formatting:**
   We use `black`, `isort`, and `flake8` for code style. Run the autoformatter:
   ```bash
   ./autoformat.sh
   ```
   This will automatically format your code and organize imports.

## Testing Requirements

- Add tests for new features and bug fixes
- Keep tests focused and fast
- Use descriptive test names

## Documentation
- Update relevant documentation when adding new features
- Include docstrings for all public APIs
- Add examples for complex functionality