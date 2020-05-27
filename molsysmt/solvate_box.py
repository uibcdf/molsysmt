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
             forcefield='AMBER99SB-ILDN', engine="LEaP", to_form= None, logfile=False, verbose=False):
    """solvate(item, geometry=None, water=None, engine=None)

    Methods and wrappers to create and solvate boxes

    Parameters
    ----------

    anion: 'Cl-', 'Br-', 'F-', and 'I-'
    num_anions: number of cations to add. integer or "neutralize"
    cation: "NA"  'Cs+', 'K+', 'Li+', 'Na+', and 'Rb+'
    num_cations: number of cations to add. integer or "neutralize"
    box_geometry: "cubic" or "truncated_octahedral" (Default: "truncated_octahedral")

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

    from .utils.forms import digest as digest_forms

    form_in, _ = digest_forms(item)
    if to_form is None:
        to_form = form_in

    if engine=="LEaP":

        from molsysmt.utils import TLeap
        from molsysmt.utils.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile
        from os import getcwd, chdir
        from molsysmt.utils.forcefields import digest as digest_forcefield
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
        tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=to_form)

        rmtree(working_directory)

        return tmp_item

