"""Returning capability data independently of notebook rendering."""

from copy import deepcopy


def data_output(table, output_type):
    """Return a fresh table or a detached constructor-compatible dictionary."""
    if output_type == "dataframe":
        return table
    return deepcopy(table.to_dict(orient="split"))
