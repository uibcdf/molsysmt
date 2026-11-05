import gzip
import pickle
from importlib.resources import files

from molsysmt._private.smonitor import InternalAlgorithmError
from molsysmt.element.group.amino_acid import group_names


def path(package, file):
    return files(package).joinpath(file)


def get_group_db(group_name):
    """
    Getting the internal reference database dictionary for amino acid groups.


    Parameters
    ----------
    group_name : str
        Name of the chemical group (residue).

    Returns
    -------
    dict
        Reference dictionary containing residue connectivity and metadata.


    Notes
    -----
    This is a raw historical mixed-source catalogue, not a naming-aware chemical
    reference selector. Even variants stored under one label can describe distinct
    compounds or naming conventions. GLH, HIP, CYM and LYN contain such mixtures.
    Use get_expected_heavy_atoms or get_expected_hydrogens with source context for
    bounded reference inventories. Do not choose the first raw variant for repair
    or infer chemical-template equivalence from a reported sequence parent.

    .. versionadded:: 1.0.0
    """

    if group_name not in group_names:
        raise InternalAlgorithmError(
            "Unexpected empty state",
            caller="molsysmt.element.group.amino_acid.get_group_db",
        )
    with gzip.open(
        path("molsysmt.data.databases.amino_acids", group_name[0] + ".pkl.gz"), "rb"
    ) as fff:
        dbs = pickle.load(fff)

    db = dbs[group_name]

    return db
