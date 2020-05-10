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

        from molsysmt.utils.files_and_directories import tmp_directory, tmp_filename
        from shutil import rmtree, copyfile
        import subprocess

        current_directory = getcwd()
        working_directory = tmp_directory()
        if verbose:
            print('Working directory:', working_directory)

        tmp_prmtop = tmp_filename(dir=working_directory, extension='prmtop')
        tmp_crd = tmp_filename(dir=working_directory, extension='crd')

        forcefield = digest_forcefield(forcefield, 'LEap')
        sequence = tmp_item[12:].upper()
        sequence = ' '.join([sequence[ii:ii+3] for ii in range(0, len(sequence), 3)])

        if type(forcefield) in [list, tuple]:
            forcefield_command = "source {}\n".format(' '.join(forcefield))
        else:
            forcefield_command = "source {}\n".format(forcefield)

        if box_geometry=="cubic":
            solvate_command='solvateBox'
        elif box_geometry=="truncated_octahedral":
            solvate_command='solvateOct'

        if water_model in ['SPC', 'TIP3P']:
            solvent_model='TIP3PBOX'
        else:
            raise NotImplementedError


        implicit_solvent_command = "set default PBRadii mbondi2\n"
        explicit_solvent_command = "{} peptide {} {} iso\n".format(solvate_command, solvent_model, str(clearance.value_in_unit(unit.angstroms)))
        make_peptide_command = "peptide = sequence {{ {} }}\n".format(sequence)
        check_peptide_command = "check peptide\n"
        check_charge_command = "charge peptide\n"
        saving_command = "saveAmberParm peptide {} {}\n".format(tmp_prmtop, tmp_crd)
        quit_command = "quit\n"

        commands_list =[]
        commands_list.append(forcefield_command)
        commands_list.append(make_peptide_command)
        commands_list.append(check_peptide_command)
        commands_list.append(check_charge_command)

        if implicit_solvent == 'GBSA OBC':
            commands_list.append(implicit_solvent_command)
        else:
            commands_list.append(explicit_solvent_command)

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

        chdir(current_directory)

        tmp_item = convert([tmp_prmtop, tmp_crd], to_form=to_form)

        rmtree(working_directory)

    return tmp_item

