from molsysmt._private.digestion import digest

@digest()
def build_peptide(molecular_system, to_form='molsysmt.MolSys', engine='LEaP'):
    """
    Building a peptide from a sequence.

    This function constructs a capped or uncapped peptide from a sequence of amino acids.
    It generates the complete atomic topology, including bonds, angles, and coordinates
    for the resulting system. Optionally, terminal capping groups can be included in the input
    sequence.

    Parameters
    ----------
    molecular_system : str or list of str
        The peptide sequence provided using either three-letter or one-letter amino acid codes.
        The sequence can also include optional terminal caps such as 'ACE' or 'NME'.

    to_form : str, default='molsysmt.MolSys'
        Output form of the resulting molecular system. Must be one of the :ref:`supported forms <Introduction_Forms>`.

    engine : {'LEaP'}, default 'LEaP'
        Engine used to build the peptide. Currently, only the LEaP engine from AmberTools is supported.

    Returns
    -------
    molecular system
        A new molecular system representing the fully constructed peptide, including coordinates
        and all relevant topological information.

    Raises
    ------
    NotImplementedError
        Raised if the selected engine is not supported.

    ArgumentError
        Raised if the input sequence is invalid or contains unsupported codes.

    NotSupportedFormError
        Raised if the output form is not recognized or supported.

    Notes
    -----
    - The sequence must contain standard amino acid codes recognized by the selected engine.
    - Terminal caps can be specified explicitly by using residue names such as 'ACE' (N-terminus) and 'NME' (C-terminus).
    - The resulting structure is built in vacuum and can be subsequently solvated using :func:`molsysmt.build.solvate`.

    See Also
    --------
    :func:`molsysmt.build.add_missing_terminal_cappings`
        Add terminal groups to complete or neutralize peptide ends.

    :func:`molsysmt.build.solvate`
        Surround a molecular system with solvent molecules.

    :func:`molsysmt.structure.center`
        Center a molecular system in a simulation box.

    :func:`molsysmt.basic.view`
        Visualize the resulting molecular system in a Jupyter notebook.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AceGlyGlyNme')
    >>> msm.basic.get(molsys, n_groups=True)
    4

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Build peptide <Tutorial_Build_peptide>`

    .. versionadded:: 1.0.0
    """

    if engine=="LEaP":

        from molsysmt.basic import convert, set
        from os import getcwd, chdir
        from molsysmt.thirds.tleap import TLeap
        from molsysmt._private.files_and_directories import temp_directory, temp_filename
        from shutil import rmtree, copyfile

        sequence = convert(molecular_system, to_form='string:amino_acids_3')
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

        if to_form in ['molsysmt.MolSys', 'molsysmt.Topology']:
            set(temp_item, element='chain', selection='all', chain_name='A')

        rmtree(working_directory)

    else:

        raise NotImplementedError

    return temp_item

