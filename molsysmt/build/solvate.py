# =======================
# Creando cajas solvatadas
# =======================

from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
import numpy as np
from molsysmt import pyunitwizard as puw

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
    from molsysmt.native import MolSys, Topology, Structures
    from molsysmt.native.topology import Bonds_DataFrame

    topo = water_tile.topology
    n_atoms_tile  = topo.n_atoms
    n_groups_tile = topo.n_groups
    n_bonds_tile  = len(topo.bonds)

    # ── build offset grid ───────────────────────────────────────────────────
    ix = np.arange(n_x, dtype=np.float64)
    iy = np.arange(n_y, dtype=np.float64)
    iz = np.arange(n_z, dtype=np.float64)
    IZ, IY, IX = np.meshgrid(iz, iy, ix, indexing='ij')   # each (n_z, n_y, n_x)
    offsets = np.stack(
        [IX.ravel() * tile_nm, IY.ravel() * tile_nm, IZ.ravel() * tile_nm], axis=1
    )  # (n_tiles, 3)
    n_tiles = offsets.shape[0]

    # ── tile coordinates ─────────────────────────────────────────────────────
    # template_xyz: (n_atoms_tile, 3)  →  broadcast to (n_tiles, n_atoms_tile, 3)
    template_xyz = puw.get_value(
        water_tile.structures.coordinates, to_unit='nm'
    )[0]  # (n_atoms_tile, 3)
    tiled_xyz = template_xyz[np.newaxis] + offsets[:, np.newaxis]  # (n_tiles, n_atoms_tile, 3)
    all_xyz = tiled_xyz.reshape(1, n_tiles * n_atoms_tile, 3)      # (1, total_atoms, 3)

    # ── tile topology arrays ──────────────────────────────────────────────────
    n_total_atoms  = n_tiles * n_atoms_tile
    n_total_groups = n_tiles * n_groups_tile
    n_total_bonds  = n_tiles * n_bonds_tile

    # atoms
    atom_name_base  = topo.atoms['atom_name'].to_numpy(dtype=object)
    atom_type_base  = topo.atoms['atom_type'].to_numpy(dtype=object)
    grp_idx_base    = topo.atoms['group_index'].to_numpy(dtype=np.int64)

    atom_names  = np.tile(atom_name_base, n_tiles)
    atom_types  = np.tile(atom_type_base, n_tiles)
    grp_offsets = np.repeat(np.arange(n_tiles, dtype=np.int64) * n_groups_tile, n_atoms_tile)
    group_indices  = np.tile(grp_idx_base, n_tiles) + grp_offsets
    # component_index == group_index for water (one water per component)
    component_indices = group_indices.copy()
    chain_indices     = np.zeros(n_total_atoms, dtype=np.int64)
    atom_ids          = np.arange(1, n_total_atoms + 1, dtype=object).astype(str)

    # groups
    gname_base = topo.groups['group_name'].to_numpy(dtype=object)
    gtype_base = topo.groups['group_type'].to_numpy(dtype=object)
    mol_idx_base = topo.groups['molecule_index'].to_numpy(dtype=np.int64)

    group_names  = np.tile(gname_base, n_tiles)
    group_types  = np.tile(gtype_base, n_tiles)
    mol_offsets  = np.repeat(np.arange(n_tiles, dtype=np.int64) * n_groups_tile, n_groups_tile)
    mol_indices  = np.tile(mol_idx_base, n_tiles) + mol_offsets
    group_ids    = np.arange(1, n_total_groups + 1, dtype=object).astype(str)

    # bonds
    b1_base = topo.bonds['atom1_index'].to_numpy(dtype=np.int64)
    b2_base = topo.bonds['atom2_index'].to_numpy(dtype=np.int64)
    bond_offsets = np.repeat(np.arange(n_tiles, dtype=np.int64) * n_atoms_tile, n_bonds_tile)
    b1 = np.tile(b1_base, n_tiles) + bond_offsets
    b2 = np.tile(b2_base, n_tiles) + bond_offsets

    # ── assemble Topology ────────────────────────────────────────────────────
    new_topo = Topology(
        n_atoms=n_total_atoms,
        n_groups=n_total_groups,
        n_components=n_total_groups,  # one component per water
        n_molecules=n_total_groups,
        n_entities=0,
        n_chains=1,
        n_bonds=n_total_bonds,
    )

    new_topo.atoms['atom_id']        = pd.array(atom_ids, dtype='string')
    new_topo.atoms['atom_name']      = atom_names
    new_topo.atoms['atom_type']      = atom_types
    new_topo.atoms['group_index']    = pd.array(group_indices, dtype='Int64')
    new_topo.atoms['component_index']= pd.array(component_indices, dtype='Int64')
    new_topo.atoms['chain_index']    = pd.array(chain_indices, dtype='Int64')

    new_topo.groups['group_id']      = pd.array(group_ids, dtype='string')
    new_topo.groups['group_name']    = group_names
    new_topo.groups['group_type']    = group_types
    new_topo.groups['molecule_index']= pd.array(mol_indices, dtype='Int64')

    chain_row = topo.chains.iloc[0]
    new_topo.chains['chain_id']   = pd.array([chain_row['chain_id']], dtype='string')
    new_topo.chains['chain_name'] = [chain_row['chain_name']]
    new_topo.chains['chain_type'] = [chain_row.get('chain_type', None)]

    bonds_df = Bonds_DataFrame(n_total_bonds)
    bonds_df['atom1_index'] = pd.array(b1, dtype='Int64')
    bonds_df['atom2_index'] = pd.array(b2, dtype='Int64')
    new_topo._bonds = bonds_df

    # ── assemble Structures ──────────────────────────────────────────────────
    new_struc = Structures(
        coordinates=puw.quantity(all_xyz, 'nm'),
        structure_id=np.array(['1'], dtype=object),
    )

    result = MolSys()
    result.topology  = new_topo
    result.structures = new_struc
    return result


def _build_ions(ion_name, atom_name, atom_type, positions):
    """Build a MolSys with single-atom ion groups at the given positions.

    Parameters
    ----------
    ion_name : str
        Group/residue name (PDB convention, e.g. 'NA', 'CL').
    atom_name : str
        Atom name (same as group name for monatomic ions).
    atom_type : str
        Element symbol (e.g. 'Na', 'Cl').
    positions : np.ndarray, shape (n_ions, 3)
        Coordinates in nm for each ion.

    Returns
    -------
    molsysmt.MolSys
    """
    import pandas as pd
    from molsysmt.native import MolSys, Topology, Structures

    n_ions = positions.shape[0]

    new_topo = Topology(
        n_atoms=n_ions, n_groups=n_ions, n_components=n_ions,
        n_molecules=n_ions, n_entities=0, n_chains=1, n_bonds=0,
    )
    new_topo.atoms['atom_id']         = pd.array([str(i + 1) for i in range(n_ions)], dtype='string')
    new_topo.atoms['atom_name']       = np.full(n_ions, atom_name, dtype=object)
    new_topo.atoms['atom_type']       = np.full(n_ions, atom_type, dtype=object)
    new_topo.atoms['group_index']     = pd.array(np.arange(n_ions, dtype=np.int64), dtype='Int64')
    new_topo.atoms['component_index'] = pd.array(np.arange(n_ions, dtype=np.int64), dtype='Int64')
    new_topo.atoms['chain_index']     = pd.array(np.zeros(n_ions, dtype=np.int64), dtype='Int64')

    new_topo.groups['group_id']       = pd.array([str(i + 1) for i in range(n_ions)], dtype='string')
    new_topo.groups['group_name']     = np.full(n_ions, ion_name, dtype=object)
    new_topo.groups['group_type']     = np.full(n_ions, 'ion', dtype=object)
    new_topo.groups['molecule_index'] = pd.array(np.arange(n_ions, dtype=np.int64), dtype='Int64')

    new_topo.chains['chain_id']   = pd.array(['ION'], dtype='string')
    new_topo.chains['chain_name'] = [None]
    new_topo.chains['chain_type'] = [None]

    xyz = positions.reshape(1, n_ions, 3)
    new_struc = Structures(
        coordinates=puw.quantity(xyz, 'nm'),
        structure_id=np.array(['1'], dtype=object),
    )

    result = MolSys()
    result.topology  = new_topo
    result.structures = new_struc
    return result


@arg_digest()
def solvate (molecular_system, box_shape="truncated octahedral", clearance='14.0 angstroms',
             anion='Cl-', n_anions="neutralize", cation='Na+', n_cations="neutralize",
             ionic_strength='0.0 molar', water_model='TIP3P', engine="OpenMM",
             to_form= None, verbose=False):
    """
    Solvate a molecular system by surrounding it with explicit water molecules and ions.

    This function places the molecular system inside a solvent box of the chosen
    geometry, fills it with explicit water molecules of the selected model, and
    optionally adds counterions to neutralise the system charge and/or reach a
    target ionic strength.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Should not already contain explicit solvent.

    box_shape : {'truncated octahedral', 'rhombic dodecahedral', 'cubic', 'rectangular'}, default 'truncated octahedral'
        Geometry of the periodic simulation box. A truncated octahedral box minimises
        the volume of solvent required for a given clearance distance.
        All four shapes are supported by all engines.

    clearance : str or quantity, default '14.0 angstroms'
        Minimum distance between any atom of the solute and the nearest box face.
        Accepts a unit string parseable by pyunitwizard (e.g. ``'14.0 angstroms'``).

    anion : {'Cl-', 'Br-', 'F-', 'I-'}, default 'Cl-'
        Species used as the negative counterion.

    n_anions : int or 'neutralize', default 'neutralize'
        Number of anions to add. Use ``'neutralize'`` to add just enough to
        neutralise the system charge.

    cation : {'Cs+', 'K+', 'Li+', 'Na+', 'Rb+'}, default 'Na+'
        Species used as the positive counterion.

    n_cations : int or 'neutralize', default 'neutralize'
        Number of cations to add. Use ``'neutralize'`` to add just enough to
        neutralise the system charge.

    ionic_strength : str or quantity, default '0.0 molar'
        Target ionic strength of the solvent. Accepts a unit string parseable by
        pyunitwizard (e.g. ``'0.15 molar'``).

    water_model : {'SPC', 'SPC/E', 'TIP3P', 'TIP3P-FB', 'TIP3P-PME-B', 'TIP3P-PME-F', 'TIP4P', 'TIP4P-EW', 'TIP4P-FB', 'TIP4P-2005', 'TIP5P', 'TIP5P-EW'}, default 'TIP3P'
        Water model used to fill the solvent box.  Canonical names follow
        ``molsysmt.molecular_mechanics.forcefields.water_models``.  If the
        molecular system already stores a water model attribute, it takes
        precedence over this argument.

        Support by engine:

        * **OpenMM** — all models listed above (delegates to
          ``openmm.app.Modeller.addSolvent``).
        * **PDBFixer** — same as OpenMM (delegates to the same OpenMM routine).
        * **MolSysMT** — ``'SPC'``, ``'SPC/E'``, ``'TIP3P'``, ``'TIP4P-EW'``
          (bundled preequilibrated boxes in ``molsysmt/data/water/``).

    engine : {'OpenMM', 'PDBFixer', 'MolSysMT'}, default 'OpenMM'
        Backend used to add solvent and ions.

        * **MolSysMT** — no external dependencies.  Supports all four box
          shapes.  Water models limited to ``'SPC'``, ``'SPC/E'``,
          ``'TIP3P'``, ``'TIP4P-EW'``.  Ions placed via rejection-sampling
          (≥ 5 Å from solute, ≥ 0.5 Å between ions).
        * **OpenMM** — delegates to ``openmm.app.Modeller.addSolvent``.
          Supports all water models and box shapes.
        * **PDBFixer** — same as OpenMM (delegates to the same routine).

    to_form : str or None, default None
        Target form for the output molecular system. If None, the form of the
        input ``molecular_system`` is used.

    verbose : bool, default False
        If True, progress information may be printed by the engine.

    Returns
    -------
    molecular system
        A new solvated molecular system in the form specified by ``to_form`` (or
        in the same form as the input). Component, molecule, and chain metadata
        from the original system are preserved and entity labels are rebuilt.

    Raises
    ------
    NotImplementedError
        Raised if the requested ``engine`` or ``water_model`` is not supported.

    Notes
    -----
    After solvation, water molecules and ions are automatically assigned to a new
    chain by ``assign_selection_to_new_chain``. Atom and residue IDs in the output
    topology are renumbered sequentially to work around a known OpenMM bug.

    The forcefield used for solvation is read from the molecular system when
    available; otherwise the MolSysMT default forcefield is used.

    .. versionadded:: 1.0.0
    """

    logfile=False

    from molsysmt.basic import get_form, convert

    if to_form is None:
        to_form = get_form(molecular_system)

    if engine=="OpenMM":

        from openmm import Vec3
        from molsysmt.basic import get, set
        from molsysmt.build._private import assign_selection_to_new_chain
        from openmm.app import ForceField
        from molsysmt.configure import default_attribute
        from molsysmt.molecular_mechanics import get_engine_forcefield

        component_indices, component_names = get(molecular_system, element='component', component_index=True,
                                                 component_name=True)
        molecule_indices, molecule_names = get(molecular_system, element='molecule', molecule_index=True,
                                               molecule_name=True)
        chain_indices, chain_ids, chain_names = get(molecular_system, element='chain', chain_index=True,
                                                    chain_id=True, chain_name=True)

        clearance = puw.convert(clearance, to_form='openmm.unit')
        ionic_strength = puw.convert(ionic_strength, to_form='openmm.unit')

        modeller = convert(molecular_system, to_form='openmm.Modeller')

        aux_water_model, aux_forcefield = get(molecular_system, water_model=True, forcefield=True)

        if aux_water_model is not None:
            water_model = aux_water_model

        if aux_forcefield is None:
            forcefield = default_attribute['forcefield']
        else:
            forcefield = aux_forcefield

        forcefield = get_engine_forcefield(forcefield, water_model=water_model, engine='OpenMM')

        solvent_model=None

        if water_model=='SPC':
            solvent_model='tip3p'
        elif water_model in ['TIP3P','TIP3PFB','SPCE','TIP4PEW','TIP4PFB','TIP5P']:
            solvent_model=water_model.lower()
        else:
            raise NotImplementedError()

        openmm_forcefield = ForceField(*forcefield)

        if box_shape=="truncated octahedral":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1.0, 0, 0), Vec3(1.0/3.0, 2.0*np.sqrt(2.0)/3.0,0.0), Vec3(-1.0/3.0, np.sqrt(2.0)/3.0, np.sqrt(6.0)/3.0)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(openmm_forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        elif box_shape=="rhombic dodecahedral":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(0.5, 0.5, np.sqrt(2)/2)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(openmm_forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        else:

           modeller.addSolvent(openmm_forcefield, model=solvent_model, padding=clearance,
                               ionicStrength=ionic_strength, positiveIon=cation,
                               negativeIon=anion)

        # fixing a bug of OpenMM
        list_atoms = list(modeller.topology.atoms())
        atom_id = int(list_atoms[0].id)
        for atom in list_atoms[1:]:
            atom_id += 1
            atom.id = str(atom_id)
        list_residues = list(modeller.topology.residues())
        residue_id = int(list_residues[0].id)
        for residue in list_residues[1:]:
            residue_id += 1
            residue.id = str(residue_id)
        #

        tmp_item = convert(modeller, to_form=to_form)

        del(modeller)

        set(tmp_item, element='component', selection=component_indices, component_name=component_names,
            skip_digestion=True)
        set(tmp_item, element='molecule', selection=molecule_indices, molecule_name=molecule_names,
            skip_digestion=True)
        set(tmp_item, element='chain', selection=chain_indices, chain_id=chain_ids, chain_name=chain_names,
            skip_digestion=True)

        if to_form=='molsysmt.MolSys':
            tmp_item.topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
        elif to_form=='molsysmt.Topology':
            tmp_item.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

        assign_selection_to_new_chain(tmp_item, selection='group_type in ["water","ion"]')

        return tmp_item

    elif engine=="PDBFixer":

        from openmm import Vec3
        from molsysmt.basic import get, set
        from molsysmt.build._private import assign_selection_to_new_chain

        component_indices, component_names = get(molecular_system, element='component', component_index=True,
                                                 component_name=True)
        molecule_indices, molecule_names = get(molecular_system, element='molecule', molecule_index=True,
                                               molecule_name=True)
        chain_indices, chain_ids, chain_names = get(molecular_system, element='chain', chain_index=True,
                                                    chain_id=True, chain_name=True)

        clearance = puw.convert(clearance, to_form='openmm.unit')
        ionic_strength = puw.convert(ionic_strength, to_form='openmm.unit')

        pdbfixer = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        max_size = max(max((pos[i] for pos in pdbfixer.positions))-min((pos[i] for pos in pdbfixer.positions)) for i in range(3))

        box_size = None
        box_vectors = None

        if box_shape=="truncated octahedral":

            vectors = Vec3(1.0, 0, 0), Vec3(1.0/3.0, 2.0*np.sqrt(2.0)/3.0,0.0), Vec3(-1.0/3.0,
                    np.sqrt(2.0)/3.0, np.sqrt(6.0)/3.0)

        elif box_shape=="rhombic dodecahedral":

            vectors = Vec3(1.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(0.5, 0.5, np.sqrt(2)/2)

        elif box_shape=="cubic":

            vectors = Vec3(1.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 1.0)

        box_vectors = [(max_size+clearance)*v for v in vectors]

        pdbfixer.addSolvent(boxVectors = box_vectors,
                            ionicStrength=ionic_strength, positiveIon=cation,
                            negativeIon=anion)

        tmp_item = convert(pdbfixer, to_form=to_form)

        del(pdbfixer)

        set(tmp_item, element='component', selection=component_indices, component_name=component_names,
            skip_digestion=True)
        set(tmp_item, element='molecule', selection=molecule_indices, molecule_name=molecule_names,
            skip_digestion=True)
        set(tmp_item, element='chain', selection=chain_indices, chain_id=chain_ids, chain_name=chain_names,
            skip_digestion=True)

        if to_form=='molsysmt.MolSys':
            tmp_item.topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
        elif to_form=='molsysmt.Topology':
            tmp_item.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

        assign_selection_to_new_chain(tmp_item, selection='group_type in ["water","ion"]')

        return tmp_item

    elif engine == 'MolSysMT':

        import math
        from molsysmt.basic import convert, get, merge, remove
        from molsysmt.structure import translate
        from molsysmt.build import remove_overlapping_molecules
        from molsysmt.build._private import assign_selection_to_new_chain
        from importlib.resources import files

        # ── water-model → template mapping ─────────────────────────────────
        # Keys are normalised (uppercase, stripped of -/_ ) for robust matching.
        # Canonical names (from molsysmt.attribute) → normalised:
        #   'SPC' → 'SPC', 'SPC/E' → 'SPCE', 'TIP3P' → 'TIP3P', 'TIP4P-EW' → 'TIP4PEW'
        _water_templates = {
            'TIP3P':   {'file': 'tip3p.pdb',   'tile_nm': 3.0,      'o_name': 'O',  'canonical': 'TIP3P'},
            'SPCE':    {'file': 'spce.pdb',    'tile_nm': 3.0,      'o_name': 'O',  'canonical': 'SPC/E'},
            'TIP4PEW': {'file': 'tip4pew.pdb', 'tile_nm': 3.0,      'o_name': 'O',  'canonical': 'TIP4P-EW'},
            'SPC':     {'file': 'spc216.gro',  'tile_nm': 1.86206,  'o_name': 'OW', 'canonical': 'SPC'},
        }
        wkey = water_model.upper().replace('-', '').replace('/', '').replace(' ', '').replace('_', '')
        if wkey not in _water_templates:
            _supported = ['SPC', 'SPC/E', 'TIP3P', 'TIP4P-EW']
            raise NotImplementedError(
                f"water_model={water_model!r} is not supported with engine='MolSysMT'. "
                f"Supported models: {_supported}. "
                "Use engine='OpenMM' for other water models."
            )
        tmpl_info = _water_templates[wkey]
        tile_nm   = tmpl_info['tile_nm']
        o_name    = tmpl_info['o_name']

        # ── ion lookup table (PDB residue name, atom name, element symbol) ─
        _ion_info = {
            'Na+': ('NA', 'NA', 'Na'),
            'K+':  ('K',  'K',  'K'),
            'Li+': ('LI', 'LI', 'Li'),
            'Rb+': ('RB', 'RB', 'Rb'),
            'Cs+': ('CS', 'CS', 'Cs'),
            'Cl-': ('CL', 'CL', 'Cl'),
            'Br-': ('BR', 'BR', 'Br'),
            'F-':  ('F',  'F',  'F'),
            'I-':  ('I',  'I',  'I'),
        }
        if cation not in _ion_info:
            raise NotImplementedError(f"cation={cation!r} is not supported with engine='MolSysMT'.")
        if anion not in _ion_info:
            raise NotImplementedError(f"anion={anion!r} is not supported with engine='MolSysMT'.")

        # ── save solute metadata ─────────────────────────────────────────────
        component_indices, component_names = get(molecular_system, element='component',
            component_index=True, component_name=True)
        molecule_indices, molecule_names = get(molecular_system, element='molecule',
            molecule_index=True, molecule_name=True)
        chain_indices, chain_ids, chain_names = get(molecular_system, element='chain',
            chain_index=True, chain_id=True, chain_name=True)

        # ── 1. Convert solute to native form ────────────────────────────────
        solute = convert(molecular_system, to_form='molsysmt.MolSys', skip_digestion=True)
        clearance_nm = puw.get_value(clearance, to_unit='nm')

        # ── 2. Compute box matrix ────────────────────────────────────────────
        coords_nm = puw.get_value(solute.structures.coordinates, to_unit='nm')[0]
        mins = coords_nm.min(axis=0)
        maxs = coords_nm.max(axis=0)
        extents = maxs - mins

        if box_shape == 'cubic':
            side = float(extents.max()) + 2.0 * clearance_nm
            box_matrix = np.diag([side, side, side])
        elif box_shape == 'rectangular':
            box_matrix = np.diag(extents + 2.0 * clearance_nm)
        elif box_shape == 'truncated octahedral':
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
            box_matrix = np.array([
                [L,           0.0,                     0.0],
                [L / 3.0,     L * 2.0 * math.sqrt(2.0) / 3.0, 0.0],
                [-L / 3.0,    L * math.sqrt(2.0) / 3.0,        L * math.sqrt(6.0) / 3.0],
            ])
        elif box_shape == 'rhombic dodecahedral':
            # Box vectors: v1=L(1,0,0), v2=L(0,1,0), v3=L(0.5, 0.5, √2/2)
            L = float(extents.max()) + 2.0 * clearance_nm
            box_matrix = np.array([
                [L,       0.0,     0.0],
                [0.0,     L,       0.0],
                [L / 2.0, L / 2.0, L * math.sqrt(2.0) / 2.0],
            ])
        else:
            raise NotImplementedError(
                f"box_shape={box_shape!r} is not supported with engine='MolSysMT'. "
                "Supported shapes: 'cubic', 'rectangular', 'truncated octahedral', "
                "'rhombic dodecahedral'."
            )

        # ── 3. Center solute in box ──────────────────────────────────────────
        solute_center = (mins + maxs) / 2.0
        box_center    = 0.5 * box_matrix.sum(axis=0)
        shift = (box_center - solute_center).reshape(1, 1, 3)
        solute = translate(solute, translation=puw.quantity(shift, 'nm'), in_place=False)

        # ── 4. Load water template ───────────────────────────────────────────
        water_path = str(files('molsysmt.data.water').joinpath(tmpl_info['file']))
        water_tile = convert(water_path, to_form='molsysmt.MolSys', skip_digestion=True)

        # ── 5. Tile water boxes to fill the simulation box ──────────────────
        # For non-orthogonal boxes, compute the bounding box of all 8 unit-cell
        # corners in Cartesian space to determine tile counts.
        corners = np.array(
            [[i, j, k] for i in (0.0, 1.0) for j in (0.0, 1.0) for k in (0.0, 1.0)],
            dtype=np.float64,
        )
        cart_corners = corners @ box_matrix          # (8, 3) Cartesian corner positions
        max_extents  = cart_corners.max(axis=0)      # largest extent per axis
        n_x = int(math.ceil(max_extents[0] / tile_nm)) + 1
        n_y = int(math.ceil(max_extents[1] / tile_nm)) + 1
        n_z = int(math.ceil(max_extents[2] / tile_nm)) + 1

        all_water = _build_tiled_water(water_tile, n_x, n_y, n_z, tile_nm)
        del water_tile

        # ── 6. Filter water molecules outside the box ────────────────────────
        # Use fractional coordinates: s = xyz @ M⁻¹; keep if all s_i ∈ [0, 1).
        # This works for any parallelepiped (orthogonal or not).
        o_indices, o_coords = get(all_water, element='atom',
                                  selection=f'atom_name=="{o_name}"',
                                  atom_index=True, coordinates=True,
                                  skip_digestion=True)
        o_xyz = puw.get_value(o_coords, to_unit='nm')[0]
        o_indices_arr = np.asarray(o_indices)

        M_inv  = np.linalg.inv(box_matrix)
        s      = o_xyz @ M_inv                        # fractional coordinates (n_w, 3)
        outside = ~np.all((s >= 0.0) & (s < 1.0), axis=1)
        if np.any(outside):
            outside_atom_indices = o_indices_arr[outside].tolist()
            outside_mol_indices = np.unique(
                get(all_water, element='atom', selection=outside_atom_indices,
                    molecule_index=True, skip_digestion=True)
            ).tolist()
            all_water = remove(all_water,
                                selection=f'molecule_index in @outside_mol_indices',
                                skip_digestion=True)

        # ── 7. Merge solute + water and set box vectors ───────────────────────
        solvated = merge([solute, all_water], skip_digestion=True)
        del all_water, solute

        solvated.structures.box = puw.quantity(box_matrix.reshape(1, 3, 3), 'nm')

        # ── 8. Remove water molecules overlapping with solute ─────────────────
        solvated = remove_overlapping_molecules(
            solvated,
            selection='molecule_type=="water"',
            selection_2='molecule_type!="water"',
            threshold='2.5 angstroms',
            pbc=False,
        )

        # ── 8.5. Add ions ──────────────────────────────────────────────────────
        # Determine ion counts.
        # Charge comes from the original solute (before solvation).
        n_cat_to_add = 0
        n_an_to_add  = 0

        if n_cations == 'neutralize' or n_anions == 'neutralize':
            from molsysmt.physchem import get_charge as _get_charge
            solute_charge = int(round(puw.get_value(
                _get_charge(molecular_system, element='system', definition='physical_pH7'),
                to_unit='elementary_charge',
            )))
        else:
            solute_charge = 0   # not needed

        if n_cations == 'neutralize':
            n_cat_to_add = max(-solute_charge, 0)
        elif n_cations != 0:
            n_cat_to_add = int(n_cations)

        if n_anions == 'neutralize':
            n_an_to_add = max(solute_charge, 0)
        elif n_anions != 0:
            n_an_to_add = int(n_anions)

        # Extra pairs for ionic strength (OpenMM formula: n_pairs ≈ n_waters × C / 55.4 M)
        ionic_strength_M = puw.get_value(ionic_strength, to_unit='molar')
        if ionic_strength_M > 0.0:
            n_waters = get(solvated, element='molecule',
                           selection='molecule_type=="water"', n_molecules=True,
                           skip_digestion=True)
            n_pairs = int(round(n_waters * ionic_strength_M / 55.4))
            n_cat_to_add += n_pairs
            n_an_to_add  += n_pairs

        n_ions_total = n_cat_to_add + n_an_to_add

        if n_ions_total > 0:

            # Positions of all water oxygens (candidates for ion placement)
            o_atom_indices, o_mol_indices, o_coords = get(
                solvated, element='atom',
                selection=f'atom_name=="{o_name}"',
                atom_index=True, molecule_index=True, coordinates=True,
                skip_digestion=True,
            )
            o_xyz      = puw.get_value(o_coords, to_unit='nm')[0]        # (n_w, 3)
            o_mol_idx  = np.asarray(o_mol_indices, dtype=np.int64)       # (n_w,)

            # Positions of all solute (non-water) atoms for distance checks
            solute_xyz = puw.get_value(
                get(solvated, element='atom',
                    selection='molecule_type!="water"',
                    coordinates=True, skip_digestion=True),
                to_unit='nm',
            )[0]                                                          # (n_sol, 3)

            min_dist_nm      = 0.5    # 5 Å — exclude waters in pockets / channels
            ion_ion_cutoff_nm = 0.05  # 0.5 Å — avoid placing two ions on top of each other

            # Shuffle candidates and run rejection loop
            rng      = np.random.default_rng()
            order    = rng.permutation(len(o_xyz))
            accepted_mol_indices = []   # water molecule indices to remove
            accepted_positions   = []   # ion positions (nm)

            for idx in order:
                if len(accepted_positions) >= n_ions_total:
                    break
                o_pos = o_xyz[idx]

                # Distance to nearest solute atom
                diff  = solute_xyz - o_pos          # (n_sol, 3)
                if np.sqrt((diff * diff).sum(axis=1)).min() < min_dist_nm:
                    continue

                # Distance to already-placed ions
                too_close = False
                for prev_pos in accepted_positions:
                    d = o_pos - prev_pos
                    if np.sqrt((d * d).sum()) < ion_ion_cutoff_nm:
                        too_close = True
                        break
                if too_close:
                    continue

                accepted_mol_indices.append(int(o_mol_idx[idx]))
                accepted_positions.append(o_pos)

            if len(accepted_positions) < n_ions_total:
                raise InternalAlgorithmError(
                    caller="molsysmt.build.solvate",
                    message=(
                        f"Could not place all {n_ions_total} ions: only "
                        f"{len(accepted_positions)} valid water positions found. "
                        "Try reducing ionic_strength or increasing clearance."
                    )
                )

            # Remove the selected water molecules
            solvated = remove(
                solvated,
                selection=f'molecule_index in @accepted_mol_indices',
                skip_digestion=True,
            )

            # Build ion MolSys objects and merge
            positions_arr = np.array(accepted_positions)   # (n_ions_total, 3)

            if n_cat_to_add > 0:
                g, a, t = _ion_info[cation]
                cat_ms = _build_ions(g, a, t, positions_arr[:n_cat_to_add])
                solvated = merge([solvated, cat_ms], skip_digestion=True)

            if n_an_to_add > 0:
                g, a, t = _ion_info[anion]
                an_ms = _build_ions(g, a, t, positions_arr[n_cat_to_add:])
                solvated = merge([solvated, an_ms], skip_digestion=True)

        # ── 9. Post-processing ─────────────────────────────────────────────────
        tmp_item = convert(solvated, to_form=to_form, skip_digestion=True)
        del solvated

        if to_form == 'molsysmt.MolSys':
            tmp_item.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                               redefine_names=True, redefine_types=True)
        elif to_form == 'molsysmt.Topology':
            tmp_item.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                      redefine_names=True, redefine_types=True)

        from molsysmt.basic import set as msm_set
        msm_set(tmp_item, element='component', selection=component_indices,
                component_name=component_names, skip_digestion=True)
        msm_set(tmp_item, element='molecule', selection=molecule_indices,
                molecule_name=molecule_names, skip_digestion=True)
        msm_set(tmp_item, element='chain', selection=chain_indices,
                chain_id=chain_ids, chain_name=chain_names, skip_digestion=True)

        assign_selection_to_new_chain(tmp_item, selection='group_type in ["water", "ion"]')

        return tmp_item

    #elif engine=="LEaP":

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
