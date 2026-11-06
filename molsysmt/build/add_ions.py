"""Adding monovalent ions by periodic whole-water replacement."""

from copy import deepcopy

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest


@signal(tags=["build", "solvation"])
@arg_digest()
def add_ions(
    molecular_system,
    anion="Cl-",
    n_anions=0,
    cation="Na+",
    n_cations=0,
    ionic_strength="0 molar",
    expected_total_charge=None,
    charge_source="formal_charge",
    min_solute_distance="0.5 nm",
    min_ion_distance="0.5 nm",
    random_seed=None,
    max_attempts=10,
    to_form="molsysmt.MolSys",
    return_report=False,
    skip_digestion=False,
):
    """Adding monovalent ions by reproducible periodic water replacement.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing stable molecule membership, one chemical
        state, one structure, finite coordinates and a nonsingular periodic box.
        Water molecules must be declared and have exactly one oxygen each.
    anion : str, default='Cl-'
        Negative species: 'Cl-', 'Br-', 'F-' or 'I-'.
    n_anions : int or str, default=0
        Additional anions, or 'neutralize' to resolve this population from charge.
    cation : str, default='Na+'
        Positive species: 'Na+', 'K+', 'Li+', 'Rb+' or 'Cs+'.
    n_cations : int or str, default=0
        Additional cations, or 'neutralize'. Booleans and negative counts fail.
    ionic_strength : quantity or str, default='0 molar'
        Additional 1:1 salt pairs: round-half-up of remaining water count times
        concentration in molar divided by 55.4 molar, after base replacements.
        This water-count proxy excludes base/neutralizing ions and existing ions;
        it is not a measured final ionic strength or a box-volume concentration.
    expected_total_charge : int or quantity, default=None
        Declared total of the entire source, including existing solvent/ions, in
        elementary-charge units. Used for neutralization instead of charge_source.
        A neutralizing total must be within 1e-4 e of an integer.
    charge_source : str, default='formal_charge'
        Neutralization reads complete stored 'formal_charge' or 'partial_charge'.
        'physical_pH7' explicitly opts into a tabulated group approximation.
        Exact-count-only calls do not require or infer source charge.
    min_solute_distance : quantity or str, default='0.5 nm'
        Positive clearance between a new ion and every source nonwater atom.
    min_ion_distance : quantity or str, default='0.5 nm'
        Positive clearance between new ions and between new and existing ions.
        Distances equal to either cutoff are excluded conservatively.
    random_seed : int, default=None
        Nonnegative PCG64 seed. None generates and reports a fresh seed.
        Reproduction requires the same ordered input, parameters and software.
    max_attempts : int, default=10
        Positive bound on independent greedy placement attempts. Failure can
        occur even when a different packing exists; no relaxation is performed.
    to_form : str, default='molsysmt.MolSys'
        Requested output form. Other forms may discard native reports/analyses.
    return_report : bool, default=False
        Return a dictionary with molecular_system and a detached report.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or dict
        Independent system, optionally with an operation-scoped report containing
        counts, seed, distances in nm, charge evidence and both atom maps. A
        removed input atom maps to -1; an added output atom maps to -1 in the
        reverse map. Ion atoms replace complete water molecules, including extra
        sites, and receive known formal charges, without partial charges or
        force-field parameters. Original coordinate values and box are retained.

    Raises
    ------
    ArgumentError
        If counts, species, units, seed or algorithm parameters are invalid.
    StructuralInconsistencyError
        If source data/charge are insufficient, neutralization is impossible,
        or placement cannot satisfy the requested distances within its bound.

    Notes
    -----
    The random_water_replacement method is inspired by OpenMM Modeller._addIons,
    with shared MolSysMT periodic cell-list geometry and an explicit seed and
    failure bound. It does not reproduce all OpenMM criteria or equilibrate a
    solution. All source counts refer to added populations; existing ions remain.
    For mixed explicit/'neutralize' requests the automatic species must cancel
    the source plus the explicitly added charge, or the request fails.

    Native output stores a detached preparation report in ChemicalStates. Atom
    edits remap analyses and invalidate their evaluated coverage conservatively;
    a zero-addition result preserves coverage. Native atom-growth policies clear
    unsupported atom-aligned mechanical/structural observations with diagnostics.
    No source object is mutated, including on failure. Public quantities honor
    PyUnitWizard; native coordinates remain in nm without changing unit policy.

    See Also
    --------
    molsysmt.build.solvate : Construct solvent before adding ions.
    molsysmt.build.make_water_box : Construct a standalone water box.

    Examples
    --------
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> water = msm.build.make_water_box(msm.pyunitwizard.quantity(2*np.eye(3), 'nm'))
    >>> result = msm.build.add_ions(water, n_cations=1, n_anions=1, random_seed=7,
    ...                           return_report=True)
    >>> result['report']['added']['total']
    2

    .. admonition:: User guide

       See :ref:`Tutorial_Add_ions` for count, charge and correspondence contracts.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__
    from molsysmt._private.pbc_validation import validate_box_array
    from molsysmt._private.preparation_history import append_report
    from molsysmt.basic import convert, remove

    from . import _ion_replacement as core

    # Validate explicitly at the older supported ArgDigest boundary as well.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=core.CALLER)
    n_cations = core.nonnegative_integer(n_cations, "n_cations", neutralize=True)
    n_anions = core.nonnegative_integer(n_anions, "n_anions", neutralize=True)
    concentration = core.scalar_quantity(ionic_strength, "molar", "ionic_strength")
    solute_cutoff = core.scalar_quantity(
        min_solute_distance, "nm", "min_solute_distance", positive=True
    )
    ion_cutoff = core.scalar_quantity(
        min_ion_distance, "nm", "min_ion_distance", positive=True
    )
    source = convert(molecular_system, to_form="molsysmt.MolSys")
    if (
        source.topology is None
        or source.chemical_states is None
        or source.chemical_states.n_chemical_states != 1
    ):
        core.fail(
            "Ion replacement requires stable topology and exactly one chemical state."
        )
    coordinates = None if source.structures is None else source.structures.coordinates
    if coordinates is None or coordinates.shape != (1, source.topology.n_atoms, 3):
        core.fail(
            "Ion replacement requires exactly one structure with coordinates for every atom."
        )
    xyz = np.asarray(puw.get_value(coordinates, to_unit="nm"))
    if not np.isfinite(xyz).all():
        core.fail("Ion replacement requires finite source coordinates.")
    box = source.structures.box
    validate_box_array(
        None if box is None else puw.get_value(box, to_unit="nm"), 1, caller=core.CALLER
    )
    oxygens, membership, water_atoms = core.water_candidates(source)
    charge, charge_origin = None, "not_required"
    if n_cations == "neutralize" or n_anions == "neutralize":
        charge, charge_origin = core.charge_total(
            source, expected_total_charge, charge_source
        )
    positive, negative, pairs = core.resolve_counts(
        n_cations, n_anions, charge, len(oxygens), concentration
    )
    seed = int(np.random.SeedSequence().entropy) if random_seed is None else random_seed
    count = positive + negative
    n_atoms = source.topology.n_atoms
    removed = np.empty(0, dtype=np.int64)
    removed_molecules = np.empty(0, dtype=np.int64)
    attempts = 0
    if count:
        chosen, attempts = core.place(
            source,
            oxygens,
            water_atoms,
            count,
            solute_cutoff,
            ion_cutoff,
            np.random.Generator(np.random.PCG64(seed)),
            max_attempts,
        )
        removed_molecules = membership[oxygens[chosen]]
        removed = np.flatnonzero(np.isin(membership, removed_molecules))
        positions = xyz[0, oxygens[chosen]].copy()
        source = remove(source, selection=removed, to_form="molsysmt.MolSys")
        source.interactions = {
            name: analysis.invalidate_structures(np.arange(analysis.n_structures))
            for name, analysis in source.interactions.items()
        }
        for species, points in (
            (cation, positions[:positive]),
            (anion, positions[positive:]),
        ):
            if len(points):
                ions = core.build_ions(species, points)
                ions.structures.box = source.structures.box
                source.add(ions)
    retained = np.setdiff1d(np.arange(n_atoms, dtype=np.int64), removed)
    old_to_new = np.full(n_atoms, -1, dtype=np.int64)
    old_to_new[retained] = np.arange(len(retained))
    new_to_old = np.concatenate((retained, np.full(count, -1, dtype=np.int64)))
    report = dict(
        schema="molsysmt.ion_replacement@1",
        n_source_atoms=n_atoms,
        n_output_atoms=source.topology.n_atoms,
        method="random_water_replacement",
        requested=dict(
            cation=cation,
            n_cations=n_cations,
            anion=anion,
            n_anions=n_anions,
            ionic_strength_molar=concentration,
        ),
        added=dict(cation=positive, anion=negative, salt_pairs=pairs, total=count),
        charge=dict(
            source=charge_origin,
            total_elementary_charge=charge,
            output_total_elementary_charge=None
            if charge is None
            else charge + positive - negative,
        ),
        random=dict(
            generator="PCG64",
            seed=str(seed),
            attempts=attempts,
            max_attempts=max_attempts,
        ),
        parameters=dict(
            min_solute_distance_nm=solute_cutoff,
            min_ion_distance_nm=ion_cutoff,
            pbc=True,
            concentration_convention="water_count_55.4_molar_after_base_replacements",
        ),
        removed_water_molecule_indices=removed_molecules.copy(),
        removed_atom_indices=removed,
        source_to_output_atom_indices=old_to_new,
        output_to_source_atom_indices=new_to_old,
        software=dict(molsysmt=__version__, numpy=np.__version__),
    )
    core.attribute(report)
    append_report(source.chemical_states._states[0], report, 0)
    output = (
        source if to_form == "molsysmt.MolSys" else convert(source, to_form=to_form)
    )
    return (
        dict(molecular_system=output, report=deepcopy(report))
        if return_report
        else output
    )
