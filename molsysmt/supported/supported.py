from copy import deepcopy

from pandas import DataFrame

from molsysmt import _depdigest
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentChoiceError
from molsysmt.form import _dict_modules

from ._report import data_output


class _SupportedMetadata:
    def __init__(self):
        self._initialized = False
        self._dict_forms_of_type = {ii: [] for ii in ["class", "string", "file"]}
        self._convert_from = {}
        self._convert_to = {}

    def _ensure_initialized(self):
        if not self._initialized:
            self._initialize()
            self._initialized = True

    def _initialize(self):
        # Build dict_forms_of_type
        for ii, jj in _dict_modules.items():
            if jj.form_type in self._dict_forms_of_type:
                self._dict_forms_of_type[jj.form_type].append(ii)

        for ii, jj in self._dict_forms_of_type.items():
            self._dict_forms_of_type[ii] = sorted(jj)

        # Build conversion maps
        for in_form in _dict_modules.keys():
            # Accessing _convert_to forces the module to be imported if not already
            if hasattr(_dict_modules[in_form], "_convert_to"):
                aux_list = list(_dict_modules[in_form]._convert_to.keys())
                if in_form in aux_list:
                    aux_list.remove(in_form)
                self._convert_from[in_form] = aux_list

        for in_form, out_forms in self._convert_from.items():
            for out_form in out_forms:
                if out_form not in self._convert_to:
                    self._convert_to[out_form] = []
                self._convert_to[out_form].append(in_form)

        for in_form in self._convert_from.keys():
            self._convert_from[in_form] = sorted(self._convert_from[in_form])

        for out_form in self._convert_to.keys():
            self._convert_to[out_form] = sorted(self._convert_to[out_form])

    @property
    def dict_forms_of_type(self):
        self._ensure_initialized()
        return self._dict_forms_of_type

    @property
    def convert_from(self):
        self._ensure_initialized()
        return self._convert_from

    @property
    def convert_to(self):
        self._ensure_initialized()
        return self._convert_to


_metadata = _SupportedMetadata()

## Types


@arg_digest()
def forms(form_type=None, *, output_type="styler", skip_digestion=False):
    """
    Reporting supported forms in a visual or programmatic representation.

    Parameters
    ----------
    form_type : str or None, default=None
        Category filter: class, file, string, all or None (all categories).
    output_type : str, default='styler'
        Representation: styler, dataframe, dictionary or list. Dictionary has
        index, columns and data keys accepted by pandas.DataFrame. List contains
        the form names in the same order as the table.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pandas.io.formats.style.Styler, pandas.DataFrame, dict or list
        Filtered rows with Form, Type, Dependency and Info columns, ordered by
        type then form name, ignoring case. Plain outputs retain raw metadata;
        only the styled output renders Info links. Each call returns fresh data.

    Notes
    -----
    Discovery follows the current form registry and capability visibility policy.
    A listed adapter does not certify every optional provider operation runnable.

    Examples
    --------
    >>> 'molsysmt.MolSys' in forms(output_type='list')
    True

    .. versionadded:: 1.0.0
    """

    tmp_output = []

    if form_type in [None, "all"]:
        tmp_output = list(_dict_modules.keys())
    elif form_type in _metadata.dict_forms_of_type:
        tmp_output = _metadata.dict_forms_of_type[form_type]
    else:
        raise ArgumentChoiceError(
            "form_type", form_type, ["all", *_metadata.dict_forms_of_type]
        )

    rows = []
    for form in tmp_output:
        mod = _dict_modules[form]
        # Get directory name to look up dependency
        import os

        dir_name = os.path.basename(os.path.dirname(mod.__file__))
        dep = _depdigest.MAPPING.get(dir_name, "Native")

        rows.append([form, mod.form_type, dep, deepcopy(mod.form_info)])

    df = DataFrame(rows, columns=["Form", "Type", "Dependency", "Info"])
    df = df.sort_values(
        by=["Type", "Form"], ascending=[True, True], key=lambda col: col.str.casefold()
    )

    if output_type == "list":
        return df["Form"].tolist()
    if output_type != "styler":
        return data_output(df, output_type)

    def make_clickable(val):
        if isinstance(val, (list, tuple)) and len(val) >= 2 and val[1]:
            return '<a target="_blank" href="{}">{}</a>'.format(val[1], val[0])
        elif isinstance(val, (list, tuple)) and len(val) > 0:
            return val[0]
        return str(val)

    return (
        df.style.hide(axis="index")
        .format({"Info": make_clickable})
        .set_table_attributes('class="dataframe"')
    )


@arg_digest()
def conversions(
    from_form=None,
    to_form=None,
    from_form_type=None,
    to_form_type=None,
    from_viewer=None,
    to_viewer=None,
    as_rows="from",
    *,
    output_type="styler",
    skip_digestion=False,
):
    """
    Reporting declared conversion routes in visual or programmatic form.

    Parameters
    ----------
    from_form : str, list, tuple or None, default=None
        Source form names; None includes the current registry. Unknown names
        retain false entries, rather than declaring a route.
    to_form : str, list, tuple or None, default=None
        Destination form names; None includes the current registry.
    from_form_type : str or None, default=None
        Optional class, file or string filter overriding source form names.
    to_form_type : str or None, default=None
        Optional class, file or string filter overriding destination form names.
    from_viewer : str or None, default=None
        Optional MolSysViewer or NGLView source filter, applied before type filters.
    to_viewer : str or None, default=None
        Optional MolSysViewer or NGLView destination filter.
    as_rows : str, default='from'
        Use from for source rows or to for destination rows.
    output_type : str, default='styler'
        Representation: styler, dataframe or dictionary. Dictionary has index,
        columns and data keys accepted by pandas.DataFrame, retaining both axes.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pandas.io.formats.style.Styler, pandas.DataFrame or dict
        Boolean route matrix with case-insensitively sorted row/column labels.
        Empty filters retain the other requested axis. Data is fresh per call.

    Notes
    -----
    True describes a declared adapter route, not guaranteed execution for every
    input or installed optional provider. Self routes retain the existing false
    diagonal. No molecular system is loaded to construct this report.

    Examples
    --------
    >>> table = conversions(from_form=['molsysmt.MolSys'],
    ...     to_form=['molsysmt.MolSys'], output_type='dataframe')
    >>> table.shape
    (1, 1)
    >>> bool(table.iloc[0, 0])
    False

    .. versionadded:: 1.0.0
    """

    if from_viewer is not None or to_viewer is not None:
        from .viewers import viewers_forms

        if from_viewer is not None:
            from_form = viewers_forms[from_viewer]

        if to_viewer is not None:
            to_form = viewers_forms[to_viewer]

    if from_form_type is not None:
        if from_form_type in _metadata.dict_forms_of_type:
            from_form = _metadata.dict_forms_of_type[from_form_type]
        else:
            raise ArgumentChoiceError(
                "from_form_type", from_form_type, _metadata.dict_forms_of_type
            )

    if to_form_type is not None:
        if to_form_type in _metadata.dict_forms_of_type:
            to_form = _metadata.dict_forms_of_type[to_form_type]
        else:
            raise ArgumentChoiceError(
                "to_form_type", to_form_type, _metadata.dict_forms_of_type
            )

    if type(from_form) is str:
        from_form = [from_form]

    if type(to_form) is str:
        to_form = [to_form]

    if from_form is None:
        from_form = list(_dict_modules.keys())

    if to_form is None:
        to_form = list(_dict_modules.keys())

    from_form = list(dict.fromkeys(from_form))
    to_form = list(dict.fromkeys(to_form))
    tmp_output = DataFrame(False, index=from_form, columns=to_form, dtype=bool)

    for ii in from_form:
        for jj in to_form:
            if ii in _metadata.convert_from.keys():
                if jj in _metadata.convert_from[ii]:
                    tmp_output.at[ii, jj] = True

    if as_rows == "from":
        pass
    elif as_rows == "to":
        tmp_output = tmp_output.T
    else:
        raise ArgumentChoiceError("as_rows", as_rows, ["from", "to"])

    tmp_output = tmp_output.reindex(
        sorted(tmp_output.columns, key=str.casefold), axis=1
    )
    tmp_output = tmp_output.sort_index(key=lambda index: index.str.casefold())

    if output_type != "styler":
        return data_output(tmp_output, output_type)

    def color(val):
        if val is False:
            color = "#E2856E"
        else:
            color = "#C2CFB2"
        return "background-color: %s" % color

    # return tmp_output.style.applymap(color).set_properties(**{'text-align': 'center'})
    return tmp_output.style.map(color).set_properties(**{"text-align": "center"})


@arg_digest()
def syntaxes(*, output_type="styler", skip_digestion=False):
    """
    Returning the directional selection-syntax capability matrix.

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
        Table reporting whether each syntax can parse selection strings and
        whether MolSysMT can translate selected indices into that syntax.


    Notes
    -----
    A syntax may be supported in only one direction. The scope column records
    form or element restrictions that apply to an implemented direction.

    Examples
    --------
    >>> 'Syntax' in syntaxes(output_type='dataframe').columns
    True


    .. versionadded:: 1.0.0
    """

    from ._syntaxes import syntax_capabilities

    rows = [
        {
            "Syntax": name,
            "Selection input": capabilities["select"],
            "Translation output": capabilities["to_syntax"],
            "Scope": capabilities["scope"],
        }
        for name, capabilities in syntax_capabilities.items()
    ]
    table = DataFrame(rows)
    if output_type != "styler":
        return data_output(table, output_type)
    return table.style.hide(axis="index").set_table_attributes('class="dataframe"')
