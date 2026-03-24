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

    water_model : {'SPC', 'SPCE', 'TIP3P', 'TIP3PFB', 'TIP4PEW', 'TIP4PFB', 'TIP5P'}, default 'TIP3P'
        Water model used to parameterise solvent molecules. If the molecular system
        already stores a water model attribute, it takes precedence.

    engine : {'OpenMM', 'PDBFixer'}, default 'OpenMM'
        Backend used to add solvent and ions.

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
