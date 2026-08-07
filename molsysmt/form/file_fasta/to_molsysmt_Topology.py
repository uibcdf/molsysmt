from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:fasta')
@dep_digest('Bio')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from Bio import SeqIO
    from molsysmt.native import MolSysBuilder

    # aa1 -> aa3 mapping (canonical 20 + ambiguous codes)
    _aa1_to_aa3 = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
        'O': 'PYL', 'U': 'SEC', 'B': 'ASX', 'Z': 'GLX', 'X': 'XAA', 'J': 'XLE',
    }

    records = list(SeqIO.parse(item, 'fasta'))

    builder = MolSysBuilder(skip_digestion=True)

    for chain_idx, record in enumerate(records):
        seq = str(record.seq)
        chain_id = record.id
        entity_name = record.description

        group_indices_in_chain = []

        for aa1 in seq:
            aa3 = _aa1_to_aa3.get(aa1.upper(), 'XAA')

            # Add one representative atom (CA) per residue
            atom_index = builder.add_atom(atom_name='CA', skip_digestion=True)

            # Add a group for this residue
            group_index = builder.add_group(
                atom_indices=[atom_index],
                group_name=aa3,
                group_type='amino acid',
                skip_digestion=True,
            )
            group_indices_in_chain.append(group_index)

        # Add chain
        chain_index = builder.add_chain(
            group_indices=group_indices_in_chain,
            chain_id=chain_id,
            chain_type='protein',
            skip_digestion=True,
        )

        # Add molecule (one per chain/sequence)
        molecule_index = builder.add_molecule(
            group_indices=group_indices_in_chain,
            molecule_name=chain_id,
            molecule_type='protein',
            skip_digestion=True,
        )

        # Add entity (one per sequence record)
        builder.add_entity(
            molecule_indices=[molecule_index],
            entity_name=entity_name,
            entity_type='protein',
            skip_digestion=True,
        )

    tmp_item = builder.topology
    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
