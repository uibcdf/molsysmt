#!/usr/bin/env python3
"""Validate docstring completeness, formatting, bidirectional signature consistency, and default value fidelity across MolSysMT."""

import ast
import inspect
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


def normalize_default_repr(val_str: str) -> str:
    """Normalize default value string representation for literal comparison."""
    if val_str == "<no_default>":
        return val_str
    try:
        val = ast.literal_eval(val_str)
        return repr(val)
    except Exception:
        return val_str.strip()


def parse_docstring_params_and_defaults(doc: str) -> tuple[list[str], dict[str, str]]:
    """Extract parameter names and documented default values from NumPy-style docstrings."""
    if not doc or 'Parameters' not in doc:
        return [], {}
    lines = doc.splitlines()
    in_params = False
    param_names = []
    param_defaults = {}
    
    for line in lines:
        stripped = line.strip()
        if stripped == 'Parameters':
            in_params = True
            continue
        if in_params:
            if stripped.startswith('---'):
                continue
            if stripped in ('Returns', 'Raises', 'Notes', 'See Also', 'Examples', 'References') or stripped.startswith('.. '):
                break
            if line and not line.startswith('        ') and ':' in stripped:
                # Match parameter definition: name : type, default=value
                match_def = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?:.*?,\s*)?default=([^\n]+)$', stripped)
                if match_def:
                    p_name = match_def.group(1)
                    p_def = match_def.group(2).strip()
                    param_names.append(p_name)
                    param_defaults[p_name] = p_def
                else:
                    match_no_def = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:', stripped)
                    if match_no_def:
                        p_name = match_no_def.group(1)
                        param_names.append(p_name)
                        param_defaults[p_name] = "<no_default>"
            elif line.startswith('    ') and not line.startswith('        ') and ':' not in stripped and stripped:
                # Undecorated parameter name on its own line
                match_plain = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)$', stripped)
                if match_plain:
                    p_name = match_plain.group(1)
                    param_names.append(p_name)
                    param_defaults[p_name] = "<no_default>"

    return param_names, param_defaults


def validate() -> int:
    print("Running MolSysMT bidirectional docstring and default validation...")
    
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
                    errors.append(f"{full_name}: Parameter '{p.name}' from signature is not in docstring Parameters section.")
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
        print(f"\nFAILED: Found {len(errors)} bidirectional docstring/default issues across {total_checked} public functions:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(f"PASSED: All {total_checked} public functions have valid, bidirectionally consistent NumPy docstrings with exact default fidelity!")
        return 0

if __name__ == '__main__':
    sys.exit(validate())
