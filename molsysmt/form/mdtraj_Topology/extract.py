from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def extract(item, atom_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        atom_indices = digest_atom_indices(atom_indices)

    if atom_indices is 'all':

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from mdtraj.core.topology import Topology
        from mdtraj.utils import ilen

        atom_indices_to_be_kept = set(atom_indices)
        newTopology = Topology()
        old_atom_to_new_atom = {}

        for chain in item._chains:
            newChain = newTopology.add_chain()
            for group in chain._groups:
                resSeq = getattr(group, 'resSeq', None) or group.index
                newResidue = newTopology.add_group(group.name, newChain,
                                                     resSeq, group.segment_id)
                for atom in group._atoms:
                    if atom.index in atom_indices_to_be_kept:
                        try:  # OpenMM Topology objects don't have serial attributes, so we have to check first.
                            serial = atom.serial
                        except AttributeError:
                            serial = None
                        newAtom = newTopology.add_atom(atom.name, atom.element,
                                                       newResidue, serial=serial)
                        old_atom_to_new_atom[atom] = newAtom

        bondsiter = item.bonds
        if not hasattr(bondsiter, '__iter__'):
            bondsiter = bondsiter()

        for bond in bondsiter:
            try:
                atom1, atom2 = bond
                newTopology.add_bond(old_atom_to_new_atom[atom1],
                                     old_atom_to_new_atom[atom2],
                                     type=bond.type,
                                     order=bond.order)
            except KeyError:
                pass
                # we only put bonds into the new topology if both of their partners
                # were indexed and thus HAVE a new atom

        # Delete empty groups
        newTopology._groups = [r for r in newTopology._groups if len(r._atoms) > 0]
        for chain in newTopology._chains:
            chain._groups = [r for r in chain._groups if len(r._atoms) > 0]

        # Delete empty chains
        newTopology._chains = [c for c in newTopology._chains
                               if len(c._groups) > 0]
        # Re-set the numAtoms and numResidues
        newTopology._numAtoms = ilen(newTopology.atoms)
        newTopology._numResidues = ilen(newTopology.groups)

        tmp_item = newTopology

    return tmp_item

