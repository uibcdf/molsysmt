"""Building capability- and instance-aware chemical conversion preflight reports."""

from molsysmt.basic.conversion_report import ConversionIssue, ConversionReport


_CHEMICAL_ATTRIBUTES = (
    'isotope',
    'formal_charge',
    'atom_is_aromatic',
    'n_unpaired_electrons',
    'n_implicit_hydrogens',
    'allows_implicit_hydrogens',
    'atom_stereochemistry',
    'bond_id',
    'bond_order',
    'fractional_bond_order',
    'bond_type',
    'bond_is_aromatic',
    'bond_is_conjugated',
    'bond_stereochemistry',
    'bond_stereo_atom_indices',
    'bond_donor_atom_index',
    'bond_acceptor_atom_index',
    'bond_joins_components',
    'bond_evidence',
    'connectivity_completeness',
    'component_completeness',
    'component_evidence',
)

# Static route coverage is deliberately conservative. A pair belongs here only
# after its complete source semantics are traversed by the preflight and covered
# by executable evidence. Stage A2 activates native declarative pairs as their
# schema-driven audits land.
_STRUCTURES_TO_STRUCTURES_DICT_PROFILE = {
    'directly_preserved': frozenset({
        'structure_id',
        'time',
        'box',
        'coordinates',
        'velocities',
        'occupancy',
        'b_factor',
        'alternate_location',
        'temperature',
        'potential_energy',
        'kinetic_energy',
    }),
    'derived_without_loss': frozenset({
        'atom_index',
        'n_atoms',
        'structure_index',
        'box_shape',
        'box_angles',
        'box_lengths',
        'box_volume',
        'n_structures',
    }),
    'covered_by_dependencies': {
        'n_bioassemblies': 'bioassembly',
        'total_energy': ('potential_energy', 'kinetic_energy'),
    },
    'loss_candidates': (
        'bioassembly',
    ),
}

_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE = {
    'directly_preserved': frozenset({
        'atom_id',
        'atom_name',
        'atom_type',
        'isotope',
        'group_id',
        'group_name',
        'group_type',
        'chain_id',
        'chain_name',
        'chain_type',
        'molecule_id',
        'molecule_name',
        'molecule_type',
        'entity_id',
        'entity_name',
        'entity_type',
        'bond_type',
        'bond_order',
    }),
    'derived_without_loss': frozenset({
        'atom_index',
        'group_index',
        'chain_index',
        'molecule_index',
        'entity_index',
        'bond_index',
        'bonded_atoms',
        'bonded_atom_pairs',
        'inner_bonded_atoms',
        'inner_bonded_atom_pairs',
        'inner_bond_index',
        'n_atoms',
        'n_groups',
        'n_chains',
        'n_molecules',
        'n_entities',
        'n_bonds',
        'n_inner_bonds',
        'n_amino_acids',
        'n_nucleotides',
        'n_ions',
        'n_waters',
        'n_small_molecules',
        'n_peptides',
        'n_proteins',
        'n_dnas',
        'n_rnas',
        'n_lipids',
        'n_polysaccharides',
        'n_saccharides',
    }),
    'covered_by_dependencies': {
        'chemical_state_index': 'chemical_state_inventory',
        'n_chemical_states': 'chemical_state_inventory',
        'reference_chemical_state_index': 'chemical_state_inventory',
        'n_components': 'component_index',
    },
    'loss_candidates': (
        'chemical_state_id',
        'connectivity_completeness',
        'component_completeness',
        'component_evidence',
        'component_index',
        'component_id',
        'component_name',
        'component_type',
        'bond_id',
        'fractional_bond_order',
        'bond_is_aromatic',
        'bond_is_conjugated',
        'bond_stereochemistry',
        'bond_stereo_atom_indices',
        'bond_donor_atom_index',
        'bond_acceptor_atom_index',
        'bond_joins_components',
        'bond_evidence',
        'formal_charge',
        'atom_is_aromatic',
        'n_unpaired_electrons',
        'n_implicit_hydrogens',
        'allows_implicit_hydrogens',
        'atom_stereochemistry',
    ),
}

_MOLSYS_TO_MOLSYS_DICT_PROFILE = {
    'directly_preserved': (
        _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE['directly_preserved']
        | frozenset({
            'structure_id',
            'time',
            'box',
            'coordinates',
        })
    ),
    'derived_without_loss': (
        _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE['derived_without_loss']
        | frozenset({
            'structure_index',
            'box_shape',
            'box_angles',
            'box_lengths',
            'box_volume',
            'n_structures',
        })
    ),
    'covered_by_dependencies': {
        **_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE['covered_by_dependencies'],
        'n_bioassemblies': 'bioassembly',
        'total_energy': ('potential_energy', 'kinetic_energy'),
    },
    'loss_candidates': (
        *_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE['loss_candidates'],
        'velocities',
        'occupancy',
        'b_factor',
        'alternate_location',
        'bioassembly',
        'temperature',
        'potential_energy',
        'kinetic_energy',
        'structure_chemical_state_index',
        'partial_charge',
        'atom_ff_type',
        'forcefield',
        'non_bonded_method',
        'cutoff_distance',
        'switch_distance',
        'dispersion_correction',
        'ewald_error_tolerance',
        'hydrogen_mass',
        'constraints',
        'flexible_constraints',
        'water_model',
        'rigid_water',
        'implicit_solvent',
        'solute_dielectric',
        'solvent_dielectric',
        'salt_concentration',
        'kappa',
    ),
}

_DECLARED_CAPABILITY_PROJECTION_PROFILE = {
    'mode': 'declared_capability_projection',
}

_MOLSYS_TO_BUILDER_PROFILE = {
    'mode': 'molsys_to_builder',
}

_BUILDER_TO_MOLSYS_DICT_PROFILE = {
    'mode': 'builder_to_molsysdict',
}

_PDB_WRITE_PROFILE = {
    'mode': 'pdb_write',
}

_PDB_READ_PROFILE = {
    'mode': 'pdb_read',
}

_COORDINATE_TRAJECTORY_PROFILE = {
    'mode': 'coordinate_trajectory',
}

_H5MSM_TO_STRUCTURES_PROFILE = {
    'mode': 'h5msm_to_structures',
}

_CONVERSION_AUDIT_PROFILES = {
    (
        'molsysmt.Structures',
        'molsysmt.StructuresDict',
    ): _STRUCTURES_TO_STRUCTURES_DICT_PROFILE,
    (
        'molsysmt.Topology',
        'molsysmt.TopologyDict',
    ): _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE,
    (
        'molsysmt.MolSys',
        'molsysmt.MolSysDict',
    ): _MOLSYS_TO_MOLSYS_DICT_PROFILE,
    (
        'molsysmt.MolSys',
        'molsysmt.Topology',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        'molsysmt.MolSys',
        'molsysmt.Structures',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        'molsysmt.StructuresDict',
        'molsysmt.MolSys',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        'molsysmt.StructuresDict',
        'molsysmt.Topology',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        'molsysmt.MolSys',
        'molsysmt.MolSysBuilder',
    ): _MOLSYS_TO_BUILDER_PROFILE,
    (
        'molsysmt.MolSysBuilder',
        'molsysmt.MolSys',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    (
        'molsysmt.MolSysBuilder',
        'molsysmt.MolSysDict',
    ): _BUILDER_TO_MOLSYS_DICT_PROFILE,
    (
        'molsysmt.MolSysDict',
        'molsysmt.MolSysBuilder',
    ): _DECLARED_CAPABILITY_PROJECTION_PROFILE,
    ('molsysmt.MolSys', 'string:pdb_text'): _PDB_WRITE_PROFILE,
    ('molsysmt.MolSys', 'file:pdb'): _PDB_WRITE_PROFILE,
    ('file:h5msm', 'molsysmt.Structures'): _H5MSM_TO_STRUCTURES_PROFILE,
    (
        'molsysmt.H5MSMFileHandler',
        'molsysmt.Structures',
    ): _H5MSM_TO_STRUCTURES_PROFILE,
}

for _pdb_source_form in (
    'file:pdb',
    'string:pdb_text',
    'molsysmt.PDBFileHandler',
):
    for _pdb_target_form in (
        'molsysmt.MolSys',
        'molsysmt.Topology',
        'molsysmt.Structures',
    ):
        _CONVERSION_AUDIT_PROFILES[
            (_pdb_source_form, _pdb_target_form)
        ] = _PDB_READ_PROFILE

del _pdb_source_form, _pdb_target_form

for _coordinate_pair in (
    ('XYZ', 'molsysmt.Structures'),
    ('XYZ', 'molsysmt.MolSys'),
    ('XYZ', 'molsysmt.Topology'),
    ('XYZ', 'file:xyznpy'),
    ('file:xyznpy', 'XYZ'),
    ('file:xyz', 'XYZ'),
    ('file:dcd', 'molsysmt.Structures'),
    ('file:dcd', 'molsysmt.MolSys'),
    ('file:dcd', 'file:h5msm'),
    ('mdtraj.DCDTrajectoryFile', 'molsysmt.Structures'),
    ('mdtraj.DCDTrajectoryFile', 'molsysmt.MolSys'),
    ('file:xtc', 'molsysmt.Structures'),
    ('file:xtc', 'mdtraj.Trajectory'),
    ('file:xtc', 'file:h5msm'),
    ('mdtraj.XTCTrajectoryFile', 'molsysmt.Structures'),
):
    _CONVERSION_AUDIT_PROFILES[_coordinate_pair] = (
        _COORDINATE_TRAJECTORY_PROFILE
    )

del _coordinate_pair

_EXHAUSTIVE_AUDIT_PAIRS = frozenset(_CONVERSION_AUDIT_PROFILES)


def get_conversion_audit_scopes(source_form, target_form):
    """Returning the statically supported preflight scopes for a form pair."""

    pair = (source_form, target_form)
    if pair in _EXHAUSTIVE_AUDIT_PAIRS:
        return ('all',)
    if source_form == target_form:
        return ('representation',)
    return ('chemical_state',)


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
    for attribute in profile['loss_candidates']:
        if getattr(item, attribute) is not None:
            issues.append(
                ConversionIssue(
                    attribute=attribute,
                    reason=(
                        'molsysmt.StructuresDict cannot represent the supplied '
                        f'{attribute} semantics.'
                    ),
                    kind='schema_limitation',
                    scope='structures',
                )
            )
    return issues


def _schema_limitation(attribute, target_form, scope='chemical_state'):
    return ConversionIssue(
        attribute=attribute,
        reason=(
            f'{target_form} cannot represent the supplied '
            f'{attribute} semantics.'
        ),
        kind='schema_limitation',
        scope=scope,
    )


def _states_have_atom_column(states, column):
    return any(
        column in state.atom_attributes
        and state.atom_attributes[column].notna().any()
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
    aromatic = bonds['is_aromatic']
    explicit_false = ((aromatic == False) & aromatic.notna()).any()  # noqa: E712
    if 'bond_order' not in bonds:
        return explicit_false
    formal_order_takes_precedence = (
        (aromatic == True) & bonds['bond_order'].notna()  # noqa: E712
    ).any()
    return explicit_false or formal_order_takes_precedence


def _audit_native_topology_to_dict(
    item,
    target_form='molsysmt.TopologyDict',
):
    """Return native topology semantics omitted by TopologyDict 0.1."""

    states = item._chemical_states
    issues = []

    if len(states) != 1:
        issues.append(
            ConversionIssue(
                attribute='chemical_state_index',
                reason=(
                    f'{target_form} 0.1 stores one resolved chemical '
                    'state and cannot preserve the ordered state inventory.'
                ),
                kind='state_collapse',
                scope='chemical_state',
            )
        )

    if any(state.state_id is not None for state in states):
        issues.append(
            _schema_limitation('chemical_state_id', target_form)
        )

    if any(state.connectivity_completeness != 'unavailable' for state in states):
        issues.append(
            _schema_limitation(
                'connectivity_completeness',
                target_form,
            )
        )

    if any(state.component_completeness != 'unavailable' for state in states):
        issues.append(
            _schema_limitation('component_completeness', target_form)
        )
    if any(state.component_evidence != 'unknown' for state in states):
        issues.append(
            _schema_limitation('component_evidence', target_form)
        )
    if any(state.component_indices.notna().any() for state in states):
        issues.append(_schema_limitation('component_index', target_form))

    for attribute, column in (
        ('component_id', 'component_id'),
        ('component_name', 'component_name'),
        ('component_type', 'component_type'),
    ):
        if any(
            column in state.components
            and state.components[column].notna().any()
            for state in states
        ):
            issues.append(_schema_limitation(attribute, target_form))

    bond_columns = (
        ('bond_id', 'bond_id'),
        ('fractional_bond_order', 'fractional_bond_order'),
        ('bond_is_conjugated', 'is_conjugated'),
        ('bond_stereochemistry', 'stereochemistry'),
        ('bond_donor_atom_index', 'donor_atom_index'),
        ('bond_acceptor_atom_index', 'acceptor_atom_index'),
        ('bond_evidence', 'evidence'),
    )
    for attribute, column in bond_columns:
        if _states_have_bond_column(states, column):
            issues.append(_schema_limitation(attribute, target_form))

    if (
        _states_have_bond_column(states, 'stereo_atom1_index')
        or _states_have_bond_column(states, 'stereo_atom2_index')
    ):
        issues.append(
            _schema_limitation('bond_stereo_atom_indices', target_form)
        )

    if _states_have_bond_column(
        states,
        'is_aromatic',
        predicate=_aromatic_flag_is_not_preserved,
    ):
        issues.append(_schema_limitation('bond_is_aromatic', target_form))

    if _states_have_bond_column(
        states,
        'joins_components',
    ):
        issues.append(
            _schema_limitation('bond_joins_components', target_form)
        )

    atom_columns = (
        ('formal_charge', 'formal_charge'),
        ('atom_is_aromatic', 'is_aromatic'),
        ('n_unpaired_electrons', 'n_unpaired_electrons'),
        ('n_implicit_hydrogens', 'n_implicit_hydrogens'),
        ('allows_implicit_hydrogens', 'allows_implicit_hydrogens'),
        ('atom_stereochemistry', 'stereochemistry'),
    )
    for attribute, column in atom_columns:
        if _states_have_atom_column(states, column):
            issues.append(_schema_limitation(attribute, target_form))

    return issues


def _audit_native_molsys_to_dict(item):
    """Return native MolSys semantics omitted by MolSysDict 0.1."""

    target_form = 'molsysmt.MolSysDict'
    issues = _audit_native_topology_to_dict(
        item.topology,
        target_form=target_form,
    )

    for attribute in (
        'velocities',
        'occupancy',
        'b_factor',
        'alternate_location',
        'bioassembly',
        'temperature',
        'potential_energy',
        'kinetic_energy',
    ):
        if getattr(item.structures, attribute) is not None:
            issues.append(
                _schema_limitation(
                    attribute,
                    target_form,
                    scope='structures',
                )
            )

    explicit_associations = item._structure_chemical_state_indices
    if explicit_associations is not None:
        known = explicit_associations.dropna()
        association_is_implicit_single_state = (
            len(item.topology._chemical_states) == 1
            and len(known) == len(explicit_associations)
            and (known == 0).all()
        )
        if not association_is_implicit_single_state:
            issues.append(
                ConversionIssue(
                    attribute='structure_chemical_state_index',
                    reason=(
                        'molsysmt.MolSysDict 0.1 cannot preserve the explicit '
                        'structure-to-chemical-state association.'
                    ),
                    kind='state_association_loss',
                    scope='chemical_state',
                )
            )

    for attribute in (
        'partial_charge',
        'atom_ff_type',
        'forcefield',
        'non_bonded_method',
        'cutoff_distance',
        'switch_distance',
        'dispersion_correction',
        'ewald_error_tolerance',
        'hydrogen_mass',
        'constraints',
        'flexible_constraints',
        'water_model',
        'rigid_water',
        'implicit_solvent',
        'solute_dielectric',
        'solvent_dielectric',
        'salt_concentration',
        'kappa',
    ):
        if getattr(item.molecular_mechanics, attribute) is not None:
            issues.append(
                _schema_limitation(
                    attribute,
                    target_form,
                    scope='molecular_mechanics',
                )
            )

    return issues


def _audit_native_builder_to_dict(item):
    """Return builder semantics omitted by MolSysDict 0.1."""

    target_form = 'molsysmt.MolSysDict'
    issues = _audit_native_topology_to_dict(
        item.topology,
        target_form=target_form,
    )

    for attribute in (
        'velocities',
        'occupancy',
        'b_factor',
        'alternate_location',
        'bioassembly',
        'temperature',
        'potential_energy',
        'kinetic_energy',
    ):
        if getattr(item.structures, attribute) is not None:
            issues.append(
                _schema_limitation(
                    attribute,
                    target_form,
                    scope='structures',
                )
            )

    return issues


def _attribute_scope(attribute):
    from molsysmt.attribute import (
        is_chemical_state_attribute,
        is_mechanical_attribute,
        is_structural_attribute,
    )

    if is_chemical_state_attribute(attribute, skip_digestion=True):
        return 'chemical_state'
    if is_mechanical_attribute(attribute, skip_digestion=True):
        return 'molecular_mechanics'
    if is_structural_attribute(attribute, skip_digestion=True):
        return 'structures'
    return 'topology'


def _audit_declared_capability_projection(item, source_form, target_form):
    """Return present declared source attributes unsupported by the target."""

    from molsysmt.form import _dict_modules

    source_module = _dict_modules[source_form]
    target_attributes = _dict_modules[target_form].attributes
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
                    f'{target_form} cannot represent the supplied '
                    f'{attribute} semantics.'
                ),
                kind='unsupported',
                scope=_attribute_scope(attribute),
            )
        )

    return issues


def _audit_native_molsys_to_builder(item):
    """Return MolSys semantics that an editable builder cannot preserve."""

    issues = _audit_declared_capability_projection(
        item,
        'molsysmt.MolSys',
        'molsysmt.MolSysBuilder',
    )
    issues = [
        issue
        for issue in issues
        if issue.attribute != 'structure_chemical_state_index'
    ]

    explicit_associations = item._structure_chemical_state_indices
    if explicit_associations is not None:
        known = explicit_associations.dropna()
        association_is_implicit_single_state = (
            len(item.topology._chemical_states) == 1
            and len(known) == len(explicit_associations)
            and (known == 0).all()
        )
        if not association_is_implicit_single_state:
            issues.append(
                ConversionIssue(
                    attribute='structure_chemical_state_index',
                    reason=(
                        'molsysmt.MolSysBuilder cannot preserve the explicit '
                        'structure-to-chemical-state association.'
                    ),
                    kind='state_association_loss',
                    scope='chemical_state',
                )
            )

    return issues


def _selected_native_pdb_payload(
    item,
    selection='all',
    structure_indices='all',
    syntax='MolSysMT',
):
    """Return the exact native payload requested for PDB serialization."""

    import numpy as np
    from molsysmt._private.variables import is_all

    if is_all(selection):
        atom_indices = 'all'
    else:
        from molsysmt.basic import select

        atom_indices = select(
            item, selection=selection, syntax=syntax, skip_digestion=True
        )
    if is_all(structure_indices):
        selected_structures = 'all'
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
    selection='all',
    structure_indices='all',
    syntax='MolSysMT',
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
        payload, 'molsysmt.MolSys', target_form
    )

    expected_atom_ids = [
        str(index) for index in range(1, payload.topology.n_atoms + 1)
    ]
    actual_atom_ids = payload.topology.atoms['atom_id'].astype(str).tolist()
    if actual_atom_ids != expected_atom_ids:
        issues.append(ConversionIssue(
            attribute='atom_id',
            reason=(
                'PDB writing uses canonical serials because native atom IDs are '
                'not one unique contiguous decimal sequence.'
            ),
            kind='canonicalization',
            scope='topology',
        ))

    structure_ids = payload.structures.structure_id
    if structure_ids is not None and payload.structures.n_structures > 1:
        values = [str(value) for value in structure_ids]
        if (
            len(set(values)) != len(values)
            or any(
                not value.isdigit() or not 1 <= int(value) <= 9999
                for value in values
            )
        ):
            issues.append(ConversionIssue(
                attribute='structure_id',
                reason=(
                    'PDB MODEL identifiers must be unique decimal values between '
                    '1 and 9999 and will therefore be canonicalized.'
                ),
                kind='canonicalization',
                scope='structures',
            ))

    if (
        payload.structures.box is not None
        and payload.structures.n_structures > 1
    ):
        boxes = puw.get_value(payload.structures.box, to_unit='nm')
        if not np.allclose(boxes, boxes[0], equal_nan=True):
            issues.append(ConversionIssue(
                attribute='box',
                reason=(
                    'PDB CRYST1 stores one unit cell for the complete model set.'
                ),
                kind='schema_limitation',
                scope='structures',
            ))

    if payload.structures.coordinates is not None:
        coordinates = puw.get_value(
            payload.structures.coordinates, to_unit='angstrom'
        )
        if (
            not np.isfinite(coordinates).all()
            or np.any(coordinates < -999.999)
            or np.any(coordinates > 9999.999)
        ):
            issues.append(ConversionIssue(
                attribute='coordinates',
                reason='PDB coordinates exceed their fixed-width 8.3 fields.',
                kind='numeric_capacity',
                scope='structures',
            ))

    formal_charge = payload.topology._get_chemical_state_atom_attribute(
        'formal_charge'
    )
    if (
        formal_charge is not None
        and formal_charge.notna().any()
        and np.any(np.abs(formal_charge.dropna().to_numpy(dtype=int)) > 9)
    ):
        issues.append(ConversionIssue(
            attribute='formal_charge',
            reason='PDB formal-charge magnitudes occupy one decimal digit.',
            kind='numeric_capacity',
            scope='chemical_state',
        ))

    bonds = payload.topology._get_chemical_state_bonds()
    if 'bond_type' in bonds and bonds['bond_type'].notna().any():
        issues.append(ConversionIssue(
            attribute='bond_type',
            reason=(
                'PDB connectivity does not encode the source bond-type field; '
                'a covalent interpretation is reconstructed on reading.'
            ),
            kind='schema_limitation',
            scope='chemical_state',
        ))

    deduplicated = {}
    for issue in issues:
        deduplicated[(issue.attribute, issue.kind, issue.scope)] = issue
    return list(deduplicated.values())


def _pdb_handler(item, source_form):
    """Return a PDB handler and whether this audit owns it."""

    if source_form == 'molsysmt.PDBFileHandler':
        return item, False
    if source_form == 'file:pdb':
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

    topology = _build_topology_from_content(
        handler, get_missing_bonds=False
    )
    indices = select(
        topology, selection=selection, syntax=syntax, skip_digestion=True
    )
    return [int(index) for index in indices], canonical_atoms


def _audit_pdb_read(
    item,
    source_form,
    target_form,
    selection='all',
    syntax='MolSysMT',
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
        selected_keys = {
            canonical_atoms[index].site_key for index in selected_indices
        }
        issues = []
        for content_issue in handler.content.issues:
            if (
                content_issue.atom_site_keys
                and not selected_keys.intersection(content_issue.atom_site_keys)
            ):
                continue
            issues.append(ConversionIssue(
                attribute=content_issue.attribute,
                reason=content_issue.reason,
                kind='adapter_limitation',
                scope=_attribute_scope(content_issue.attribute),
            ))

        if any(
            canonical_atoms[index].insertion_code
            for index in selected_indices
        ):
            issues.append(ConversionIssue(
                attribute='group_id',
                reason=(
                    'Native group IDs do not encode the separate PDB insertion code.'
                ),
                kind='adapter_limitation',
                scope='topology',
            ))

        _, variants = _canonical_atoms(handler.content)
        _, unresolved_bonds, repeated_conect = _get_explicit_bonds(
            handler.content, canonical_atoms, variants
        )
        if unresolved_bonds:
            issues.append(ConversionIssue(
                attribute='bonded_atoms',
                reason=(
                    'At least one explicit PDB connectivity endpoint is missing '
                    'or ambiguous.'
                ),
                kind='adapter_limitation',
                scope='chemical_state',
            ))
        if repeated_conect:
            issues.append(ConversionIssue(
                attribute='bond_order',
                reason=(
                    'Repeated PDB CONECT endpoints are retained as one bond and '
                    'are not interpreted silently as a bond order.'
                ),
                kind='adapter_limitation',
                scope='chemical_state',
            ))

        if target_form == 'molsysmt.Topology':
            issues.append(ConversionIssue(
                attribute='coordinates',
                reason='A topology-only target intentionally omits PDB structures.',
                kind='target_projection',
                scope='structures',
            ))
        elif target_form == 'molsysmt.Structures':
            issues.append(ConversionIssue(
                attribute='atom_name',
                reason='A structures-only target intentionally omits PDB topology.',
                kind='target_projection',
                scope='topology',
            ))
        return issues
    finally:
        if opened_here:
            handler.close()


def _audit_coordinate_trajectory(source_form, target_form):
    """Return exhaustive losses for one narrow coordinate-format projection."""

    if target_form == 'molsysmt.Topology':
        return [ConversionIssue(
            attribute='coordinates',
            reason='A topology-only target intentionally omits trajectory coordinates.',
            kind='target_projection',
            scope='structures',
        )]
    if (
        source_form in {'file:xtc', 'mdtraj.XTCTrajectoryFile'}
        and target_form == 'mdtraj.Trajectory'
    ):
        return [ConversionIssue(
            attribute='structure_id',
            reason=(
                'MDTraj Trajectory has no independent carrier for XTC step IDs.'
            ),
            kind='schema_limitation',
            scope='structures',
        )]
    return []


def _audit_h5msm_to_structures(item, source_form):
    """Return losses from an H5MSM compound form to native structures."""

    opened_here = False
    if source_form == 'file:h5msm':
        from molsysmt.form.file_h5msm.to_molsysmt_H5MSMFileHandler import (
            to_molsysmt_H5MSMFileHandler,
        )

        handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
        opened_here = True
    else:
        handler = item

    try:
        issues = []
        topology = handler.file['topology']
        if int(topology.attrs.get('n_atoms', 0)) > 0:
            issues.append(ConversionIssue(
                attribute='atom_id',
                reason='A structures-only target intentionally omits H5MSM topology.',
                kind='target_projection',
                scope='topology',
            ))

        structures = handler.file['structures']
        state_indices = structures.get('chemical_state_index')
        if state_indices is not None and state_indices.shape[0] > 0:
            issues.append(ConversionIssue(
                attribute='structure_chemical_state_index',
                reason=(
                    'Native Structures does not carry H5MSM '
                    'structure-to-chemical-state associations.'
                ),
                kind='target_projection',
                scope='chemical_state',
            ))
        return issues
    finally:
        if opened_here:
            handler.close()


def _audit_registered_profile(
    item,
    source_form,
    target_form,
    selection='all',
    structure_indices='all',
    syntax='MolSysMT',
):
    """Return issues from one evidence-backed exhaustive audit profile."""

    pair = (source_form, target_form)
    if pair == ('molsysmt.Structures', 'molsysmt.StructuresDict'):
        return _audit_native_structures_to_dict(item)
    if pair == ('molsysmt.Topology', 'molsysmt.TopologyDict'):
        return _audit_native_topology_to_dict(item)
    if pair == ('molsysmt.MolSys', 'molsysmt.MolSysDict'):
        return _audit_native_molsys_to_dict(item)
    profile = _CONVERSION_AUDIT_PROFILES.get(pair)
    if (
        profile is not None
        and profile.get('mode') == 'declared_capability_projection'
    ):
        return _audit_declared_capability_projection(
            item,
            source_form,
            target_form,
        )
    if profile is not None and profile.get('mode') == 'molsys_to_builder':
        return _audit_native_molsys_to_builder(item)
    if (
        profile is not None
        and profile.get('mode') == 'builder_to_molsysdict'
    ):
        return _audit_native_builder_to_dict(item)
    if profile is not None and profile.get('mode') == 'pdb_write':
        return _audit_native_pdb_write(
            item,
            target_form,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
    if profile is not None and profile.get('mode') == 'pdb_read':
        return _audit_pdb_read(
            item,
            source_form,
            target_form,
            selection=selection,
            syntax=syntax,
        )
    if (
        profile is not None
        and profile.get('mode') == 'coordinate_trajectory'
    ):
        return _audit_coordinate_trajectory(source_form, target_form)
    if profile is not None and profile.get('mode') == 'h5msm_to_structures':
        return _audit_h5msm_to_structures(item, source_form)
    return []


def _native_multistate_has(item, source_form, attribute):
    topology = item.topology if source_form == 'molsysmt.MolSys' else item
    atom_columns = {
        'formal_charge': 'formal_charge',
        'atom_is_aromatic': 'is_aromatic',
        'n_unpaired_electrons': 'n_unpaired_electrons',
        'n_implicit_hydrogens': 'n_implicit_hydrogens',
        'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
        'atom_stereochemistry': 'stereochemistry',
    }
    bond_columns = {
        'bond_id': 'bond_id',
        'bond_order': 'bond_order',
        'fractional_bond_order': 'fractional_bond_order',
        'bond_type': 'bond_type',
        'bond_is_aromatic': 'is_aromatic',
        'bond_is_conjugated': 'is_conjugated',
        'bond_stereochemistry': 'stereochemistry',
        'bond_stereo_atom_indices': 'stereo_atom1_index',
        'bond_donor_atom_index': 'donor_atom_index',
        'bond_acceptor_atom_index': 'acceptor_atom_index',
        'bond_joins_components': 'joins_components',
        'bond_evidence': 'evidence',
    }
    if attribute in atom_columns:
        column = atom_columns[attribute]
        return any(
            column in state.atom_attributes
            and state.atom_attributes[column].notna().any()
            for state in topology._chemical_states
        )
    if attribute in bond_columns:
        column = bond_columns[attribute]
        return any(
            column in state.bonds and state.bonds[column].notna().any()
            for state in topology._chemical_states
        )
    return None


def _instance_has(module, item, attribute, source_form):
    if not module.attributes.get(attribute, False):
        return False
    if source_form in {'molsysmt.Topology', 'molsysmt.MolSys'}:
        topology = item.topology if source_form == 'molsysmt.MolSys' else item
        if (
            len(topology._chemical_states) != 1
            and topology._reference_chemical_state_index is None
        ):
            output = _native_multistate_has(item, source_form, attribute)
            if output is not None:
                return output
    return bool(
        module.has_attribute(
            item, attribute, include_none=False, skip_digestion=True
        )
    )


def build_conversion_report(
    molecular_system,
    from_form,
    to_form,
    selection='all',
    structure_indices='all',
    syntax='MolSysMT',
):
    """Build a conservative preflight report without mutating either system."""

    from molsysmt.form import _dict_modules

    target_form = _canonical_target_form(to_form)
    source_item, source_form = _single_source(molecular_system, from_form)
    issues = []

    if source_item is not None:
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
        if (
            not registered_profile
            and source_form in {'file:h5msm', 'molsysmt.H5MSMFileHandler'}
        ):
            if source_form == 'file:h5msm':
                from molsysmt.form.file_h5msm.to_molsysmt_Topology import (
                    to_molsysmt_Topology,
                )
            else:
                from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology import (
                    to_molsysmt_Topology,
                )

            inspection_item = to_molsysmt_Topology(source_item, skip_digestion=True)
            inspection_form = 'molsysmt.Topology'
            inspection_module = _dict_modules[inspection_form]
        if not registered_profile:
            target_attributes = _dict_modules[target_form].attributes
            for attribute in _CHEMICAL_ATTRIBUTES:
                if _instance_has(
                    inspection_module, inspection_item, attribute, inspection_form
                ) and not target_attributes.get(
                    attribute, False
                ):
                    issues.append(
                        ConversionIssue(
                            attribute=attribute,
                            reason=(
                                f'{target_form} cannot represent the supplied '
                                f'{attribute} semantics.'
                            ),
                        )
                    )

        if source_form in {'molsysmt.Topology', 'molsysmt.MolSys'}:
            topology = (
                source_item.topology
                if source_form == 'molsysmt.MolSys'
                else source_item
            )
            if (
                not registered_profile
                and len(topology._chemical_states) > 1
                and target_form not in {
                'molsysmt.Topology', 'molsysmt.MolSys', 'file:h5msm',
                'molsysmt.H5MSMFileHandler',
                }
            ):
                issues.append(
                    ConversionIssue(
                        attribute='chemical_state_index',
                        reason=(
                            f'{target_form} cannot preserve the ordered multi-state inventory.'
                        ),
                        kind='state_collapse',
                    )
                )

            if (
                target_form == 'pdbfixer.PDBFixer'
                and (
                    len(topology._chemical_states) == 1
                    or topology._reference_chemical_state_index is not None
                )
            ):
                source_bonds = topology._get_chemical_state_bonds()
                if source_bonds.empty:
                    issues.append(
                        ConversionIssue(
                            attribute='bonded_atoms',
                            reason=(
                                'PDBFixer may reconstruct standard-residue bonds when the '
                                'source declares a known-empty covalent graph.'
                            ),
                            kind='target_inference',
                        )
                    )

        if source_form in {'MDAnalysis.Topology', 'MDAnalysis.Universe'} and target_form in {
            'molsysmt.Topology', 'molsysmt.MolSys'
        }:
            from molsysmt.form.MDAnalysis_Topology._chemical_state import (
                has_opaque_bond_types,
            )

            mda_topology = (
                source_item._topology
                if source_form == 'MDAnalysis.Universe'
                else source_item
            )
            if has_opaque_bond_types(mda_topology):
                issues.append(
                    ConversionIssue(
                        attribute='bond_source_type',
                        reason=(
                            'MDAnalysis supplies an opaque scalar bond type that has no '
                            'documented canonical chemical mapping.'
                        ),
                        kind='adapter_limitation',
                    )
                )

        if source_form == 'parmed.Structure' and target_form in {
            'molsysmt.Topology', 'molsysmt.MolSys'
        }:
            from molsysmt.form.parmed_Structure._chemical_state import (
                has_mechanical_bond_types,
                has_unsupported_relationships,
            )

            if has_unsupported_relationships(source_item):
                issues.append(
                    ConversionIssue(
                        attribute='bond_type',
                        reason=(
                            'ParmEd contains ionic, hydrogen, three-center, or other '
                            'relationships that do not belong to the native covalent bond graph.'
                        ),
                        kind='adapter_limitation',
                    )
                )
            if has_mechanical_bond_types(source_item):
                issues.append(
                    ConversionIssue(
                        attribute='bond_mechanical_parameters',
                        reason=(
                            'ParmEd bond parameter objects belong to molecular mechanics and '
                            'are not imported by this topology conversion.'
                        ),
                        kind='adapter_limitation',
                    )
                )

        if source_form == 'mmcif.PdbxContainers.DataContainer' and target_form in {
            'molsysmt.Topology', 'molsysmt.MolSys'
        }:
            from molsysmt.form.mmcif_PdbxContainers_DataContainer._bond_state import (
                has_unknown_chem_comp_bond_orders,
            )

            if has_unknown_chem_comp_bond_orders(source_item):
                issues.append(
                    ConversionIssue(
                        attribute='bond_order',
                        reason=(
                            'mmCIF supplies a chem_comp_bond.value_order code that has '
                            'no documented canonical chemical mapping.'
                        ),
                        kind='adapter_limitation',
                    )
                )
    same_form = source_form == target_form
    audited_scopes = get_conversion_audit_scopes(source_form, target_form)
    is_exhaustive = is_conversion_audit_exhaustive(source_form, target_form)

    # Static graph audits cannot assume that every third-party identity
    # converter preserves its complete representation. At runtime, an actual
    # single-form identity instance supplies stronger evidence: the conversion
    # stays within the same representation and can be classified exhaustively.
    if source_item is not None and same_form:
        audited_scopes = ('all',)
        is_exhaustive = True

    outcome = 'lossy' if issues else ('exact' if same_form else 'equivalent')
    return ConversionReport(
        from_form=source_form,
        to_form=target_form,
        outcome=outcome,
        audited_scopes=audited_scopes,
        is_exhaustive=is_exhaustive,
        issues=tuple(issues),
    )
