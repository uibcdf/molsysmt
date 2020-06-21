import simtk.unit as unit

def build_peptide (item, forcefield='AMBER96', implicit_solvent=None, water_model='TIP3P', to_form='molsysmt.MolSys',
                   box_geometry='cubic', clearance=10*unit.angstroms, engine='LEaP', logfile=True, verbose=True):

    # implicit_solvent in ['GBSA OBC']
    # water_model in ['TIP3P']
    # box_geometry: "cubic" or "truncated_octahedral"

    from molsysmt.utils.forcefields import digest as digest_forcefield
    from molsysmt import convert
    from os import getcwd, chdir

    tmp_item = convert(item, to_form='aminoacids3:seq')

    if engine=="LEaP":

        from molsysmt.utils import TLeap
        from molsysmt.utils.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile

        sequence = tmp_item[12:].upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])

        if type(forcefield) not in [tuple, list]:
            forcefield = [forcefield]

        if water_model =='SPC':
            solvent_model='SPCBOX'
            forcefield.append('SPC')
        elif water_model == 'TIP3P':
            solvent_model='TIP3PBOX'
            forcefield.append('TIP3P')
        else:
            raise NotImplementedError

        current_directory = getcwd()
        working_directory = tmp_directory()
        tmp_prmtop = tmp_filename(dir=working_directory, extension='prmtop')
        tmp_inpcrd = tmp_prmtop.replace('prmtop','inpcrd')
        tmp_logfile = tmp_prmtop.replace('prmtop','leap.log')

        if verbose:
            print('Working directory:', working_directory)

        tleap = TLeap()
        forcefield = digest_forcefield(forcefield, 'LEap')
        tleap.load_parameters(*forcefield)

        if implicit_solvent == 'GBSA OBC':
            tleap.set_global_parameter(PBRadii='mbondi2')

        tleap.make_sequence('peptide', sequence)
        tleap.check_unit('peptide')
        tleap.get_total_charge('peptide')

        if implicit_solvent is None:
            tleap.solvate('peptide', solvent_model, clearance, box_geometry)

        tleap.save_unit('peptide', tmp_prmtop)

        errors=tleap.run(verbose=verbose)

        del(tleap)

        if logfile:
            copyfile(tmp_logfile, current_directory+'/build_peptide.log')

        tmp_item = convert([tmp_prmtop, tmp_inpcrd], to_form=to_form)

        rmtree(working_directory)

    return tmp_item

