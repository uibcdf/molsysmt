from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentChoiceError
from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest()
def get_charge(molecular_system, element='group', selection='all', definition='physical_pH7',
               forcefield='AMBER14', water_model=None, syntax='MolSysMT', skip_digestion=False):
    """
    Electric charge for the selected elements.

    Returns the electric charge aggregated at the requested hierarchical level.
    Two families of definitions are supported:

    * ``'physical_pH7'`` and ``'collantes'`` — residue-based tabulated scales
      that assign a fixed charge to each amino acid group.  The charge is then
      summed across all groups within the requested element.
    * ``'OpenMM'`` — reads partial charges from an ``openmm.System`` or
      ``openmm.Simulation`` object's ``NonbondedForce``.  If a different form
      is provided, the system is first converted to ``openmm.System`` using
      the specified ``forcefield``.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'group'
        Hierarchical element for which charge is returned.  When
        ``definition`` is ``'physical_pH7'`` or ``'collantes'``, ``element``
        must be ``'group'`` or coarser (``'atom'`` raises an error).  When
        ``definition`` is ``'OpenMM'`` and the form is ``openmm.System``,
        only ``'atom'`` and ``'system'`` are supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of elements to include in the output.
    definition : {'physical_pH7', 'collantes', 'OpenMM'}, default 'physical_pH7'
        Charge definition to use.

        * ``'physical_pH7'``: fixed integer charges at pH 7 for the 20
          standard amino acids (e.g. Arg +1, Asp −1).
        * ``'collantes'``: alternative tabulated scale from Collantes et al.
        * ``'OpenMM'``: partial charges extracted from an OpenMM
          ``NonbondedForce``.
    forcefield : str, default 'AMBER14'
        Force field used to build the ``openmm.System`` when
        ``definition='OpenMM'`` and the input is not already an OpenMM
        system object.
    water_model : str or None, default None
        Water model passed to the OpenMM system builder (when applicable).
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    quantity
        Electric charge as a PyUnitWizard quantity in elementary charge
        units (e).  Shape is ``(n_elements,)`` for atom/group/component/
        molecule/chain/entity elements, or a scalar for ``element='system'``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported ``definition`` is requested.
    ArgumentChoiceError
        If ``element='atom'`` is combined with a residue-based definition, or
        if a mid-hierarchy element is combined with the ``openmm.System`` form.

    Notes
    -----
    Values are rounded to 4 decimal places for the ``'OpenMM'`` definition
    to avoid floating-point noise from unit conversions.

    .. versionadded:: 1.0.0
    """
    
    from molsysmt.basic import get

    if definition in ['physical_pH7', 'collantes']:


        if definition=='physical_pH7':
            from molsysmt.physchem.groups.charge import physical_pH7 as values, units
        elif definition=='collantes':
            from molsysmt.physchem.groups.charge import collantes as values, units
        else:
            raise NotImplementedMethodError()

        output = []

        if element=='atom':
            raise ArgumentChoiceError(
                argument="element",
                value=element,
                choices=['group', 'component', 'molecule', 'chain', 'entity', 'system'],
                caller="molsysmt.physchem.get_charge",
                message='Only elements bigger than, or equal to, groups are allowed when definition is "physical_pH7" or "collantes"'
            )

        elif element=='group':

            group_names = get(molecular_system, element=element, selection=selection, group_name=True)
            for ii in group_names:
                output.append(group_table_value(values, ii))
            output = puw.quantity(np.array(output), units)

        elif element in ['component', 'molecule', 'chain', 'entity']:

            group_names = get(molecular_system, element=element, selection=selection, group_name=True)
            for aux in group_names:
                output.append(np.sum([group_table_value(values, ii) for ii in aux]))
            output = puw.quantity(np.array(output), units)

        elif element=='system':

            group_names = get(molecular_system, element='group', selection='all', group_names=True)
            output = puw.quantity(np.sum([group_table_value(values, ii) for ii in group_names]), units)

    elif definition == 'OpenMM':

        from molsysmt.basic import convert, get_form
        from openmm import NonbondedForce

        form_in = get_form(molecular_system)

        if form_in == 'openmm.System':

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.getNumForces()):
                    force = molecular_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                raise ArgumentChoiceError(
                    argument="element",
                    value=element,
                    choices=["atom", "system"],
                    caller="molsysmt.physchem.get_charge",
                    message='openmm.System only allows element in ["atom", "system"]'
                )

            elif element=='system':

                var_aux = 0.0
                for force_index in range(molecular_system.getNumForces()):
                    force = molecular_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in range(molecular_system.getNumParticles()):
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        elif form_in == 'openmm.Simulation':

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for atom_list in atom_indices:
                            var_aux = 0.0
                            for index in atom_list:
                                var_aux+=force.getParticleParameters(int(index))[0]._value
                            output.append(var_aux)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element=='system':

                atom_indices = get(molecular_system, element='atom', selection='all', index=True)

                var_aux = 0.0
                for force_index in range(molecular_system.system.getNumForces()):
                    force = molecular_system.system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

        else:

            openmm_system = convert(molecular_system, to_form='openmm.System', forcefield=forcefield)

            if element=='atom':

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in atom_indices:
                            output.append(force.getParticleParameters(int(index))[0]._value)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

                atom_indices = get(molecular_system, element=element, selection=selection, atom_index=True)

                output = []

                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for atom_list in atom_indices:
                            var_aux = 0.0
                            for index in atom_list:
                                var_aux+=force.getParticleParameters(int(index))[0]._value
                            output.append(var_aux)

                output = np.array(output, dtype=float).round(4)*puw.unit('e')

            elif element=='system':

                var_aux = 0.0
                for force_index in range(openmm_system.getNumForces()):
                    force = openmm_system.getForce(force_index)
                    if isinstance(force, NonbondedForce):
                        for index in range(openmm_system.getNumParticles()):
                            var_aux+=force.getParticleParameters(int(index))[0]._value

                output = np.round(var_aux,4)*puw.unit('e')

    else:

        raise NotImplementedMethodError

    output = puw.standardize(output)

    return output

