from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
import numpy as np

@arg_digest()
def get_mass(molecular_system, element ='system', selection = 'all', syntax = 'MolSysMT', definition='physical',
             skip_digestion=False):
    """
    Total mass of the selected elements.

    Returns the mass aggregated at the requested hierarchical level.  Two
    definitions are available: a table of standard atomic masses
    (``'physical'``) and mass values read directly from an OpenMM object
    (``'OpenMM'``).

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'system'
        Hierarchical element for which mass is returned.  For elements coarser
        than ``'atom'``, the masses of all constituent atoms are summed.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of elements to include in the output.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    definition : {'physical', 'OpenMM'}, default 'physical'
        Mass definition to use.

        * ``'physical'``: standard atomic masses from the periodic table
          (IUPAC values), summed per element.
        * ``'OpenMM'``: masses extracted from an ``openmm.Topology``,
          ``openmm.Modeller``, ``pdbfixer.PDBFixer``, or ``openmm.System``
          object.  Element-level aggregation above ``'atom'`` is supported
          for topology-based forms only.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    quantity
        Mass as a PyUnitWizard quantity in dalton (amu).  Shape is
        ``(n_elements,)`` for atom/group/component/molecule/chain/entity
        elements, or a scalar for ``element='system'``.

    Raises
    ------
    NotImplementedError
        If the requested combination of ``element`` and form is not supported
        under the ``'OpenMM'`` definition.

    Notes
    -----
    Standard atomic masses (``'physical'``) follow IUPAC 2021 values.
    Results are converted to pint units and standardized through PyUnitWizard
    before being returned.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, get_form
    from molsysmt.physchem.atoms.mass import physical, units

    output = []

    if definition=='physical':

        if element == 'atom':
            atom_types = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_type=True)
            for ii in atom_types:
                output.append(physical[ii.capitalize()])
        elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
            atom_types_in_element = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, atom_type=True)
            for aux in atom_types_in_element:
                output.append(np.sum([physical[ii.capitalize()] for ii in aux]))
        elif element == 'system':
            atom_types_in_element = get(molecular_system, element='atom', selection='all',
                                        syntax=syntax, atom_type=True)
            output.append(np.sum([physical[ii.capitalize()] for ii in atom_types_in_element]))

        if element =='system':
            output = output[0]*puw.unit(units)
        else:
            output = puw.quantity(np.array(output), units)
    
    elif definition=='OpenMM':

        from openmm import unit as _unit

        form_in = get_form(molecular_system)

        if form_in in ["openmm.Modeller", "openmm.Topology", "pdbfixer.PDBFixer"]:

            if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
                openmm_topology = molecular_system.Topology
            else:
                openmm_topology = molecular_system

            openmm_atoms = list(openmm_topology.atoms())

            if element == 'atom':
                atom_indices = get(openmm_topology, element=element, selection=selection, syntax=syntax, atom_indices=True)
                for ii in atom_indices:
                    output.append(openmm_atoms[ii].element.mass)
                output = puw.utils.sequences.concatenate(output)
            elif element in ['group', 'component', 'molecule', 'chain', 'entity']:
                atom_indices_in_element = get(openmm_topology, element=element, selection=selection,
                                            syntax=syntax, atom_indices=True)
                for aux in atom_indices_in_element:
                    output.append(np.sum([openmm_atoms[ii].element.mass for ii in aux]))
                output = puw.utils.sequences.concatenate(output)
            elif element == 'system':
                if is_all(selection):
                    aux = 0.0*_unit.amu
                    for ii in openmm_atoms:
                        aux += ii.element.mass
                    output=aux
                else:
                    raise NotImplementedError

        elif form_in == "openmm.System":

            if element == 'atom':
                atom_indices = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_indices=True)
                for ii in atom_indices:
                    output.append(molecular_system.getParticleMass(ii))
                output = puw.utils.sequences.concatenate(output)
            elif element == 'system':
                if is_all(selection):
                    aux = 0.0 * _unit.amu
                    for ii in range(molecular_system.getNumParticles()):
                        aux += molecular_system.getParticleMass(ii)
                    output=aux
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

    if puw.get_form(output) != 'pint':
        output = puw.convert(output, to_form='pint')
    output = puw.standardize(output)

    return output

