"""
Regression test for the `with_blocks` option of `get_dihedral_quartets`.

The blocks of one quartet are the two groups of atoms that move apart when that
dihedral angle is rotated. They have different sizes, so the collection is ragged and
must not be pushed through `numpy.array`, which raised on every real system.
"""

import molsysmt as msm
import numpy as np
from molsysmt import systems


def test_with_blocks_returns_the_two_groups_of_every_quartet(t4_h5msm_molsys):
    quartets, blocks = msm.topology.get_dihedral_quartets(
        t4_h5msm_molsys, phi=True, with_blocks=True)

    quartets = np.asarray(quartets)
    assert quartets.shape[1] == 4
    assert len(blocks) == quartets.shape[0]

    # Cutting the central bond of a quartet normally splits its component in two. It
    # does not for proline, whose ring keeps the two halves connected, and that single
    # block is the chemically correct answer rather than a defect.
    for quartet_blocks in blocks:
        assert len(quartet_blocks) in (1, 2)
        assert all(isinstance(block, set) for block in quartet_blocks)

    single = [index for index, quartet_blocks in enumerate(blocks) if len(quartet_blocks) == 1]
    for index in single:
        group_names = msm.get(t4_h5msm_molsys, element='atom',
                              selection=list(quartets[index]), group_name=True)
        assert 'PRO' in list(group_names)
    assert len(single) < len(blocks), 'every quartet cannot be a proline one' 

    # The sizes genuinely differ, which is what made numpy refuse the conversion.
    sizes = {len(block) for quartet_blocks in blocks for block in quartet_blocks}
    assert len(sizes) > 1

    # The two blocks of a quartet are disjoint and neither is empty.
    first, second = blocks[0]
    assert first and second
    assert first.isdisjoint(second)


def test_with_blocks_supports_several_dihedral_types(t4_h5msm_molsys):
    quartets, blocks = msm.topology.get_dihedral_quartets(
        t4_h5msm_molsys, phi=True, psi=True, with_blocks=True)

    assert len(quartets) == 2
    assert len(blocks) == 2
    for quartets_of_type, blocks_of_type in zip(quartets, blocks):
        assert len(blocks_of_type) == np.asarray(quartets_of_type).shape[0]


def test_with_blocks_indexing_used_by_the_documentation(t4_h5msm_molsys):
    # The tutorial does `phi_blocks[2][0]` and `phi_blocks[2][1]`, then converts each
    # to a list for a selection. That access pattern has to keep working.
    _, phi_blocks = msm.topology.get_dihedral_quartets(
        t4_h5msm_molsys, phi=True, with_blocks=True)

    block_0 = list(phi_blocks[2][0])
    block_1 = list(phi_blocks[2][1])
    assert len(msm.select(t4_h5msm_molsys, selection=block_0)) == len(block_0)
    assert len(msm.select(t4_h5msm_molsys, selection=block_1)) == len(block_1)
