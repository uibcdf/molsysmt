import functools
import inspect
from molsysmt._private.digestion import *

# The following dictionary maps the name of an argument
# to a digestion function. To add a new argument, create a digestion
# function and then put it in this dictionary.

digestion_functions = {
    "box": digest_box,
    "comparison": digest_comparison,
    "coordinates": digest_coordinates,
    "element": digest_element,
    "engine": digest_engine,
    "form": digest_form,
    "indices": digest_indices,
    "item": digest_item,
    "molecular_system": digest_single_molecular_system,
    "molecular_systems": digest_multiple_molecular_systems,
    "output": digest_output,
    "syntaxis": digest_syntaxis,
    "selection": digest_selection,
    "selections": digest_multiple_selections,
    "step": digest_step,
    "time": digest_time,
    "structure_indices": digest_structure_indices,
    "to_form": digest_form,
}


def digest(check_args=True):
    """ Decorator to digest the input arguments of a function, with
        the option to disable argument checking.

        When a function decorated with this decorator is called, its
        arguments will be checked and modified if necessary. If one
        of the arguments doesn't fill the requirements a corresponding
        error will be raised.

        The decorator uses the dictionary defined above which maps the
        name of an argument to a digestion function.


        Parameters
        ----------
        check_args: bool, default=True
            If true, it will digest all arguments passed to the
            decorated function.

    """

    def decorator(func):
        # Use functools to preserve the metadata of the decorated function.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if not check_args:
                return func(*args, **kwargs)

            # Get default arguments
            signature = inspect.signature(func)
            all_args = {
                name: value.default
                for name, value in signature.parameters.items()
                if value.default is not inspect.Parameter.empty
            }

            # Get args, updating if any default arguments were passed by the caller.
            # We also digest those arguments which have a digestion function. If they don't
            # have one, we don't modify them.
            args_names = inspect.getfullargspec(func)[0]
            for ii, argument_name in enumerate(args_names):
                if ii >= len(args):
                    break
                try:
                    digested_value = digestion_functions[argument_name](args[ii])
                except KeyError:
                    digested_value = args[ii]
                all_args[argument_name] = digested_value

            # Get kwargs, updating if any default arguments were passed by the caller
            for argument_name, value in kwargs.items():
                try:
                    digested_value = digestion_functions[argument_name](value)
                except KeyError:
                    digested_value = value
                all_args[argument_name] = digested_value

            return func(**all_args)
        return wrapper
    return decorator
