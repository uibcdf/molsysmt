import subprocess
import sys

def test_validate_docstrings():
    """Ensure that all public docstrings meet MolSysMT standards."""
    res = subprocess.run([sys.executable, 'devtools/scripts/validate_docstrings.py'], capture_output=True, text=True)
    assert res.returncode == 0, f"Docstring validation failed:\n{res.stdout}\n{res.stderr}"
