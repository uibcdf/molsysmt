from molsysmt._private.argdigest import arg_digest
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    NotImplementedMethodError,
)
from molsysmt._private.variables import is_all
from molsysmt.element.bond import bond_length_tolerance, max_expected_bond_length


@arg_digest()
def get_missing_bonds(
    molecular_system,
    selection="all",
    structure_index=0,
    max_bond_length="2 angstroms",
    disulfide_bonds=False,
    disulfide_group_names=None,
    pbc=True,
    syntax="MolSysMT",
    engine="MolSysMT",
    sorted=True,
    skip_digestion=False,
):
    """
    Identifying candidate missing covalent bonds.

    This function compares the bonds inferred from group templates and/or distance-based
    neighbor searches against the bonds already recorded in the topology of the molecular
    system and returns candidate missing pairs. Peptidic bonds are considered only
    between consecutive source groups in the same declared chain. Selecting separated
    groups does not make them consecutive. These criteria are heuristics and do not
    establish a complete or chemically validated molecular graph.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Integer lists refer to source atom indices. Both atoms of
        each returned pair must belong to the selection. Defaults to 'all'.
    structure_index : int, default=0
        Source structure index used for distance-based candidates. Defaults to 0.
    max_bond_length : quantity or str, default='2 angstroms'
        Distance cutoff for geometric candidates, with explicit length units.
        Peptide candidates must also satisfy the element-pair threshold.
        Defaults to '2 angstroms'.
    disulfide_bonds : bool, default=False
        Whether to include geometric disulfide candidates. Defaults to False.
    disulfide_group_names : list of str or None, default=None
        Group names examined for disulfide candidates. None uses ['CYS'].
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='MolSysMT'
        Candidate engine: 'MolSysMT' or the optional 'pytraj' backend.
        Defaults to 'MolSysMT'.
    sorted : bool, default=True
        Whether to sort the returned bonded atom pairs.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of [int, int]
        List of ``[atom_index_1, atom_index_2]`` pairs representing bonds that are
        inferred from templates or distance criteria but not yet recorded in the
        molecular system topology. Indices refer to the source atom axis. An empty
        result is an empty list; this function does not modify the source.


    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    ArgumentChoiceError
        Raised if a terminal capping group cannot be classified as N- or C-terminal.


    Notes
    -----
    For groups with a known template (water, ion, amino acid, terminal capping,
    small molecule, saccharide), intra-group bonds are taken from the corresponding
    template. For groups without a template, bonds are inferred by a distance-based
    neighbor search using ``max_bond_length`` and element-pair thresholds stored in
    ``molsysmt.element.bond``.

    Peptidic C–N candidates connect source group indices ``g`` and ``g + 1``
    only when both have one defined, identical chain index. Missing or ambiguous
    chain membership is not used to infer peptide bonds. Distances are evaluated
    only for these pairs, using the requested structure and PBC setting.
    Group IDs need not be consecutive. Chain membership alone cannot preserve
    file-specific segment breaks that a source adapter has not retained.

    The optional PyTraj route eagerly reads an intermediate PDB and materializes
    its bond pairs before retiring the managed scratch directory. Preparation,
    read and extraction failures also retire the scratch; cleanup errors remain
    visible. Returned pairs do not depend on the intermediate file.

    Examples
    --------
    >>> import molsysmt as msm
    >>> system = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> msm.build.get_missing_bonds(system)
    []

    .. admonition:: User guide

       See :ref:`Tutorial_Get_missing_bonds` for auditing missing connectivity.


    .. versionadded:: 1.0.0
    """

    if disulfide_group_names is None:
        disulfide_group_names = ["CYS"]

    bonds = []

    if engine == "MolSysMT":
        from molsysmt import get, select
        from molsysmt.element.group.amino_acid import (
            get_bonded_atom_pairs as _bonds_in_amino_acid,
        )
        from molsysmt.element.group.ion import get_bonded_atom_pairs as _bonds_in_ion
        from molsysmt.element.group.saccharide import (
            get_bonded_atom_pairs as _bonds_in_saccharide,
        )
        from molsysmt.element.group.small_molecule import (
            get_bonded_atom_pairs as _bonds_in_small_molecule,
        )
        from molsysmt.element.group.terminal_capping import (
            get_bonded_atom_pairs as _bonds_in_terminal_capping,
        )
        from molsysmt.element.group.terminal_capping import (
            is_c_terminal_capping,
            is_n_terminal_capping,
        )
        from molsysmt.element.group.water import (
            get_bonded_atom_pairs as _bonds_in_water,
        )

        atom_mask = None
        group_selection = "all"
        if not is_all(selection):
            atom_mask = select(molecular_system, selection=selection, syntax=syntax)
            selected_groups = get(
                molecular_system,
                element="atom",
                selection=atom_mask,
                group_index=True,
                skip_digestion=True,
            )
            group_selection = list(
                dict.fromkeys(index for index in selected_groups if index is not None)
            )

        old_bonds = get(
            molecular_system,
            selection="all" if atom_mask is None else atom_mask,
            inner_bonded_atom_pairs=True,
            skip_digestion=True,
        )

        aux_lists = get(
            molecular_system,
            element="group",
            selection=group_selection,
            group_index=True,
            chain_index=True,
            group_name=True,
            group_type=True,
            atom_index=True,
            atom_name=True,
            atom_type=True,
            skip_digestion=True,
        )

        group_chains = {}
        aux_peptidic_bonds_C = {}
        aux_peptidic_bonds_N = {}

        bonds = []

        for (
            group_index,
            chain_index,
            group_name,
            group_type,
            atom_indices,
            atom_names,
            atom_types,
        ) in zip(*aux_lists):
            group_chains[group_index] = chain_index

            aux_bonds = None

            match group_type:
                case "water":
                    aux_bonds = _bonds_in_water(atom_names, atom_indices, sorted=False)
                case "ion":
                    aux_bonds = _bonds_in_ion(
                        group_name, atom_names, atom_indices, sorted=False
                    )
                case "amino acid":
                    aux_bonds = _bonds_in_amino_acid(
                        group_name, atom_names, atom_indices, sorted=False
                    )
                    if "C" in atom_names:
                        aux_peptidic_bonds_C[group_index] = atom_indices[
                            atom_names.index("C")
                        ]
                    if "N" in atom_names:
                        aux_peptidic_bonds_N[group_index] = atom_indices[
                            atom_names.index("N")
                        ]
                case "terminal capping":
                    aux_bonds = _bonds_in_terminal_capping(
                        group_name, atom_names, atom_indices, sorted=False
                    )
                    if is_c_terminal_capping(group_name):
                        aux_peptidic_bonds_C[group_index] = atom_indices[
                            atom_names.index("C")
                        ]
                    elif is_n_terminal_capping(group_name):
                        aux_peptidic_bonds_N[group_index] = atom_indices[
                            atom_names.index("N")
                        ]
                    else:
                        raise ArgumentChoiceError(
                            "terminal_capping",
                            "unknown",
                            ["C-terminal", "N-terminal"],
                            caller="molsysmt.build.get_missing_bonds",
                        )
                case "small molecule":
                    aux_bonds = _bonds_in_small_molecule(
                        group_name, atom_names, atom_indices, sorted=False
                    )
                case "saccharide":
                    aux_bonds = _bonds_in_saccharide(
                        group_name, atom_names, atom_indices, sorted=False
                    )
                case "polysaccharide":
                    aux_bonds = None
                case "lipid":
                    aux_bonds = None
                case "nucleotide":
                    aux_bonds = None
                case _:
                    aux_bonds = None

            if aux_bonds is None:
                aux_bonds = _bonds_in_group_without_template(
                    molecular_system,
                    atom_indices,
                    atom_names,
                    atom_types,
                    group_name,
                    group_type,
                    structure_index=structure_index,
                    max_bond_length=max_bond_length,
                    sorted=False,
                )

            bonds += aux_bonds

        # peptidic bonds

        aux_bonds = _get_peptidic_bonds(
            molecular_system,
            aux_peptidic_bonds_C,
            aux_peptidic_bonds_N,
            group_chains,
            structure_index=structure_index,
            max_bond_length=max_bond_length,
            pbc=pbc,
            sorted=False,
        )

        bonds += aux_bonds

        # disulfide bonds

        if disulfide_bonds:
            from .get_disulfide_bonds import get_disulfide_bonds

            aux_bonds = get_disulfide_bonds(
                molecular_system,
                selection=selection,
                structure_index=structure_index,
                max_bond_length=None,
                group_names=disulfide_group_names,
                pbc=pbc,
                sorted=False,
                skip_digestion=True,
            )

            bonds += aux_bonds

        # mask with selection

        if atom_mask is not None:
            mask = set(atom_mask)
            tmp_bonds = []
            for bond in bonds:
                if (bond[0] in mask) and (bond[1] in mask):
                    tmp_bonds.append(bond)
            bonds = tmp_bonds

        # remove old bonds

        if old_bonds:
            tmp_bonds = []
            for ii in bonds:
                if ii not in old_bonds:
                    tmp_bonds.append(ii)
            bonds = tmp_bonds

    elif engine == "pytraj":
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from molsysmt.basic import convert, get

        old_bonds = get(
            molecular_system,
            element="atom",
            selection=selection,
            inner_bonded_atoms=True,
        )

        for ii in range(len(old_bonds)):
            if old_bonds[ii][0] > old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]

        with TemporaryDirectory(prefix="molsysmt-pytraj-bonds-") as directory:
            temp_pdb_file = str(Path(directory) / "input.pdb")
            temp_molecular_system = convert(molecular_system, to_form=temp_pdb_file)
            temp_molecular_system = convert(
                temp_molecular_system,
                to_form="pytraj.Topology",
                max_bond_length=max_bond_length,
            )

            new_bonds = []
            for atom1_index, atom2_index in temp_molecular_system.bond_indices.tolist():
                if atom1_index > atom2_index:
                    atom1_index, atom2_index = atom2_index, atom1_index
                new_bonds.append([atom1_index, atom2_index])

        output = []
        for bond in new_bonds:
            if bond not in old_bonds:
                output.append(bond)

        bonds = output

    else:
        raise NotImplementedMethodError

    if sorted:
        bonds = sorted_list_of_pairs(bonds)

    return bonds


def _bonds_in_group_without_template(
    molecular_system,
    atom_indices,
    atom_names,
    atom_types,
    group_name,
    group_type,
    structure_index=0,
    max_bond_length="2 angstroms",
    pbc=True,
    sorted=True,
):
    """Infer missing bonds within a group lacking a template by neighbor search."""

    from molsysmt.element.atom import get_atom_type_from_atom_name
    from molsysmt.structure import get_neighbors

    bonds = []

    pairs, dists = get_neighbors(
        molecular_system,
        selection=atom_indices,
        structure_indices=structure_index,
        threshold=max_bond_length,
        output_type="pairs",
        unique_pairs=True,
        output_indices="selection",
        sorted=False,
        pbc=pbc,
        skip_digestion=True,
    )

    n_bonds_hs = {}

    for pair, dist in zip(pairs[0], dists[0]):
        atom_type_1 = atom_types[pair[0]]
        atom_type_2 = atom_types[pair[1]]

        if atom_type_1 is None:
            atom_type_1 = get_atom_type_from_atom_name(atom_names[pair[0]])
        if atom_type_2 is None:
            atom_type_2 = get_atom_type_from_atom_name(atom_names[pair[1]])

        atom_index_1 = atom_indices[pair[0]]
        atom_index_2 = atom_indices[pair[1]]

        add_bond = False

        try:
            aux_bond_distance = max_expected_bond_length[group_type][atom_type_1][
                atom_type_2
            ]
            if aux_bond_distance is not None:
                if dist <= aux_bond_distance + bond_length_tolerance:
                    add_bond = True
        except Exception:
            message = (
                f"No max bond length defined between atom types {atom_type_1} and {atom_type_2} "
                f"in group type {group_type}. The bond between atoms {[atom_index_1, atom_index_2]} was defined "
                f"by max_bond_length={round(max_bond_length, 4)}."
            )
            print("Warning: " + message)
            add_bond = True

        if add_bond:
            bonds.append([atom_index_1, atom_index_2])
            if atom_type_1 == "H":
                if atom_index_1 in n_bonds_hs:
                    n_bonds_hs[atom_index_1] += 1
                else:
                    n_bonds_hs[atom_index_1] = 1
            if atom_type_2 == "H":
                if atom_index_2 in n_bonds_hs:
                    n_bonds_hs[atom_index_2] += 1
                else:
                    n_bonds_hs[atom_index_2] = 1

    for ii in n_bonds_hs.keys():
        if n_bonds_hs[ii] > 1:
            print(
                f"Warning: H atom {ii} in group {group_name} has {n_bonds_hs[ii]} bonds"
            )

    if sorted:
        bonds = sorted_list_of_pairs(bonds)

    return bonds


def _get_peptidic_bonds(
    molecular_system,
    aux_peptidic_bonds_C,
    aux_peptidic_bonds_N,
    group_chains,
    structure_index=0,
    max_bond_length="2 angstroms",
    pbc=True,
    sorted=True,
):
    """Filter explicit adjacent, same-chain backbone pairs by distance."""

    from numbers import Integral

    from molsysmt.structure import get_distances

    bonds = []

    aux_C = []
    aux_N = []

    for group_index in aux_peptidic_bonds_C.keys():
        chain_index = group_chains[group_index]
        next_chain_index = group_chains.get(group_index + 1)
        if (
            group_index + 1 in aux_peptidic_bonds_N
            and isinstance(chain_index, Integral)
            and isinstance(next_chain_index, Integral)
            and chain_index >= 0
            and chain_index == next_chain_index
        ):
            aux_C.append(aux_peptidic_bonds_C[group_index])
            aux_N.append(aux_peptidic_bonds_N[group_index + 1])

    if len(aux_C):
        dists = get_distances(
            molecular_system,
            selection=aux_C,
            selection_2=aux_N,
            structure_indices=structure_index,
            pairs=True,
            pbc=pbc,
            skip_digestion=True,
        )
        for atom_C, atom_N, dist in zip(aux_C, aux_N, dists[0]):
            if (
                dist <= max_bond_length
                and dist
                <= max_expected_bond_length["protein"]["C"]["N"] + bond_length_tolerance
            ):
                bonds.append([atom_C, atom_N])

    if sorted:
        bonds = sorted_list_of_pairs(bonds)

    return bonds
