
def argument_names_standardization(caller, kwargs):

    if caller=='molsysmt.basic.get.get':

        element = kwargs['element']

        if 'name' in kwargs:
            kwargs[element+'_name'] = kwargs.pop('name')
        if 'index' in kwargs:
            kwargs[element+'_index'] = kwargs.pop('index')
        if 'id' in kwargs:
            kwargs[element+'_id'] = kwargs.pop('id')
        if 'type' in kwargs:
            kwargs[element+'_type'] = kwargs.pop('type')
        if 'order' in kwargs:
            kwargs[element+'_order'] = kwargs.pop('order')

    return kwargs
