"""Building solvent boxes and delegating native ion replacement."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError

"""
Solvate Box
==============
Methods and wrappers to create and solvate boxes
"""


def _build_tiled_water(water_tile, n_x, n_y, n_z, tile_nm):
    """Build a tiled water MolSys using pure numpy, without creating N³ intermediate objects.

    Parameters
    ----------
    water_tile : molsysmt.MolSys
        Pre-equilibrated single-box water template.
    n_x, n_y, n_z : int
        Number of tile repetitions in each direction.
    tile_nm : float
        Edge length of one water tile (nm).

    Returns
    -------
    molsysmt.MolSys
        A single MolSys containing all n_x*n_y*n_z copies of the water box
        with correct translated coordinates, ready for out-of-box filtering.
    """
    import pandas as pd

    from molsysmt.native import MolSys, Structures
    from molsysmt.native._chemical_state import Bonds_DataFrame

    topo = water_tile.topology
    topo_bonds = water_tile.chemical_states._get_chemical_state_bonds()
    n_atoms_tile = topo.n_atoms
    n_groups_tile = topo.n_groups
    n_bonds_tile = len(topo_bonds)

    # ── build offset grid ───────────────────────────────────────────────────
    ix = np.arange(n_x, dtype=np.float64)
    iy = np.arange(n_y, dtype=np.float64)
    iz = np.arange(n_z, dtype=np.float64)
    IZ, IY, IX = np.meshgrid(iz, iy, ix, indexing="ij")  # each (n_z, n_y, n_x)
    offsets = np.stack(
        [IX.ravel() * tile_nm, IY.ravel() * tile_nm, IZ.ravel() * tile_nm], axis=1
    )  # (n_tiles, 3)
    n_tiles = offsets.shape[0]

    # ── tile coordinates ─────────────────────────────────────────────────────
    # template_xyz: (n_atoms_tile, 3)  →  broadcast to (n_tiles, n_atoms_tile, 3)
    template_xyz = puw.get_value(water_tile.structures.coordinates, to_unit="nm")[
        0
    ]  # (n_atoms_tile, 3)
    tiled_xyz = (
        template_xyz[np.newaxis] + offsets[:, np.newaxis]
    )  # (n_tiles, n_atoms_tile, 3)
    all_xyz = tiled_xyz.reshape(1, n_tiles * n_atoms_tile, 3)  # (1, total_atoms, 3)

    # ── tile topology arrays ──────────────────────────────────────────────────
    n_total_atoms = n_tiles * n_atoms_tile
    n_total_groups = n_tiles * n_groups_tile
    n_total_bonds = n_tiles * n_bonds_tile

    # atoms
    atom_name_base = topo.atoms["atom_name"].to_numpy(dtype=object)
    atom_type_base = topo.atoms["atom_type"].to_numpy(dtype=object)
    grp_idx_base = topo.atoms["group_index"].to_numpy(dtype=np.int64)

    atom_names = np.tile(atom_name_base, n_tiles)
    atom_types = np.tile(atom_type_base, n_tiles)
    grp_offsets = np.repeat(
        np.arange(n_tiles, dtype=np.int64) * n_groups_tile, n_atoms_tile
    )
    group_indices = np.tile(grp_idx_base, n_tiles) + grp_offsets
    # component_index == group_index for water (one water per component)
    component_indices = group_indices.copy()
    chain_indices = np.zeros(n_total_atoms, dtype=np.int64)
    atom_ids = np.arange(1, n_total_atoms + 1, dtype=object).astype(str)

    # groups
    gname_base = topo.groups["group_name"].to_numpy(dtype=object)
    gtype_base = topo.groups["group_type"].to_numpy(dtype=object)
    mol_idx_base = topo.groups["molecule_index"].to_numpy(dtype=np.int64)

    group_names = np.tile(gname_base, n_tiles)
    group_types = np.tile(gtype_base, n_tiles)
    mol_offsets = np.repeat(
        np.arange(n_tiles, dtype=np.int64) * n_groups_tile, n_groups_tile
    )
    mol_indices = np.tile(mol_idx_base, n_tiles) + mol_offsets
    group_ids = np.arange(1, n_total_groups + 1, dtype=object).astype(str)

    # bonds
    b1_base = topo_bonds["atom1_index"].to_numpy(dtype=np.int64)
    b2_base = topo_bonds["atom2_index"].to_numpy(dtype=np.int64)
    bond_offsets = np.repeat(
        np.arange(n_tiles, dtype=np.int64) * n_atoms_tile, n_bonds_tile
    )
    b1 = np.tile(b1_base, n_tiles) + bond_offsets
    b2 = np.tile(b2_base, n_tiles) + bond_offsets

    # ── assemble Topology ────────────────────────────────────────────────────
    result = MolSys(
        n_atoms=n_total_atoms,
        n_groups=n_total_groups,
        n_components=n_total_groups,  # one component per water
        n_molecules=n_total_groups,
        n_entities=0,
        n_chains=1,
        n_bonds=n_total_bonds,
    )

    new_topo = result.topology
    new_topo.atoms["atom_id"] = pd.array(atom_ids, dtype="string")
    new_topo.atoms["atom_name"] = atom_names
    new_topo.atoms["atom_type"] = atom_types
    new_topo.atoms["group_index"] = pd.array(group_indices, dtype="Int64")
    result.chemical_states._set_component_indices(component_indices)
    new_topo.atoms["chain_index"] = pd.array(chain_indices, dtype="Int64")

    new_topo.groups["group_id"] = pd.array(group_ids, dtype="string")
    new_topo.groups["group_name"] = group_names
    new_topo.groups["group_type"] = group_types
    new_topo.groups["molecule_index"] = pd.array(mol_indices, dtype="Int64")

    chain_row = topo.chains.iloc[0]
    new_topo.chains["chain_id"] = pd.array([chain_row["chain_id"]], dtype="string")
    new_topo.chains["chain_name"] = [chain_row["chain_name"]]
    new_topo.chains["chain_type"] = [chain_row.get("chain_type", None)]

    bonds_df = Bonds_DataFrame(n_total_bonds)
    bonds_df["atom1_index"] = pd.array(b1, dtype="Int64")
    bonds_df["atom2_index"] = pd.array(b2, dtype="Int64")
    result.chemical_states._set_chemical_state_bonds(bonds_df)

    # ── assemble Structures ──────────────────────────────────────────────────
    new_struc = Structures(
        coordinates=puw.quantity(all_xyz, "nm"),
        structure_id=np.array(["1"], dtype=object),
    )

    # Declare stable hierarchy once during construction; later chemistry edits
    # must not be needed to recover solvent/ion molecule labels.
    new_topo.rebuild_molecules(redefine_indices=False)
    new_topo.rebuild_entities()
    result.structures = new_struc
    return result


def _place_in_box_origin_convention(item):
    """Translate a solvated system so the box it declares occupies ``[0, L)``.

    `devguide/INTERFACES.md`, *Periodic box origin*: the box vectors describe shape and
    size, and the cell they span starts at the origin. The three solvation engines do
    not agree on this by themselves — the native one centres the solute before adding
    water and lands there, while OpenMM's `Modeller` and PDBFixer return a system
    centred on the origin, which is a corner of that cell.

    The move is a rigid translation, so no molecule is split and nothing else changes.
    It is idempotent: a system already in the convention is shifted by zero.
    """

    import numpy as np

    from molsysmt.basic import get
    from molsysmt.structure import translate

    box = get(item, element="system", box=True, skip_digestion=True)
    if box is None:
        return item

    box_value = np.asarray(puw.get_value(box, to_unit="nm"), dtype=float)[0]
    coordinates = np.asarray(
        puw.get_value(
            get(item, element="system", coordinates=True, skip_digestion=True),
            to_unit="nm",
        ),
        dtype=float,
    )

    system_center = (coordinates[0].min(axis=0) + coordinates[0].max(axis=0)) / 2.0
    box_center = 0.5 * box_value.sum(axis=0)
    shift = (box_center - system_center).reshape(1, 1, 3)

    if np.allclose(shift, 0.0, atol=1e-6):
        return item

    return translate(item, translation=puw.quantity(shift, "nm"), in_place=False)


@signal(tags=["build", "solvation"])
@arg_digest()
@dep_digest("openmm", when={"engine": "OpenMM"})
@dep_digest("pdbfixer", when={"engine": "PDBFixer"})
def solvate(
    molecular_system,
    box_shape="truncated octahedral",
    clearance="14.0 angstroms",
    anion="Cl-",
    n_anions="neutralize",
    cation="Na+",
    n_cations="neutralize",
    ionic_strength="0.0 molar",
    water_model="TIP3P",
    engine="OpenMM",
    to_form=None,
    verbose=False,
    random_seed=None,
    skip_digestion=False,
):
    """
    Solvating a molecular system with explicit water molecules and ions.

    This function places the molecular system inside a solvent box of the chosen
    geometry, fills it with explicit water molecules of the selected model, and
    optionally adds counterions to neutralise the system charge and/or reach a
    target ionic strength.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format. The system must
        contain exactly one structure. Select one structure first with
        ``structure_indices`` when the input is an ensemble or trajectory.
    box_shape : str, default='truncated octahedral'
        'cubic', 'truncated octahedral' or 'rhombic dodecahedral'. Native
        MolSysMT also supports 'rectangular'.
    clearance : quantity or str, default='14.0 angstroms'
        Positive solvent clearance, using any supported length unit.
    anion : str, default='Cl-'
        Monovalent negative ion: 'Cl-', 'Br-', 'F-' or 'I-'.
    n_anions : int or str, default='neutralize'
        Additional anions, or 'neutralize'. OpenMM/native explicit counts
        are applied through build.add_ions; PDBFixer rejects explicit counts.
    cation : str, default='Na+'
        Monovalent positive ion: 'Na+', 'K+', 'Li+', 'Rb+' or 'Cs+'.
    n_cations : int or str, default='neutralize'
        Additional cations, or 'neutralize'. Mixed requests solve the automatic
        population from source charge plus the explicitly added population.
    ionic_strength : quantity or str, default='0.0 molar'
        Nonnegative additional salt concentration. Native replacement adds
        equal ion pairs after base replacements using the 55.4 molar
        water-count proxy; it does not measure final total ionic strength.
    water_model : str, default='TIP3P'
        Water model parameter identifier (e.g., 'TIP3P').
    engine : str, default='OpenMM'
        Solvent builder: 'OpenMM', 'PDBFixer' or native 'MolSysMT'. Optional
        providers are loaded only for their selected route.
    to_form : str, default=None
        Requested output form. None preserves the input form.
    verbose : bool, default=False
        Legacy verbosity control; no additional report is printed.
    random_seed : int, default=None
        Nonnegative PCG64 seed for native ion placement. Supplying one also
        selects native placement after OpenMM water construction. PDBFixer
        rejects this control because its public solvation API cannot honor it.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system
        A new solvated molecular system in the form specified by ``to_form`` (or
        in the same form as the input). Component, molecule, and chain metadata
        from the original system are preserved and entity labels are rebuilt.


    Raises
    ------
    ArgumentError
        If the source does not contain exactly one structure, controls are
        invalid, or a PDBFixer request includes explicit counts or a seed.
    StructuralInconsistencyError
        If native replacement cannot place the requested population, or a
        charge-dependent request is inconsistent.
    NotImplementedError
        Raised if the requested ``engine`` or ``water_model`` is not supported.


    Notes
    -----
    After solvation, water molecules and ions are automatically assigned to a new
    chain by ``assign_selection_to_new_chain``. In the OpenMM route, retained
    source atom/group IDs keep their original string labels, duplicates and
    missing values in native output. Only generated sites receive new labels:
    positive decimal strings starting at 1, skipping every known retained label
    in their atom or group namespace. IDs are never parsed as integer indices.
    Native finalization precedes the requested output conversion; foreign forms
    and file formats retain their own label/serial representation constraints.
    Provider traversal must agree with positional atom/group indices; a
    noncanonical source is rejected before solvent construction.

    The forcefield used for solvation is read from the molecular system when
    available; otherwise the MolSysMT default forcefield is used.

    Unseeded default OpenMM neutralization/concentration uses the ordinary
    provider algorithm. Explicit counts or a seed construct water with provider
    neutralization/salt disabled, then call build.add_ions. Neutralization in
    that route uses the OpenMM force-field charge of the complete source. Native
    solvation retains its historical physical_pH7 tabulated source approximation;
    this is not a chemical-state or force-field assignment. For explicit charge
    control use build.add_ions on a separately solvated system.

    Native replacement retains seed, parameters, provenance and atom maps in
    ChemicalStates preparation history, with axes local to the water-replacement
    input, not the original unsolvated source. Its solvation context records the
    original source atom/group counts: the first source-atom-count entries of
    the forward map refer to that original source, including -1 for an original
    water replaced by an ion. Ordinary OpenMM construction without native
    replacement retains the source as the leading atom/group prefix. Source
    ownership and positional correspondence do not depend on unique labels.
    Counts mean added ions. Known
    charged waters fail; placement does not equilibrate ions or assign new
    force-field parameters. Unsupported atom-aligned observations may be cleared
    by native atom-growth policies. Native coordinates remain in nm regardless
    of the application's PyUnitWizard presentation policy.

    OpenMM solvation with native ion replacement retains a detached software
    reference in that preparation history. Optional Ackredit tracking uses the
    same versioned OpenMM identity as implicit-model construction, with separate
    operation contexts in the application's current session. No attribution
    provider is required for the scientific result or stored provenance.

    See Also
    --------
    molsysmt.build.add_ions : Add ions to existing solvent with explicit evidence.
    molsysmt.build.make_water_box : Build a standalone water box.

    Examples
    --------
    Selecting one structure from an ensemble before solvation:

    >>> import molsysmt as msm
    >>> ensemble = msm.systems['Trp-Cage']['1l2y.h5msm']
    >>> molsys = msm.convert(
    ...     ensemble, to_form='molsysmt.MolSys', structure_indices=0
    ... )
    >>> msm.get(molsys, n_structures=True)
    1

    .. admonition:: User guide

       See :ref:`Tutorial_Solvate` and :ref:`Tutorial_Add_ions` for engine contracts.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import convert, get, get_form
    from molsysmt.build._ion_replacement import scalar_quantity

    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller="molsysmt.build.solvate")
    scalar_quantity(clearance, "nm", "clearance", positive=True)
    scalar_quantity(ionic_strength, "molar", "ionic_strength")
    if box_shape == "rectangular" and engine != "MolSysMT":
        raise ArgumentError(
            "box_shape",
            value=box_shape,
            caller="molsysmt.build.solvate",
            message="Rectangular solvation is supported by engine='MolSysMT'.",
        )
    if engine == "PDBFixer" and (
        n_anions != "neutralize" or n_cations != "neutralize" or random_seed is not None
    ):
        raise ArgumentError(
            "n_anions/n_cations/random_seed",
            caller="molsysmt.build.solvate",
            message="PDBFixer supports only default neutralization with no seed control. Use engine='OpenMM' or 'MolSysMT' for explicit counts or seeded native placement.",
        )

    n_structures = get(molecular_system, n_structures=True)
    if n_structures != 1:
        raise ArgumentError(
            "molecular_system",
            value=n_structures,
            caller="molsysmt.build.solvate",
            message=(
                f"solvate() received {n_structures} structures, but solvation requires "
                "exactly one. Select one structure with structure_indices before "
                "calling solvate()."
            ),
        )

    if to_form is None:
        to_form = get_form(molecular_system)

    if engine == "OpenMM":
        from openmm import Vec3
        from openmm.app import ForceField

        from molsysmt.basic import get, set
        from molsysmt.build._private import assign_selection_to_new_chain
        from molsysmt.configure import default_attribute
        from molsysmt.molecular_mechanics import get_engine_forcefield

        component_indices, component_names = get(
            molecular_system,
            element="component",
            component_index=True,
            component_name=True,
        )
        molecule_indices, molecule_names = get(
            molecular_system,
            element="molecule",
            molecule_index=True,
            molecule_name=True,
        )
        chain_indices, chain_ids, chain_names = get(
            molecular_system,
            element="chain",
            chain_index=True,
            chain_id=True,
            chain_name=True,
        )

        clearance = puw.convert(clearance, to_form="openmm.unit")
        ionic_strength = puw.convert(ionic_strength, to_form="openmm.unit")

        modeller = convert(molecular_system, to_form="openmm.Modeller")
        from ._solvation_ids import capture, restore

        source_labels = capture(molecular_system, modeller)

        aux_water_model, aux_forcefield = get(
            molecular_system, water_model=True, forcefield=True
        )

        if aux_water_model is not None:
            water_model = aux_water_model

        if aux_forcefield is None:
            forcefield = default_attribute["forcefield"]
        else:
            forcefield = aux_forcefield

        forcefield = get_engine_forcefield(
            forcefield, water_model=water_model, engine="OpenMM"
        )

        solvent_model = None

        if water_model == "SPC":
            solvent_model = "tip3p"
        elif water_model in {
            "TIP3P",
            "TIP3P-FB",
            "SPC/E",
            "TIP4P-EW",
            "TIP4P-FB",
            "TIP5P",
        }:
            solvent_model = {
                "TIP3P": "tip3p",
                "TIP3P-FB": "tip3p",
                "SPC/E": "spce",
                "TIP4P-EW": "tip4pew",
                "TIP4P-FB": "tip4pew",
                "TIP5P": "tip5p",
            }[water_model]
        else:
            raise NotImplementedError()

        openmm_forcefield = ForceField(*forcefield)
        native_ions = (
            n_anions != "neutralize"
            or n_cations != "neutralize"
            or random_seed is not None
        )
        ion_strength = ionic_strength
        ion_options = {}
        solute_charge = None
        if native_ions:
            from openmm import unit

            from molsysmt.physchem import get_charge

            if n_anions == "neutralize" or n_cations == "neutralize":
                solute_charge = get_charge(
                    openmm_forcefield.createSystem(modeller.topology),
                    definition="OpenMM",
                    element="system",
                )
            ion_strength = 0 * unit.molar
            ion_options["neutralize"] = False

        if box_shape == "truncated octahedral":
            max_size = max(
                max((pos[i] for pos in modeller.positions))
                - min((pos[i] for pos in modeller.positions))
                for i in range(3)
            )
            vectors = (
                Vec3(1.0, 0, 0),
                Vec3(1.0 / 3.0, 2.0 * np.sqrt(2.0) / 3.0, 0.0),
                Vec3(-1.0 / 3.0, np.sqrt(2.0) / 3.0, np.sqrt(6.0) / 3.0),
            )
            box_vectors = [(max_size + clearance) * v for v in vectors]

            modeller.addSolvent(
                openmm_forcefield,
                model=solvent_model,
                boxVectors=box_vectors,
                ionicStrength=ion_strength,
                positiveIon=cation,
                negativeIon=anion,
                **ion_options,
            )

        elif box_shape == "rhombic dodecahedral":
            max_size = max(
                max((pos[i] for pos in modeller.positions))
                - min((pos[i] for pos in modeller.positions))
                for i in range(3)
            )
            vectors = (
                Vec3(1.0, 0.0, 0.0),
                Vec3(0.0, 1.0, 0.0),
                Vec3(0.5, 0.5, np.sqrt(2) / 2),
            )
            box_vectors = [(max_size + clearance) * v for v in vectors]

            modeller.addSolvent(
                openmm_forcefield,
                model=solvent_model,
                boxVectors=box_vectors,
                ionicStrength=ion_strength,
                positiveIon=cation,
                negativeIon=anion,
                **ion_options,
            )

        else:
            modeller.addSolvent(
                openmm_forcefield,
                model=solvent_model,
                padding=clearance,
                ionicStrength=ion_strength,
                positiveIon=cation,
                negativeIon=anion,
                **ion_options,
            )

        tmp_item = convert(modeller, to_form="molsysmt.MolSys")

        del modeller

        set(
            tmp_item,
            element="component",
            selection=component_indices,
            component_name=component_names,
            skip_digestion=True,
        )
        set(
            tmp_item,
            element="molecule",
            selection=molecule_indices,
            molecule_name=molecule_names,
            skip_digestion=True,
        )
        set(
            tmp_item,
            element="chain",
            selection=chain_indices,
            chain_id=chain_ids,
            chain_name=chain_names,
            skip_digestion=True,
        )

        tmp_item.topology.rebuild_entities(
            redefine_indices=True,
            redefine_ids=True,
            redefine_names=True,
            redefine_types=True,
        )

        assign_selection_to_new_chain(
            tmp_item, selection='group_type in ["water","ion"]'
        )

        tmp_item = _place_in_box_origin_convention(tmp_item)

        source_to_output = None
        if native_ions:
            from molsysmt.build.add_ions import add_ions

            tmp_item = add_ions(
                tmp_item,
                anion=anion,
                n_anions=n_anions,
                cation=cation,
                n_cations=n_cations,
                ionic_strength=ionic_strength,
                expected_total_charge=solute_charge,
                random_seed=random_seed,
            )
            history = tmp_item.chemical_states._states[0]._preparation_history[-1][
                "report"
            ]
            source_to_output = history["source_to_output_atom_indices"]
            from copy import deepcopy

            import openmm

            from molsysmt import _ackredit
            from molsysmt._private.scientific_citations import SOFTWARE

            history["solvation"] = dict(
                engine="OpenMM",
                version=openmm.__version__,
                forcefield=list(forcefield),
                water_model=water_model,
                charge_source="forcefield"
                if solute_charge is not None
                else "not_required",
                n_source_atoms=len(source_labels["atom_ids"]),
                n_source_groups=len(source_labels["group_ids"]),
            )
            item = dict(
                id=f"software:openmm:{openmm.__version__}",
                type="software",
                **deepcopy(SOFTWARE["openmm"]),
                version=openmm.__version__,
                roles=["executed_software"],
            )
            history["software"]["openmm"] = openmm.__version__
            history["solvation"]["attribution"] = dict(
                schema="molsysmt.scientific_attribution@1",
                target="molsysmt.build.solvate",
                items=[item],
            )
            with _ackredit.scope("molsysmt.build.solvate") as provider:
                _ackredit.credit(
                    provider,
                    [item],
                    "molsysmt.build.solvate",
                    contextual=True,
                    context={
                        "engine": "openmm",
                        "forcefield": list(forcefield),
                        "water_model": water_model,
                        "charge_source": history["solvation"]["charge_source"],
                    },
                )
        restore(tmp_item, source_labels, source_to_output)
        if to_form != "molsysmt.MolSys":
            tmp_item = convert(tmp_item, to_form=to_form)
        return tmp_item

    elif engine == "PDBFixer":
        from openmm import Vec3

        from molsysmt.basic import get, set
        from molsysmt.build._private import assign_selection_to_new_chain

        component_indices, component_names = get(
            molecular_system,
            element="component",
            component_index=True,
            component_name=True,
        )
        molecule_indices, molecule_names = get(
            molecular_system,
            element="molecule",
            molecule_index=True,
            molecule_name=True,
        )
        chain_indices, chain_ids, chain_names = get(
            molecular_system,
            element="chain",
            chain_index=True,
            chain_id=True,
            chain_name=True,
        )

        clearance = puw.convert(clearance, to_form="openmm.unit")
        ionic_strength = puw.convert(ionic_strength, to_form="openmm.unit")

        pdbfixer = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        max_size = max(
            max((pos[i] for pos in pdbfixer.positions))
            - min((pos[i] for pos in pdbfixer.positions))
            for i in range(3)
        )

        box_vectors = None

        if box_shape == "truncated octahedral":
            vectors = (
                Vec3(1.0, 0, 0),
                Vec3(1.0 / 3.0, 2.0 * np.sqrt(2.0) / 3.0, 0.0),
                Vec3(-1.0 / 3.0, np.sqrt(2.0) / 3.0, np.sqrt(6.0) / 3.0),
            )

        elif box_shape == "rhombic dodecahedral":
            vectors = (
                Vec3(1.0, 0.0, 0.0),
                Vec3(0.0, 1.0, 0.0),
                Vec3(0.5, 0.5, np.sqrt(2) / 2),
            )

        elif box_shape == "cubic":
            vectors = Vec3(1.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 1.0)

        box_vectors = [(max_size + clearance) * v for v in vectors]

        pdbfixer.addSolvent(
            boxVectors=box_vectors,
            ionicStrength=ionic_strength,
            positiveIon=cation,
            negativeIon=anion,
        )

        tmp_item = convert(pdbfixer, to_form=to_form)

        del pdbfixer

        set(
            tmp_item,
            element="component",
            selection=component_indices,
            component_name=component_names,
            skip_digestion=True,
        )
        set(
            tmp_item,
            element="molecule",
            selection=molecule_indices,
            molecule_name=molecule_names,
            skip_digestion=True,
        )
        set(
            tmp_item,
            element="chain",
            selection=chain_indices,
            chain_id=chain_ids,
            chain_name=chain_names,
            skip_digestion=True,
        )

        if to_form == "molsysmt.MolSys":
            tmp_item.topology.rebuild_entities(
                redefine_indices=True,
                redefine_ids=True,
                redefine_names=True,
                redefine_types=True,
            )
        elif to_form == "molsysmt.Topology":
            tmp_item.rebuild_entities(
                redefine_indices=True,
                redefine_ids=True,
                redefine_names=True,
                redefine_types=True,
            )

        assign_selection_to_new_chain(
            tmp_item, selection='group_type in ["water","ion"]'
        )

        tmp_item = _place_in_box_origin_convention(tmp_item)

        return tmp_item

    elif engine == "MolSysMT":
        import math
        from importlib.resources import files

        from molsysmt.basic import convert, get, merge, remove
        from molsysmt.build import add_missing_bonds, remove_overlapping_molecules
        from molsysmt.build._private import assign_selection_to_new_chain
        from molsysmt.structure import translate

        # ── water-model → template mapping ─────────────────────────────────
        # Keys are normalised (uppercase, stripped of -/_ ) for robust matching.
        # Canonical names (from molsysmt.attribute) → normalised:
        #   'SPC' → 'SPC', 'SPC/E' → 'SPCE', 'TIP3P' → 'TIP3P', 'TIP4P-EW' → 'TIP4PEW'
        _water_templates = {
            "TIP3P": {
                "file": "tip3p.pdb",
                "tile_nm": 3.0,
                "o_name": "O",
                "canonical": "TIP3P",
            },
            "SPCE": {
                "file": "spce.pdb",
                "tile_nm": 3.0,
                "o_name": "O",
                "canonical": "SPC/E",
            },
            "TIP4PEW": {
                "file": "tip4pew.pdb",
                "tile_nm": 3.0,
                "o_name": "O",
                "canonical": "TIP4P-EW",
            },
            "SPC": {
                "file": "spc216.gro",
                "tile_nm": 1.86206,
                "o_name": "OW",
                "canonical": "SPC",
            },
        }
        wkey = (
            water_model.upper()
            .replace("-", "")
            .replace("/", "")
            .replace(" ", "")
            .replace("_", "")
        )
        if wkey not in _water_templates:
            _supported = ["SPC", "SPC/E", "TIP3P", "TIP4P-EW"]
            raise NotImplementedError(
                f"water_model={water_model!r} is not supported with engine='MolSysMT'. "
                f"Supported models: {_supported}. "
                "Use engine='OpenMM' for other water models."
            )
        tmpl_info = _water_templates[wkey]
        tile_nm = tmpl_info["tile_nm"]
        o_name = tmpl_info["o_name"]

        # ── save solute metadata ─────────────────────────────────────────────
        component_indices, component_names = get(
            molecular_system,
            element="component",
            component_index=True,
            component_name=True,
        )
        molecule_indices, molecule_names = get(
            molecular_system,
            element="molecule",
            molecule_index=True,
            molecule_name=True,
        )
        chain_indices, chain_ids, chain_names = get(
            molecular_system,
            element="chain",
            chain_index=True,
            chain_id=True,
            chain_name=True,
        )

        # ── 1. Convert solute to native form ────────────────────────────────
        solute = convert(
            molecular_system, to_form="molsysmt.MolSys", skip_digestion=True
        )
        clearance_nm = puw.get_value(clearance, to_unit="nm")

        # ── 2. Compute box matrix ────────────────────────────────────────────
        coords_nm = puw.get_value(solute.structures.coordinates, to_unit="nm")[0]
        mins = coords_nm.min(axis=0)
        maxs = coords_nm.max(axis=0)
        extents = maxs - mins

        if box_shape == "cubic":
            side = float(extents.max()) + 2.0 * clearance_nm
            box_matrix = np.diag([side, side, side])
        elif box_shape == "rectangular":
            box_matrix = np.diag(extents + 2.0 * clearance_nm)
        elif box_shape == "truncated octahedral":
            # Smallest truncated octahedron enclosing the solute + clearance.
            # The circumradius of a truncated octahedron with edge length a is
            # sqrt(5)/2 * a, and L (the conventional cell edge) = a*sqrt(2).
            # We choose L so that every vertex is at least (max_extent/2 + clearance) away
            # from the center.  For the TO the inscribed-sphere radius = L*sqrt(3)/3,
            # so we need L = (max_half_extent + clearance) * 2*sqrt(3)/sqrt(3) …
            # Simpler: use the circumscribed-sphere radius: max_half = max(extents)/2;
            # L = 2*(max_half + clearance) guarantees the bounding box fits.
            # Box vectors (rows): v1=L(1,0,0), v2=L(1/3, 2√2/3, 0), v3=L(-1/3, √2/3, √6/3)
            L = float(extents.max()) + 2.0 * clearance_nm
            box_matrix = np.array(
                [
                    [L, 0.0, 0.0],
                    [L / 3.0, L * 2.0 * math.sqrt(2.0) / 3.0, 0.0],
                    [-L / 3.0, L * math.sqrt(2.0) / 3.0, L * math.sqrt(6.0) / 3.0],
                ]
            )
        elif box_shape == "rhombic dodecahedral":
            # Box vectors: v1=L(1,0,0), v2=L(0,1,0), v3=L(0.5, 0.5, √2/2)
            L = float(extents.max()) + 2.0 * clearance_nm
            box_matrix = np.array(
                [
                    [L, 0.0, 0.0],
                    [0.0, L, 0.0],
                    [L / 2.0, L / 2.0, L * math.sqrt(2.0) / 2.0],
                ]
            )
        else:
            raise NotImplementedError(
                f"box_shape={box_shape!r} is not supported with engine='MolSysMT'. "
                "Supported shapes: 'cubic', 'rectangular', 'truncated octahedral', "
                "'rhombic dodecahedral'."
            )

        # ── 3. Center solute in box ──────────────────────────────────────────
        solute_center = (mins + maxs) / 2.0
        box_center = 0.5 * box_matrix.sum(axis=0)
        shift = (box_center - solute_center).reshape(1, 1, 3)
        solute = translate(
            solute, translation=puw.quantity(shift, "nm"), in_place=False
        )

        # ── 4. Load water template ───────────────────────────────────────────
        water_path = str(files("molsysmt.data.water").joinpath(tmpl_info["file"]))
        water_tile = convert(
            water_path,
            to_form="molsysmt.MolSys",
            get_missing_bonds=False,
            skip_digestion=True,
        )
        add_missing_bonds(water_tile, engine="MolSysMT", skip_digestion=True)
        water_tile.topology.rebuild_molecules(force=True)
        water_tile.topology.rebuild_chains(
            redefine_indices=False,
            redefine_ids=False,
            redefine_names=False,
            redefine_types=True,
        )
        water_tile.topology.rebuild_entities(force=True)

        # ── 5. Tile water boxes to fill the simulation box ──────────────────
        # For non-orthogonal boxes, compute the bounding box of all 8 unit-cell
        # corners in Cartesian space to determine tile counts.
        corners = np.array(
            [[i, j, k] for i in (0.0, 1.0) for j in (0.0, 1.0) for k in (0.0, 1.0)],
            dtype=np.float64,
        )
        cart_corners = corners @ box_matrix  # (8, 3) Cartesian corner positions
        max_extents = cart_corners.max(axis=0)  # largest extent per axis
        n_x = int(math.ceil(max_extents[0] / tile_nm)) + 1
        n_y = int(math.ceil(max_extents[1] / tile_nm)) + 1
        n_z = int(math.ceil(max_extents[2] / tile_nm)) + 1

        all_water = _build_tiled_water(water_tile, n_x, n_y, n_z, tile_nm)
        del water_tile

        # ── 6. Filter water molecules outside the box ────────────────────────
        # Use fractional coordinates: s = xyz @ M⁻¹; keep if all s_i ∈ [0, 1).
        # This works for any parallelepiped (orthogonal or not).
        o_indices, o_coords = get(
            all_water,
            element="atom",
            selection=f'atom_name=="{o_name}"',
            atom_index=True,
            coordinates=True,
            skip_digestion=True,
        )
        o_xyz = puw.get_value(o_coords, to_unit="nm")[0]
        o_indices_arr = np.asarray(o_indices)

        M_inv = np.linalg.inv(box_matrix)
        s = o_xyz @ M_inv  # fractional coordinates (n_w, 3)
        outside = ~np.all((s >= 0.0) & (s < 1.0), axis=1)
        if np.any(outside):
            outside_atom_indices = o_indices_arr[outside].tolist()
            # The removal selection resolves this local via @outside_mol_indices.
            outside_mol_indices = np.unique(  # noqa: F841
                get(
                    all_water,
                    element="atom",
                    selection=outside_atom_indices,
                    molecule_index=True,
                    skip_digestion=True,
                )
            ).tolist()
            all_water = remove(
                all_water,
                selection="molecule_index in @outside_mol_indices",
                skip_digestion=True,
            )

        # ── 7. Merge solute + water and set box vectors ───────────────────────
        solvated = merge([solute, all_water], skip_digestion=True)
        del all_water, solute

        solvated.structures.box = puw.quantity(box_matrix.reshape(1, 3, 3), "nm")

        # ── 8. Remove water molecules overlapping with solute ─────────────────
        solvated = remove_overlapping_molecules(
            solvated,
            selection='molecule_type=="water"',
            selection_2='molecule_type!="water"',
            threshold="2.5 angstroms",
            pbc=False,
        )

        # Native solvation retains its historical explicit pH-7 approximation;
        # the standalone operation instead defaults to stored formal charges.
        from molsysmt.build.add_ions import add_ions

        native_charge = None
        if n_cations == "neutralize" or n_anions == "neutralize":
            from molsysmt.physchem import get_charge

            native_charge = get_charge(
                molecular_system, element="system", definition="physical_pH7"
            )
        solvated = add_ions(
            solvated,
            anion=anion,
            n_anions=n_anions,
            cation=cation,
            n_cations=n_cations,
            ionic_strength=ionic_strength,
            expected_total_charge=native_charge,
            random_seed=random_seed,
        )
        history = solvated.chemical_states._states[0]._preparation_history[-1]["report"]
        history["solvation"] = dict(
            engine="MolSysMT",
            water_model=water_model,
            charge_source="tabulated_physical_pH7_approximation"
            if native_charge is not None
            else "not_required",
        )

        # ── 9. Post-processing ─────────────────────────────────────────────────
        tmp_item = convert(solvated, to_form=to_form, skip_digestion=True)
        del solvated

        if to_form == "molsysmt.MolSys":
            tmp_item.topology.rebuild_entities(
                redefine_indices=True,
                redefine_ids=True,
                redefine_names=True,
                redefine_types=True,
            )
        elif to_form == "molsysmt.Topology":
            tmp_item.rebuild_entities(
                redefine_indices=True,
                redefine_ids=True,
                redefine_names=True,
                redefine_types=True,
            )

        from molsysmt.basic import set as msm_set

        msm_set(
            tmp_item,
            element="component",
            selection=component_indices,
            component_name=component_names,
            skip_digestion=True,
        )
        msm_set(
            tmp_item,
            element="molecule",
            selection=molecule_indices,
            molecule_name=molecule_names,
            skip_digestion=True,
        )
        msm_set(
            tmp_item,
            element="chain",
            selection=chain_indices,
            chain_id=chain_ids,
            chain_name=chain_names,
            skip_digestion=True,
        )

        assign_selection_to_new_chain(
            tmp_item, selection='group_type in ["water", "ion"]'
        )

        tmp_item = _place_in_box_origin_convention(tmp_item)

        return tmp_item

    # elif engine=="LEaP":

    #    from molsysmt.third_party.tleap import TLeap
    #    from molsysmt._private.files_and_directories import temp_directory, temp_filename
    #    from molsysmt.form.file_pdb import replace_HETATM_by_ATOM_in_terminal_cappings
    #    from shutil import rmtree, copyfile
    #    from os import getcwd, chdir
    #    from molsysmt.basic import set, get, select, remove, contains
    #    from molsysmt.build import define_new_chain

    #    component_indices, component_names = get(molecular_system, element='component', component_index=True,
    #                                             component_name=True)
    #    molecule_indices, molecule_names = get(molecular_system, element='molecule', molecule_index=True,
    #                                           molecule_name=True)
    #    chain_indices, chain_ids, chain_names = get(molecular_system, element='chain', chain_index=True,
    #                                                chain_id=True, chain_name=True)

    #    if contains(molecular_system, hydrogens=True):
    #        raise ValueError("A molecular system without hydrogen atoms is needed.")
    #        #molecular_system = remove_hydrogens(molecular_system)
    #        #if verbose:
    #        #    print("All Hydrogen atoms were removed to be added by LEaP\n\n")

    #    indices_NME_C = select(molecular_system, element='atom', selection='group_name=="NME" and atom_name=="C"')
    #    with_NME_C = (len(indices_NME_C)>0)

    #    if with_NME_C:
    #        set(molecular_system, element='atom', selection='group_name=="NME" and atom_name=="C"', atom_name='CH3')

    #    current_directory = getcwd()
    #    working_directory = temp_directory()
    #    pdbfile_in = temp_filename(dir=working_directory, extension='pdb')
    #    _ = convert(molecular_system, to_form=pdbfile_in)
    #    #replace_HETATM_from_capping_atoms(pdbfile_in)

    #    tmp_prmtop = temp_filename(dir=working_directory, extension='prmtop')
    #    tmp_inpcrd = tmp_prmtop.replace('prmtop','inpcrd')
    #    tmp_logfile = tmp_prmtop.replace('prmtop','leap.log')

    #    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
    #    parameters = molecular_mechanics.get_leap_parameters()
    #    forcefield = parameters['forcefield']
    #    water = parameters['water_model']

    #    solvent_model=None
    #    if water=='SPC':
    #        solvent_model='SPCBOX'
    #    elif water=='TIP3P':
    #        solvent_model='TIP3PBOX'
    #    elif water =='TIP4P':
    #        solvent_model='TIP4PBOX'

    #    if False:
    #        print('Working directory:', working_directory)

    #    tleap = TLeap()
    #    tleap.load_parameters(*forcefield)
    #    tleap.load_unit('MolecularSystem', pdbfile_in)
    #    tleap.check_unit('MolecularSystem')
    #    tleap.get_total_charge('MolecularSystem')
    #    tleap.solvate('MolecularSystem', solvent_model, clearance, box_geometry=box_shape)

    #    if n_anions != 0:
    #        if n_anions=='neutralize':
    #            n_anions=0
    #        tleap.add_ions('MolecularSystem', anion, num_ions=n_anions, replace_solvent=True)

    #    if n_cations != 0:
    #        if n_cations=='neutralize':
    #            n_cations=0
    #        tleap.add_ions('MolecularSystem', cation, num_ions=n_cations, replace_solvent=True)

    #    tleap.save_unit('MolecularSystem', tmp_prmtop)
    #    errors=tleap.run(working_directory=working_directory, verbose=False)

    #    del(tleap)

    #    if logfile:
    #        copyfile(tmp_logfile, current_directory+'/build_peptide.log')

    #    tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=to_form)

    #    if with_NME_C:
    #        set(tmp_item, element='atom', selection='group_name=="NME" and atom_name=="CH3"', atom_name='C')

    #    rmtree(working_directory)

    #    set(tmp_item, element='component', selection=component_indices, component_name=component_names,
    #        skip_digestion=True)
    #    set(tmp_item, element='molecule', selection=molecule_indices, molecule_name=molecule_names,
    #        skip_digestion=True)
    #    set(tmp_item, element='chain', selection=chain_indices, chain_id=chain_ids, chain_name=chain_names,
    #        skip_digestion=True)

    #    if to_form=='molsysmt.MolSys':
    #        tmp_item.topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
    #    elif to_form=='molsysmt.Topology':
    #        tmp_item.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

    #    define_new_chain(tmp_item, selection='group_type in ["water","ion"]')

    #    return tmp_item

    else:
        raise NotImplementedError
