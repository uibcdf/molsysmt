# Contributing to MolSysMT

Thank you for your interest in contributing to **MolSysMT**! Whether you're fixing bugs, adding new features, improving documentation, or writing tests, your help is appreciated.

This guide provides the basic steps to get started and outlines the standards we follow across the project.

---

## 🐛 Reporting a bug or proposing a change

**Open an [issue](https://github.com/uibcdf/molsysmt/issues).** That is the front door,
and it is the right one whether you have a patch or only a symptom.

A useful report answers three questions, and the more of them you can answer the faster
we get to the cause:

- **What** goes wrong, or what you would like to exist.
- **How** to see it — the shortest snippet that reproduces it, pasted rather than
  described, with the traceback if there is one.
- **Why** it matters to you: which call, which workflow, and what you did instead.

Please include your MolSysMT version, your Python version, and your platform. If the
problem involves a molecular file, a small one that shows it is worth more than a large
one that also does.

We triage by reproducing. When we do, we answer on the issue restating the problem as we
verified it and linking the working record in `devguide/`, where the analysis lives from
then on. The issue keeps the state and the resolution.

**Maintainers and automated agents** filing from inside the repository follow
[`devguide/reporting_protocol.md`](devguide/reporting_protocol.md), which is stricter:
every entry carries front matter, an issue, and a test that must exist before it can be
closed.

Please do not open a public issue for a security problem. Report it privately through
GitHub's security advisories instead.

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
👉 [Docstring Style Guide](docs/content/developer/documentation/api/docstrings.md)

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

## Working with the Devcontainer (Codex, ...)

To work with Codex, open this repository in a Devcontainer (VS Code: Reopen in
Container or Codespaces). The container will be built automatically using
.devcontainer/devcontainer.json and will install MolSysMT in editable mode.

## 🙌 Need Help?

Feel free to open an issue or ask questions. We’re happy to help!

---

Thanks again for contributing to **MolSysMT**! 🚀
