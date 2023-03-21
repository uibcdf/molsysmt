from molsysmt._private.digestion import digest


@digest()
def is_composed_of(molecular_system, selection='all', syntax='MolSysMT', ions=False, waters=False,
                   small_molecules=False, peptides=False, proteins=False, dnas=False, rnas=False,
                   lipids=False, oligosaccharides=False, saccharides=False):

    from . import get

    n_ions, n_waters, n_small_molecules, n_peptides, n_proteins, \
    n_dnas, n_rnas, n_lipids, n_oligosaccharides, n_saccharides = get(molecular_system, element="system",
                                            selection=selection, syntax=syntax,
                                            n_ions=True, n_waters=True, n_small_molecules=True,
                                            n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True,
                                            n_lipids=True, n_oligosaccharides=True, n_saccharides=True)

    aux_list = [[ions, n_ions],
                [waters, n_waters],
                [small_molecules, n_small_molecules],
                [peptides, n_peptides],
                [proteins, n_proteins],
                [dnas, n_dnas],
                [rnas, n_rnas],
                [lipids, n_lipids],
                [oligosaccharides, n_oligosaccharides],
                [saccharides, n_saccharides],
                ]

    output = True

    for condition, in_system in aux_list:

        if type(condition) == int:
            if condition != in_system:
                output = False
                break

        elif type(condition) == bool:
            if condition == True:
                if in_system == 0:
                    output = False
                    break
            else:
                if in_system > 0:
                    output = False
                    break

    return output
