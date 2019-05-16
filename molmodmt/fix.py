from .multitool import get_form as _get_form
from .multitool import get as _get
from .utils.exceptions import *

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

def fix_pdb_structure(item, missing_atoms=True, missing_residues=True, nonstandard_residues=True,
                      missing_terminals=True, missing_loops=False, missing_hydrogens=True,
                      pH=7.4, output_form=None, engine_atoms='pdbfixer', engine_loops='modeller',
                     verbose=True):

    from .multitool import get_form as _get_form
    from .multitool import convert as _convert

    in_form = _get_form(item)
    if output_form is None:
        output_form=in_form

    tmp_item = None

    if in_form not in ['pdb','pdb:id','pdbfixer.PDBFixer']:
        raise BadCallError(BadCallMessage)

    if engine_atoms=='pdbfixer':

        tmp_item = _convert(item,'pdbfixer')

        if missing_residues:
            tmp_item.findMissingResidues()
        if missing_atoms:
            tmp_item.findMissingAtoms()
        if nonstandard_residues:
            tmp_item.findNonstandardResidues()

        if verbose:
            print(tmp_item.missingResidues)
            print(tmp_item.missingAtoms)
            print(tmp_item.nonstandardResidues)

        tmp_item.addMissingAtoms()

        if missing_hydrogens:
            tmp_item.addMissingHydrogens(pH=pH)

    if missing_loops:

        from .model_loops import add_loop as _add_loop
        tmp_item = _add_loop(tmp_item, engine=engine_loops)

    tmp_item = _convert(tmp_item, output_form)

    return tmp_item

