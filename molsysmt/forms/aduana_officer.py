# This file is necessary to load only the forms apis compatible with the libraries and modules
# installed in the user python environment.

import os
from importlib.util import find_spec

api_form_name = {}
api_module = {}
api_type = {}
api_dependencies = {}
api_convert_dependencies = {}
api_select_dependencies = {}

modules_already = {'molsysmt', 'numpy', 'pyunitwizard', 'urllib', 'json', 'os'}
modules_required = set()
modules_detected = {}
api_to_be_loaded = {}
converts_to_be_loaded = {}
selects_to_be_loaded = {}

def parser_api(filepath):

    dependencies = set()
    convert = {}
    select = {}

    inside_def = None

    with open(filepath, 'r') as fff:
        for line in fff:

            line = line.lstrip().rstrip()

            if line.startswith('form_name'):
                form_name = line.split('=')[1]

            if line.startswith('def'):
                inside_def = line.split(' ')[1].split('(')[0]
                if inside_def.startswith('to_'):
                    convert[inside_def]=set()
                elif inside_def.startswith('select_with_'):
                    select[inside_def]=set()

            if line.startswith('from ') or line.startswith('import '):
                module_required = line.split(' ')[1]
                if inside_def is None:
                    dependencies.add(module_required)
                elif inside_def.startswith('to_'):
                    convert[inside_def].add(module_required)
                elif inside_def.startswith('select_with_'):
                    select[inside_def].add(module_required)

    tmp_dependencies = set()
    for module in dependencies:
        module = module.split('.')[0]
        if module == 'simtk':
            module = 'simtk.openmm'
        tmp_dependencies.add(module)

    dependencies = tmp_dependencies

    return form_name, dependencies, convert, select

current_dir = os.path.dirname(os.path.abspath(__file__))

for dirname, typename in [['classes', 'class'], ['files', 'file'], ['ids', 'id'], ['seqs', 'seq'], ['viewers', 'viewer']]:

    type_dir = os.path.join(current_dir, dirname)
    list_apis = [filename.split('.')[0] for filename in os.listdir(type_dir) if filename.startswith('api')]

    for api in list_apis:

        form_name, dependencies, convert, select = parser_api(os.path.join(type_dir, api+'.py'))

        api_form_name[api] = form_name
        api_type[api] = typename
        api_module[api] = 'molsysmt.forms.'+dirname+'.'+api
        api_dependencies[api] = dependencies - modules_already
        modules_required.update(api_dependencies[api])
        api_convert_dependencies[api] = convert
        api_select_dependencies[api] = select

# modules detected:
modules_detected = {ii: find_spec(ii) is not None for ii in modules_required}

# apis to be loaded:
for api in api_form_name:
    goes = True
    for dependency in api_dependencies[api]:
        if not modules_detected[dependency]:
            goes = False
            break
    api_to_be_loaded[api] = goes

print(api_to_be_loaded)

# converts to be loaded:
for api in api_to_be_loaded:
    if api_to_be_loaded[api]:
        converts_to_be_loaded[api] = {}
        for method in api_convert_dependencies[api]:

            goes = True
            if 

#print('### Convert')
#print(api_convert_dependencies)
#print(' ')
#print('### Select')
#print(api_select_dependencies)
#print(' ')

