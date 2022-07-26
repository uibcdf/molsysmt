import molsysmt.config as config

import functools
import inspect
from importlib import import_module
import os

from ..functions import invoked_by_user

###

digestion_parameters= {}
digestion_functions = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(current_dir+'/argument'):
    if filename.endswith('.py') and filename!="__init__.py":
        argument = filename[:-3]
        module = import_module('molsysmt._private.digestion.argument.' + argument)
        function = getattr(module, 'digest_'+argument)
        parameters = inspect.getargspec(function)
        digestion_functions[argument]=function
        digestion_parameters[argument]=[]
        for parameter in parameters[0]:
            if parameter not in [argument, 'caller']:
                digestion_parameters[argument].append(parameter)
        del(argument, module, function, parameters)

def digest(output=False, **kwargs):

    digest_parameters = kwargs

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

            skip_digestion = True

            if config.argument_checking:
                if invoked_by_user():
                    skip_digestion = False

            if config.testing:
                skip_digestion = False

            if skip_digestion:
                if output:
                    return digest_output(func(*args, **kwargs))
                else:
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
                            elif parameter in digest_parameters:
                                parameters_dict[parameter] = digest_parameters[parameter]
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
                auxilary_output = func(**digested_args)
                if isinstance(output, (list, tuple)):
                    if len(auxiliary_output) == 1:
                        auxiliary_output = auxiliary_output[0]
                return auxiliary_output
            else:
                return func(**digested_args)

        return wrapper
    return digestor

