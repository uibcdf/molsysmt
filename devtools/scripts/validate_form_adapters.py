#!/usr/bin/env python
"""
validate_form_adapters.py

Scans all subfolders in molsysmt/form/ and dynamically audits each adapter
against the structural contract defined in molsysmt/form/AGENTS.md.
"""
import os
import sys
import importlib
import inspect

# Add repository root to python path to import molsysmt correctly
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def main():
    print("=" * 80)
    print("MOLSYSMT FORM ADAPTERS STRUCTURAL CONFORMANCE AUDIT")
    print("=" * 80)

    form_dir = os.path.join(REPO_ROOT, "molsysmt", "form")
    if not os.path.exists(form_dir):
        print(f"Error: molsysmt/form directory not found at {form_dir}", file=sys.stderr)
        sys.exit(1)

    # Get all form adapter subdirectories
    adapters = sorted([
        d for d in os.listdir(form_dir)
        if os.path.isdir(os.path.join(form_dir, d)) and d != "__pycache__"
    ])

    print(f"Found {len(adapters)} form adapters to audit.\n")

    passed_count = 0
    failed_count = 0
    failures = {}

    for adapter_name in adapters:
        module_path = f"molsysmt.form.{adapter_name}"
        errors = []

        # 1. Laziness and Import Check
        try:
            mod = importlib.import_module(module_path)
        except Exception as exc:
            errors.append(f"Import Failure: Module could not be imported. "
                          f"This indicates illegal top-level eager imports or syntax errors: {exc}")
            failures[adapter_name] = errors
            failed_count += 1
            print(f"❌ {adapter_name:<40} [FAILED: Import Failure]")
            continue

        # 2. Check Contract Variables
        expected_vars = {
            'form_name': str,
            'form_type': str,
            'bonds_are_explicit': bool,
            'bonds_can_be_computed': bool,
        }

        for var, expected_type in expected_vars.items():
            if not hasattr(mod, var):
                errors.append(f"Missing Variable: contract requires '{var}' to be defined.")
            else:
                val = getattr(mod, var)
                if not isinstance(val, expected_type):
                    errors.append(f"Type Mismatch: '{var}' must be of type {expected_type.__name__}, got {type(val).__name__}.")

        # Check piped properties (can be string or None)
        piped_vars = ['piped_topological_attribute', 'piped_structural_attribute', 'piped_any_attribute']
        for var in piped_vars:
            if not hasattr(mod, var):
                errors.append(f"Missing Variable: contract requires '{var}' to be defined.")
            else:
                val = getattr(mod, var)
                if val is not None and not isinstance(val, str):
                    errors.append(f"Type Mismatch: '{var}' must be str or None, got {type(val).__name__}.")

        # 3. Check Contract Callables and properties
        expected_callables = ['is_form', 'has_attribute']
        for method in expected_callables:
            if not hasattr(mod, method):
                errors.append(f"Missing Callable: contract requires '{method}' to be defined.")
            else:
                val = getattr(mod, method)
                if not callable(val):
                    errors.append(f"Invalid Contract: '{method}' must be a callable function.")

        # Check attributes variable (must be dict)
        if not hasattr(mod, 'attributes'):
            errors.append("Missing Variable: contract requires 'attributes' dict to be defined.")
        else:
            val = getattr(mod, 'attributes')
            if not isinstance(val, (dict, list, set)):
                errors.append(f"Type Mismatch: 'attributes' must be a dict/list/set, got {type(val).__name__}.")

        # Check convert dictionary
        if not hasattr(mod, "_convert_to"):
            errors.append("Missing Converter Map: '_convert_to' dictionary is required.")
        else:
            conv = getattr(mod, "_convert_to")
            if not isinstance(conv, dict):
                errors.append(f"Type Mismatch: '_convert_to' must be a dict, got {type(conv).__name__}.")

        # 4. Check Iterator Context Manager Protocols
        # Expose warnings for placeholders, but strictly fail for active heavy forms.
        has_heavy_support = False
        if hasattr(mod, "_heavy_support"):
            heavy_map = getattr(mod, "_heavy_support")
            if isinstance(heavy_map, dict) and any(heavy_map.values()):
                has_heavy_support = True

        try:
            iterators_mod = importlib.import_module(f"{module_path}.iterators")
            if hasattr(iterators_mod, "StructuresIterator"):
                struct_iter_cls = getattr(iterators_mod, "StructuresIterator")
                if inspect.isclass(struct_iter_cls):
                    has_enter = hasattr(struct_iter_cls, "__enter__")
                    has_exit = hasattr(struct_iter_cls, "__exit__")
                    if not has_enter or not has_exit:
                        msg = "Iterator Conformance Violation: 'StructuresIterator' is defined but missing __enter__/__exit__."
                        if has_heavy_support:
                            errors.append(f"Strict Failure: Active heavy form lacks context manager. {msg}")
                        else:
                            # Just a placeholder warning
                            print(f"  ⚠️  {adapter_name:<38} [Warning: placeholder StructuresIterator lacks context manager]")
        except ModuleNotFoundError:
            pass  # iterators module is optional
        except Exception as exc:
            errors.append(f"Iterator Load Error: 'iterators' module failed to import: {exc}")

        # Summary
        if errors:
            failures[adapter_name] = errors
            failed_count += 1
            print(f"❌ {adapter_name:<40} [FAILED: {len(errors)} violations]")
        else:
            passed_count += 1
            print(f"✅ {adapter_name:<40} [PASS]")

    print("\n" + "=" * 80)
    print("AUDIT RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total Audited Forms : {len(adapters)}")
    print(f"Passed Forms        : {passed_count}")
    print(f"Failed Forms        : {failed_count}")
    print("-" * 80)

    if failed_count > 0:
        print("\nDETAILED CONFORMANCE VIOLATIONS:")
        for name, err_list in sorted(failures.items()):
            print(f"\n📁 Form: {name}")
            for err in err_list:
                print(f"  • {err}")
        print("\n" + "=" * 80)
        print("Audit Status: FAILED (regressions or non-conforming forms detected)")
        print("=" * 80)
        # Note: Do not exit with 1 on first draft so developer can see results in output,
        # but in CI/CD we should exit with 1. We'll exit with 1 here to be a strict regression gate.
        sys.exit(1)
    else:
        print("\nAudit Status: SUCCESS (all active forms conform to the repository standard)")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
