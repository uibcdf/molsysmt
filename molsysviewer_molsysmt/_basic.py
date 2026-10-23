"""Thin explicit scientific wrappers; no unknown mutating exports are proxied."""

import inspect
import re

from argdigest import arg_digest
from smonitor import signal


def _native_documentation(name):
    def decorate(function):
        from molsysmt import basic

        doc = inspect.getdoc(getattr(basic, name)) or ""
        doc = re.sub(
            r"(?m)^molecular_system :[^\n]*\n(?:[ \t]+[^\n]*\n|\n)*",
            "",
            doc,
            count=1,
        )
        # Keep the provider's parameter/result definitions as the help source.
        # Examples are explicitly native calls, not invented addon signatures.
        first, _, rest = doc.partition("\n")
        function.__doc__ = (
            first + "\n\nThe primary molecular system is the current view.molsys. "
            "The remaining parameters and returns follow the native function below. "
            "Its examples show ordinary MolSysMT calls.\n" + rest
        )
        return function

    return decorate


class _BasicTools:
    _NAMES = (
        "get",
        "select",
        "info",
        "get_attributes",
        "has_attribute",
        "get_label",
        "extract",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        if extra and "molecular_system" in extra:
            raise TypeError(
                "The primary molecular_system is bound to view.molsys and cannot be overridden."
            )
        target = self._owner._target()
        from molsysmt import basic

        return getattr(basic, name)(target, **parameters, **(extra or {}))

    @_native_documentation("get")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        mask=None,
        syntax="MolSysMT",
        get_missing_bonds=True,
        output_type="values",
        chemical_state="reference",
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get",
            {
                "element": element,
                "selection": selection,
                "structure_indices": structure_indices,
                "mask": mask,
                "syntax": syntax,
                "get_missing_bonds": get_missing_bonds,
                "output_type": output_type,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("select")
    @signal(tags=["addon", "selection"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def select(
        self,
        selection="all",
        structure_indices="all",
        element="atom",
        mask=None,
        syntax="MolSysMT",
        to_syntax=None,
        chemical_state="reference",
        skip_digestion=False,
    ):
        return self._call(
            "select",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "element": element,
                "mask": mask,
                "syntax": syntax,
                "to_syntax": to_syntax,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("info")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def info(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        output_type="styler",
        skip_digestion=False,
        *,
        mask=None,
    ):
        return self._call(
            "info",
            {
                "element": element,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "output_type": output_type,
                "skip_digestion": skip_digestion,
                "mask": mask,
            },
        )

    @_native_documentation("get_attributes")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_attributes(
        self,
        include_none=False,
        attribute_type="all",
        output_type="list",
        skip_digestion=False,
    ):
        return self._call(
            "get_attributes",
            {
                "include_none": include_none,
                "attribute_type": attribute_type,
                "output_type": output_type,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("has_attribute")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def has_attribute(
        self,
        attribute,
        include_none=False,
        structure_indices="all",
        chemical_state="reference",
        skip_digestion=False,
    ):
        return self._call(
            "has_attribute",
            {
                "attribute": attribute,
                "include_none": include_none,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_label")
    @signal(tags=["addon", "get"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_label(
        self,
        element="atom",
        selection="all",
        string="{name}-{id}@{index}",
        syntax="MolSysMT",
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get_label",
            {
                "element": element,
                "selection": selection,
                "string": string,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("extract")
    @signal(tags=["addon", "extract"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def extract(
        self,
        selection="all",
        structure_indices="all",
        to_form=None,
        output_filename=None,
        copy_if_all=True,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "extract",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "to_form": to_form,
                "output_filename": output_filename,
                "copy_if_all": copy_if_all,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )
