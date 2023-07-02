def run_NPT_equilibration (item, temperature='300 K', pressure='1.0 atm',
                       time='1.0 ns', protocol=0, forcefield=['AMBER99SB-ILDN','TIP3P'],
                       engine='OpenMM', verbose=True, form_out=None, *kwargs):
    """
    To be written soon...

    Description

    Parameters
    ----------
    item : molecular model
        Molecular model in any form to be operated by the method.
    protocol : int (default 0)
        description.
    forcefield : list or str (default ["AMBER99SB-ILDN", "TIP3P"])
        Forcefield to model the inter-atomic interactions.
    engine : str (default "OpenMM")

    Returns
    -------
    item : molecular model
        The result is a new molecular model with coordinates or positions relaxed to the nearest local minimum of
        the potential energy.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    >>> minimized_system = m3t.minimze(system)
    >>> minimized_equilibrated = m3t.equilibration_NPT(system)
    """

    #from molsysmt.basic import get_form, get, convert

    #engine = _digest_engines(engine)

    #if engine=='OpenMM':

    #    #in_form = get_form(item)

    #    #forcefield = _digest_forcefields(forcefield, engine)

    #    #in_form = get_form(item)

    #    #topology = _convert(item, 'openmm.Topology')
    #    #positions = get(item, coordinates=True)
    #    #positions = reformat(attribute='coordinates', value=positions,
    #    #                     is_format=in_form, to_format='openmm')

    #    #if protocol==0:

    #    #    new_positions, new_velocities, equil_data = _equil_NPT_OpenMM_protocol_0(topology,
    #    #                                                                             positions,
    #    #                                                                             temperature=temperature,
    #    #                                                                             pressure=pressure,
    #    #                                                                             time=time,
    #    #                                                                             forcefield=forcefield,
    #    #                                                                             verbose=verbose,
    #    #                                                                             progress_bar=progress_bar)

    #    raise NotImplementedError

    #else:

    #    raise NotImplementedError

    raise NotImplementedError

