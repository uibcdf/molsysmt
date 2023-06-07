# =======================
# Creando cajas solvatadas
# =======================

from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt import pyunitwizard as puw

"""
Solvate Box
==============
Methods and wrappers to create and solvate boxes
"""

@digest()
def solvate (molecular_system, box_shape="truncated octahedral", clearance='14.0 angstroms',
             anion='Cl-', n_anions="neutralize", cation='Na+', n_cations="neutralize",
             ionic_strength='0.0 molar', engine="OpenMM",
             water_model='TIP3P', forcefield='AMBER14',
             to_form= None, verbose=False):

    """solvate(item, geometry=None, water=None, engine=None)
    Methods and wrappers to create and solvate boxes
    Parameters
    ----------
    anion: 'Cl-', 'Br-', 'F-', and 'I-'
    n_anions: number of cations to add. integer or "neutralize"
    cation: "NA"  'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'
    n_cations: number of cations to add. integer or "neutralize"
    box_shape: "cubic", "truncated_octahedral" or "rhombic_dodecahedron" (Default: "truncated_octahedral")
    Returns
    -------
    item : bla bla
        bla bla
    Examples
    --------
    See Also
    --------
    Notes
    -----
    """

    logfile=False

    from molsysmt.basic import get_form, convert

    if to_form is None:
        to_form = get_form(molecular_system)

    if engine=="OpenMM":

        from openmm import Vec3
        from molsysmt.basic import get
        from molsysmt.molecular_mechanics import get_forcefield
        from openmm.app import ForceField

        clearance = puw.convert(clearance, to_form='openmm.unit')
        ionic_strength = puw.convert(ionic_strength, to_form='openmm.unit')

        modeller = convert(molecular_system, to_form='openmm.Modeller')

        aux_water_model = get(molecular_system, water_model=True)
        aux_forcefield = get_forcefield(molecular_system, engine='OpenMM')

        if aux_water_model is not None:
            water_model = aux_water_model

        if aux_forcefield is not None:
            forcefield = aux_forcefield
        else:
            forcefield = get_forcefield({'forcefield':forcefield, 'water_model':water_model}, engine='OpenMM')

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

        tmp_item = convert(modeller, to_form=to_form)

        del(modeller)

        return tmp_item

    elif engine=="PDBFixer":

        from openmm import Vec3

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

        return tmp_item

    elif engine=="LEaP":

        from molsysmt.thirds.tleap import TLeap
        from molsysmt._private.files_and_directories import temp_directory, temp_filename
        from molsysmt.form.file_pdb import replace_HETATM_by_ATOM_in_terminal_cappings
        from shutil import rmtree, copyfile
        from os import getcwd, chdir
        from molsysmt.basic import set as _set, select, remove, contains

        if contains(molecular_system, hydrogens=True):
            raise ValueError("A molecular system without hydrogen atoms is needed.")
            #molecular_system = remove_hydrogens(molecular_system)
            #if verbose:
            #    print("All Hydrogen atoms were removed to be added by LEaP\n\n")

        indices_NME_C = select(molecular_system, element='atom', selection='group_name=="NME" and atom_name=="C"')
        with_NME_C = (len(indices_NME_C)>0)

        if with_NME_C:
            _set(molecular_system, element='atom', selection='group_name=="NME" and atom_name=="C"', atom_name='CH3')

        current_directory = getcwd()
        working_directory = temp_directory()
        pdbfile_in = temp_filename(dir=working_directory, extension='pdb')
        _ = convert(molecular_system, to_form=pdbfile_in)
        #replace_HETATM_from_capping_atoms(pdbfile_in)

        tmp_prmtop = temp_filename(dir=working_directory, extension='prmtop')
        tmp_inpcrd = tmp_prmtop.replace('prmtop','inpcrd')
        tmp_logfile = tmp_prmtop.replace('prmtop','leap.log')

        molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
        parameters = molecular_mechanics.get_leap_parameters()
        forcefield = parameters['forcefield']
        water = parameters['water_model']

        solvent_model=None
        if water=='SPC':
            solvent_model='SPCBOX'
        elif water=='TIP3P':
            solvent_model='TIP3PBOX'
        elif water =='TIP4P':
            solvent_model='TIP4PBOX'

        if False:
            print('Working directory:', working_directory)

        tleap = TLeap()
        tleap.load_parameters(*forcefield)
        tleap.load_unit('MolecularSystem', pdbfile_in)
        tleap.check_unit('MolecularSystem')
        tleap.get_total_charge('MolecularSystem')
        tleap.solvate('MolecularSystem', solvent_model, clearance, box_geometry=box_shape)

        if n_anions != 0:
            if n_anions=='neutralize':
                n_anions=0
            tleap.add_ions('MolecularSystem', anion, num_ions=n_anions, replace_solvent=True)

        if n_cations != 0:
            if n_cations=='neutralize':
                n_cations=0
            tleap.add_ions('MolecularSystem', cation, num_ions=n_cations, replace_solvent=True)

        tleap.save_unit('MolecularSystem', tmp_prmtop)
        errors=tleap.run(working_directory=working_directory, verbose=False)

        del(tleap)

        if logfile:
            copyfile(tmp_logfile, current_directory+'/build_peptide.log')

        tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=to_form)

        if with_NME_C:
            _set(tmp_item, element='atom', selection='group_name=="NME" and atom_name=="CH3"', atom_name='C')

        rmtree(working_directory)

        return tmp_item

    else:

        raise NotImplementedError

