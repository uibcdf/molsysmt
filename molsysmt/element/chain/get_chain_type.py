from molsysmt._private.digestion import digest
from ..molecule import _singular_molecule_type_to_plural
import numpy as np

@digest()
def get_chain_type(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_types=False, syntax='MolSysMT', skip_digestion=False):

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

#atom_indices = [ii.tolist() for ii in self.atoms.groupby('chain_index').groups.values()]
#
#if len(atom_indices)==1 and len(atom_indices[0])==self.atoms.shape[0]:
#
#    chain_types_from_chain = ['system']
#
#    del(atom_indices)
#
#else:
#
#    group_indices = []
#    for aux_atom_indices in atom_indices:
#        group_indices.append(np.unique(self.atoms.iloc[aux_atom_indices,3]))
#
#    component_indices = []
#    for aux_group_indices in group_indices:
#        component_indices.append(np.unique(self.groups.iloc[aux_group_indices,3]))
#
#    molecule_indices = []
#    for aux_component_indices in component_indices:
#        molecule_indices.append(np.unique(self.components.iloc[aux_component_indices,3]))
#
#    molecule_types = []
#    for aux_molecule_indices in molecule_indices:
#        molecule_types.append(self.molecules.iloc[aux_molecule_indices,2].tolist())
#
#    chain_types_from_chain = []
#
#    for aux_molecule_types in molecule_types:
#        aux = []
#        array_molecule_types = np.array(aux_molecule_types)
#        for aux_type in ['protein', 'peptide', 'dna', 'rna', 'polysaccharide', 'saccharide',
#                         'small molecule', 'lipid', 'ion', 'water']:
#            if aux_type in aux_molecule_types:
#                counter = np.sum(array_molecule_types == aux_type)
#                if counter == 1:
#                    aux.append(aux_type)
#                elif aux_type=='water':
#                    aux.append(aux_type)
#                else:
#                    aux.append(_singular_molecule_type_to_plural[aux_type])
#        chain_types_from_chain.append(' + '.join(aux))
#
#    del(atom_indices, group_indices, component_indices, molecule_indices, molecule_types)
#
#self.chains["chain_type"] = np.array(chain_types_from_chain, dtype=object)

