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
                      pH=7.4, to_form=None, engine_fix_pdb='PDBFixer', engine_hydrogens='PDBFixer',
                      engine_loops='Modeller', verbose=False):

    from .utils.forms import digest as digest_forms
    from .utils.engines import digest as digest_engines
    from .multitool import convert

    form_in, form_out = digest_forms(item, to_form)
    engine_fix_pdb = digest_engines(engine_fix_pdb)
    engine_hydrogens = digest_engines(engine_hydrogens)
    engine_loops = digest_engines(engine_loops)

    tmp_item = None

    if form_in not in ['pdb','pdb:id','pdbfixer.PDBFixer']:

        raise BadCallError(BadCallMessage)

    if engine_fix_pdb=='PDBFixer':

        tmp_item = convert(item,'pdbfixer.PDBFixer')

        if missing_residues:
            tmp_item.findMissingResidues()
        if missing_atoms:
            tmp_item.findMissingAtoms()
        if nonstandard_residues:
            tmp_item.findNonstandardResidues()

        if verbose:
            print('Missing residues:', tmp_item.missingResidues)
            print('Non standard residues:', tmp_item.nonstandardResidues)
            print('Missing atoms', tmp_item.missingAtoms)
            print('Missing terminals:', tmp_item.missingTerminals)

        tmp_item.addMissingAtoms()

        if verbose:
            print('Missing residues or atoms reported fixed.')

    if missing_hydrogens:

        from .protonation import add_missing_hydrogens
        tmp_item = add_missing_hydrogens(tmp_item, pH=pH, engine=engine_hydrogens, verbose=verbose)

    if missing_loops:

        from .model_loops import add_loop
        tmp_item = add_loop(tmp_item, engine=engine_loops)

    tmp_item = convert(tmp_item, form_out)

    return tmp_item

