"""MolSysMT exceptions backed by smonitor catalogs."""

from __future__ import annotations

from ..functions import caller_name
from . import CATALOG
from .emitter import message_from_catalog


class ArgumentError(Exception):
    def __init__(self, argument, value=None, caller=None, message=None, code=None):
        if not caller:
            caller = caller_name()

        default_message = f"Error in {caller} due to the {argument} argument with value {value}."
        if message:
            default_message += f" {message}"

        entry = CATALOG["exceptions"]["ArgumentError"]
        if code:
            # Look up specific entry if code is provided
            for exc_entry in CATALOG["exceptions"].values():
                if exc_entry.get("code") == code:
                    entry = exc_entry
                    break

        full_message = message_from_catalog(
            entry,
            extra={"argument": argument, "value": value, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class IteratorError(Exception):
    def __init__(self, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = "An error was found in the iterator arguments."
        if message:
            default_message += f" {message}"

        full_message = message_from_catalog(
            CATALOG["exceptions"]["IteratorError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class LibraryNotFoundError(Exception):
    def __init__(self, library, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = f"The python library {library} was not found."
        if message:
            default_message += f" {message}"

        full_message = message_from_catalog(
            CATALOG["exceptions"]["LibraryNotFoundError"],
            extra={"library": library, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class MolecularSystemNeededError(Exception):
    def __init__(self, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = (
            f"The function or method {caller} works over a molecular system. "
            f"Either no molecular system or multiple systems were provided."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["MolecularSystemNeededError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class MolecularSystemsNeededError(Exception):
    def __init__(self, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = (
            f"The function or method {caller} works over multiple molecular systems. "
            f"Either no molecular system or a single system was provided."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["MolecularSystemsNeededError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotCompatibleConversionError(Exception):
    def __init__(self, from_form, to_form, missing_arguments, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = (
            f"Error in conversion from {from_form} to {to_form}. "
            f"The following input attributes of arguments are missing: {missing_arguments}."
        )
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotCompatibleConversionError"],
            extra={
                "from_form": from_form,
                "to_form": to_form,
                "missing_arguments": missing_arguments,
                "caller": caller,
            },
            default_message=default_message,
        )

        super().__init__(full_message)


class NotImplementedConversionError(Exception):
    def __init__(self, from_form, to_form, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = f"Error in conversion from {from_form} to {to_form}"
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotImplementedConversionError"],
            extra={"from_form": from_form, "to_form": to_form, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotImplementedIteratorError(Exception):
    def __init__(self, form, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = f"Iterator has not been implemented for form {form}"
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotImplementedIteratorError"],
            extra={"form": form, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotImplementedMethodError(Exception):
    def __init__(self, method=None, arguments=None, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = "This method was not implemented yet."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotImplementedMethodError"],
            extra={"caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotSupportedFormError(Exception):
    def __init__(self, form, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = f"The form {form} used in {caller} is not supported by MolSysMT."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotSupportedFormError"],
            extra={"form": form, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotSupportedSyntaxError(Exception):
    def __init__(self, form, caller=None, message=None):
        if not caller:
            caller = caller_name()

        default_message = f"The syntax {form} used in {caller} is not supported by MolSysMT."
        if message:
            default_message += message

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotSupportedSyntaxError"],
            extra={"syntax": form, "caller": caller},
            default_message=default_message,
        )

        super().__init__(full_message)


class NotWithThisFormError(Exception):
    def __init__(self, caller=None, message=None):
        if not caller:
            caller = caller_name()

        full_message = message_from_catalog(
            CATALOG["exceptions"]["NotWithThisFormError"],
            extra={"caller": caller},
            default_message="",
        )

        super().__init__(full_message)


class FileAlreadyHandledError(Exception):
    def __init__(self, filename=None):
        safe_filename = filename or "<unknown>"
        default_message = f"The file {safe_filename} is already handled by MolSysMT."

        full_message = message_from_catalog(
            CATALOG["exceptions"]["FileAlreadyHandledError"],
            extra={"filename": safe_filename},
            default_message=default_message,
        )

        super().__init__(full_message)


from .warnings import NotDigestedArgumentWarning  # noqa: E402

__all__ = [
    "ArgumentError",
    "IteratorError",
    "LibraryNotFoundError",
    "MolecularSystemNeededError",
    "MolecularSystemsNeededError",
    "NotCompatibleConversionError",
    "NotImplementedConversionError",
    "NotImplementedIteratorError",
    "NotImplementedMethodError",
    "NotSupportedFormError",
    "NotSupportedSyntaxError",
    "NotWithThisFormError",
    "FileAlreadyHandledError",
    "NotDigestedArgumentWarning",
]
