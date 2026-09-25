# MolSysMT Course Devtools

This directory contains standalone automation scripts for validating, polishing, and executing notebooks in **"The Four Paths of the MolSysMT's Master"** course.

These tools are **100% self-contained** within `docs/content/course/devtools/`. If the course is ever migrated to a separate repository or website, this entire directory will migrate alongside the course content.

---

## 🛠️ Available Scripts

### 1. `validate_course.py`
Linter script that checks course integrity:
- Validates that every notebook conforms to the 7 canonical sections defined in `docs/content/course/AGENTS.md`.
- Ensures every notebook has a paired `[Notebook_Name].AGENTS.md` micro-governance file.
- Verifies that all modules listed in `course_manifest.yml` exist on disk.

```bash
python devtools/validate_course.py
```

### 2. `polish_notebooks.py`
Cleans up metadata and execution counters for all course notebooks before committing:
- Resets execution count (`execution_count: null`).
- Cleans execution outputs (optional) or transitory cell metadata.

```bash
python devtools/polish_notebooks.py
```

### 3. `execute_notebooks.py`
Runs all course notebooks end-to-end to verify that code cells execute without errors:

```bash
python devtools/execute_notebooks.py
```
