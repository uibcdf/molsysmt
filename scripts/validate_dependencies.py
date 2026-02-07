import os
import ast
import sys
from collections import defaultdict

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(PROJECT_ROOT, 'molsysmt')
SOFT_DEPENDENCIES = {
    'mdtraj', 'MDAnalysis', 'openmm', 'openmmtools', 'parmed', 
    'pytraj', 'nglview', 'pdbfixer', 'biopython', 'plotly', 'mmtf'
}
# Files exempt from the check (infrastructure)
EXEMPT_FILES = {
    os.path.join(SRC_ROOT, '_depdigest.py'),
    # Legacy/Third-party code wrapper (hard to refactor safely without breaking upstream compatibility)
    os.path.join(SRC_ROOT, 'form', 'file_mmtf', 'to_mdtraj.py'), 
}

# Directories exempt from the check (Development tools, Tests, etc.)
EXEMPT_DIRS = [
    os.path.join(SRC_ROOT, 'data', '_make'),
    os.path.join(SRC_ROOT, 'docs', 'generate_static_views'),
    os.path.join(SRC_ROOT, 'attic'),
    os.path.join(SRC_ROOT, 'tests'),
    os.path.join(PROJECT_ROOT, 'sandbox'),
    os.path.join(PROJECT_ROOT, 'tests'),
]

def is_exempt(file_path):
    # Exempt individual files
    if file_path in EXEMPT_FILES:
        return True
    
    # Exempt directories
    for exempt_dir in EXEMPT_DIRS:
        if file_path.startswith(exempt_dir):
            return True
            
    return False

def check_top_level_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            print(f"SyntaxError parsing {file_path}")
            return []

    violations = []
    
    for node in tree.body:
        # We only look at top-level nodes in the module body
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split('.')[0]
                if root_module in SOFT_DEPENDENCIES:
                    violations.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split('.')[0]
                if root_module in SOFT_DEPENDENCIES:
                    violations.append((node.lineno, node.module))

    return violations

def validate_codebase():
    print(f"Scanning codebase at {SRC_ROOT} for top-level soft dependency imports...")
    
    all_violations = defaultdict(list)
    
    for root, _, files in os.walk(SRC_ROOT):
        for file in files:
            if not file.endswith('.py'):
                continue
            
            file_path = os.path.join(root, file)
            if is_exempt(file_path):
                continue
                
            violations = check_top_level_imports(file_path)
            if violations:
                all_violations[file_path] = violations

    if all_violations:
        print("\n[FAIL] Found top-level imports of soft dependencies:")
        for path, errs in all_violations.items():
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            print(f"  {rel_path}:")
            for line, mod in errs:
                print(f"    Line {line}: import {mod}")
        return False
    else:
        print("\n[PASS] No top-level imports of soft dependencies found.")
        return True

if __name__ == "__main__":
    success = validate_codebase()
    sys.exit(0 if success else 1)
