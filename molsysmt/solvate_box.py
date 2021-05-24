# =======================
# Creando cajas solvatadas
# =======================
import numpy as np
from molsysmt import puw
from molsysmt._private_tools.exceptions import *

"""
Solvate Box
==============

Methods and wrappers to create and solvate boxes

"""

def solvate (molecular_system, box_geometry="truncated_octahedral", clearance='14.0 angstroms',
             anion='Cl-', num_anions="neutralize", cation='Na+', num_cations="neutralize",
             ionic_strength='0.0 molar', engine="LEaP",
             to_form= None, logfile=False, verbose=False):
    """solvate(item, geometry=None, water=None, engine=None)

    Methods and wrappers to create and solvate boxes

    Parameters
    ----------

    anion: 'Cl-', 'Br-', 'F-', and 'I-'
    num_anions: number of cations to add. integer or "neutralize"
    cation: "NA"  'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'
    num_cations: number of cations to add. integer or "neutralize"
    box_geometry: "cubic", "truncated_octahedral" or "rhombic_dodecahedron" (Default: "truncated_octahedral")

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

    from molsysmt._private_tools._digestion import digest_to_form, digest_engine
    from molsysmt.multitool import get_form, convert

    engine = digest_engine(engine)
    to_form = digest_to_form(to_form)
    if to_form is None:
        to_form = get_form(molecular_system)

    if engine=="OpenMM":

        from simtk.openmm import Vec3

        clearance = puw.convert(clearance, to_form='simtk.unit')
        ionic_strength = puw.convert(ionic_strength, to_form='simtk.unit')

        modeller = convert(molecular_system, to_form='openmm.Modeller')
        molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
        parameters = molecular_mechanics.get_openmm_System_parameters()
        forcefield = molecular_mechanics.to_openmm_ForceField()

        solvent_model=None
        if molecular_mechanics.water_model=='SPC':
            solvent_model='tip3p'
        elif molecular_mechanics.water_model in ['TIP3P','TIP3PFB','SPCE', 'TIP4PEW','TIP4PFB','TIP5P']:
            solvent_model=molecular_mechanics.water_model.lower()
        else:
            raise NotImplementedError()

        if box_geometry=="truncated_octahedral":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1,0,0), Vec3(1/3,2*np.sqrt(2)/3,0), Vec3(-1/3,1/3,np.sqrt(6)/3)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        elif box_geometry=="rhombic_dodecahedron":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1,0,0), Vec3(0,1,0), Vec3(0.5,0.5,np.sqrt(2)/2)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        else:

           modeller.addSolvent(forcefield, model=solvent_model, padding=clearance,
                               ionicStrength=ionic_strength, positiveIon=cation,
                               negativeIon=anion)

        tmp_item = convert(modeller, to_form=to_form)

        del(modeller)

        return tmp_item

    elif engine=="PDBFixer":

        clearance = puw.convert(clearance, to_form='simtk.unit')
        ionic_strength = puw.convert(ionic_strength, to_form='simtk.unit')

        pdbfixer = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        max_size = max(max((pos[i] for pos in pdbfixer.positions))-min((pos[i] for pos in pdbfixer.positions)) for i in range(3))

        box_size = None
        box_vectors = None

        if box_geometry=="truncated_octahedral":
            vectors = mm.Vec3(1,0,0), mm.Vec3(1/3,2*np.sqrt(2)/3,0), mm.Vec3(-1/3,1/3,np.sqrt(6)/3)
            box_vectors = [(max_size+clearance)*v for v in vectors]
        elif box_geometry=="rhombic_dodecahedron":
            vectors = mm.Vec3(1,0,0), mm.Vec3(0,1,0), mm.Vec3(0.5,0.5,sqrt(2)/2)
            box_vectors = [(max_size+clearance)*v for v in vectors]

        pdbfixer.addSolvent(padding=clearance,
                            boxVectors = box_vectors,
                            ionicStrength=ionic_strength, positiveIon=cation,
                            negativeIon=anion)

        tmp_item = convert(pdbfixer, to_form=to_form)

        del(pdbfixer)

        return tmp_item

    elif engine=="LEaP":

        from molsysmt.tools.tleap import TLeap
        from molsysmt._private_tools.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile
        from os import getcwd, chdir

        current_directory = getcwd()
        working_directory = tmp_directory()
        pdbfile_in = tmp_filename(dir=working_directory, extension='pdb')
        _ = convert(molecular_system, to_form=pdbfile_in)

        tmp_prmtop = tmp_filename(dir=working_directory, extension='prmtop')
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

        if verbose:
            print('Working directory:', working_directory)

        tleap = TLeap()
        tleap.load_parameters(*forcefield)
        tleap.load_unit('MolecularSystem', pdbfile_in)
        tleap.check_unit('MolecularSystem')
        tleap.get_total_charge('MolecularSystem')
        tleap.solvate('MolecularSystem', solvent_model, clearance, box_geometry=box_geometry)

        if num_anions != 0:
            if num_anions=='neutralize':
                num_anions=0
            tleap.add_ions('MolecularSystem', anion, num_ions=num_anions, replace_solvent=True)

        if num_cations != 0:
            if num_cations=='neutralize':
                num_cations=0
            tleap.add_ions('MolecularSystem', cation, num_ions=num_cations, replace_solvent=True)

        tleap.save_unit('MolecularSystem', tmp_prmtop)
        errors=tleap.run(working_directory=working_directory, verbose=verbose)

        del(tleap)

        if logfile:
            copyfile(tmp_logfile, current_directory+'/build_peptide.log')

        tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=to_form)

        rmtree(working_directory)

        return tmp_item

    else:

        raise NotImplementedError

def is_solvated(molecular_system):

    from molsysmt.multitool import get

    output = False

    n_waters, volume = get(molecular_system, target='system', n_waters=True, box_volume=True)
    if (n_waters>0) and (volume is not None):
        density_number = puw.get_value((n_waters/volume), to_unit='1/nm**3')
        if (density_number)>15:
            output = True

    return output

