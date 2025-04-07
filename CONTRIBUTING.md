# Contributing to MolSysMT

Thank you for your interest in contributing to **MolSysMT**! Whether you're fixing bugs, adding new features, improving documentation, or writing tests, your help is appreciated.

This guide provides the basic steps to get started and outlines the standards we follow across the project.

---

## 🛠️ Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

```bash
git clone https://github.com/your-username/MolSysMT.git
cd MolSysMT
```

3. (Optional) **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install -e .[dev]
```

---

## 🧪 Running Tests

We use **pytest** for testing. To run all tests:

```bash
pytest
```

To run a specific test module:
```bash
pytest tests/module/test_basic.py
```

To check code coverage:
```bash
pytest --cov=molsysmt
```

You can view the coverage report in the terminal or use the HTML output:
```bash
pytest --cov=molsysmt --cov-report=html
open htmlcov/index.html
```

---

## 📚 Writing Documentation

We use **Sphinx** with **MyST Markdown** for documentation.

To build the docs locally:
```bash
cd docs
make html
open _build/html/index.html
```

For detailed guidance on how to write docstrings, follow our:
👉 [Docstring Style Guide](docs/dev/docstrings.md)

---

## ✍️ Code Style

We aim for consistent and clean code.

- Python formatting: **Black**
- Import sorting: **isort**
- Linting: **(coming soon) Ruff**
- Docstring format: **NumPy-style with Sphinx and MyST extensions**

Before committing, you can run formatters:
```bash
black molsysmt
isort molsysmt
```

And in the future, we plan to integrate `ruff` and `docstr-coverage`.

---

## 🔁 Pull Request Guidelines

- Make sure your branch is up to date with `main`
- Include **tests** for new functionality
- Follow the docstring and code style guides
- If fixing a bug, link to the related issue in the PR description
- Keep PRs focused and concise

---

## 🙌 Need Help?

Feel free to open an issue or ask questions. We’re happy to help!

---

Thanks again for contributing to **MolSysMT**! 🚀

