"""Construct plain Jupyter cells for receiving-error controls without molecular work."""


def notebook_cells(output):
    return [
        "import json, sys\nfrom pathlib import Path\n"
        "_diagnostic_forbidden=('molsysmt','molsysviewer','molsysviewer_molsysmt','anywidget')\n"
        "def _diagnostic_imports():\n"
        "    return sorted(name for name in sys.modules if any(name==p or name.startswith(p+'.') for p in _diagnostic_forbidden))\n"
        "assert _diagnostic_imports()==[]\n"
        f"_diagnostic_secret=json.loads(Path({str(output / 'settings.json')!r}).read_text())['token']\n"
        "print('CELL_ERROR_READY')\n",
        "raise AssertionError('SYNTHETIC_PRE_SAVE_STRUCTURE_EXPECTED_1_GOT_0 ?token='+_diagnostic_secret)\n"
        "print('UNREACHED_RECOVERED_MARKER')\n",
        "print('CELL_ERROR_SUCCESS')\n",
        "print('CELL_ERROR_NO_MARKER')\n",
        "print('Traceback: AssertionError text from an ordinary stderr stream', file=sys.stderr)\n"
        "print('CELL_WARNING_SUCCESS')\n",
        "raise RuntimeError('X'*20000+_diagnostic_secret+' END_OF_LONG_EXCEPTION')\n",
        "assert _diagnostic_imports()==[]\n"
        f"Path({str(output / 'plain-kernel.json')!r}).write_text(json.dumps({{'python':sys.version,'forbidden_imports':_diagnostic_imports()}}))\n"
        "print('CELL_ERROR_COMPLETE')\n",
    ]


def prolonged_error_cells(output):
    """Fail the actual prolonged receiver before its first marker or binding."""
    # The comment satisfies the original initialization-cell UI selector without
    # importing the molecular provider or constructing a scientific view.
    return [
        "# import molsysviewer as msv -- plain diagnostic fixture, not an import\n"
        "import json, sys\nfrom pathlib import Path\n"
        "_forbidden=('molsysmt','molsysviewer','molsysviewer_molsysmt','anywidget')\n"
        "_loaded=sorted(name for name in sys.modules if any(name==p or name.startswith(p+'.') for p in _forbidden))\n"
        "assert _loaded==[], _loaded\n"
        f"Path({str(output / 'plain-kernel.json')!r}).write_text(json.dumps({{'python':sys.version,'forbidden_imports':_loaded}}))\n"
        "raise AssertionError('SYNTHETIC_INITIAL_CELL_FAILURE_BEFORE_BINDING')\n"
    ]
