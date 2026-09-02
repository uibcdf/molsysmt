#!/usr/bin/env python3
"""Validate public docstring structure, fidelity, and minimum useful content."""

import ast
import inspect
import json
import re
import sys
from pathlib import Path

import molsysmt as msm

EXEMPT_RETURNS = {
    'close', 'clear', 'info', 'show_gui', 'standardize_view', 'write_html', 'view',
    'add_arrows', 'add_contacts', 'add_cylinders', 'add_hbonds',
    'show_as_balls_and_sticks', 'show_as_cartoon', 'show_as_licorice', 'show_as_surface',
    'set_color', 'set_color_by_value'
}

API_STABILITY_REGISTRY = (
    Path(__file__).resolve().parents[1] / "data" / "public_api_stability.json"
)
SECTION_NAMES = {
    "Attributes",
    "Examples",
    "Notes",
    "Parameters",
    "Raises",
    "References",
    "Returns",
    "See Also",
    "Warns",
    "Yields",
}


def normalize_default_repr(val_str: str) -> str:
    """Normalize default value string representation for literal comparison."""
    if val_str == "<no_default>":
        return val_str
    try:
        val = ast.literal_eval(val_str)
        return repr(val)
    except Exception:
        return val_str.strip()


def _section_lines(doc: str, section_name: str) -> list[str]:
    """Return the body of a NumPy-style docstring section."""
    if not doc:
        return []

    lines = inspect.cleandoc(doc).splitlines()
    for index, line in enumerate(lines):
        if line.strip() != section_name:
            continue
        body_start = index + 1
        if body_start < len(lines) and set(lines[body_start].strip()) == {"-"}:
            body_start += 1
        body = []
        for candidate in lines[body_start:]:
            stripped = candidate.strip()
            if stripped in SECTION_NAMES or stripped.startswith(".. "):
                break
            body.append(candidate)
        return body
    return []


def parse_docstring_parameters(doc: str) -> dict[str, dict[str, str]]:
    """Extract types, defaults, and descriptions from a Parameters section."""
    parameters = {}
    current_name = None

    for line in _section_lines(doc, "Parameters"):
        stripped = line.strip()
        if not stripped:
            continue
        header = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.+)$", stripped)
        plain_header = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)$", stripped)
        if not line.startswith(" ") and (header or plain_header):
            if header:
                name, documented_type = header.groups()
                default_match = re.search(r",\s*default\s*=\s*(.+)$", documented_type)
                if default_match:
                    default = default_match.group(1).strip()
                    documented_type = documented_type[: default_match.start()].strip()
                else:
                    default = "<no_default>"
            else:
                name = plain_header.group(1)
                documented_type = ""
                default = "<no_default>"
            parameters[name] = {
                "type": documented_type,
                "default": default,
                "description": "",
            }
            current_name = name
        elif current_name is not None:
            description = parameters[current_name]["description"]
            parameters[current_name]["description"] = f"{description} {stripped}".strip()

    return parameters


def parse_docstring_params_and_defaults(doc: str) -> tuple[list[str], dict[str, str]]:
    """Extract parameter names and documented defaults from a NumPy docstring."""
    parameters = parse_docstring_parameters(doc)
    return list(parameters), {name: entry["default"] for name, entry in parameters.items()}


def _normalize_prose(text: str) -> str:
    """Normalize lightweight markup and whitespace for vacuity comparisons."""
    text = re.sub(r"[`*_]", "", text)
    return re.sub(r"\s+", " ", text).strip().casefold()


def find_vacuous_docstring_content(doc: str) -> list[str]:
    """Find known content-free patterns in a public API docstring."""
    errors = []
    for name, entry in parse_docstring_parameters(doc).items():
        description = _normalize_prose(entry["description"])
        normalized_name = _normalize_prose(name)
        restatements = {
            f"{normalized_name}.",
            f"argument {normalized_name}.",
            f"the {normalized_name} argument.",
        }
        if not description:
            errors.append(f"Parameter '{name}' has an empty description.")
        elif description in restatements:
            errors.append(f"Parameter '{name}' only restates its name.")
        if _normalize_prose(entry["type"]) == "object":
            errors.append(f"Parameter '{name}' uses the non-informative type 'object'.")

    returns_body = _section_lines(doc, "Returns")
    if returns_body:
        return_descriptions = [
            line.strip()
            for line in returns_body
            if line.startswith(" ") and line.strip()
        ]
        normalized_return_description = _normalize_prose(" ".join(return_descriptions))
        if not normalized_return_description:
            errors.append("The Returns section has an empty description.")
        elif normalized_return_description == "resulting object in object form.":
            errors.append("The Returns section uses the generated placeholder description.")

    return errors


def _resolve_public_symbol(symbol: str):
    """Resolve a registry symbol without importing modules outside MolSysMT's public tree."""
    obj = msm
    for part in symbol.split(".")[1:]:
        obj = getattr(obj, part)
    return obj


def stable_function_ids() -> set[int]:
    """Return object identities for functions classified as stable in the API registry."""
    registry = json.loads(API_STABILITY_REGISTRY.read_text())
    identities = set()
    for symbol, record in registry["symbols"].items():
        if record["stability"] != "stable":
            continue
        try:
            obj = _resolve_public_symbol(symbol)
        except (AttributeError, ImportError):
            continue
        if inspect.isfunction(obj):
            identities.add(id(obj))
    return identities


def validate() -> int:
    print("Running MolSysMT docstring fidelity and minimum-content validation...")
    
    public_modules = {
        'molsysmt': msm,
        'molsysmt.basic': msm.basic,
        'molsysmt.build': msm.build,
        'molsysmt.structure': msm.structure,
        'molsysmt.topology': msm.topology,
        'molsysmt.pbc': msm.pbc,
        'molsysmt.physchem': msm.physchem,
        'molsysmt.hbonds': msm.hbonds,
        'molsysmt.molecular_mechanics': msm.molecular_mechanics,
        'molsysmt.element': msm.element,
        'molsysmt.element.atom': msm.element.atom,
        'molsysmt.element.group': msm.element.group,
        'molsysmt.element.group.amino_acid': msm.element.group.amino_acid,
        'molsysmt.element.group.ion': msm.element.group.ion,
        'molsysmt.element.group.water': msm.element.group.water,
        'molsysmt.element.group.small_molecule': msm.element.group.small_molecule,
        'molsysmt.element.group.nucleotide': msm.element.group.nucleotide,
        'molsysmt.element.group.lipid': msm.element.group.lipid,
        'molsysmt.element.group.saccharide': msm.element.group.saccharide,
        'molsysmt.element.group.terminal_capping': msm.element.group.terminal_capping,
        'molsysmt.element.component': msm.element.component,
        'molsysmt.element.molecule': msm.element.molecule,
        'molsysmt.element.entity': msm.element.entity,
        'molsysmt.element.chain': msm.element.chain,
        'molsysmt.form': msm.form,
        'molsysmt.third_party': msm.third_party,
        'molsysmt.third_party.openmm': msm.third_party.openmm,
        'molsysmt.third_party.openmm.forces': msm.third_party.openmm.forces,
        'molsysmt.third_party.openmm.platforms': msm.third_party.openmm.platforms,
        'molsysmt.third_party.openmm.reporters': msm.third_party.openmm.reporters,
        'molsysmt.third_party.nglview': msm.third_party.nglview,
    }
    
    errors = []
    total_checked = 0
    visited = set()
    stable_ids = stable_function_ids()

    def check_fn(obj, full_name):
        nonlocal total_checked
        if full_name in visited or obj in visited:
            return
        visited.add(full_name)
        try:
            visited.add(obj)
        except Exception:
            pass
            
        total_checked += 1
        doc = inspect.getdoc(obj)
        if not doc or not doc.strip():
            errors.append(f"{full_name}: Missing docstring entirely.")
            return

        try:
            sig = inspect.signature(obj)
            sig_params = [p for p in sig.parameters.values() if p.name not in ('self', 'cls', 'kwargs', 'args', 'kwargs_iterator')]
            sig_param_names = [p.name for p in sig_params]
        except Exception:
            sig_params = []
            sig_param_names = []

        doc_param_names, doc_param_defaults = parse_docstring_params_and_defaults(doc)

        if sig_params and 'Parameters' not in doc:
            errors.append(f"{full_name}: Missing 'Parameters' section.")
        elif sig_params:
            # 1. Forward check: signature -> docstring
            for p in sig_params:
                if p.name not in doc_param_names:
                            errors.append(
                                f"{full_name}: Parameter '{p.name}' from signature is not "
                                "in docstring Parameters section."
                            )
                else:
                    # Validate default value fidelity (Item B.3)
                    if p.default is not inspect.Parameter.empty:
                        doc_def = doc_param_defaults.get(p.name, "<no_default>")
                        if doc_def == "<no_default>":
                            errors.append(f"{full_name}: Parameter '{p.name}' has default in signature ({repr(p.default)}) but docstring specifies no default.")
                        else:
                            norm_sig = normalize_default_repr(repr(p.default))
                            norm_doc = normalize_default_repr(doc_def)
                            if norm_sig != norm_doc:
                                errors.append(f"{full_name}: Default mismatch for parameter '{p.name}': signature={repr(p.default)} vs docstring={doc_def}")
                    else:
                        doc_def = doc_param_defaults.get(p.name, "<no_default>")
                        if doc_def != "<no_default>":
                            errors.append(f"{full_name}: Parameter '{p.name}' has NO default in signature, but docstring documents default={doc_def}")

            # 2. Reverse check: docstring -> signature
            for p_name in doc_param_names:
                if p_name not in sig_param_names and p_name not in ('kwargs', 'args'):
                    errors.append(f"{full_name}: Phantom parameter '{p_name}' documented in docstring is not in function signature.")

        fn_name = full_name.split('.')[-1]
        if 'Returns' not in doc and not fn_name.startswith('set') and fn_name not in EXEMPT_RETURNS:
            errors.append(f"{full_name}: Missing 'Returns' section.")

        if id(obj) in stable_ids:
            for error in find_vacuous_docstring_content(doc):
                errors.append(f"{full_name}: {error}")

    for mod_name, mod in public_modules.items():
        for attr in dir(mod):
            if attr.startswith('_'):
                continue
            try:
                obj = getattr(mod, attr)
            except Exception:
                continue
            if inspect.isfunction(obj):
                check_fn(obj, f"{mod_name}.{attr}")

    if errors:
        print(f"\nFAILED: Found {len(errors)} docstring issues across {total_checked} public functions:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(
            f"PASSED: All {total_checked} public functions have structurally consistent "
            "NumPy docstrings, exact default fidelity, and no known vacuous stable-API content!"
        )
        return 0

if __name__ == '__main__':
    sys.exit(validate())
