def build_peptide (item, solvent='GBSA OBC', to_form='molsysmt.MolSys', forcefield=['AMBER96'],
                   engine='LEaP', logfile=True, verbose=True):

    # solvent in ['vacuum', 'GBSA OBC', 'explicit']

    from molsysmt.utils.forcefields import digest as digest_forcefield
    from molsysmt import convert
    from os import getcwd, chdir

    tmp_item = convert(item, to_form='aminoacids3:seq')

    if engine=="LEaP":

        from molsysmt.utils.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile
        import subprocess

        current_directory = getcwd()
        working_directory = tmp_directory()
        print(working_directory)
        tmp_prmtop = tmp_filename(dir=working_directory, extension='prmtop')
        tmp_crd = tmp_filename(dir=working_directory, extension='crd')

        forcefield = digest_forcefield(forcefield, 'LEap')
        sequence = tmp_item[12:].upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])


        forcefield_command = "source {}\n".format(' '.join(forcefield))
        GBSA_OBC_command = "set default PBRadii mbondi2\n"
        make_peptide_command = "peptide = sequence {{ {} }}\n".format(sequence)
        check_peptide_command = "check peptide\n"
        check_charge_command = "charge peptide\n"
        saving_command = "saveAmberParm peptide {} {}\n".format(tmp_prmtop, tmp_crd)
        quit_command = "quit\n"

        commands_list =[]
        commands_list.append(forcefield_command)

        if solvent == 'GBSA OBC':
            commands_list.append(GBSA_OBC_command)

        commands_list.append(make_peptide_command)
        commands_list.append(check_peptide_command)
        commands_list.append(check_charge_command)
        commands_list.append(saving_command)
        commands_list.append(quit_command)

        leap_file = open(working_directory+'/leap.in', "w")
        leap_file.writelines(commands_list)
        leap_file.close()

        chdir(working_directory)

        leap_output = subprocess.check_output(['tleap', '-f', 'leap.in']).decode()

        if verbose:
            print(leap_output)
        if logfile:
            copyfile(working_directory+'/leap.log',current_directory+'/build_peptide.log')

        #tmp_item = convert([tmp_prmtop, tmp_crd], to_form=to_form)
        tmp_item = None

        copyfile(tmp_prmtop,current_directory+'/peptide.prmtop')
        copyfile(tmp_crd,current_directory+'/peptide.crd')
        chdir(current_directory)
        rmtree(working_directory)

    return tmp_item
