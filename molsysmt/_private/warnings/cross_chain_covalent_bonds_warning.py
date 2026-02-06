from .user_molsysmt_warning import UserMolSysMTWarning
from ..functions import caller_name
from ..exceptions._emit import message_from_catalog
from molsysmt._private.smonitor import CATALOG

class CrossChainCovalentBondsWarning(UserMolSysMTWarning):

    def __init__(self, molecular_system, atom_pairs):

        from molsysmt.basic import get_label

        label_pairs_reported = []

        for atom1, atom2 in atom_pairs:
            chain1 = molecular_system.topology.atoms.at[atom1, 'chain_index']
            chain2 = molecular_system.topology.atoms.at[atom2, 'chain_index']
            if chain1 != chain2:
                label1 = get_label(molecular_system, element='atom', selection=atom1,
                                   string='{atom_name} {atom_id} in {group_name}{group_id} with atom_index {atom_index}',
                                   skip_digestion=True)
                label2 = get_label(molecular_system, element='atom', selection=atom2,
                                   string='{atom_name} {atom_id} in {group_name}{group_id} with atom_index {atom_index}',
                                   skip_digestion=True)
                label_pairs_reported.append((label1, label2))

        default_message = (
            f"{len(label_pairs_reported)} covalent bond(s) reported by the 'struct_conn' table "
            f"between atoms belonging to different chains were added.\n"
            "Verify whether these cross-chain bonds are expected in your system.\n"
        )

        for label1, label2 in label_pairs_reported[:-1]:
            default_message += f"  - {label1}  <-->  {label2}\n"

        if label_pairs_reported:
            default_message += f"  - {label_pairs_reported[-1][0]}  <-->  {label_pairs_reported[-1][1]}"

        caller = caller_name()
        full_message = message_from_catalog(
            CATALOG["warnings"]["CrossChainCovalentBondsWarning"],
            extra={
                "caller": caller,
                "count": len(label_pairs_reported),
                "pairs": label_pairs_reported,
            },
            default_message=default_message,
        )

        super().__init__(full_message)
