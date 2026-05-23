#!/usr/bin/env python
"""
scaffold_form.py

Developer CLI utility to scaffold a pristine, fully conforming MolSysMT form
adapter directory pre-populated with contract specifications.
"""
import os
import sys
import argparse

# Add repository root to python path to import molsysmt correctly
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new MolSysMT form adapter module with all standard contract files."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Directory name of the form adapter (e.g., 'openff_Topology', 'file_xyz').",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["class", "file", "string"],
        help="Form type contract (class, file, or string).",
    )
    parser.add_argument(
        "--class-name",
        help="Fully qualified class name to check in is_form (e.g., 'Bio.PDB.Structure.Structure'). Only used if type is 'class'.",
    )

    args = parser.parse_args()

    form_dir_name = args.name
    form_type = args.type

    # 1. Infer the canonical form_name
    if form_type == "file":
        if form_dir_name.startswith("file_"):
            suffix = form_dir_name[5:]
        else:
            suffix = form_dir_name
        form_name = f"file:{suffix}"
    elif form_type == "string":
        if form_dir_name.startswith("string_"):
            suffix = form_dir_name[7:]
        else:
            suffix = form_dir_name
        form_name = f"string:{suffix}"
    else:  # class
        form_name = form_dir_name.replace("_", ".")

    dest_dir = os.path.join(REPO_ROOT, "molsysmt", "form", form_dir_name)

    if os.path.exists(dest_dir):
        print(f"Error: Target directory already exists: {dest_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scaffolding new form adapter: {form_name}")
    print(f"Target directory            : {dest_dir}")
    print(f"Form type                   : {form_type}")

    os.makedirs(dest_dir, exist_ok=True)

    # 2. Template content definitions
    # __init__.py template
    init_content = f'''from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .get_topological_attributes import *
from .get_structural_attributes import *

form_name = '{form_name}'
form_type = '{form_type}'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

_convert_to = {{}}
'''

    # is_form.py template
    target_class = args.class_name if args.class_name else "package.module.ClassName"
    if form_type == "file":
        is_form_content = f'''import os

def is_form(item):
    """Check if the item is of form '{form_name}'."""
    output = False
    if isinstance(item, str):
        # Basic check: matches path structure or extension
        if item.endswith('.{form_dir_name.replace("file_", "")}'):
            output = True
    return output
'''
    elif form_type == "string":
        is_form_content = f'''def is_form(item):
    """Check if the item is of form '{form_name}'."""
    output = False
    if isinstance(item, str):
        if item.startswith('{form_name}:'):
            output = True
    return output
'''
    else:  # class
        is_form_content = f'''def is_form(item):
    """Check if the item is of form '{form_name}'."""
    output = False
    class_name = str(type(item))
    if '{target_class}' in class_name:
        output = True
    return output
'''

    # attributes.py template
    attributes_content = f'''from molsysmt.attribute.attributes import attributes as _all_attributes

# Initialize all attributes as unsupported (False)
attributes = {{ii: False for ii in _all_attributes}}

# Enable specific attributes supported by this form here
# Example:
# attributes['n_atoms'] = True

del(_all_attributes)
'''

    # has_attribute.py template
    has_attribute_content = f'''from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='{form_name}')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Check if the form supports the requested attribute."""
    from .attributes import attributes
    return attributes.get(attribute, False)
'''

    # iterators.py template
    iterators_content = f'''from molsysmt.form.iterators import BaseStructuresIterator, BaseTopologyIterator
from molsysmt._private.smonitor import NotImplementedIteratorError

class StructuresIterator(BaseStructuresIterator):
    """Structures iterator implementation for {form_name}."""

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1,
                 structure_indices=None, skip_digestion=True):
        self.molecular_system = molecular_system
        # Initialize resources (e.g. opening files or handles) here

    def __next__(self):
        # Yield coordinates chunk here, or raise StopIteration when done
        raise NotImplementedIteratorError

    def close(self):
        # Release open handles or file descriptors here
        pass

class TopologyIterator(BaseTopologyIterator):
    """Topology iterator implementation for {form_name}."""

    def __init__(self, molecular_system):
        self.molecular_system = molecular_system

    def __next__(self):
        raise NotImplementedIteratorError
'''

    # get_topological_attributes.py template
    get_topological_content = f'''from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import types

form = '{form_name}'

# Implement individual getter functions starting with 'get_' here.
# Example:
# @arg_digest(form=form)
# def get_n_atoms(item, skip_digestion=False):
#     return len(item.atoms)

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
'''

    # get_structural_attributes.py template
    get_structural_content = f'''from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import types

form = '{form_name}'

# Implement individual getter functions starting with 'get_' here.
# Example:
# @arg_digest(form=form)
# def get_coordinates(item, structure_indices='all', atom_indices='all', skip_digestion=False):
#     return item.coordinates

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
'''

    # 3. Write files to target directory
    files_to_write = {
        "__init__.py": init_content,
        "is_form.py": is_form_content,
        "attributes.py": attributes_content,
        "has_attribute.py": has_attribute_content,
        "iterators.py": iterators_content,
        "get_topological_attributes.py": get_topological_content,
        "get_structural_attributes.py": get_structural_content,
    }

    for fname, content in files_to_write.items():
        fpath = os.path.join(dest_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  • Created: {fname}")

    print("\n" + "=" * 80)
    print("SCAFFOLDING COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("Next Steps for implementing the form adapter:")
    print("1. Define the class matching rules in is_form.py.")
    print("2. Set supported attributes in attributes.py.")
    print("3. Implement any supported topological getters in get_topological_attributes.py.")
    print("4. Implement any supported structural getters in get_structural_attributes.py.")
    print("5. Create converters (e.g. to_molsysmt_MolSys.py) and register them in _convert_to in __init__.py.")
    print("6. Run the QA conformance linter to verify your new form adapter:")
    print("   python devtools/scripts/validate_form_adapters.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
