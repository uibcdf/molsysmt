from depdigest import get_info
from pandas import DataFrame

from molsysmt._private.argdigest import arg_digest

from ._report import data_output


@arg_digest()
def dependencies(*, output_type="styler", skip_digestion=False):
    """
    Reporting dependency status in a visual or programmatic representation.

    Parameters
    ----------
    output_type : str, default='styler'
        Representation: styler, dataframe or dictionary. Dictionary has index,
        columns and data keys accepted by pandas.DataFrame.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.


    Returns
    -------
    pandas.io.formats.style.Styler, pandas.DataFrame or dict
        Fresh dependency rows from DepDigest, sorted by Status, Type and Library.
        The report does not import optional scientific engines to execute features.

    Examples
    --------
    >>> 'Library' in dependencies(output_type='dataframe').columns
    True

    .. versionadded:: 1.0.0
    """
    rows = get_info("molsysmt")

    df = DataFrame(rows)
    df.sort_values(
        by=["Status", "Type", "Library"], ascending=[True, True, True], inplace=True
    )

    if output_type != "styler":
        return data_output(df, output_type)
    return df.style.hide(axis="index").set_properties(**{"text-align": "left"})
