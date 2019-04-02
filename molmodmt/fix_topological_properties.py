from .multitool import get_form as _get_form
from .multitool import get as _get

_chain_IDs=['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def fix_chains(item,chains=None):

    in_form = _get_form(item)

    if in_form=='parmed.Structure' or in_form=='parmed.GromacsTopologyFile':
        tmp_molecules, tmp_types=_get(item,molecules=True,molecule_type=True)
        n_proteins=0
        with_water=False
        with_ions=False
        chain={}
        for type_molecule in tmp_types:
            if type_molecule=='protein':
                n_proteins+=1
            elif type_molecule=='water':
                with_water=True
            elif type_molecule=='ion':
                with_ions=True
        ii=0
        if n_proteins>0:
            ii=n_proteins
            chain['protein']=_chain_IDs[:ii]
            ii+=-1
        if with_water:
            ii+=1
            chain['water']=_chain_IDs[ii]
        if with_ions:
            ii+=1
            chain['ion']=_chain_IDs[ii]
        n_proteins=0
        for ii in range(len(tmp_molecules)):
            if tmp_types[ii]=='protein':
                chain_molecule=chain['protein'][n_proteins]
                n_proteins+=1
            else:
                chain_molecule=chain[tmp_types[ii]]
            for atom_idx in tmp_molecules[ii]:
                item.atoms[atom_idx].residue.chain=chain_molecule
        pass

