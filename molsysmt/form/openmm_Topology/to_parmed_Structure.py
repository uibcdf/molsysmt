from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
@dep_digest("parmed")
@dep_digest("openmm")
def to_parmed_Structure(item, atom_indices="all", skip_digestion=False):
    """
    Converting OpenMM inventory, explicit bond semantics and one cell to ParmEd.


    Parameters
    ----------
    item : molecular system
        Topology supplying atom/group IDs, formal charges, bonds and optional
        periodic vectors. No coordinate structures are present in this form.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Detached, unparameterized topology with preserved explicit numeric bond
        orders and qualitative types. Cell lengths are in angstroms and angles
        in degrees.

    Raises
    ------
    LibraryNotFoundError
        If the optional ParmEd or OpenMM provider is unavailable.
    NotCompatibleConversionError
        If labels, an unknown numeric order or the raw box orientation cannot
        be preserved by ParmEd.


    .. versionadded:: 1.0.0
    """

    import parmed as pmd
    from parmed.topologyobjects import QualitativeBondType

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.parmed_Structure._from_native import (
        _serial,
        openmm_export_limitations,
        reject_limitations,
        set_box,
    )

    from .extract import extract

    selected = extract(
        item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True
    )
    reject_limitations(openmm_export_limitations(selected), "openmm.Topology")
    vectors = selected.getPeriodicBoxVectors()
    box = (
        None
        if vectors is None
        else puw.quantity([puw.get_value(vectors, to_unit="nm")], "nm")
    )
    result = pmd.Structure()
    groups = {}
    for group in selected.residues():
        provider_group = pmd.Residue(
            group.name,
            _serial(group.id),
            chain=group.chain.id,
            insertion_code=group.insertionCode,
            list=result.residues,
        )
        result.residues.append(provider_group)
        groups[group] = provider_group
    for atom in selected.atoms():
        group = atom.residue
        provider_atom = pmd.Atom(
            name=atom.name,
            number=_serial(atom.id),
            atomic_number=0 if atom.element is None else atom.element.atomic_number,
            mass=0
            if atom.element is None
            else puw.get_value(atom.element.mass, to_unit="dalton"),
            formal_charge=atom.formalCharge,
        )
        groups[group].add_atom(provider_atom)
        result.atoms.append(provider_atom)
    qualitative_types = {
        "Single": QualitativeBondType.SINGLE,
        "Double": QualitativeBondType.DOUBLE,
        "Triple": QualitativeBondType.TRIPLE,
        "Aromatic": QualitativeBondType.AROMATIC,
    }
    for bond in selected.bonds():
        result.bonds.append(
            pmd.Bond(
                result.atoms[bond[0].index],
                result.atoms[bond[1].index],
                order=bond.order,
                qualitative_type=qualitative_types.get(str(bond.type)),
            )
        )
    set_box(result, box)
    return result
