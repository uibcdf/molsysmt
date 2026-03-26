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

    box_shape : {'truncated octahedral', 'rhombic dodecahedral', 'cubic'}, default 'truncated octahedral'
        Geometry of the periodic simulation box. A truncated octahedral box minimises
        the volume of solvent required for a given clearance distance.

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
        Backend used to add solvent and ions.  ``'MolSysMT'`` requires no
        external dependencies and supports only orthogonal boxes (``'cubic'``
        and ``'rectangular'``) without ion addition.

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
        from molsysmt.config import default_attribute
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

        # ── ion addition not yet supported ──────────────────────────────────
        if n_cations != 0 or n_anions != 0:
            raise NotImplementedError(
                "Ion addition is not yet supported with engine='MolSysMT'. "
                "Set n_cations=0 and n_anions=0, or use engine='OpenMM'."
            )

        # ── non-orthogonal boxes require OpenMM ─────────────────────────────
        if box_shape not in ('cubic', 'rectangular'):
            raise NotImplementedError(
                f"box_shape={box_shape!r} is not supported with engine='MolSysMT'. "
                "Only 'cubic' and 'rectangular' orthogonal boxes are supported. "
                "Use engine='OpenMM' for truncated octahedral or rhombic dodecahedral boxes."
            )

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

        # ── 2. Compute orthogonal box dimensions ────────────────────────────
        coords_nm = puw.get_value(solute.structures.coordinates, to_unit='nm')[0]
        mins = coords_nm.min(axis=0)
        maxs = coords_nm.max(axis=0)
        extents = maxs - mins

        if box_shape == 'cubic':
            side = float(extents.max()) + 2.0 * clearance_nm
            box_lengths = np.array([side, side, side])
        else:   # rectangular
            box_lengths = extents + 2.0 * clearance_nm

        # ── 3. Center solute in box ──────────────────────────────────────────
        solute_center = (mins + maxs) / 2.0
        box_center    = box_lengths / 2.0
        shift = (box_center - solute_center).reshape(1, 1, 3)
        solute = translate(solute, translation=puw.quantity(shift, 'nm'), in_place=False)

        # ── 4. Load water template ───────────────────────────────────────────
        water_path = str(files('molsysmt.data.water').joinpath(tmpl_info['file']))
        water_tile = convert(water_path, to_form='molsysmt.MolSys', skip_digestion=True)

        # ── 5. Tile water boxes to fill the simulation box ──────────────────
        n_x = int(math.ceil(box_lengths[0] / tile_nm)) + 1
        n_y = int(math.ceil(box_lengths[1] / tile_nm)) + 1
        n_z = int(math.ceil(box_lengths[2] / tile_nm)) + 1

        tiles = []
        for ix in range(n_x):
            for iy in range(n_y):
                for iz in range(n_z):
                    offset = np.array([[[ix * tile_nm, iy * tile_nm, iz * tile_nm]]])
                    tile = translate(water_tile,
                                     translation=puw.quantity(offset, 'nm'),
                                     in_place=False)
                    tiles.append(tile)

        all_water = merge(tiles, skip_digestion=True)
        del tiles, water_tile

        # ── 6. Filter water molecules outside the box ────────────────────────
        o_indices, o_coords = get(all_water, element='atom',
                                  selection=f'atom_name=="{o_name}"',
                                  atom_index=True, coordinates=True,
                                  skip_digestion=True)
        o_xyz = puw.get_value(o_coords, to_unit='nm')[0]
        o_indices_arr = np.asarray(o_indices)

        outside = (
            (o_xyz[:, 0] < 0.0) | (o_xyz[:, 0] >= box_lengths[0]) |
            (o_xyz[:, 1] < 0.0) | (o_xyz[:, 1] >= box_lengths[1]) |
            (o_xyz[:, 2] < 0.0) | (o_xyz[:, 2] >= box_lengths[2])
        )
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

        box_mat = np.zeros((1, 3, 3))
        box_mat[0, 0, 0] = box_lengths[0]
        box_mat[0, 1, 1] = box_lengths[1]
        box_mat[0, 2, 2] = box_lengths[2]
        solvated.structures.box = puw.quantity(box_mat, 'nm')

        # ── 8. Remove water molecules overlapping with solute ─────────────────
        solvated = remove_overlapping_molecules(
            solvated,
            selection='molecule_type=="water"',
            selection_2='molecule_type!="water"',
            threshold='2.5 angstroms',
            pbc=False,
        )

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

    #    from molsysmt.thirds.tleap import TLeap
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
