"""Build a plain-kernel control without importing molecular or widget providers."""


def notebook_cells(output):
    setup = """
import importlib.metadata, json, sys
from pathlib import Path
_host_forbidden=('molsysmt','molsysviewer','molsysviewer_molsysmt','anywidget')
def _host_imports():
    return sorted(name for name in sys.modules
                  if any(name==prefix or name.startswith(prefix+'.') for prefix in _host_forbidden))
assert _host_imports()==[], _host_imports()
_host_initial_imports=_host_imports()
_host_executions=0
print('HOST_MEMORY_READY')
"""
    execute = """
from IPython.display import clear_output
assert _host_imports()==[], _host_imports()
_host_executions+=1
clear_output(wait=False)
print('HOST_MEMORY_EXECUTED',_host_executions)
"""
    final = (
        "assert _host_imports()==[], _host_imports()\n"
        "_host_receipt={'python':sys.version,'executions':_host_executions,"
        "'initial_forbidden_imports':_host_initial_imports,"
        "'final_forbidden_imports':_host_imports(),"
        "'ipykernel_version':importlib.metadata.version('ipykernel')}\n"
        f"Path({str(output / 'host-kernel.json')!r}).write_text(json.dumps(_host_receipt,indent=2))\n"
        "print('HOST_MEMORY_COMPLETE')\n"
    )
    return [setup, execute, final]
