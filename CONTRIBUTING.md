# Contributing to Craig

Thank you for your interest in contributing to Craig, the AI Compliance Manager!

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in GitHub Issues
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs (with secrets redacted!)

### Suggesting Features

Have an idea to improve Craig?

1. Open a GitHub Issue with the "enhancement" label
2. Describe:
   - The use case or problem
   - Your proposed solution
   - Why this would benefit other users
   - Any implementation ideas

### Contributing Code

#### Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file (copy from `.env.example`)

#### Development Guidelines

**Code Style**
- Follow PEP 8 style guide
- Use Black for formatting: `black .`
- Run flake8 for linting: `flake8 .`
- Add type hints where appropriate

**Testing**
- Test your changes manually with `python craig.py test`
- Use `--dry-run` mode for testing workflows
- Ensure no regressions in existing functionality

**Documentation**
- Update README.md if adding features
- Update SETUP.md if changing configuration
- Add docstrings to new functions/classes
- Comment complex logic

#### Pull Request Process

1. Update documentation as needed
2. Test your changes thoroughly
3. Commit with clear, descriptive messages
4. Push to your fork
5. Open a Pull Request with:
   - Clear title and description
   - Reference any related issues
   - Screenshots/examples if applicable
   - Note any breaking changes

#### Commit Message Format

```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: add support for custom compliance frameworks

Allows users to define custom compliance frameworks in config.
Also adds validation for framework names.

Closes #42
```

```
fix: prevent duplicate reminders for same employee

Previously, Craig could send multiple reminders in one day
if the script ran multiple times. Now uses Redis to track.
```

## Project Structure

```
craig/
├── craig.py              # Main entry point
├── config.py             # Configuration management
├── integrations/         # External API wrappers
│   ├── vanta.py
│   ├── slack.py
│   └── email.py
├── workflows/            # Automated workflows
│   ├── daily_check.py
│   └── weekly_summary.py
└── utils/                # Helper utilities
    ├── memory.py
    └── messages.py
```

## Development Tips

### Testing Locally

```bash
# Test without sending real messages
python craig.py --dry-run daily-check

# Enable debug output
python craig.py --debug daily-check

# Test integrations
python craig.py test
```

### Working with Mock Data

During development, workflows use mock data if Vanta isn't configured.
See `workflows/daily_check.py` line ~90 for the mock data structure.

### Adding New Integrations

To add a new integration (e.g., KnowBe4):

1. Create `integrations/knowbe4.py`
2. Follow the pattern from `integrations/slack.py`
3. Add configuration to `config.py`
4. Update `.env.example` with new variables
5. Document setup in SETUP.md

### Adding New Workflows

To add a new workflow:

1. Create `workflows/your_workflow.py`
2. Import in `craig.py`
3. Add command to argparse
4. Document usage in README.md

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

**Positive behavior:**
- Being respectful and considerate
- Welcoming diverse perspectives
- Giving and accepting constructive feedback
- Focusing on what's best for the community

**Unacceptable behavior:**
- Harassment or discriminatory language
- Personal attacks or insults
- Publishing others' private information
- Other conduct inappropriate in a professional setting

### Enforcement

Violations may result in temporary or permanent ban from the project.

## Questions?

- Open a GitHub Issue with the "question" label
- Tag maintainers for urgent questions
- Check existing issues and docs first

## Recognition

Contributors will be:
- Listed in project acknowledgments
- Mentioned in release notes for significant contributions
- Thanked publicly for their help!

Thank you for making Craig better! 🤖
