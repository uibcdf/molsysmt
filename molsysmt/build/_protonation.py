"""Which hydrogens a system carries that the requested pH does not call for.

`add_missing_hydrogens` compares expected against present in one direction only: it
adds what is absent and never looks at what is present and unwanted. That asymmetry is
`uibcdf/molsysmt#178`, and this module holds the other half of the comparison so the two
functions cannot drift apart — `reconcile_protonation` removes what it reports, and
`add_missing_hydrogens` warns about it.

Detection lives here rather than in either caller because the rule that decides is the
same one: `get_expected_hydrogens`, with the same terminal and disulfide context. Two
implementations of "which hydrogens belong here" would eventually disagree, and the
disagreement would be silent.
"""

from molsysmt.element.group.amino_acid import group_names
from molsysmt.element.group.amino_acid.get_expected_hydrogens import get_expected_hydrogens
from molsysmt.element.group.amino_acid.get_standard_name import get_standard_name


def _is_hydrogen(atom_name):
    if not atom_name:
        return False
    if atom_name[0] == 'H':
        return True
    return len(atom_name) >= 2 and atom_name[0].isdigit() and atom_name[1] == 'H'


def unexpected_hydrogens(native_molsys, pH):
    """Return the hydrogens present that the pH rules would not have placed.

    Parameters
    ----------
    native_molsys : molsysmt.MolSys
        System to inspect. Its topology is read, never modified.
    pH : float
        The pH the caller asked for.

    Returns
    -------
    list of tuple
        ``(atom_index, atom_name, group_index, group_name)``, ordered by atom index.

    Notes
    -----
    Only amino-acid groups are examined. A residue absent from the template database
    has no expectation to compare against, so nothing about it is reported — silence
    here means *not assessed*, not *correct*.
    """

    topology = native_molsys.topology

    topology.rebuild_components(redefine_indices=True, redefine_ids=False,
                                redefine_types=True, redefine_names=False)

    n_groups = topology.n_groups
    component_indices = topology._get_component_indices()

    first_group_of_component = {}
    last_group_of_component = {}
    for group_index in range(n_groups):
        group_atoms = topology.atoms[topology.atoms['group_index'] == group_index]
        if group_atoms.empty:
            continue
        component_index = int(component_indices.loc[group_atoms.index[0]])
        if component_index not in first_group_of_component:
            first_group_of_component[component_index] = group_index
        last_group_of_component[component_index] = group_index

    disulfide_groups = set()
    bonds = topology._get_chemical_state_bonds()
    if bonds is not None and len(bonds) > 0:
        for _, bond in bonds.iterrows():
            first = topology.atoms.loc[int(bond['atom1_index'])]
            second = topology.atoms.loc[int(bond['atom2_index'])]
            if first['atom_name'] == 'SG' and second['atom_name'] == 'SG':
                disulfide_groups.add(int(first['group_index']))
                disulfide_groups.add(int(second['group_index']))

    unexpected = []

    for group_index in range(n_groups):
        group_atoms = topology.atoms[topology.atoms['group_index'] == group_index]
        if group_atoms.empty:
            continue

        group_name = topology.groups.loc[group_index, 'group_name']
        canonical = get_standard_name(group_name)
        lookup = canonical if canonical is not None else group_name
        if lookup not in group_names:
            continue

        component_index = int(component_indices.loc[group_atoms.index[0]])

        present_names = group_atoms['atom_name'].tolist()
        expected = get_expected_hydrogens(
            group_name,
            present_atom_names=present_names,
            pH=pH,
            is_n_terminal=(first_group_of_component.get(component_index) == group_index),
            is_c_terminal=(last_group_of_component.get(component_index) == group_index),
            is_disulfide=(group_index in disulfide_groups),
        )
        if expected is None:
            continue

        expected_set = set(expected)
        for atom_index, atom_name in zip(group_atoms.index.tolist(), present_names):
            if _is_hydrogen(atom_name) and atom_name not in expected_set:
                unexpected.append((int(atom_index), str(atom_name),
                                   int(group_index), str(group_name)))

    unexpected.sort()
    return unexpected
