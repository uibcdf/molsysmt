from molsysmt._private.exceptions import *
from molsysmt.api_items import dict_type, dict_convert, dict_info
from molsysmt.api_items import forms as _forms

dict_forms_of_type = { ii:[] for ii in ['class', 'string', 'file']}

for ii, jj in dict_type.items():
    dict_forms_of_type[jj].append(ii)

for ii,jj in dict_forms_of_type.items():
    dict_forms_of_type[ii]=sorted(jj)

convert_from = {}
convert_to = {}

for in_form in dict_convert.keys():
    convert_from[in_form]=dict_convert[in_form].keys()

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
        tmp_output=_forms
    elif form_type in dict_forms_of_type:
        tmp_output=dict_forms_of_type[form_type]
    else:
        raise BadCallError()


    from pandas import DataFrame

    df=DataFrame([[form, dict_type[form], dict_info[form]] for form in tmp_output], columns=['Form', 'Type', 'Info'])
    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val[1], val[0])
    return df.style.hide_index().format({'Info':make_clickable}).set_properties(**{'text-align':'left','colheader_justify':'left'}).\
            set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])


def convert(from_form=None, to_form=None, from_form_type=None, to_form_type=None, as_rows='from'):

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
        from_form = _forms

    if to_form is None:
        to_form = _forms


    from pandas import DataFrame

    dict_df = {}
    false_dict = {ii:False for ii in to_form}
    for ii in from_form:
        dict_df[ii]=false_dict


    for ii in from_form:
        for jj in to_form:
            if jj in convert_from[ii]:
                dict_df[ii][jj]=True

    if as_rows=='from':
        tmp_output = DataFrame.from_dict(dict_df, orient='index')
    elif as_rows=='to':
        tmp_output = DataFrame.from_dict(dict_df)
    else:
        raise BadCallError()


    def color(val):
        if val is False:
            color = '#E2856E'
        else:
            color = '#C2CFB2'
        return 'background-color: %s' % color

    return tmp_output.style.applymap(color).set_properties(**{'text-align': 'center'})


def select():
    pass

def viewers(from_form=None, from_form_type=None, to_viewer=None):

    if to_viewer is None:
        return convert(from_form=from_form, from_form_type=from_form_type, to_form_type='viewer')
    else:
        raise NotImplementedError

