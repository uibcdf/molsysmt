from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import digest_engine

def add_missing_heavy_atoms(molecular_system, selection='all', missing_heavy_atoms=None, engine='PDBFixer',
                            syntaxis='MolSysMT'):

    engine = digest_engine(engine)

    output = None

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        output_form = get_form(molecular_system)

        if missing_heavy_atoms is None:
            from molsysmt.build import get_missing_heavy_atoms
            missing_heavy_atoms = get_missing_heavy_atoms(molecular_system, selection=selection, syntaxis=syntaxis)



        tmp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        tmp_molecular_system.missingResidues = {}
        tmp_molecular_system.findMissingAtoms()
        tmp_molecular_system.missingTerminals = {}

        aux_dict = {}

        for group, atoms in tmp_molecular_system.missingAtoms.items():
            if group.index in missing_heavy_atoms:
                aux_dict[group]=[]
                for atom in atoms:
                    if atom.name in missing_heavy_atoms[group.index]:
                        aux_dict[group].append(atom)

        tmp_molecular_system.missingAtoms = aux_dict

        tmp_molecular_system.addMissingAtoms()

        output = convert(tmp_molecular_system, to_form=output_form)

    else:

        raise NotImplementedError

    return output

