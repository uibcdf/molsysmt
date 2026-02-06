from .user_molsysmt_warning import UserMolSysMTWarning

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

        msg = (f"{len(label_pairs_reported)} covalent bond(s) reported by the 'struct_conn' table "
               f"between atoms belonging to different chains were added.\n"
               "Verify whether these cross-chain bonds are expected in your system.\n")

        for label1, label2 in label_pairs_reported[:-1]:
            msg += f"  - {label1}  <-->  {label2}\n"

        msg += f"  - {label_pairs_reported[-1][0]}  <-->  {label_pairs_reported[-1][1]}"
        try:
            from smonitor.integrations import emit_from_catalog
            from molsysmt._private.smonitor import CATALOG, PACKAGE_ROOT, with_meta

            emit_from_catalog(
                CATALOG["warnings"]["CrossChainCovalentBondsWarning"],
                package_root=PACKAGE_ROOT,
                extra=with_meta({
                    "caller": None,
                    "count": len(label_pairs_reported),
                    "pairs": label_pairs_reported,
                }),
            )
        except Exception:
            pass

        super().__init__(msg)
