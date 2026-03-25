from molsysmt._private.arg_digestion import arg_digest
from ..molecule import _singular_molecule_type_to_plural
import numpy as np

@arg_digest()
def get_chain_type(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_types=False, syntax='MolSysMT', skip_digestion=False):
    """Returning chain types for a molecular system.

    Notes
    -----
    Explicit types are preserved when available. If types are redefined, they
    are inferred locally from the molecule types assigned to each chain.
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_chain_type_from_topology

        if isinstance(molecular_system, Topology):
            return project_chain_type_from_topology(
                molecular_system, element=element, redefine_indices=redefine_indices, redefine_types=redefine_types
            )
        if isinstance(molecular_system, MolSys):
            return project_chain_type_from_topology(
                molecular_system.topology, element=element, redefine_indices=redefine_indices, redefine_types=redefine_types
            )

    from molsysmt import get
    from ..molecule import get_molecule_type, get_n_molecules

    redefine_molecule_indices = False
    redefine_molecule_types = False

    if redefine_indices:

        redefine_molecule_types = True
        redefine_types = True

    if redefine_types:

        molecule_types_from_chain = get_molecule_type(molecular_system, element='chain', selection=selection,
                                                      redefine_indices=redefine_molecule_indices,
                                                      redefine_types=redefine_molecule_types)

        for ii in range(len(molecule_types_from_chain)):
            if isinstance(molecule_types_from_chain[ii], str):
                molecule_types_from_chain[ii]=[molecule_types_from_chain[ii]]

        n_molecules = get_n_molecules(molecular_system, redefine_molecules=redefine_molecule_indices)

        chain_types_from_chain = []

        if len(molecule_types_from_chain)==1 and len(molecule_types_from_chain[0])==n_molecules:
            chain_types_from_chain = ['system']
        else:
            for molecule_types in molecule_types_from_chain:
                aux = []
                array_molecule_types = np.array(molecule_types)
                for aux_type in ['protein', 'peptide', 'dna', 'rna', 'polysaccharide', 'small molecule', 'lipid',
                                 'ion', 'water', 'unknown']:
                    if aux_type in molecule_types:
                        counter = np.sum(array_molecule_types == aux_type)
                        if counter == 1:
                            aux.append(aux_type)
                        elif aux_type=='water':
                            aux.append(aux_type)
                        else:
                            aux.append(_singular_molecule_type_to_plural[aux_type])
                chain_types_from_chain.append(' + '.join(aux))

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      chain_index=True)
            output = np.array(chain_types_from_chain, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      chain_index=True)
            output = np.array(chain_types_from_chain, dtype=object)[aux].tolist()
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      chain_index=True)
            output = np.array(chain_types_from_chain, dtype=object)[aux].tolist()
        elif element == 'molecule':
            aux = get(molecular_system, element='molecule', selection=selection, syntax=syntax,
                      chain_index=True)
            output = np.array(chain_types_from_chain, dtype=object)[aux].tolist()
        elif element == 'chain':
            output = chain_types_from_chain
        elif element == 'entity':
            aux = get(molecular_system, element='entity', selection=selection, syntax=syntax,
                      chain_index=True)
            output = []
            for chains_in_entity in aux:
                output.append(np.array(chain_types_from_chain,
                    dtype=object)[chains_in_entity].tolist())
        else:
            raise NotImplementedError

    else:

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_type=True)

    return output
