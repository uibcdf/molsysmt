from molsysmt._private.digestion import digest
from ..molecule import _singular_molecule_type_to_plural
import numpy as np

@digest()
def get_chain_type(molecular_system, element='atom', selection='all',
        redefine_types=False, redefine_molecule_indices=False, redefine_molecule_types=False, syntax='MolSysMT'):

    from ..molecule import get_molecule_type, get_n_molecules
    from molsysmt.basic import get

    if redefine_molecule_indices:

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
                for aux_type in ['protein', 'peptide', 'dna', 'rna', 'oligosaccharide', 'small molecule', 'lipid',
                                 'ion', 'water']:
                    if aux_type in molecule_types:
                        counter = np.sum(array_molecule_types == aux_type)
                        if counter == 1:
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

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_type=True)

    return output

