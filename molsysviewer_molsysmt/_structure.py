"""Explicit primary-bound structure tools; scientific behavior remains native."""

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
        "translate",
        "rotate",
        "flip",
        "least_rmsd_fit",
        "least_rmsd_align",
        "center",
        "move_away",
        "align_principal_axes",
        "set_dihedral_angles",
        "shift_dihedral_angles",
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

    @_native_documentation("translate", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def translate(
        self,
        translation=None,
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "translate",
            {
                "translation": translation,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("rotate", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def rotate(
        self,
        rotation=None,
        rotation_center=None,
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "rotate",
            {
                "rotation": rotation,
                "rotation_center": rotation_center,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("flip", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def flip(
        self,
        vector=None,
        point="[0,0,0] nm",
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        in_place=False,
        *,
        skip_digestion=False,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "flip",
            {
                "vector": vector,
                "point": point,
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "in_place": in_place,
            },
            update_view,
        )

    @_native_documentation("least_rmsd_fit", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def least_rmsd_fit(
        self,
        selection="all",
        selection_fit='atom_type!="H"',
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection_fit=None,
        reference_structure_index=0,
        to_form=None,
        in_place=False,
        syntax="MolSysMT",
        engine="MolSysMT",
        parallel=None,
        num_threads=None,
        use_gpu=None,
        gpu_backend=None,
        precision=None,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "least_rmsd_fit",
            {
                "selection": selection,
                "selection_fit": selection_fit,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection_fit": reference_selection_fit,
                "reference_structure_index": reference_structure_index,
                "to_form": to_form,
                "in_place": in_place,
                "syntax": syntax,
                "engine": engine,
                "parallel": parallel,
                "num_threads": num_threads,
                "use_gpu": use_gpu,
                "gpu_backend": gpu_backend,
                "precision": precision,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("least_rmsd_align", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def least_rmsd_align(
        self,
        selection='atom_name=="CA"',
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection=None,
        reference_structure_index=0,
        syntax="MolSysMT",
        engine_sequence_alignment="Biopython",
        engine_least_rmsd_fit="MolSysMT",
        in_place=False,
        use_gpu=None,
        gpu_backend=None,
        precision=None,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "least_rmsd_align",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "reference_structure_index": reference_structure_index,
                "syntax": syntax,
                "engine_sequence_alignment": engine_sequence_alignment,
                "engine_least_rmsd_fit": engine_least_rmsd_fit,
                "in_place": in_place,
                "use_gpu": use_gpu,
                "gpu_backend": gpu_backend,
                "precision": precision,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("center", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def center(
        self,
        selection="all",
        source_center_selection=None,
        target_center_selection=None,
        target_coordinates=None,
        weights=None,
        structure_indices="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "center",
            {
                "selection": selection,
                "source_center_selection": source_center_selection,
                "target_center_selection": target_center_selection,
                "target_coordinates": target_coordinates,
                "weights": weights,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "engine": engine,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("move_away", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def move_away(
        self,
        selection="all",
        center_of_selection="all",
        weights=None,
        structure_indices=0,
        reference_molecular_system=None,
        reference_center_of_selection="all",
        reference_weights=None,
        reference_structure_indices=None,
        direction=None,
        distance="3 angstroms",
        in_place=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "move_away",
            {
                "selection": selection,
                "center_of_selection": center_of_selection,
                "weights": weights,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_center_of_selection": reference_center_of_selection,
                "reference_weights": reference_weights,
                "reference_structure_indices": reference_structure_indices,
                "direction": direction,
                "distance": distance,
                "in_place": in_place,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )

    @_native_documentation("align_principal_axes", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def align_principal_axes(
        self,
        selection="all",
        principal_axes_of_selection=None,
        principal_axes_type="inertia",
        structure_indices="all",
        weights=None,
        axes=None,
        center=False,
        syntax="MolSysMT",
        engine="MolSysMT",
        in_place=False,
        *,
        skip_digestion=False,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "align_principal_axes",
            {
                "selection": selection,
                "principal_axes_of_selection": principal_axes_of_selection,
                "principal_axes_type": principal_axes_type,
                "structure_indices": structure_indices,
                "weights": weights,
                "axes": axes,
                "center": center,
                "syntax": syntax,
                "engine": engine,
                "in_place": in_place,
            },
            update_view,
        )

    @_native_documentation("set_dihedral_angles", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def set_dihedral_angles(
        self,
        dihedral_quartets=None,
        angles=None,
        blocks=None,
        structure_indices="all",
        pbc=True,
        in_place=False,
        engine="MolSysMT",
        *,
        skip_digestion=False,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "set_dihedral_angles",
            {
                "dihedral_quartets": dihedral_quartets,
                "angles": angles,
                "blocks": blocks,
                "structure_indices": structure_indices,
                "pbc": pbc,
                "in_place": in_place,
                "engine": engine,
            },
            update_view,
        )

    @_native_documentation("shift_dihedral_angles", module="structure")
    @signal(tags=["addon", "structure", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def shift_dihedral_angles(
        self,
        dihedral_quartets=None,
        shifts=None,
        blocks=None,
        structure_indices="all",
        pbc=True,
        in_place=False,
        engine="MolSysMT",
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "shift_dihedral_angles",
            {
                "dihedral_quartets": dihedral_quartets,
                "shifts": shifts,
                "blocks": blocks,
                "structure_indices": structure_indices,
                "pbc": pbc,
                "in_place": in_place,
                "engine": engine,
                "skip_digestion": skip_digestion,
            },
            update_view,
        )
