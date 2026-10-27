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
        "get_protor_atom_type",
        "get_protor_vdw_radius",
        "get_surface_area",
        "get_volume",
        "get_area_buried",
        "get_buried_fraction",
        "get_sasa",
        "get_hydrogen_inventory",
        "get_chemical_readiness",
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

    @_native_documentation("get_protor_atom_type", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_protor_atom_type(
        self, selection="all", syntax="MolSysMT", skip_digestion=False
    ):
        return self._call(
            "get_protor_atom_type",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_protor_vdw_radius", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_protor_vdw_radius(
        self, selection="all", syntax="MolSysMT", skip_digestion=False
    ):
        return self._call(
            "get_protor_vdw_radius",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_surface_area", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_surface_area(
        self,
        element="group",
        selection="all",
        syntax="MolSysMT",
        definition="collantes",
        skip_digestion=False,
    ):
        return self._call(
            "get_surface_area",
            {
                "element": element,
                "selection": selection,
                "syntax": syntax,
                "definition": definition,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_volume", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_volume(
        self,
        selection="all",
        syntax="MolSysMT",
        definition="grantham",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_volume",
            {
                "selection": selection,
                "syntax": syntax,
                "definition": definition,
            },
        )

    @_native_documentation("get_area_buried", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_area_buried(
        self, element="group", selection="all", definition="rose", skip_digestion=False
    ):
        return self._call(
            "get_area_buried",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_buried_fraction", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_buried_fraction(
        self,
        element="group",
        selection="all",
        definition="janin",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_buried_fraction",
            {
                "element": element,
                "selection": selection,
                "definition": definition,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_sasa", module="physchem")
    @signal(tags=["addon", "physchem"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_sasa(
        self,
        element="atom",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        probe_radius="1.4 angstroms",
        n_sphere_points=240,
        use_cell_list="auto",
        use_gpu=None,
        gpu_backend=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
        *,
        pbc=True,
    ):
        return self._call(
            "get_sasa",
            {
                "element": element,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "engine": engine,
                "probe_radius": probe_radius,
                "n_sphere_points": n_sphere_points,
                "use_cell_list": use_cell_list,
                "use_gpu": use_gpu,
                "gpu_backend": gpu_backend,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
                "pbc": pbc,
            },
        )

    @_native_documentation("get_hydrogen_inventory", module="physchem")
    @signal(tags=["addon", "physchem", "diagnostics"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_hydrogen_inventory(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_hydrogen_inventory",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_chemical_readiness", module="physchem")
    @signal(tags=["addon", "physchem", "diagnostics"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_chemical_readiness(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_chemical_readiness",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )
