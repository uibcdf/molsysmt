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
import ast
import json

# Add repository root to python path to import molsysmt correctly
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ATTRIBUTE_DELIVERY_BASELINE = os.path.join(
    REPO_ROOT,
    "devtools",
    "data",
    "form_attribute_delivery_baseline.json",
)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _discover_declared_form_names(form_dir, adapters):
    """Return adapter-to-form mappings without importing adapter modules."""
    output = {}
    errors = []
    for adapter_name in adapters:
        init_file = os.path.join(form_dir, adapter_name, "__init__.py")
        if not os.path.isfile(init_file):
            continue
        with open(init_file, encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=init_file)
        values = []
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if any(isinstance(target, ast.Name) and target.id == "form_name" for target in node.targets):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    values.append(node.value.value)
        if len(values) != 1:
            errors.append(
                f"{adapter_name}: expected one literal form_name declaration, found {len(values)}."
            )
        else:
            output[adapter_name] = values[0]
    return output, errors


def _directly_delivers(module, attribute_name, attribute_spec):
    """Return whether an adapter exposes a getter supported by the catalog."""
    return any(
        callable(getattr(module, f"get_{attribute_name}_from_{element}", None))
        for element in attribute_spec["get_from"]
    )


def _delivery_pipe(module, attribute_spec):
    """Return the pipe used by a single-attribute get request, if any."""
    if attribute_spec["topological"] or attribute_spec["chemical_state"]:
        return module.piped_topological_attribute
    if attribute_spec["structural"]:
        return module.piped_structural_attribute
    return None


def _attribute_is_deliverable(form_name, attribute_name, modules, catalog, visited=None):
    """Check direct and transitively piped delivery for one declared attribute."""
    attribute_spec = catalog[attribute_name]
    if not attribute_spec["get_from"]:
        return True

    visited = set() if visited is None else visited
    if form_name in visited:
        return False
    visited = visited | {form_name}

    module = modules[form_name]
    if _directly_delivers(module, attribute_name, attribute_spec):
        return True

    from molsysmt._private.attribute_derivation import can_derive_attribute

    if any(
        can_derive_attribute(module, attribute_name, element)
        for element in attribute_spec["get_from"]
    ):
        return True

    pipe = _delivery_pipe(module, attribute_spec)
    if pipe is None or pipe not in modules:
        return False
    converter = module._convert_to.get(pipe)
    if not (callable(converter) or isinstance(converter, str)):
        return False
    if not modules[pipe].attributes.get(attribute_name, False):
        return False
    return _attribute_is_deliverable(pipe, attribute_name, modules, catalog, visited)


def _audit_attribute_delivery(modules):
    """Return declared attributes unreachable through getters or valid pipes."""
    from molsysmt.attribute import attributes as catalog

    violations = {}
    for form_name, module in sorted(modules.items()):
        unreachable = sorted(
            attribute_name
            for attribute_name, declared in module.attributes.items()
            if declared
            and (
                attribute_name not in catalog
                or not _attribute_is_deliverable(
                    form_name,
                    attribute_name,
                    modules,
                    catalog,
                )
            )
        )
        if unreachable:
            violations[form_name] = unreachable
    return violations


def _load_attribute_delivery_baseline():
    """Load the accepted delivery debt used as a monotonic regression ratchet."""
    with open(ATTRIBUTE_DELIVERY_BASELINE, encoding="utf-8") as file:
        baseline = json.load(file)
    attribute_order = baseline["attribute_order"]
    output = {}
    for form_name, hexadecimal_mask in baseline["form_masks"].items():
        mask = int(hexadecimal_mask, 16)
        output[form_name] = {
            attribute_name
            for index, attribute_name in enumerate(attribute_order)
            if mask & (1 << index)
        }
    return output


def _compact_delivery_baseline(violations):
    """Encode the exact violation sets as compact, subset-comparable bit masks."""
    attribute_order = sorted({name for names in violations.values() for name in names})
    attribute_indices = {name: index for index, name in enumerate(attribute_order)}
    form_masks = {}
    for form_name, names in sorted(violations.items()):
        mask = 0
        for name in names:
            mask |= 1 << attribute_indices[name]
        form_masks[form_name] = hex(mask)
    return {"attribute_order": attribute_order, "form_masks": form_masks}


def _compare_delivery_with_baseline(violations):
    """Return newly introduced and resolved delivery violations."""
    baseline = _load_attribute_delivery_baseline()
    current = {form_name: set(names) for form_name, names in violations.items()}
    forms = set(baseline) | set(current)
    new = {
        form_name: sorted(current.get(form_name, set()) - baseline.get(form_name, set()))
        for form_name in forms
        if current.get(form_name, set()) - baseline.get(form_name, set())
    }
    resolved = {
        form_name: sorted(baseline.get(form_name, set()) - current.get(form_name, set()))
        for form_name in forms
        if baseline.get(form_name, set()) - current.get(form_name, set())
    }
    return new, resolved


def _tier_1_delivery_violations(violations, form_tiers):
    """Return every unreachable declaration on the contractual form surface."""

    return {
        form_name: sorted(names)
        for form_name, names in violations.items()
        if form_tiers.get(form_name) == 1 and names
    }


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

    from molsysmt._private.form_tier import FORM_TIERS

    declared_forms, registry_errors = _discover_declared_form_names(form_dir, adapters)
    discovered_names = set(declared_forms.values())
    duplicate_names = sorted({name for name in discovered_names if list(declared_forms.values()).count(name) > 1})
    missing_tiers = sorted(discovered_names - set(FORM_TIERS))
    stale_tiers = sorted(set(FORM_TIERS) - discovered_names)
    invalid_tiers = sorted(name for name, tier in FORM_TIERS.items() if tier not in {1, 2, 3})

    if duplicate_names:
        registry_errors.append(f"Duplicate form_name declarations: {duplicate_names}")
    if missing_tiers:
        registry_errors.append(f"Forms missing explicit tier entries: {missing_tiers}")
    if stale_tiers:
        registry_errors.append(f"Tier entries without form adapters: {stale_tiers}")
    if invalid_tiers:
        registry_errors.append(f"Forms with invalid tier values: {invalid_tiers}")

    if registry_errors:
        print("FORM TIER REGISTRY VIOLATIONS:")
        for error in registry_errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"Explicit form-tier registry: {len(FORM_TIERS)}/{len(adapters)} adapters classified.\n")

    passed_count = 0
    failed_count = 0
    failures = {}
    loaded_modules = {}

    for adapter_name in adapters:
        module_path = f"molsysmt.form.{adapter_name}"
        errors = []

        # 1. Laziness and Import Check
        try:
            mod = importlib.import_module(module_path)
            loaded_modules[mod.form_name] = mod
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

    delivery_violations = _audit_attribute_delivery(loaded_modules)
    tier_1_delivery_violations = _tier_1_delivery_violations(
        delivery_violations,
        FORM_TIERS,
    )
    new_delivery_violations, resolved_delivery_violations = _compare_delivery_with_baseline(
        delivery_violations
    )
    n_delivery_violations = sum(len(names) for names in delivery_violations.values())

    print("\n" + "=" * 80)
    print("ATTRIBUTE DELIVERY AUDIT")
    print("=" * 80)
    print(
        f"Current accepted debt: {n_delivery_violations} unreachable declarations "
        f"across {len(delivery_violations)} forms."
    )
    if resolved_delivery_violations:
        n_resolved = sum(len(names) for names in resolved_delivery_violations.values())
        print(f"Resolved since baseline: {n_resolved}")
    if tier_1_delivery_violations:
        print("Tier 1 unreachable declarations:")
        for form_name, names in sorted(tier_1_delivery_violations.items()):
            print(f"  - {form_name}: {', '.join(names)}")
        failed_count += 1
        failures["tier_1_attribute_delivery"] = [
            "Tier 1 forms cannot carry accepted unreachable declaration debt."
        ]
    if new_delivery_violations:
        print("New unreachable declarations:")
        for form_name, names in sorted(new_delivery_violations.items()):
            print(f"  - {form_name}: {', '.join(names)}")
        failed_count += 1
        failures["attribute_delivery"] = [
            "Declared attributes must have a catalog-compatible getter or a usable pipe."
        ]
    else:
        print("Delivery ratchet: PASS (no new unreachable declarations)")

    if "--print-delivery-baseline" in sys.argv:
        print("\nBEGIN ATTRIBUTE DELIVERY BASELINE")
        print(json.dumps(_compact_delivery_baseline(delivery_violations), indent=2, sort_keys=True))
        print("END ATTRIBUTE DELIVERY BASELINE")

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
        print("\nAudit Status: SUCCESS (structural checks passed; delivery debt did not regress)")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
