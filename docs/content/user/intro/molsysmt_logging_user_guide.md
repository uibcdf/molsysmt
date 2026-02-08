# MolSysMT Logging Setup — User Guide

MolSysMT provides an integrated logging system that also captures Python warnings. This allows you to see all important messages in a consistent format.

---

## Default behavior

By default, when logging is set up, warnings and logs are displayed as:

```
MOLSYSMT WARNING | TopologyWarning: 3 covalent bond(s) reported by 'struct_conn' between chains ['A', 'B'] were added.
```

---

## Quick setup

In most cases, you only need to call:

```python
import molsysmt as msm

msm.config.setup_logging()
```

This will:

- Configure a logger named `molsysmt`
- Capture all Python warnings
- Show them with a consistent format (`MOLSYSMT WARNING | Category: message`)
- Default to level `WARNING`

---

## Changing log level

You can change the level to see more or fewer messages:

```python
msm.config.setup_logging(level="INFO")
```

Levels available: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

---

## Example usage

```python
import warnings
import molsysmt as msm

msm.config.setup_logging(level="INFO")

warnings.warn(msm.SelectionWarning("Ambiguous selection 'CA'"))
```

Output:

```
MOLSYSMT WARNING | SelectionWarning: Ambiguous selection 'CA'
```

---

## Handling Exceptions

MolSysMT exceptions are available directly from the package root:

```python
import molsysmt as msm

try:
    msm.convert('invalid.file', to_form='molsysmt.MolSys')
except msm.ArgumentError as e:
    print(f"Caught expected error: {e}")
```

---

## Environment variables

You can also control logging through environment variables:

- `MOLSYSMT_LOG_LEVEL` — set the logging level (default `WARNING`)
- `MOLSYSMT_SIMPLE_WARNINGS` — if set to `1`, simplifies warnings (removes file:line prefix)

Example:

```bash
export MOLSYSMT_LOG_LEVEL=INFO
export MOLSYSMT_SIMPLE_WARNINGS=1
```

---

## When to use

- Use `setup_logging()` at the beginning of your script or notebook to enable consistent logging.
- For advanced control (e.g., sending logs to a file), see the developer guide.
