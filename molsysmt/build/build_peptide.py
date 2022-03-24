def build_peptide (molecular_system, box_geometry='cubic', clearance='10.0 Å',
                   to_form='molsysmt.MolSys', engine='LEaP', logfile=False, verbose=False,
                   check=True):

    # box_geometry: "cubic" or "truncated octahedral"

    from molsysmt._private.engine import digest_engine

    engine = digest_engine(engine)

    if engine=="LEaP":

        from molsysmt.basic import convert
        from os import getcwd, chdir
        from molsysmt.tools.tleap import TLeap
        from molsysmt._private.files_and_directories import temp_directory, temp_filename
        from shutil import rmtree, copyfile

        sequence = convert(molecular_system, to_form='string:aminoacids3')
        sequence = sequence.upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])
        molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')
        mm_parameters = molecular_mechanics.get_leap_parameters()
        forcefield = mm_parameters['forcefield']
        water_model = mm_parameters['water_model']
        implicit_solvent = mm_parameters['implicit_solvent']

        if water_model is not None:
            if water_model =='SPC':
                solvent_model='SPCBOX'
            elif water_model == 'TIP3P':
                solvent_model='TIP3PBOX'
            else:
                raise NotImplementedError

        current_directory = getcwd()
        working_directory = temp_directory()
        temp_prmtop = temp_filename(dir=working_directory, extension='prmtop')
        temp_inpcrd = temp_prmtop.replace('prmtop','inpcrd')
        temp_logfile = temp_prmtop.replace('prmtop','leap.log')

        if verbose:
            print('Working directory:', working_directory)

        tleap = TLeap()

        tleap.load_parameters(*forcefield)

        if implicit_solvent == 'OBC1':
            tleap.set_global_parameter(PBRadii='mbondi2')

        tleap.make_sequence('peptide', sequence)
        tleap.check_unit('peptide')
        tleap.get_total_charge('peptide')

        if water_model is not None:
            tleap.solvate('peptide', solvent_model, clearance, box_geometry)

        tleap.save_unit('peptide', temp_prmtop)

        errors=tleap.run(working_directory=working_directory, verbose=verbose)


        del(tleap)

        if logfile:
            copyfile(temp_logfile, current_directory+'/build_peptide.log')

        temp_item = convert([temp_prmtop, temp_inpcrd], to_form=to_form)

        rmtree(working_directory)

    else:

        raise NotImplementedError

    return temp_item

