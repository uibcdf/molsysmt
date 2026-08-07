import pytest

from molsysmt._private.argdigest.argument.item import digest_item
from molsysmt._private.argdigest.argument.items import digest_items
from molsysmt._private.smonitor import ArgumentError


def test_item_and_items_digesters(builder_pdb_molsys):
    assert digest_item(builder_pdb_molsys) is builder_pdb_molsys
    assert digest_item(builder_pdb_molsys, form='molsysmt.MolSys') is builder_pdb_molsys
    assert digest_item(None, caller='molsysmt.form.molsysmt_MolSys.append_structures') is None
    out = digest_items([builder_pdb_molsys, builder_pdb_molsys], forms=['molsysmt.MolSys', 'molsysmt.MolSys'])
    assert len(out) == 2

    with pytest.raises(ArgumentError):
        digest_item(builder_pdb_molsys, form='molsysmt.Topology')
    with pytest.raises(ArgumentError):
        digest_items([builder_pdb_molsys, object()])
