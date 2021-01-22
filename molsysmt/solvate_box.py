# =======================
# Creando cajas solvatadas
# =======================

from simtk import unit
from os import remove

"""
Solvate Box
==============

Methods and wrappers to create and solvate boxes

"""

def solvate (item, box_geometry="truncated_octahedral", clearance=14.0*unit.angstroms, water='TIP3P',
             anion='Cl-', num_anions="neutralize", cation='Na+', num_cations="neutralize",
             ionic_strength= 0.0*unit.molar, forcefield='AMBER99SB-ILDN', engine="LEaP",
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

    from .tools.forms import digest as digest_forms

    form_in, form_out = digest_forms(item)

    if engine=="OpenMM":

        from molsysmt import convert
        from molsysmt.tools.forcefields import digest as digest_forcefield
        from simtk.openmm.app import ForceField
        from simtk.openmm import Vec3
        from numpy import sqrt

        modeller = convert(item, to_form='openmm.Modeller')

        solvent_model=None
        if water=='SPC':
            solvent_model='tip3p'
        elif water=='TIP3P':
            solvent_model='tip3p'
        elif water=='TIP3PFB':
            solvent_model='tip3pfb'
        elif water=='SPCE':
            solvent_model='spce'
        elif water =='TIP4PEW':
            solvent_model='tip4pew'
        elif water =='TIP4PFB':
            solvent_model='tip4pfb'
        elif water =='TIP5P':
            solvent_model='tip5p'

        forcefield_parameters = digest_forcefield([forcefield, water], 'OpenMM')
        forcefield = ForceField(*forcefield_parameters)

        if box_geometry=="truncated_octahedral":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1,0,0), Vec3(1/3,2*sqrt(2)/3,0), Vec3(-1/3,1/3,sqrt(6)/3)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        elif box_geometry=="rhombic_dodecahedron":

            max_size = max(max((pos[i] for pos in modeller.positions))-min((pos[i] for pos in modeller.positions)) for i in range(3))
            vectors = Vec3(1,0,0), Vec3(0,1,0), Vec3(0.5,0.5,sqrt(2)/2)
            box_vectors = [(max_size+clearance)*v for v in vectors]

            modeller.addSolvent(forcefield, model=solvent_model, boxVectors = box_vectors, ionicStrength=ionic_strength,
                                positiveIon=cation, negativeIon=anion)

        else:

           modeller.addSolvent(forcefield, model=solvent_model, padding=clearance,
                               ionicStrength=ionic_strength, positiveIon=cation,
                               negativeIon=anion)

        tmp_item = convert(modeller, to_form=form_out)

        del(modeller)

        return tmp_item

    elif engine=="PDBFixer":

        from molsysmt import convert

        pdbfixer = convert(item, to_form='openmm.Modeller')
        max_size = max(max((pos[i] for pos in pdbfixer.positions))-min((pos[i] for pos in pdbfixer.positions)) for i in range(3))

        box_size = None
        box_vectors = None

        if box_geometry=="truncated_octahedral":
            vectors = mm.Vec3(1,0,0), mm.Vec3(1/3,2*sqrt(2)/3,0), mm.Vec3(-1/3,1/3,sqrt(6)/3)
            box_vectors = [(max_size+clearance)*v for v in vectors]
        elif box_geometry=="rhombic_dodecahedron":
            vectors = mm.Vec3(1,0,0), mm.Vec3(0,1,0), mm.Vec3(0.5,0.5,sqrt(2)/2)
            box_vectors = [(max_size+clearance)*v for v in vectors]

        solvent_model=None
        if water=='SPC':
            solvent_model='tip3p'
        elif water=='TIP3P':
            solvent_model='tip3p'
        elif water=='TIP3PFB':
            solvent_model='tip3pfb'
        elif water=='SPCE':
            solvent_model='spce'
        elif water =='TIP4PEW':
            solvent_model='tip4pew'
        elif water =='TIP4PFB':
            solvent_model='tip4pfb'
        elif water =='TIP5P':
            solvent_model='tip5p'

        pdbfixer.addSolvent(model=solvent_model, padding=clearance,
                            boxVectors = box_vectors,
                            ionicStrength=ionic_strength, positiveIon=cation,
                            negativeIon=anion)
        tmp_item = convert(modeller, to_form=form_out)
        del(pdbfixer)

        return tmp_item

    elif engine=="LEaP":

        from molsysmt.tools import TLeap
        from molsysmt.tools.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile
        from os import getcwd, chdir
        from molsysmt.tools.forcefields import digest as digest_forcefield
        from molsysmt import convert

        current_directory = getcwd()
        working_directory = tmp_directory()
        pdbfile_in = tmp_filename(dir=working_directory, extension='pdb')
        convert(item, to_form=pdbfile_in)

        tmp_prmtop = tmp_filename(dir=working_directory, extension='prmtop')
        tmp_inpcrd = tmp_prmtop.replace('prmtop','inpcrd')
        tmp_logfile = tmp_prmtop.replace('prmtop','leap.log')
        #pdbfile_out = tmp_filename(dir=working_directory, extension='pdb')
        #tmp_logfile = pdbfile_out.replace('pdb','leap.log')

        forcefield_parameters = digest_forcefield([forcefield, water], 'LEap')

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
        tleap.load_parameters(*forcefield_parameters)
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

        #tmp_item = convert(pdbfile_out, to_form=to_form)
        tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=form_out)

        rmtree(working_directory)

        return tmp_item

    else:

        raise NotImplementedError

def is_solvated(item):

    from molsysmt import get

    output = False

    n_waters, volume = get(item, target='system', n_waters=True, box_volume=True)
    if (n_waters>0) and (volume is not None):
        density_number = (n_waters/volume)._value
        if (density_number)>15:
            output = True

    return output

