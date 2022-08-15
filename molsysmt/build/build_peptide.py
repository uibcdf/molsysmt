from molsysmt._private.digestion import digest

@digest()
def build_peptide (molecular_system, to_form='molsysmt.MolSys', engine='LEaP'):

    if engine=="LEaP":

        from molsysmt.basic import convert
        from os import getcwd, chdir
        from molsysmt.thirds.tleap import TLeap
        from molsysmt._private.files_and_directories import temp_directory, temp_filename
        from shutil import rmtree, copyfile

        sequence = convert(molecular_system, to_form='string:aminoacids3')
        sequence = sequence.upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])

        current_directory = getcwd()
        working_directory = temp_directory()
        temp_prmtop = temp_filename(dir=working_directory, extension='prmtop')
        temp_inpcrd = temp_prmtop.replace('prmtop','inpcrd')
        temp_logfile = temp_prmtop.replace('prmtop','leap.log')

        if False:
            print('Working directory:', working_directory)

        tleap = TLeap()

        # 'AMBER14'
        tleap.load_parameters("leaprc.protein.ff14SB")

        # implicit_solvent 'OBC1'
        tleap.set_global_parameter(PBRadii='mbondi2')

        tleap.make_sequence('peptide', sequence)
        tleap.check_unit('peptide')
        tleap.get_total_charge('peptide')

        tleap.save_unit('peptide', temp_prmtop)

        errors=tleap.run(working_directory=working_directory, verbose=False)

        del(tleap)

        temp_item = convert([temp_prmtop, temp_inpcrd], to_form=to_form)

        rmtree(working_directory)

    else:

        raise NotImplementedError

    return temp_item

