from molsysmt._private.exceptions import *
from molsysmt.form import _dict_modules
from pandas import DataFrame

dict_forms_of_type = { ii:[] for ii in ['class', 'string', 'file']}

for ii, jj in _dict_modules.items():
    dict_forms_of_type[jj.form_type].append(ii)

for ii,jj in dict_forms_of_type.items():
    dict_forms_of_type[ii]=sorted(jj)

convert_from = {}
convert_to = {}

for in_form in _dict_modules.keys():
    aux_list = list(_dict_modules[in_form]._convert_to.keys())
    aux_list.remove(in_form)
    convert_from[in_form] = aux_list

for in_form, out_forms in convert_from.items():
    for out_form in out_forms:
        try:
            convert_to[out_form].append(in_form)
        except:
            convert_to[out_form]=[]
            convert_to[out_form].append(in_form)

for in_form in convert_from.keys():
    convert_from[in_form]=sorted(convert_from[in_form])

for out_form in convert_to.keys():
    convert_to[out_form]=sorted(convert_to[out_form])

## Types

def forms(form_type=None):

    tmp_output = []

    if form_type in [None,'all']:
        tmp_output=list(_dict_modules.keys())
    elif form_type in dict_forms_of_type:
        tmp_output=dict_forms_of_type[form_type]
    else:
        raise BadCallError()

    df=DataFrame([[form, _dict_modules[form].form_type, _dict_modules[form].form_info] for form in tmp_output], columns=['Form', 'Type', 'Info'])
    df = df.sort_values(by=['Type', 'Form'], ascending=[True, True], key=lambda col: col.str.casefold())

    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val[1], val[0])
    return df.style.hide(axis="index").format({'Info':make_clickable}).set_properties(**{'text-align':'left','colheader_justify':'left'}).\
            set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])


def conversions(from_form=None, to_form=None, from_form_type=None, to_form_type=None,
                from_viewer=None, to_viewer=None, as_rows='from'):

    if from_viewer is not None or to_viewer is not None:

        from .viewers import viewers_forms

        if from_viewer is not None:
            from_form=viewers_forms[from_viewer]

        if to_viewer is not None:
            to_form=viewers_forms[to_viewer]

    if from_form_type is not None:
        if from_form_type in dict_forms_of_type:
            from_form = dict_forms_of_type[from_form_type]
        else:
            raise BadCallError()

    if to_form_type is not None:
        if to_form_type in dict_forms_of_type:
            to_form = dict_forms_of_type[to_form_type]
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
            if ii in convert_from.keys():
                if jj in convert_from[ii]:
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

    pass

