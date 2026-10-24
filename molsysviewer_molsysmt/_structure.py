"""Explicit primary-bound geometric readers; scientific behavior remains native."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _StructureTools:
    _NAMES = (
        "get_distances",
        "get_vectors",
        "get_center",
        "get_radius_of_gyration",
        "get_angles",
        "get_dihedral_angles",
        "get_rmsd",
        "get_least_rmsd",
        "get_principal_axes",
        "get_least_squares_plane",
        "get_maximum_distances",
        "get_contacts",
        "get_rmsf",
        "get_minimum_distances",
        "get_neighbors",
        "get_symmetry_corrected_rmsd",
        "get_secondary_structure",
        "principal_component_analysis",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        from molsysmt import structure

        return self._owner._read(getattr(structure, name), parameters, extra)

    @_native_documentation("get_distances", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_distances(
        self,
        selection="all",
        structure_indices="all",
        center_of_atoms=False,
        weights=None,
        molecular_system_2=None,
        selection_2=None,
        structure_indices_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        pairs=False,
        pbc=True,
        output_type="numpy.ndarray",
        output_indices=None,
        output_structure_indices=None,
        engine="MolSysMT",
        syntax="MolSysMT",
        heavy_mode="auto",
        use_gpu=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_distances",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "center_of_atoms": center_of_atoms,
                "weights": weights,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "structure_indices_2": structure_indices_2,
                "center_of_atoms_2": center_of_atoms_2,
                "weights_2": weights_2,
                "pairs": pairs,
                "pbc": pbc,
                "output_type": output_type,
                "output_indices": output_indices,
                "output_structure_indices": output_structure_indices,
                "engine": engine,
                "syntax": syntax,
                "heavy_mode": heavy_mode,
                "use_gpu": use_gpu,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_vectors", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_vectors(
        self,
        selection="all",
        structure_indices="all",
        center_of_atoms=False,
        weights=None,
        molecular_system_2=None,
        selection_2=None,
        structure_indices_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        pairs=False,
        pbc=True,
        output_type="numpy.ndarray",
        output_indices=None,
        output_structure_indices=None,
        engine="MolSysMT",
        syntax="MolSysMT",
        heavy_mode="auto",
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_vectors",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "center_of_atoms": center_of_atoms,
                "weights": weights,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "structure_indices_2": structure_indices_2,
                "center_of_atoms_2": center_of_atoms_2,
                "weights_2": weights_2,
                "pairs": pairs,
                "pbc": pbc,
                "output_type": output_type,
                "output_indices": output_indices,
                "output_structure_indices": output_structure_indices,
                "engine": engine,
                "syntax": syntax,
                "heavy_mode": heavy_mode,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_center", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_center(
        self,
        selection="all",
        weights=None,
        structure_indices="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        heavy_mode="auto",
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_center",
            {
                "selection": selection,
                "weights": weights,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "engine": engine,
                "heavy_mode": heavy_mode,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_radius_of_gyration", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_radius_of_gyration(
        self,
        selection="all",
        structure_indices="all",
        weights=None,
        syntax="MolSysMT",
        engine="MolSysMT",
        heavy_mode="auto",
        use_gpu=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_radius_of_gyration",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "weights": weights,
                "syntax": syntax,
                "engine": engine,
                "heavy_mode": heavy_mode,
                "use_gpu": use_gpu,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_angles", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_angles(
        self,
        triplets,
        structure_indices="all",
        pbc=False,
        use_gpu=None,
        gpu_backend=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_angles",
            {
                "triplets": triplets,
                "structure_indices": structure_indices,
                "pbc": pbc,
                "use_gpu": use_gpu,
                "gpu_backend": gpu_backend,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_dihedral_angles", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_dihedral_angles(
        self,
        selection="all",
        dihedral_quartets=None,
        structure_indices="all",
        syntax="MolSysMT",
        pbc=False,
        use_gpu=None,
        *,
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get_dihedral_angles",
            {
                "selection": selection,
                "dihedral_quartets": dihedral_quartets,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "pbc": pbc,
                "use_gpu": use_gpu,
            },
            kwargs,
        )

    @_native_documentation("get_rmsd", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_rmsd(
        self,
        selection='atom_type!="H"',
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection=None,
        reference_structure_index=0,
        syntax="MolSysMT",
        engine="MolSysMT",
        heavy_mode="auto",
        use_gpu=None,
        parallel=None,
        num_threads=None,
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_rmsd",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "reference_structure_index": reference_structure_index,
                "syntax": syntax,
                "engine": engine,
                "heavy_mode": heavy_mode,
                "use_gpu": use_gpu,
                "parallel": parallel,
                "num_threads": num_threads,
            },
        )

    @_native_documentation("get_least_rmsd", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_least_rmsd(
        self,
        selection='atom_type!="H"',
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection=None,
        reference_structure_index=0,
        syntax="MolSysMT",
        engine="MolSysMT",
        use_gpu=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_least_rmsd",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "reference_structure_index": reference_structure_index,
                "syntax": syntax,
                "engine": engine,
                "use_gpu": use_gpu,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_principal_axes", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_principal_axes(
        self,
        selection="all",
        structure_indices="all",
        weights=None,
        principal_axes_type="inertia",
        syntax="MolSysMT",
        engine="MolSysMT",
        use_gpu=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_principal_axes",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "weights": weights,
                "principal_axes_type": principal_axes_type,
                "syntax": syntax,
                "engine": engine,
                "use_gpu": use_gpu,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_least_squares_plane", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_least_squares_plane(
        self,
        selection="all",
        structure_indices="all",
        pbc=False,
        syntax="MolSysMT",
        heavy_mode="auto",
        skip_digestion=False,
    ):
        return self._call(
            "get_least_squares_plane",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "pbc": pbc,
                "syntax": syntax,
                "heavy_mode": heavy_mode,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_maximum_distances", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_maximum_distances(
        self,
        selection="all",
        center_of_atoms=False,
        weights=None,
        as_entity=True,
        structure_indices="all",
        molecular_system_2=None,
        selection_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        as_entity_2=True,
        structure_indices_2=None,
        pairs=False,
        pbc=False,
        engine="MolSysMT",
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_maximum_distances",
            {
                "selection": selection,
                "center_of_atoms": center_of_atoms,
                "weights": weights,
                "as_entity": as_entity,
                "structure_indices": structure_indices,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "center_of_atoms_2": center_of_atoms_2,
                "weights_2": weights_2,
                "as_entity_2": as_entity_2,
                "structure_indices_2": structure_indices_2,
                "pairs": pairs,
                "pbc": pbc,
                "engine": engine,
                "syntax": syntax,
            },
        )

    @_native_documentation("get_contacts", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_contacts(
        self,
        selection=None,
        center_of_atoms=False,
        weights=None,
        structure_indices="all",
        selection_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        structure_indices_2=None,
        threshold="12 angstroms",
        pairs=False,
        pbc=True,
        syntax="MolSysMT",
        output_type="numpy.ndarray",
        output_indices=None,
        use_gpu=None,
        gpu_backend=None,
        cell_list=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_contacts",
            {
                "selection": selection,
                "center_of_atoms": center_of_atoms,
                "weights": weights,
                "structure_indices": structure_indices,
                "selection_2": selection_2,
                "center_of_atoms_2": center_of_atoms_2,
                "weights_2": weights_2,
                "structure_indices_2": structure_indices_2,
                "threshold": threshold,
                "pairs": pairs,
                "pbc": pbc,
                "syntax": syntax,
                "output_type": output_type,
                "output_indices": output_indices,
                "use_gpu": use_gpu,
                "gpu_backend": gpu_backend,
                "cell_list": cell_list,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_rmsf", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_rmsf(
        self,
        selection='atom_type!="H"',
        structure_indices="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        heavy_mode="auto",
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "get_rmsf",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "engine": engine,
                "heavy_mode": heavy_mode,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_minimum_distances", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_minimum_distances(
        self,
        selection="all",
        center_of_atoms=False,
        weights=None,
        as_entity=True,
        structure_indices="all",
        molecular_system_2=None,
        selection_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        as_entity_2=True,
        structure_indices_2=None,
        pairs=False,
        pbc=False,
        engine="MolSysMT",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_minimum_distances",
            {
                "selection": selection,
                "center_of_atoms": center_of_atoms,
                "weights": weights,
                "as_entity": as_entity,
                "structure_indices": structure_indices,
                "molecular_system_2": molecular_system_2,
                "selection_2": selection_2,
                "center_of_atoms_2": center_of_atoms_2,
                "weights_2": weights_2,
                "as_entity_2": as_entity_2,
                "structure_indices_2": structure_indices_2,
                "pairs": pairs,
                "pbc": pbc,
                "engine": engine,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_neighbors", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_neighbors(
        self,
        selection="all",
        structure_indices="all",
        center_of_atoms=False,
        weights=None,
        molecular_system_2=None,
        selection_2=None,
        structure_indices_2=None,
        center_of_atoms_2=False,
        weights_2=None,
        threshold=None,
        n_neighbors=None,
        pairs=False,
        unique_pairs=False,
        mutual_only=False,
        pbc=True,
        output_type="numpy.ndarray",
        output_indices=None,
        output_structure_indices=None,
        sorted=True,
        engine="MolSysMT",
        syntax="MolSysMT",
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        parameters = {
            "selection": selection,
            "structure_indices": structure_indices,
            "center_of_atoms": center_of_atoms,
            "weights": weights,
            "molecular_system_2": molecular_system_2,
            "selection_2": selection_2,
            "structure_indices_2": structure_indices_2,
            "center_of_atoms_2": center_of_atoms_2,
            "weights_2": weights_2,
            "threshold": threshold,
            "n_neighbors": n_neighbors,
            "pairs": pairs,
            "unique_pairs": unique_pairs,
            "mutual_only": mutual_only,
            "pbc": pbc,
            "output_type": output_type,
            "output_indices": output_indices,
            "output_structure_indices": output_structure_indices,
            "sorted": sorted,
            "engine": engine,
            "syntax": syntax,
            "parallel": parallel,
            "num_threads": num_threads,
            "skip_digestion": skip_digestion,
        }
        # Preserve native criterion admission before forwarding wrapper defaults.
        # An omitted criterion must remain omitted at the native public boundary.
        for name in ("threshold", "n_neighbors"):
            if parameters[name] is None:
                del parameters[name]
        return self._call("get_neighbors", parameters)

    @_native_documentation("get_symmetry_corrected_rmsd", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_symmetry_corrected_rmsd(
        self,
        selection='atom_type!="H"',
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection=None,
        reference_structure_index=0,
        chemical_state="reference",
        reference_chemical_state="reference",
        correspondences=None,
        baseline_atom_correspondence=None,
        method="declared_graph_isomorphism",
        max_matches=100000,
        tie_tolerance="1e-12 nm",
        syntax="MolSysMT",
        heavy_mode="auto",
        parallel=None,
        num_threads=None,
        skip_digestion=False,
        *,
        fixed_atom_correspondence=None,
        candidate_atom_correspondences=None,
    ):
        return self._call(
            "get_symmetry_corrected_rmsd",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "reference_structure_index": reference_structure_index,
                "chemical_state": chemical_state,
                "reference_chemical_state": reference_chemical_state,
                "correspondences": correspondences,
                "baseline_atom_correspondence": baseline_atom_correspondence,
                "method": method,
                "max_matches": max_matches,
                "tie_tolerance": tie_tolerance,
                "syntax": syntax,
                "heavy_mode": heavy_mode,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
                "fixed_atom_correspondence": fixed_atom_correspondence,
                "candidate_atom_correspondences": candidate_atom_correspondences,
            },
        )

    @_native_documentation("get_secondary_structure", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_secondary_structure(
        self,
        selection="all",
        structure_indices="all",
        simplified=True,
        syntax="MolSysMT",
        engine="MDTraj",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_secondary_structure",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "simplified": simplified,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("principal_component_analysis", module="structure")
    @signal(tags=["addon", "structure"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def principal_component_analysis(
        self,
        selection="all",
        structure_indices="all",
        weights=None,
        syntax="MolSysMT",
        engine="MolSysMT",
        use_gpu=None,
        parallel=None,
        num_threads=None,
        skip_digestion=False,
    ):
        return self._call(
            "principal_component_analysis",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "weights": weights,
                "syntax": syntax,
                "engine": engine,
                "use_gpu": use_gpu,
                "parallel": parallel,
                "num_threads": num_threads,
                "skip_digestion": skip_digestion,
            },
        )
