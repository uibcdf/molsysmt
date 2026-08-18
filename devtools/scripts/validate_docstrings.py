#!/usr/bin/env python
"""Validate docstring completeness and formatting across MolSysMT."""

import inspect
import sys
import molsysmt as msm
import pkgutil

EXEMPT_RETURNS = {
    'close', 'clear', 'info', 'show_gui', 'standardize_view', 'write_html', 'view',
    'add_arrows', 'add_contacts', 'add_cylinders', 'add_hbonds',
    'show_as_balls_and_sticks', 'show_as_cartoon', 'show_as_licorice', 'show_as_surface',
    'set_color'
}

def validate():
    print("Running MolSysMT docstring validation...")
    
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
            params = [p for p in sig.parameters.keys() if p not in ('self', 'cls')]
        except Exception:
            params = []

        if params and 'Parameters' not in doc:
            errors.append(f"{full_name}: Missing 'Parameters' section.")
        elif params:
            for p in params:
                if p not in doc and p != 'kwargs' and p != 'args':
                    errors.append(f"{full_name}: Parameter '{p}' is not documented in docstring.")

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
        print(f"\nFAILED: Found {len(errors)} docstring issues across {total_checked} public functions:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(f"PASSED: All {total_checked} public functions have valid, complete docstrings!")
        return 0

if __name__ == '__main__':
    sys.exit(validate())
