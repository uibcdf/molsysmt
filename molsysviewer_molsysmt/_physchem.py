"""Explicit bound property readers; scientific definitions stay in MolSysMT."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _PhyschemTools:
    _NAMES = (
        "get_mass",
        "get_charge",
        "get_atomic_radius",
        "get_electronegativity",
        "get_hydrophobicity",
        "get_polarity",
        "get_transmembrane_tendency",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt import physchem

        return self._owner._read(getattr(physchem, name), parameters)

    @_native_documentation("get_mass", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_mass(
        self,
        element="system",
        selection="all",
        syntax="MolSysMT",
        definition="physical",
        skip_digestion=False,
    ):
        return self._call(
            "get_mass",
            {
                "element": element,
                "selection": selection,
                "syntax": syntax,
                "definition": definition,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_charge", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_charge(
        self,
        element="group",
        selection="all",
        definition="physical_pH7",
        forcefield="AMBER14",
        water_model=None,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_charge",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "forcefield": forcefield,
                "water_model": water_model,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_atomic_radius", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_atomic_radius(
        self,
        element="atom",
        selection="all",
        definition="vdw",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_atomic_radius",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_electronegativity", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_electronegativity(
        self,
        element="atom",
        selection="all",
        definition="pauling",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_electronegativity",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_hydrophobicity", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hydrophobicity(
        self,
        element="group",
        selection="all",
        definition="eisenberg",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_hydrophobicity",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_polarity", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_polarity(
        self,
        element="group",
        selection="all",
        syntax="MolSysMT",
        definition="grantham",
        skip_digestion=False,
    ):
        return self._call(
            "get_polarity",
            {
                "element": element,
                "selection": selection,
                "syntax": syntax,
                "definition": definition,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_transmembrane_tendency", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_transmembrane_tendency(
        self,
        element="group",
        selection="all",
        syntax="MolSysMT",
        definition="zhao",
        skip_digestion=False,
    ):
        return self._call(
            "get_transmembrane_tendency",
            {
                "element": element,
                "selection": selection,
                "syntax": syntax,
                "definition": definition,
                "skip_digestion": skip_digestion,
            },
        )
