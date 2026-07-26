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
        'b_factor',
        'alternate_location',
        'occupancy',
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
        'temperature',
        'potential_energy',
        'kinetic_energy',
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
}

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


def _audit_registered_profile(item, source_form, target_form):
    """Return issues from one evidence-backed exhaustive audit profile."""

    pair = (source_form, target_form)
    if pair == ('molsysmt.Structures', 'molsysmt.StructuresDict'):
        return _audit_native_structures_to_dict(item)
    if pair == ('molsysmt.Topology', 'molsysmt.TopologyDict'):
        return _audit_native_topology_to_dict(item)
    if pair == ('molsysmt.MolSys', 'molsysmt.MolSysDict'):
        return _audit_native_molsys_to_dict(item)
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


def build_conversion_report(molecular_system, from_form, to_form):
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
            _audit_registered_profile(source_item, source_form, target_form)
        )
        source_module = _dict_modules[source_form]
        inspection_item = source_item
        inspection_form = source_form
        inspection_module = source_module
        if source_form in {'file:h5msm', 'molsysmt.H5MSMFileHandler'}:
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
