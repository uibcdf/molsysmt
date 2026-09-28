"""Compatibility imports for the historical hydrogen-bond namespace."""

from molsysmt.interactions.hbonds import (
    acceptor_exclusion_rules,
    acceptor_inclusion_rules,
    donor_exclusion_rules,
    donor_inclusion_rules,
    get_acceptor_atoms,
    get_buch_hbonds,
    get_donor_atoms,
    get_luzard_chandler_hbonds,
)

__all__ = [
    "acceptor_exclusion_rules",
    "acceptor_inclusion_rules",
    "donor_exclusion_rules",
    "donor_inclusion_rules",
    "get_acceptor_atoms",
    "get_buch_hbonds",
    "get_donor_atoms",
    "get_luzard_chandler_hbonds",
]
