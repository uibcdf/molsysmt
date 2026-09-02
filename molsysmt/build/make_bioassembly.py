from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_iterable_of_iterables
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest()
def make_bioassembly(molecular_system, bioassembly=None, structure_indices=0, to_form=None, skip_digestion=False):
    """
    Construct the biological assembly of a molecular system from its asymmetric unit.

    Many structures deposited in the PDB represent only the asymmetric unit, while the
    biologically relevant form (the bioassembly) is obtained by applying a set of
    rotation and translation operations to replicate the chains. This function reads
    the bioassembly transformation matrices stored in the molecular system, applies
    them, and returns the fully assembled system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    bioassembly : object, default=None
        Argument bioassembly.
    structure_indices : int, list, tuple, or numpy.ndarray, default=0
        Structure indices (0-based) to include or process.
    to_form : object, default=None
        Argument to_form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system
        The biological assembly as a merged molecular system in the form specified
        by ``to_form`` (or in the same form as the input if ``to_form`` is None).


    Raises
    ------
    NotImplementedError
        Raised when the bioassembly specifies different chain sets for different
        transformation operators (heterogeneous assemblies), which is not yet
        supported.


    Notes
    -----
    Each transformation in the bioassembly consists of a rotation matrix and a
    translation vector. The function extracts the relevant chains, applies each
    rotation and translation in sequence, and merges all transformed copies into
    a single molecular system.

    Source ``chain_id`` values are preserved for their first occurrence. Generated
    copies that would repeat an identifier receive the next unused uppercase
    identifier (``A`` through ``Z``, then ``AA``, ``AB``, and so on). Author-provided
    ``chain_name`` values are preserved and may repeat across copies.


    Examples
    --------
    >>> import molsysmt as msm
    >>> path = msm.systems['Barnase-Barstar']['1brs.bcif.gz']
    >>> molsys = msm.convert(path)
    >>> assembled_molsys = make_bioassembly(molsys, bioassembly='1')
    >>> chain_ids = msm.get(assembled_molsys, element='chain', chain_id=True)
    >>> len(chain_ids) == len(set(chain_ids))
    True


    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Make_bioassembly`.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import extract, merge, get, copy
    from molsysmt.structure import rotate, translate

    if bioassembly is None:

        aux_bioassemblies = get(molecular_system, bioassembly=True)
        bioassembly = list(aux_bioassemblies.keys())[0]
        bioassembly = aux_bioassemblies[bioassembly]

    elif isinstance(bioassembly, str):

        aux_bioassemblies = get(molecular_system, bioassembly=True)
        bioassembly = aux_bioassemblies[bioassembly]

    aux_rotations = []
    for rotation in bioassembly['rotations']:
        rotation = rotation[np.newaxis,np.newaxis,:,:]
        aux_rotations.append(rotation)

    aux_translations = []
    for translation in bioassembly['translations']:
        value, unit = puw.get_value_and_unit(translation)
        translation = puw.quantity(value[np.newaxis, np.newaxis, :], unit, standardized=True)
        aux_translations.append(translation)

    units = []

    if _all_chains_equal(bioassembly):

        chains = bioassembly['chain_indices'][0]

        if isinstance(chains, int):
            chains = [chains]

        subsystem = extract(molecular_system, structure_indices=[0], selection='chain_index in @chains',
                            syntax='MolSysMT', skip_digestion=True)

        for rotation, translation in zip(aux_rotations, aux_translations):

            unit = copy(subsystem, skip_digestion=True)
            unit = rotate(unit, rotation=rotation, skip_digestion=True)
            unit = translate(unit, translation=translation, skip_digestion=True)

            units.append(unit)

    else:

        if not is_iterable_of_iterables(bioassembly['chain_indices']):

            chains = bioassembly['chain_indices']

            if isinstance(chains, int):
                chains = [chains]

            subsystem = extract(molecular_system, structure_indices=[0], selection='chain_index in @chains',
                                syntax='MolSysMT', skip_digestion=True)

            for rotation, translation in zip(aux_rotations, aux_translations):

                unit = copy(subsystem, skip_digestion=True)
                unit = rotate(unit, rotation=rotation, skip_digestion=True)
                unit = translate(unit, translation=translation, skip_digestion=True)
            
                units.append(unit)

        else:

            raise NotImplementedError

    _make_chain_ids_unique(units)

    output = merge(units, to_form=to_form, skip_digestion=True)

    return output

def _all_chains_equal(bioassembly):
    """Check that all biological assemblies share the same chain index array."""

    output = True

    first_chains = bioassembly['chain_indices'][0]

    for chains in bioassembly['chain_indices']:
        if not np.all(chains==first_chains):
            output = False
            break

    return output


def _make_chain_ids_unique(units):
    """Preserve source chain IDs once and replace assembly-copy collisions."""

    from molsysmt.basic import get, set as set_attribute
    from molsysmt.element.chain import all_chain_names

    chain_ids_by_unit = []
    reserved_chain_ids = set()

    for unit in units:
        chain_ids = [str(chain_id) for chain_id in get(
            unit, element='chain', chain_id=True, skip_digestion=True
        )]
        chain_ids_by_unit.append(chain_ids)
        reserved_chain_ids.update(chain_ids)

    used_chain_ids = set()
    available_chain_ids = iter(
        chain_id for chain_id in all_chain_names if chain_id not in reserved_chain_ids
    )

    for unit, chain_ids in zip(units, chain_ids_by_unit):
        output_chain_ids = []

        for chain_id in chain_ids:
            if chain_id not in used_chain_ids:
                output_chain_id = chain_id
            else:
                output_chain_id = next(available_chain_ids)

            output_chain_ids.append(output_chain_id)
            used_chain_ids.add(output_chain_id)

        set_attribute(
            unit,
            element='chain',
            chain_id=output_chain_ids,
            skip_digestion=True,
        )
