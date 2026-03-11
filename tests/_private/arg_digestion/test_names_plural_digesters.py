import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.atom_names import digest_atom_names
from molsysmt._private.arg_digestion.argument.group_names import digest_group_names
from molsysmt._private.arg_digestion.argument.disulfide_group_names import digest_disulfide_group_names
from molsysmt._private.arg_digestion.argument.to_group_names import digest_to_group_names

CALLER = "molsysmt.build.mutate.mutate"


def test_atom_names_accept_scalar_all_and_nested_iterables():
    assert digest_atom_names(None) is None
    assert digest_atom_names("all") == "all"
    assert digest_atom_names("CA") == ["CA"]
    assert digest_atom_names(np.array(["N", "CA"])) == ["N", "CA"]
    assert digest_atom_names(("C", "O")) == ["C", "O"]
    assert digest_atom_names([["N", "CA"], ["C", "O"]]) == [["N", "CA"], ["C", "O"]]

    with pytest.raises(ArgumentError):
        digest_atom_names(3, caller=CALLER)


@pytest.mark.parametrize("digester", [digest_group_names, digest_disulfide_group_names])
def test_group_name_digesters_accept_strings_and_sequences(digester):
    assert digester("CYS") == ["CYS"]
    assert list(digester(("CYS", "CYX"))) == ["CYS", "CYX"]

    ndarray_value = digester(np.array(["CYS", "CYX"], dtype=object))
    assert list(ndarray_value) == ["CYS", "CYX"]

    with pytest.raises(ArgumentError):
        digester(["CYS", 3], caller=CALLER)



def test_to_group_names_accepts_string_and_string_iterables():
    assert digest_to_group_names("ACE", caller=CALLER) == ["ACE"]
    assert list(digest_to_group_names(("ACE", "NME"), caller=CALLER)) == ["ACE", "NME"]
    assert list(digest_to_group_names(np.array(["ACE", "NME"]), caller=CALLER)) == ["ACE", "NME"]

    with pytest.raises(ArgumentError):
        digest_to_group_names(["ACE", 5], caller=CALLER)
