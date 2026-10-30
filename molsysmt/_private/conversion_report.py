"""Building capability- and instance-aware chemical conversion preflight reports."""

from molsysmt.basic.conversion_report import ConversionIssue, ConversionReport

_CHEMICAL_ATTRIBUTES = (
    "isotope",
    "formal_charge",
    "atom_is_aromatic",
    "n_unpaired_electrons",
    "n_implicit_hydrogens",
    "n_explicit_hydrogens",
    "allows_implicit_hydrogens",
    "atom_stereochemistry",
    "bond_id",
    "bond_order",
    "fractional_bond_order",
    "bond_type",
    "bond_is_aromatic",
    "bond_is_conjugated",
    "bond_stereochemistry",
    "bond_stereo_atom_indices",
    "bond_donor_atom_index",
    "bond_acceptor_atom_index",
    "bond_joins_components",
    "bond_evidence",
    "connectivity_completeness",
    "component_completeness",
    "component_evidence",
)

# Static route coverage is deliberately conservative. A pair belongs here only
# after its complete source semantics are traversed by the preflight and covered
# by executable evidence. Stage A2 activates native declarative pairs as their
# schema-driven audits land.
_STRUCTURES_TO_STRUCTURES_DICT_PROFILE = {
    "directly_preserved": frozenset(
        {
            "structure_id",
            "time",
            "box",
            "coordinates",
            "velocities",
            "occupancy",
            "b_factor",
            "alternate_location",
            "temperature",
            "potential_energy",
            "kinetic_energy",
        }
    ),
    "derived_without_loss": frozenset(
        {
            "atom_index",
            "n_atoms",
            "structure_index",
            "box_shape",
            "box_angles",
            "box_lengths",
            "box_volume",
            "n_structures",
        }
    ),
    "covered_by_dependencies": {
        "n_bioassemblies": "bioassembly",
        "total_energy": ("potential_energy", "kinetic_energy"),
    },
    "loss_candidates": ("bioassembly",),
}

_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE = {
    "directly_preserved": frozenset(
        {
            "atom_id",
            "atom_name",
            "atom_type",
            "isotope",
            "group_id",
            "group_name",
            "group_type",
            "chain_id",
            "chain_name",
            "chain_type",
            "molecule_id",
            "molecule_name",
            "molecule_type",
            "entity_id",
            "entity_name",
            "entity_type",
        }
    ),
    "derived_without_loss": frozenset(
        {
            "atom_index",
            "group_index",
            "chain_index",
            "molecule_index",
            "entity_index",
            "n_atoms",
            "n_groups",
            "n_chains",
            "n_molecules",
            "n_entities",
            "n_amino_acids",
            "n_nucleotides",
            "n_ions",
            "n_waters",
            "n_small_molecules",
            "n_peptides",
            "n_proteins",
            "n_dnas",
            "n_rnas",
            "n_lipids",
            "n_polysaccharides",
            "n_saccharides",
        }
    ),
    "covered_by_dependencies": {},
    "loss_candidates": (),
}

_MOLSYS_TO_MOLSYS_DICT_PROFILE = {
    "directly_preserved": (
        _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE["directly_preserved"]
        | frozenset(
            {
                "structure_id",
                "time",
                "box",
                "coordinates",
                "allows_implicit_hydrogens",
                "alternate_location",
                "atom_is_aromatic",
                "atom_stereochemistry",
                "b_factor",
                "bioassembly",
                "bond_acceptor_atom_index",
                "bond_donor_atom_index",
                "bond_evidence",
                "bond_id",
                "bond_index",
                "bond_is_aromatic",
                "bond_is_conjugated",
                "bond_joins_components",
                "bond_order",
                "bond_stereo_atom_indices",
                "bond_stereochemistry",
                "bond_type",
                "bonded_atom_pairs",
                "bonded_atoms",
                "chemical_state_id",
                "chemical_state_index",
                "component_completeness",
                "component_evidence",
                "component_id",
                "component_index",
                "component_name",
                "component_type",
                "connectivity_completeness",
                "formal_charge",
                "fractional_bond_order",
                "inner_bond_index",
                "inner_bonded_atom_pairs",
                "inner_bonded_atoms",
                "kinetic_energy",
                "n_bonds",
                "n_chemical_states",
                "n_components",
                "n_explicit_hydrogens",
                "n_implicit_hydrogens",
                "n_inner_bonds",
                "n_unpaired_electrons",
                "occupancy",
                "potential_energy",
                "reference_chemical_state_index",
                "structure_chemical_state_index",
                "temperature",
                "velocities",
            }
        )
    ),
    "derived_without_loss": (
        _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE["derived_without_loss"]
        | frozenset(
            {
                "structure_index",
                "box_shape",
                "box_angles",
                "box_lengths",
                "box_volume",
                "n_structures",
            }
        )
    ),
    "covered_by_dependencies": {
        **_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE["covered_by_dependencies"],
        "n_bioassemblies": "bioassembly",
        "total_energy": ("potential_energy", "kinetic_energy"),
    },
    "loss_candidates": (
        "partial_charge",
        "atom_ff_type",
        "forcefield",
        "non_bonded_method",
        "cutoff_distance",
        "switch_distance",
        "dispersion_correction",
        "ewald_error_tolerance",
        "hydrogen_mass",
        "constraints",
        "flexible_constraints",
        "water_model",
        "rigid_water",
        "implicit_solvent",
        "solute_dielectric",
        "solvent_dielectric",
        "salt_concentration",
        "kappa",
    ),
}

_DECLARED_CAPABILITY_PROJECTION_PROFILE = {
    "mode": "declared_capability_projection",
}

_MOLSYS_TO_BUILDER_PROFILE = {
    "mode": "molsys_to_builder",
}

_BUILDER_TO_MOLSYS_DICT_PROFILE = {
    "mode": "builder_to_molsysdict",
}

_PDB_WRITE_PROFILE = {
    "mode": "pdb_write",
}

_PDB_READ_PROFILE = {
    "mode": "pdb_read",
}

_COORDINATE_TRAJECTORY_PROFILE = {
    "mode": "coordinate_trajectory",
}

_H5MSM_TO_STRUCTURES_PROFILE = {
    "mode": "h5msm_to_structures",
}

_CONVERSION_AUDIT_PROFILES = {
    (
        "molsysmt.Structures",
        "molsysmt.StructuresDict",
    ): _STRUCTURES_TO_STRUCTURES_DICT_PROFILE,
    (
        "molsysmt.Topology",
        "molsysmt.TopologyDict",
    ): _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE,
    (
        "molsysmt.MolSys",
        "molsysmt.MolSysDict",
    ): _MOLSYS_TO_MOLSYS_DICT_PROFILE,
    (
        "molsysmt.MolSys",
        "molsysmt.TopologyDict",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.MolSysBuilder",
        "molsysmt.TopologyDict",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.MolSys",
        "molsysmt.Topology",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.MolSys",
        "molsysmt.Structures",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.Topology",
        "molsysmt.MolSys",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.Structures",
        "molsysmt.MolSys",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.StructuresDict",
        "molsysmt.MolSys",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.StructuresDict",
        "molsysmt.Topology",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.MolSys",
        "molsysmt.MolSysBuilder",
    ): _MOLSYS_TO_BUILDER_PROFILE,
    (
        "molsysmt.MolSysBuilder",
        "molsysmt.MolSys",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        "molsysmt.MolSysBuilder",
        "molsysmt.MolSysDict",
    ): _BUILDER_TO_MOLSYS_DICT_PROFILE,
    (
        "molsysmt.MolSysDict",
        "molsysmt.MolSysBuilder",
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    ("molsysmt.MolSys", "string:pdb_text"): _PDB_WRITE_PROFILE,
    ("molsysmt.MolSys", "file:pdb"): _PDB_WRITE_PROFILE,
    ("file:h5msm", "molsysmt.Structures"): _H5MSM_TO_STRUCTURES_PROFILE,
    (
        "molsysmt.H5MSMFileHandler",
        "molsysmt.Structures",
    ): _H5MSM_TO_STRUCTURES_PROFILE,
}

for _pdb_source_form in (
    "file:pdb",
    "string:pdb_text",
    "molsysmt.PDBFileHandler",
):
    for _pdb_target_form in (
        "molsysmt.MolSys",
        "molsysmt.Topology",
        "molsysmt.Structures",
    ):
        _CONVERSION_AUDIT_PROFILES[(_pdb_source_form, _pdb_target_form)] = (
            _PDB_READ_PROFILE
        )

del _pdb_source_form, _pdb_target_form

for _coordinate_pair in (
    ("XYZ", "molsysmt.Structures"),
    ("XYZ", "molsysmt.MolSys"),
    ("XYZ", "molsysmt.Topology"),
    ("XYZ", "file:xyznpy"),
    ("file:xyznpy", "XYZ"),
    ("file:xyz", "XYZ"),
    ("file:dcd", "molsysmt.Structures"),
    ("file:dcd", "molsysmt.MolSys"),
    ("file:dcd", "file:h5msm"),
    ("mdtraj.DCDTrajectoryFile", "molsysmt.Structures"),
    ("mdtraj.DCDTrajectoryFile", "molsysmt.MolSys"),
    ("file:xtc", "molsysmt.Structures"),
    ("file:xtc", "mdtraj.Trajectory"),
    ("file:xtc", "file:h5msm"),
    ("mdtraj.XTCTrajectoryFile", "molsysmt.Structures"),
):
    _CONVERSION_AUDIT_PROFILES[_coordinate_pair] = _COORDINATE_TRAJECTORY_PROFILE

del _coordinate_pair

_EXHAUSTIVE_AUDIT_PAIRS = frozenset(_CONVERSION_AUDIT_PROFILES)


def get_conversion_audit_scopes(source_form, target_form):
    """Returning the statically supported preflight scopes for a form pair."""

    pair = (source_form, target_form)
    if pair in _EXHAUSTIVE_AUDIT_PAIRS:
        return ("all",)
    if source_form == target_form:
        return ("representation",)
    return ("chemical_state",)


def is_conversion_audit_exhaustive(source_form, target_form):
    """Returning whether static preflight coverage is exhaustive for a pair."""

    return (source_form, target_form) in _EXHAUSTIVE_AUDIT_PAIRS


def _canonical_target_form(to_form):
    from molsysmt.form import _dict_modules

    if to_form in _dict_modules:
        return to_form
    from molsysmt.basic import get_form

    return get_form(to_form)


def _single_source(molecular_system, from_form):
    if isinstance(from_form, (list, tuple)):
        return None, tuple(from_form)
    return molecular_system, from_form


def _audit_native_structures_to_dict(item):
    """Return current Structures payloads omitted by StructuresDict."""

    profile = _STRUCTURES_TO_STRUCTURES_DICT_PROFILE
    issues = []
    for attribute in profile["loss_candidates"]:
        if getattr(item, attribute) is not None:
            issues.append(
                ConversionIssue(
                    attribute=attribute,
                    reason=(
                        "molsysmt.StructuresDict cannot represent the supplied "
                        f"{attribute} semantics."
                    ),
                    kind="schema_limitation",
                    scope="structures",
                )
            )
    return issues


def _schema_limitation(attribute, target_form, scope="chemical_state"):
    return ConversionIssue(
        attribute=attribute,
        reason=(f"{target_form} cannot represent the supplied {attribute} semantics."),
        kind="schema_limitation",
        scope=scope,
    )


def _states_have_atom_column(states, column):
    return any(
        column in state.atom_attributes and state.atom_attributes[column].notna().any()
        for state in states
    )


def _states_have_bond_column(states, column, predicate=None):
    for state in states:
        if column not in state.bonds or not state.bonds[column].notna().any():
            continue
        if predicate is None or predicate(state.bonds):
            return True
    return False


def _aromatic_flag_is_not_preserved(bonds):
    aromatic = bonds["is_aromatic"]
    explicit_false = ((aromatic == False) & aromatic.notna()).any()  # noqa: E712
    if "bond_order" not in bonds:
        return explicit_false
    formal_order_takes_precedence = (
        (aromatic == True) & bonds["bond_order"].notna()  # noqa: E712
    ).any()
    return explicit_false or formal_order_takes_precedence


def _audit_native_topology_to_dict(item, target_form="molsysmt.TopologyDict"):
    """Stable schema 0.2 preserves the canonical inventory and memberships."""
    return []


def _audit_native_molsys_to_dict(item):
    """Report mechanical data outside the independent schema 0.2 domains."""
    target_form = "molsysmt.MolSysDict"
    issues = []
    for attribute in (
        "partial_charge",
        "atom_ff_type",
        "forcefield",
        "non_bonded_method",
        "cutoff_distance",
        "switch_distance",
        "dispersion_correction",
        "ewald_error_tolerance",
        "hydrogen_mass",
        "constraints",
        "flexible_constraints",
        "water_model",
        "rigid_water",
        "implicit_solvent",
        "solute_dielectric",
        "solvent_dielectric",
        "salt_concentration",
        "kappa",
    ):
        if getattr(item.molecular_mechanics, attribute) is not None:
            issues.append(
                _schema_limitation(
                    attribute,
                    target_form,
                    scope="molecular_mechanics",
                )
            )

    return issues


def _audit_native_builder_to_dict(item):
    """Schema 0.2 retains the builder's admitted independent stored domains."""
    return []


def _attribute_scope(attribute):
    from molsysmt.attribute import (
        is_chemical_state_attribute,
        is_mechanical_attribute,
        is_structural_attribute,
    )

    if is_chemical_state_attribute(attribute, skip_digestion=True):
        return "chemical_state"
    if is_mechanical_attribute(attribute, skip_digestion=True):
        return "molecular_mechanics"
    if is_structural_attribute(attribute, skip_digestion=True):
        return "structures"
    return "topology"


def _audit_declared_capability_projection(item, source_form, target_form):
    """Return present declared source attributes unsupported by the target."""

    from molsysmt.form import _dict_modules

    source_module = _dict_modules[source_form]
    target_attributes = _dict_modules[
        "molsysmt.Topology" if target_form == "molsysmt.TopologyDict" else target_form
    ].attributes
    issues = []

    for attribute, declared in source_module.attributes.items():
        if not declared or target_attributes.get(attribute, False):
            continue
        if not _instance_has(source_module, item, attribute, source_form):
            continue
        issues.append(
            ConversionIssue(
                attribute=attribute,
                reason=(
                    f"{target_form} cannot represent the supplied "
                    f"{attribute} semantics."
                ),
                kind="unsupported",
                scope=_attribute_scope(attribute),
            )
        )

    return issues


def _audit_native_molsys_to_builder(item):
    """Return MolSys semantics that an editable builder cannot preserve."""

    issues = _audit_declared_capability_projection(
        item,
        "molsysmt.MolSys",
        "molsysmt.MolSysBuilder",
    )
    issues = [
        issue for issue in issues if issue.attribute != "structure_chemical_state_index"
    ]

    # Builder retains the independent collection and explicit state/structure map.
    return issues


def _selected_native_pdb_payload(
    item,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
):
    """Return the exact native payload requested for PDB serialization."""

    import numpy as np

    from molsysmt._private.variables import is_all

    if is_all(selection):
        atom_indices = "all"
    else:
        from molsysmt.basic import select

        atom_indices = select(
            item, selection=selection, syntax=syntax, skip_digestion=True
        )
    if is_all(structure_indices):
        selected_structures = "all"
    else:
        selected_structures = np.atleast_1d(structure_indices).astype(int)
    return item.extract(
        atom_indices=atom_indices,
        structure_indices=selected_structures,
        copy_if_all=True,
        skip_digestion=True,
    )


def _audit_native_pdb_write(
    item,
    target_form,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
):
    """Return exhaustive, payload-aware limitations of native PDB writing."""

    import numpy as np

    from molsysmt import pyunitwizard as puw

    payload = _selected_native_pdb_payload(
        item,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
    )
    issues = _audit_declared_capability_projection(
        payload, "molsysmt.MolSys", target_form
    )

    expected_atom_ids = [str(index) for index in range(1, payload.topology.n_atoms + 1)]
    actual_atom_ids = payload.topology.atoms["atom_id"].astype(str).tolist()
    if actual_atom_ids != expected_atom_ids:
        issues.append(
            ConversionIssue(
                attribute="atom_id",
                reason=(
                    "PDB writing uses canonical serials because native atom IDs are "
                    "not one unique contiguous decimal sequence."
                ),
                kind="canonicalization",
                scope="topology",
            )
        )

    structure_ids = payload.structures.structure_id
    if structure_ids is not None and payload.structures.n_structures > 1:
        values = [str(value) for value in structure_ids]
        if len(set(values)) != len(values) or any(
            not value.isdigit() or not 1 <= int(value) <= 9999 for value in values
        ):
            issues.append(
                ConversionIssue(
                    attribute="structure_id",
                    reason=(
                        "PDB MODEL identifiers must be unique decimal values between "
                        "1 and 9999 and will therefore be canonicalized."
                    ),
                    kind="canonicalization",
                    scope="structures",
                )
            )

    if payload.structures.box is not None and payload.structures.n_structures > 1:
        boxes = puw.get_value(payload.structures.box, to_unit="nm")
        if not np.allclose(boxes, boxes[0], equal_nan=True):
            issues.append(
                ConversionIssue(
                    attribute="box",
                    reason=(
                        "PDB CRYST1 stores one unit cell for the complete model set."
                    ),
                    kind="schema_limitation",
                    scope="structures",
                )
            )

    if payload.structures.coordinates is not None:
        coordinates = puw.get_value(payload.structures.coordinates, to_unit="angstrom")
        if (
            not np.isfinite(coordinates).all()
            or np.any(coordinates < -999.999)
            or np.any(coordinates > 9999.999)
        ):
            issues.append(
                ConversionIssue(
                    attribute="coordinates",
                    reason="PDB coordinates exceed their fixed-width 8.3 fields.",
                    kind="numeric_capacity",
                    scope="structures",
                )
            )

    formal_charge = payload.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge"
    )
    if (
        formal_charge is not None
        and formal_charge.notna().any()
        and np.any(np.abs(formal_charge.dropna().to_numpy(dtype=int)) > 9)
    ):
        issues.append(
            ConversionIssue(
                attribute="formal_charge",
                reason="PDB formal-charge magnitudes occupy one decimal digit.",
                kind="numeric_capacity",
                scope="chemical_state",
            )
        )

    bonds = payload.chemical_states._resolve_chemical_state().bonds
    if "bond_type" in bonds and bonds["bond_type"].notna().any():
        issues.append(
            ConversionIssue(
                attribute="bond_type",
                reason=(
                    "PDB connectivity does not encode the source bond-type field; "
                    "a covalent interpretation is reconstructed on reading."
                ),
                kind="schema_limitation",
                scope="chemical_state",
            )
        )

    deduplicated = {}
    for issue in issues:
        deduplicated[(issue.attribute, issue.kind, issue.scope)] = issue
    return list(deduplicated.values())


def _pdb_handler(item, source_form):
    """Return a PDB handler and whether this audit owns it."""

    if source_form == "molsysmt.PDBFileHandler":
        return item, False
    if source_form == "file:pdb":
        from molsysmt.form.file_pdb.to_molsysmt_PDBFileHandler import (
            to_molsysmt_PDBFileHandler,
        )
    else:
        from molsysmt.form.string_pdb_text.to_molsysmt_PDBFileHandler import (
            to_molsysmt_PDBFileHandler,
        )
    return to_molsysmt_PDBFileHandler(item, skip_digestion=True), True


def _selected_pdb_site_indices(handler, selection, syntax):
    """Return canonical PDB site indices inspected by one conversion."""

    from molsysmt._private.variables import is_all
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys import (
        _build_topology_from_content,
        _canonical_atoms,
    )

    canonical_atoms, _ = _canonical_atoms(handler.content)
    if is_all(selection):
        return list(range(len(canonical_atoms))), canonical_atoms
    from molsysmt.basic import select

    topology = _build_topology_from_content(handler, get_missing_bonds=False)
    indices = select(topology, selection=selection, syntax=syntax, skip_digestion=True)
    return [int(index) for index in indices], canonical_atoms


def _audit_pdb_read(
    item,
    source_form,
    target_form,
    selection="all",
    syntax="MolSysMT",
):
    """Return exhaustive, content-aware limitations of native PDB reading."""

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys import (
        _canonical_atoms,
        _get_explicit_bonds,
    )

    handler, opened_here = _pdb_handler(item, source_form)
    try:
        selected_indices, canonical_atoms = _selected_pdb_site_indices(
            handler, selection, syntax
        )
        selected_keys = {canonical_atoms[index].site_key for index in selected_indices}
        issues = []
        for content_issue in handler.content.issues:
            if content_issue.atom_site_keys and not selected_keys.intersection(
                content_issue.atom_site_keys
            ):
                continue
            issues.append(
                ConversionIssue(
                    attribute=content_issue.attribute,
                    reason=content_issue.reason,
                    kind="adapter_limitation",
                    scope=_attribute_scope(content_issue.attribute),
                )
            )

        if any(canonical_atoms[index].insertion_code for index in selected_indices):
            issues.append(
                ConversionIssue(
                    attribute="group_id",
                    reason=(
                        "Native group IDs do not encode the separate PDB insertion code."
                    ),
                    kind="adapter_limitation",
                    scope="topology",
                )
            )

        _, variants = _canonical_atoms(handler.content)
        _, unresolved_bonds, repeated_conect = _get_explicit_bonds(
            handler.content, canonical_atoms, variants
        )
        if unresolved_bonds:
            issues.append(
                ConversionIssue(
                    attribute="bonded_atoms",
                    reason=(
                        "At least one explicit PDB connectivity endpoint is missing "
                        "or ambiguous."
                    ),
                    kind="adapter_limitation",
                    scope="chemical_state",
                )
            )
        if repeated_conect:
            issues.append(
                ConversionIssue(
                    attribute="bond_order",
                    reason=(
                        "Repeated PDB CONECT endpoints are retained as one bond and "
                        "are not interpreted silently as a bond order."
                    ),
                    kind="adapter_limitation",
                    scope="chemical_state",
                )
            )

        if target_form == "molsysmt.Topology":
            issues.append(
                ConversionIssue(
                    attribute="coordinates",
                    reason="A topology-only target intentionally omits PDB structures.",
                    kind="target_projection",
                    scope="structures",
                )
            )
        elif target_form == "molsysmt.Structures":
            issues.append(
                ConversionIssue(
                    attribute="atom_name",
                    reason="A structures-only target intentionally omits PDB topology.",
                    kind="target_projection",
                    scope="topology",
                )
            )
        return issues
    finally:
        if opened_here:
            handler.close()


def _audit_coordinate_trajectory(source_form, target_form):
    """Return exhaustive losses for one narrow coordinate-format projection."""

    if target_form == "molsysmt.Topology":
        return [
            ConversionIssue(
                attribute="coordinates",
                reason="A topology-only target intentionally omits trajectory coordinates.",
                kind="target_projection",
                scope="structures",
            )
        ]
    if (
        source_form in {"file:xtc", "mdtraj.XTCTrajectoryFile"}
        and target_form == "mdtraj.Trajectory"
    ):
        return [
            ConversionIssue(
                attribute="structure_id",
                reason=(
                    "MDTraj Trajectory has no independent carrier for XTC step IDs."
                ),
                kind="schema_limitation",
                scope="structures",
            )
        ]
    return []


def _audit_h5msm_to_structures(item, source_form):
    """Return losses from an H5MSM compound form to native structures."""

    opened_here = False
    if source_form == "file:h5msm":
        from molsysmt.form.file_h5msm.to_molsysmt_H5MSMFileHandler import (
            to_molsysmt_H5MSMFileHandler,
        )

        handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
        opened_here = True
    else:
        handler = item

    try:
        issues = []
        topology = handler.file["topology"]
        if int(topology.attrs.get("n_atoms", 0)) > 0:
            issues.append(
                ConversionIssue(
                    attribute="atom_id",
                    reason="A structures-only target intentionally omits H5MSM topology.",
                    kind="target_projection",
                    scope="topology",
                )
            )

        structures = handler.file["structures"]
        state_indices = structures.get("chemical_state_index")
        if state_indices is not None and state_indices.shape[0] > 0:
            issues.append(
                ConversionIssue(
                    attribute="structure_chemical_state_index",
                    reason=(
                        "Native Structures does not carry H5MSM "
                        "structure-to-chemical-state associations."
                    ),
                    kind="target_projection",
                    scope="chemical_state",
                )
            )
        return issues
    finally:
        if opened_here:
            handler.close()


def _audit_registered_profile(
    item,
    source_form,
    target_form,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
):
    """Return issues from one evidence-backed exhaustive audit profile."""

    pair = (source_form, target_form)
    if pair == ("molsysmt.Structures", "molsysmt.StructuresDict"):
        return _audit_native_structures_to_dict(item)
    if pair == ("molsysmt.Topology", "molsysmt.TopologyDict"):
        return _audit_native_topology_to_dict(item)
    if pair == ("molsysmt.MolSys", "molsysmt.MolSysDict"):
        return _audit_native_molsys_to_dict(item)
    profile = _CONVERSION_AUDIT_PROFILES.get(pair)
    if profile is not None and profile.get("mode") == "declared_capability_projection":
        return _audit_declared_capability_projection(
            item,
            source_form,
            target_form,
        )
    if profile is not None and profile.get("mode") == "molsys_to_builder":
        return _audit_native_molsys_to_builder(item)
    if profile is not None and profile.get("mode") == "builder_to_molsysdict":
        return _audit_native_builder_to_dict(item)
    if profile is not None and profile.get("mode") == "pdb_write":
        return _audit_native_pdb_write(
            item,
            target_form,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
    if profile is not None and profile.get("mode") == "pdb_read":
        return _audit_pdb_read(
            item,
            source_form,
            target_form,
            selection=selection,
            syntax=syntax,
        )
    if profile is not None and profile.get("mode") == "coordinate_trajectory":
        return _audit_coordinate_trajectory(source_form, target_form)
    if profile is not None and profile.get("mode") == "h5msm_to_structures":
        return _audit_h5msm_to_structures(item, source_form)
    return []


def _native_multistate_has(item, source_form, attribute):
    states = (
        item.chemical_states
        if source_form in {"molsysmt.MolSys", "molsysmt.MolSysBuilder"}
        else None
    )
    if states is None:
        return None
    atom_columns = {
        "formal_charge": "formal_charge",
        "atom_is_aromatic": "is_aromatic",
        "n_unpaired_electrons": "n_unpaired_electrons",
        "n_implicit_hydrogens": "n_implicit_hydrogens",
        "n_explicit_hydrogens": "n_explicit_hydrogens",
        "allows_implicit_hydrogens": "allows_implicit_hydrogens",
        "atom_stereochemistry": "stereochemistry",
    }
    bond_columns = {
        "bond_id": "bond_id",
        "bond_order": "bond_order",
        "fractional_bond_order": "fractional_bond_order",
        "bond_type": "bond_type",
        "bond_is_aromatic": "is_aromatic",
        "bond_is_conjugated": "is_conjugated",
        "bond_stereochemistry": "stereochemistry",
        "bond_stereo_atom_indices": "stereo_atom1_index",
        "bond_donor_atom_index": "donor_atom_index",
        "bond_acceptor_atom_index": "acceptor_atom_index",
        "bond_joins_components": "joins_components",
        "bond_evidence": "evidence",
    }
    if attribute in atom_columns:
        column = atom_columns[attribute]
        return any(
            column in state.atom_attributes
            and state.atom_attributes[column].notna().any()
            for state in states._states
        )
    if attribute in bond_columns:
        column = bond_columns[attribute]
        return any(
            column in state.bonds and state.bonds[column].notna().any()
            for state in states._states
        )
    if attribute in {
        "connectivity_completeness",
        "component_completeness",
        "component_evidence",
        "n_bonds",
        "n_inner_bonds",
        "n_components",
    }:
        return states.n_chemical_states > 0
    if attribute in {
        "bond_index",
        "bonded_atoms",
        "bonded_atom_pairs",
        "inner_bond_index",
        "inner_bonded_atoms",
        "inner_bonded_atom_pairs",
    }:
        return any(len(state.bonds) for state in states._states)
    if attribute == "component_index":
        return any(
            len(state.components) or state.component_indices.notna().any()
            for state in states._states
        )
    if attribute in {"component_id", "component_name", "component_type"}:
        return any(
            state.components[attribute].notna().any() for state in states._states
        )
    return None


def _instance_has(module, item, attribute, source_form):
    if not module.attributes.get(attribute, False):
        return False
    if source_form in {"molsysmt.MolSys", "molsysmt.MolSysBuilder"}:
        states = item.chemical_states
        if states is not None and (
            states.n_chemical_states != 1
            and states.reference_chemical_state_index is None
        ):
            output = _native_multistate_has(item, source_form, attribute)
            if output is not None:
                return output
    return bool(
        module.has_attribute(item, attribute, include_none=False, skip_digestion=True)
    )


def build_conversion_report(
    molecular_system,
    from_form,
    to_form,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    converter_options=None,
):
    """Build a conservative preflight report without mutating either system."""

    from molsysmt._private.conversion_pdbqt import PDBQT_FORMS
    from molsysmt.form import _dict_modules

    target_form = _canonical_target_form(to_form)
    source_item, source_form = _single_source(molecular_system, from_form)
    issues = []
    pdbqt_identity = False

    if source_item is not None and source_form == target_form == "file:sdf":
        from molsysmt._private.variables import is_all

        if is_all(selection) and is_all(structure_indices):
            from molsysmt._private.ctfile import validate_sdf_envelope

            # The converter preserves bytes, including unknown chemistry. An
            # exhaustive byte-preservation report needs no native attribute audit.
            validate_sdf_envelope(source_item)
            return ConversionReport(
                from_form=source_form,
                to_form=target_form,
                outcome="exact",
                audited_scopes=("all",),
                is_exhaustive=True,
                issues=(),
            )

    if source_item is not None:
        from molsysmt._private.conversion_pdbqt import PDBQT_FORMS, audit_pdbqt
        from molsysmt._private.variables import is_all

        if source_form in PDBQT_FORMS or target_form in PDBQT_FORMS:
            issues.extend(
                audit_pdbqt(
                    source_item,
                    source_form,
                    target_form,
                    selection,
                    structure_indices,
                    syntax,
                )
            )
            if source_form in PDBQT_FORMS and target_form in PDBQT_FORMS:
                from molsysmt._private.pdbqt_adapter import identity_selection

                pdbqt_identity = identity_selection(
                    source_item, source_form, selection, structure_indices, syntax
                )

        if source_form == "file:sdf" and (
            target_form != "file:sdf"
            or not is_all(selection)
            or not is_all(structure_indices)
        ):
            from molsysmt._private.ctfile import read_sdf

            record = read_sdf(source_item, allow_stereo=True)
            properties = record.properties
            if properties:
                issues.append(
                    ConversionIssue(
                        attribute="sdf_properties",
                        reason="Native domains cannot retain SD property blocks: "
                        + ", ".join(name for name, _ in properties),
                        scope="source_metadata",
                    )
                )
            if any(bond.display is not None for bond in record.bonds):
                issues.append(
                    ConversionIssue(
                        attribute="sdf_bond_display",
                        reason="Native domains retain coordination roles but not the CTAB DISP drawing style.",
                        scope="source_metadata",
                    )
                )
        if target_form == "file:sdf" and source_form in {"molsysmt.MolSys", "file:sdf"}:
            from molsysmt._private.conversion_sdf import audit_sdf_write

            if source_form == "molsysmt.MolSys":
                issues.extend(
                    audit_sdf_write(source_item, selection, structure_indices, syntax)
                )
            elif not is_all(selection) or not is_all(structure_indices):
                from molsysmt.form.file_sdf._native import to_native

                native = to_native(
                    read_sdf(source_item, allow_stereo=True), discard_properties=True
                )
                issues.extend(
                    audit_sdf_write(native, selection, structure_indices, syntax)
                )
        registered_profile = (
            source_form,
            target_form,
        ) in _CONVERSION_AUDIT_PROFILES
        issues.extend(
            _audit_registered_profile(
                source_item,
                source_form,
                target_form,
                selection=selection,
                structure_indices=structure_indices,
                syntax=syntax,
            )
        )
        source_module = _dict_modules[source_form]
        inspection_item = source_item
        inspection_form = source_form
        inspection_module = source_module
        if source_form in PDBQT_FORMS:
            from molsysmt._private.pdbqt import read, to_native

            inspection_item = to_native(
                read(source_item, text=source_form == "string:pdbqt_text"),
                discard_torsion_tree=True,
            )
            inspection_form = "molsysmt.MolSys"
            inspection_module = _dict_modules[inspection_form]
        if not registered_profile and source_form in {
            "file:h5msm",
            "molsysmt.H5MSMFileHandler",
        }:
            from molsysmt._private.h5msm import modular_h5msm_axes

            if (
                source_form == "file:h5msm"
                and modular_h5msm_axes(source_item) is not None
            ):
                from molsysmt.form._h5msm05_modular import read_modular_file
                from molsysmt.native import MolSys

                payload = read_modular_file(
                    source_item, layers={"topology", "chemical_states"}
                )
                # Presence inspection does not project values across either axis.
                inspection_item = MolSys._from_partial_domains(
                    topology=payload["topology"],
                    chemical_states=payload["chemical_states"],
                )
            else:
                from molsysmt.form.molsysmt_H5MSMFileHandler._read_native import (
                    read_native,
                )

                inspection_item = read_native(source_item, skip_digestion=True)
            inspection_form = "molsysmt.MolSys"
            inspection_module = _dict_modules[inspection_form]
        if not registered_profile:
            target_attributes = _dict_modules[target_form].attributes
            for attribute in _CHEMICAL_ATTRIBUTES:
                if pdbqt_identity:
                    continue
                if (
                    target_form == "file:sdf"
                    and attribute
                    in {
                        "atom_stereochemistry",
                        "bond_stereochemistry",
                        "bond_stereo_atom_indices",
                    }
                    and (converter_options or {}).get("stereo_engine") == "rdkit"
                ):
                    # The explicit writer verifies this bounded stereo route
                    # before opening the destination. Ordinary capability
                    # reports still describe the dependency-free default.
                    continue
                if _instance_has(
                    inspection_module, inspection_item, attribute, inspection_form
                ) and not target_attributes.get(attribute, False):
                    issues.append(
                        ConversionIssue(
                            attribute=attribute,
                            reason=(
                                f"{target_form} cannot represent the supplied "
                                f"{attribute} semantics."
                            ),
                        )
                    )

        if source_form == "molsysmt.MolSys" and source_item.chemical_states is not None:
            states = source_item.chemical_states
            if (
                not registered_profile
                and states.n_chemical_states > 1
                and target_form
                not in {
                    "molsysmt.Topology",
                    "molsysmt.MolSys",
                    "file:h5msm",
                    "molsysmt.H5MSMFileHandler",
                }
            ):
                issues.append(
                    ConversionIssue(
                        attribute="chemical_state_index",
                        reason=(
                            f"{target_form} cannot preserve the ordered multi-state inventory."
                        ),
                        kind="state_collapse",
                    )
                )

            if target_form == "pdbfixer.PDBFixer" and (
                states.n_chemical_states == 1
                or states.reference_chemical_state_index is not None
            ):
                source_bonds = states._get_chemical_state_bonds()
                if source_bonds.empty:
                    issues.append(
                        ConversionIssue(
                            attribute="bonded_atoms",
                            reason=(
                                "PDBFixer may reconstruct standard-residue bonds when the "
                                "source declares a known-empty covalent graph."
                            ),
                            kind="target_inference",
                        )
                    )

        if source_form in {
            "MDAnalysis.Topology",
            "MDAnalysis.Universe",
        } and target_form in {"molsysmt.Topology", "molsysmt.MolSys"}:
            from molsysmt.form.MDAnalysis_Topology._chemical_state import (
                has_opaque_bond_types,
            )

            mda_topology = (
                source_item._topology
                if source_form == "MDAnalysis.Universe"
                else source_item
            )
            if has_opaque_bond_types(mda_topology):
                issues.append(
                    ConversionIssue(
                        attribute="bond_source_type",
                        reason=(
                            "MDAnalysis supplies an opaque scalar bond type that has no "
                            "documented canonical chemical mapping."
                        ),
                        kind="adapter_limitation",
                    )
                )

        if source_form == "parmed.Structure" and target_form in {
            "molsysmt.Topology",
            "molsysmt.MolSys",
        }:
            from molsysmt.form.parmed_Structure._chemical_state import (
                has_mechanical_bond_types,
                has_unsupported_relationships,
            )

            if has_unsupported_relationships(source_item):
                issues.append(
                    ConversionIssue(
                        attribute="bond_type",
                        reason=(
                            "ParmEd contains ionic, hydrogen, three-center, or other "
                            "relationships that do not belong to the native covalent bond graph."
                        ),
                        kind="adapter_limitation",
                    )
                )
            if has_mechanical_bond_types(source_item):
                issues.append(
                    ConversionIssue(
                        attribute="bond_mechanical_parameters",
                        reason=(
                            "ParmEd bond parameter objects belong to molecular mechanics and "
                            "are not imported by this topology conversion."
                        ),
                        kind="adapter_limitation",
                    )
                )

        if source_form == "mmcif.PdbxContainers.DataContainer" and target_form in {
            "molsysmt.Topology",
            "molsysmt.MolSys",
        }:
            from molsysmt.form.mmcif_PdbxContainers_DataContainer._bond_state import (
                has_unknown_chem_comp_bond_orders,
            )

            if has_unknown_chem_comp_bond_orders(source_item):
                issues.append(
                    ConversionIssue(
                        attribute="bond_order",
                        reason=(
                            "mmCIF supplies a chem_comp_bond.value_order code that has "
                            "no documented canonical chemical mapping."
                        ),
                        kind="adapter_limitation",
                    )
                )
    same_form = source_form == target_form
    audited_scopes = get_conversion_audit_scopes(source_form, target_form)
    if (
        source_form == "file:sdf"
        or target_form == "file:sdf"
        or source_form in PDBQT_FORMS
        or target_form in PDBQT_FORMS
    ):
        audited_scopes = tuple(
            dict.fromkeys((*audited_scopes, *(issue.scope for issue in issues)))
        )
    is_exhaustive = is_conversion_audit_exhaustive(source_form, target_form)
    if pdbqt_identity:
        audited_scopes = ("all",)
        is_exhaustive = True

    # Static graph audits cannot assume that every third-party identity
    # converter preserves its complete representation. At runtime, an actual
    # single-form identity instance supplies stronger evidence: the conversion
    # stays within the same representation and can be classified exhaustively.
    if source_item is not None and same_form:
        audited_scopes = ("all",)
        is_exhaustive = True
        if source_form == "file:sdf" and (
            not is_all(selection) or not is_all(structure_indices)
        ):
            audited_scopes = tuple(
                dict.fromkeys(
                    (
                        "chemical_state",
                        "source_metadata",
                        *(issue.scope for issue in issues),
                    )
                )
            )
            is_exhaustive = False
        if source_form in PDBQT_FORMS and not pdbqt_identity:
            audited_scopes = tuple(
                dict.fromkeys(("source_metadata", *(issue.scope for issue in issues)))
            )
            is_exhaustive = False

    outcome = "lossy" if issues else ("exact" if same_form else "equivalent")
    return ConversionReport(
        from_form=source_form,
        to_form=target_form,
        outcome=outcome,
        audited_scopes=audited_scopes,
        is_exhaustive=is_exhaustive,
        issues=tuple(issues),
    )
