from molsysmt._private.smonitor import *
from molsysmt.form import _dict_modules
from depdigest import is_installed
from molsysmt import _depdigest
from pandas import DataFrame

class _SupportedMetadata:
    def __init__(self):
        self._initialized = False
        self._dict_forms_of_type = { ii:[] for ii in ['class', 'string', 'file']}
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
            if hasattr(_dict_modules[in_form], '_convert_to'):
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

def forms(form_type=None):
    """Return a styled DataFrame listing supported forms filtered by type."""

    tmp_output = []

    if form_type in [None,'all']:
        tmp_output=list(_dict_modules.keys())
    elif form_type in _metadata.dict_forms_of_type:
        tmp_output = _metadata.dict_forms_of_type[form_type]
    else:
        raise BadCallError()

    rows = []
    for form in tmp_output:
        mod = _dict_modules[form]
        # Get directory name to look up dependency
        import os
        dir_name = os.path.basename(os.path.dirname(mod.__file__))
        dep = _depdigest.MAPPING.get(dir_name, 'Native')
        
        installed = True
        if dep != 'Native':
            installed = is_installed(dep)
            
        rows.append([form, mod.form_type, dep, installed, mod.form_info])

    df = DataFrame(rows, columns=['Form', 'Type', 'Dependency', 'Installed', 'Info'])
    df = df.sort_values(by=['Type', 'Form'], ascending=[True, True], key=lambda col: col.str.casefold() if col.name != 'Installed' else col)

    def make_clickable(val):
        if isinstance(val, (list, tuple)) and len(val) >= 2 and val[1]:
            return '<a target="_blank" href="{}">{}</a>'.format(val[1], val[0])
        elif isinstance(val, (list, tuple)) and len(val) > 0:
            return val[0]
        return str(val)
    
    return df.style.hide(axis="index").format({'Info':make_clickable}).set_table_attributes('class="dataframe"')


def conversions(from_form=None, to_form=None, from_form_type=None, to_form_type=None,
                from_viewer=None, to_viewer=None, as_rows='from'):
    """Return a styled table showing available conversions between forms."""

    if from_viewer is not None or to_viewer is not None:

        from .viewers import viewers_forms

        if from_viewer is not None:
            from_form=viewers_forms[from_viewer]

        if to_viewer is not None:
            to_form=viewers_forms[to_viewer]

    if from_form_type is not None:
        if from_form_type in _metadata.dict_forms_of_type:
            from_form = _metadata.dict_forms_of_type[from_form_type]
        else:
            raise BadCallError()

    if to_form_type is not None:
        if to_form_type in _metadata.dict_forms_of_type:
            to_form = _metadata.dict_forms_of_type[to_form_type]
        else:
            raise BadCallError()

    if type(from_form) is str:
        from_form = [from_form]

    if type(to_form) is str:
        to_form = [to_form]

    if from_form is None:
        from_form = list(_dict_modules.keys())

    if to_form is None:
        to_form = list(_dict_modules.keys())

    dict_df = {}
    false_dict = {ii:False for ii in to_form}
    for ii in from_form:
        dict_df[ii]=false_dict.copy()


    for ii in from_form:
        for jj in to_form:
            if ii in _metadata.convert_from.keys():
                if jj in _metadata.convert_from[ii]:
                    dict_df[ii][jj]=True

    if as_rows=='from':
        tmp_output = DataFrame.from_dict(dict_df, orient='index')
    elif as_rows=='to':
        tmp_output = DataFrame.from_dict(dict_df)
    else:
        raise BadCallError()

    tmp_output = tmp_output.reindex(sorted(tmp_output.columns, key=str.casefold), axis=1)
    tmp_output = tmp_output.sort_index(key=lambda index: index.str.casefold())

    def color(val):
        if val is False:
            color = '#E2856E'
        else:
            color = '#C2CFB2'
        return 'background-color: %s' % color

    #return tmp_output.style.applymap(color).set_properties(**{'text-align': 'center'})
    return tmp_output.style.map(color).set_properties(**{'text-align': 'center'})

def syntaxes():
    """Placeholder for supported syntaxes listing."""

    pass
