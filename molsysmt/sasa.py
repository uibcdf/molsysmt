def sasa (item, selection='all', frame_indices='all', target='atom', syntaxis='MolSysMT',
          engine='MDTraj', **kwargs):

    from .utils.forms import digest as digest_forms
    from .utils.engines import digest as digest_engines
    from molsysmt import convert, select

    form_in, _ = digest_forms(item)
    engine = digest_engines(engine)
    atom_indices = select(item, selection=selection, syntaxis=syntaxis)

    if engine == 'MDTraj':

        from mdtraj import shrake_rupley
        from simtk.unit import nanometers

        tmp_item = convert(item, frame_indices=frame_indices, to_form='mdtraj.Trajectory')

        sasa_array = shrake_rupley(tmp_item, mode='atom') # tiene probe_radius y n_sphere_points

        if target=='atom':

            if selection is not 'all':

                atom_indices = select(item, selection=selection, syntaxis=syntaxis)
                sasa_array = sasa_array[:,atom_indices]

        else:

            from molsysmt import get
            from numpy import empty

            sets_atoms = get(item, target=target, selection=selection, syntaxis=syntaxis,
                             atom_index=True)

            n_sets = len(sets_atoms)
            n_frames = sasa_array.shape[0]

            new_sasa_array = empty([n_frames, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:,ii] = sasa_array[:,sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = sasa_array * nanometers**2

    else:

        raise NotImplementedError("Engine not implemented yet")

    return sasa_array

