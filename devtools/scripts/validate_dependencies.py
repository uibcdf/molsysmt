import os
import ast
import sys
from collections import defaultdict

import yaml

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_ROOT = os.path.join(PROJECT_ROOT, 'molsysmt')


def _load_soft_dependency_roots():
    """Read soft dependency import roots from the normative DepDigest registry."""
    config_path = os.path.join(SRC_ROOT, '_depdigest.py')
    with open(config_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=config_path)

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == 'LIBRARIES'
            for target in node.targets
        ):
            continue
        libraries = ast.literal_eval(node.value)
        return {
            library.split('.', maxsplit=1)[0]
            for library, metadata in libraries.items()
            if metadata['type'] == 'soft'
        }

    raise RuntimeError(f'LIBRARIES was not found in {config_path}')


SOFT_DEPENDENCIES = _load_soft_dependency_roots()
OPENFF_TEST_ENV_SPECS = {
    'openff-toolkit-base>=0.17.1',
    'openff-units>=0.3.0',
}
# Files exempt from the check (infrastructure)
EXEMPT_FILES = {
    os.path.join(SRC_ROOT, '_depdigest.py'),
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

    test_env_path = os.path.join(PROJECT_ROOT, 'devtools', 'conda-envs', 'test_env.yaml')
    with open(test_env_path, 'r', encoding='utf-8') as file:
        test_dependencies = {
            str(item).replace(' ', '')
            for item in yaml.safe_load(file)['dependencies']
        }
    missing_openff_specs = OPENFF_TEST_ENV_SPECS - test_dependencies

    if all_violations:
        print("\n[FAIL] Found top-level imports of soft dependencies:")
        for path, errs in all_violations.items():
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            print(f"  {rel_path}:")
            for line, mod in errs:
                print(f"    Line {line}: import {mod}")
    if missing_openff_specs:
        print("\n[FAIL] OpenFF CI dependency bounds are incomplete:")
        for spec in sorted(missing_openff_specs):
            print(f"  missing: {spec}")

    if all_violations or missing_openff_specs:
        return False

    print("\n[PASS] No top-level imports of soft dependencies found.")
    print("[PASS] OpenFF CI dependency bounds are complete.")
    return True

if __name__ == "__main__":
    success = validate_codebase()
    sys.exit(0 if success else 1)
