import molsysmt.config as config

import functools
import inspect
from importlib import import_module

###

digestion_parameters= {}
digestion_functions = {}

def _import_digestion(argument, module, parameters=[]):
    function='digest_'+argument
    import_module(function, module)
    digestion_functions[argument]=getattr(function)
    digestion_parameters[argument]=parameters

## molecular_system
_import_digestion('molecular_system', '.molecular_system')
_import_digestion('multiple_molecular_systems', '.molecular_system')

## item
_import_digestion('item', '.item')

### syntax
_import_digestion('syntax', '.syntax', parameters=['form'])

## selection
_import_digestion('selection', '.selection', parameters=['syntax'])

## element
_import_digestion('element', '.element')

## engine
_import_digestion('engine', '.engine')

## form
_import_digestion('form', '.form')
_import_digestion('to_form', '.form')

## atom
_import_digestion('atom_index', '.atom')
_import_digestion('atom_id', '.atom')
_import_digestion('atom_name', '.atom')
_import_digestion('atom_type', '.atom')
_import_digestion('atom_indices', '.atom')

## group
_import_digestion('group_index', '.group')
_import_digestion('group_id', '.group')
_import_digestion('group_name', '.group')
_import_digestion('group_type', '.group')
_import_digestion('group_indices', '.group')

## component
_import_digestion('component_index', '.component')
_import_digestion('component_id', '.component')
_import_digestion('component_name', '.component')
_import_digestion('component_type', '.component')
_import_digestion('component_indices', '.component')

## molecule
_import_digestion('molecule_index', '.molecule')
_import_digestion('molecule_id', '.molecule')
_import_digestion('molecule_name', '.molecule')
_import_digestion('molecule_type', '.molecule')
_import_digestion('molecule_indices', '.molecule')

## chain
_import_digestion('chain_index', '.chain')
_import_digestion('chain_id', '.chain')
_import_digestion('chain_name', '.chain')
_import_digestion('chain_type', '.chain')
_import_digestion('chain_indices', '.chain')

## entity
_import_digestion('entity_index', '.entity')
_import_digestion('entity_id', '.entity')
_import_digestion('entity_name', '.entity')
_import_digestion('entity_type', '.entity')
_import_digestion('entity_indices', '.entity')

## structure
_import_digestion('structure_indices', '.structure')
_import_digestion('multiple_structure_indices', '.structure')

## coordinates
_import_digestion('coordinates', '.coordinates')

## box
_import_digestion('box', '.box')
_import_digestion('box_lengths', '.box')
_import_digestion('box_angles', '.box')

## step
_import_digestion('step', '.step')

## time
_import_digestion('time', '.time')

## comparison
_import_digestion('comparison', '.comparison')

## viewers
_import_digestion('viewer', '.viewers')

## output
_import_digestion('output', '.output')


def digest(form=None, output=False, test=False, debug=False):

    def digestor(func):
        """ Decorator to digest the input arguments of a function, with
               the option to disable argument checking.

               When a function decorated with this decorator is called, its
               arguments will be checked and modified if necessary. If one
               of the arguments doesn't fill the requirements a corresponding
               error will be raised.

               The decorator uses the dictionary defined above which maps the
               name of an argument to a digestion function.

        """
        # Use functools to preserve the metadata of the decorated function.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if not config.argument_checking:
                return func(*args, **kwargs)

            # Get default arguments
            signature = inspect.signature(func)
            all_args = {
                name: value.default
                for name, value in signature.parameters.items()
                if value.default is not inspect.Parameter.empty
            }

            # Updating if any default arguments were passed by the caller.

            all_args.update(kwargs)

            # Get args, updating if any default arguments were passed by the caller.
            # We also digest those arguments which have a digestion function. If they don't
            # have one, we don't modify them.
            args_names = inspect.getfullargspec(func)[0]
            for argument_value, argument_name in zip(args, args_names):
                all_args[argument_name] = argument_value


            # Digestions:

            digested_args = {}
            not_digested_args = {}

            def gut(arg_name):
                if arg_name not in digested_args:
                    if arg_name in digestion_functions:
                        parameters_dict = {}
                        for parameter in digestion_parameters[arg_name]:
                            if parameter in all_args:
                                gut(parameter)
                                parameters_dict[parameter] = digested_args[parameter]
                            elif parameter in locals():
                                parameters_dict[parameter] = getattr(parameter)
                            else:
                                raise ValueError()
                        digested_args[arg_name] = digestion_functions(all_args[arg_name],
                                                                      caller=func.__name__,
                                                                      **parameters_dict)
                    else:
                        not_digested_args[arg_name] = all_args[arg_name]
                pass

            for arg_name in all_args:
                gut(arg_name)

            for arg_name in not_digested_args:
                print(f'Problem with arg_name {arg_name}')

            if output:
                return digest_output(func(**digested_args))
            else:
                return func(**digested_args)

        return wrapper
    return digestor
