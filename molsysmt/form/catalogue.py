"""What is known about the forms without importing any of them.

Every `molsysmt/form/<plugin>/` directory declares its identity in a `form.json`: the form
name, the category, the file extension, and -- for forms that hold an instance of a class
-- the `(top-level module, class name)` an item of that form has.

Reading those declarations costs one `os.scandir` and 89 small reads, about 2 ms, once per
process. Learning the same facts by importing the plugins costs about 3.9 s and pulls in
every third-party library MolSysMT can talk to, which is what used to happen the first
time anything asked a question about forms.

The class key is compared as **strings**, so recognising an `openmm.Topology` never
imports OpenMM. Only acting on it does.

`devtools/scripts/generate_form_declarations.py` writes the declarations, and
`tests/test_form_plugin_conventions.py` fails if one stops matching its module.
"""

import json
import os
from functools import lru_cache

_catalogue = None


def _load():
    """Read every declaration. Called once; the result is held for the process."""

    global _catalogue

    if _catalogue is not None:
        return _catalogue

    root = os.path.dirname(os.path.abspath(__file__))
    by_form = {}
    with os.scandir(root) as entries:
        for entry in entries:
            if not entry.is_dir() or entry.name == '__pycache__':
                continue
            try:
                with open(os.path.join(entry.path, 'form.json')) as handler:
                    declaration = json.load(handler)
            except FileNotFoundError:
                continue
            declaration['plugin'] = entry.name
            by_form[declaration['form_name']] = declaration

    forms_lowercase = {name.lower(): name for name in by_form}
    class_index = {}
    extension_index = {}
    for name, declaration in by_form.items():
        keys = declaration.get('item_class_keys')
        if keys is None and declaration.get('item_class_key') is not None:
            keys = [declaration['item_class_key']]
        if keys:
            for key in keys:
                if key is not None:
                    class_index[(key[0], key[1])] = name
        extension = declaration.get('extension')
        if extension is not None:
            extension_index[extension.lower()] = name


    _catalogue = {
        'by_form': by_form,
        'forms_lowercase': forms_lowercase,
        'class_index': class_index,
        'extension_index': extension_index,
        'extension_suffixes': tuple(sorted(extension_index, key=len, reverse=True)),
    }
    return _catalogue


def form_names():
    """Every declared form name."""

    return tuple(_load()['by_form'])


def forms_lowercase():
    """Lowercased form name -> the canonical spelling."""

    return _load()['forms_lowercase']


def form_type(form_name):
    """`'file'`, `'string'` or `'class'`, or None when the form is not declared."""

    declaration = _load()['by_form'].get(form_name)
    return None if declaration is None else declaration['form_type']


def plugin_of(form_name):
    """The subpackage implementing a form, or None when it is not declared."""

    declaration = _load()['by_form'].get(form_name)
    return None if declaration is None else declaration['plugin']


def form_of_class(item):
    """The form whose items are instances of this item's class, or None.

    Walks the item's own class and its bases, so a subclass of a supported class is
    recognised as the form it specialises. No import happens: the comparison is between
    the strings a class carries and the strings a form declared.
    """

    index = _load()['class_index']
    for klass in type(item).__mro__:
        module = klass.__module__
        form = index.get((module.split('.', 1)[0], klass.__name__))
        if form is not None:
            return form
    return None


def form_of_extension(name):
    """The file form a path names, or None.

    Longest extension first, so `1l2y.bcif.gz` is a `file:bcif.gz` and not a `file:gz`.
    Molecular text is rejected before suffix inspection, and only extension-sized slices
    are copied. Consequently, auxiliary memory does not grow with an in-memory molecular
    payload or a long path.
    """

    index = _load()['extension_index']
    if '\n' in name or '\r' in name:
        return None

    for extension in _load()['extension_suffixes']:
        suffix_length = len(extension) + 1
        if len(name) < suffix_length:
            continue
        suffix = name[-suffix_length:]
        if suffix[0] == '.' and suffix[1:].lower() == extension:
            return index[extension]
    return None


_modules = {}


def module_of(form_name):
    """Import and return the plugin implementing a form. Only that one.

    The registry cannot do this: it learns a form's name by importing the module that
    declares it, so it has to import all of them before it can hand back any. Here the name
    came from the declaration, so the module is known before it is loaded.
    """

    if form_name in _modules:
        return _modules[form_name]

    plugin = plugin_of(form_name)
    if plugin is None:
        return None

    from importlib import import_module

    module = import_module(f'molsysmt.form.{plugin}')
    _modules[form_name] = module
    return module


@lru_cache(maxsize=None)
def forms_of_type(*form_types):
    """The declared forms of the given categories, in catalogue order. No imports.

    Cached: the sweep that falls back on this asks for the same categories every time, and
    the catalogue does not change while the process runs.
    """

    return tuple(name for name, declaration in _load()['by_form'].items()
                 if declaration['form_type'] in form_types)
