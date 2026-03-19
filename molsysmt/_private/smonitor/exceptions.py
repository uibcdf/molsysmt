"""MolSysMT exceptions backed by smonitor catalogs."""

from __future__ import annotations

from smonitor.integrations import CatalogException, FormatError as CoreFormatError, InconsistencyError
from ..functions import caller_name
from . import CATALOG, META


class MolSysMTCatalogException(CatalogException):
    def __init__(self, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        if "caller" not in kwargs["extra"]:
            kwargs["extra"]["caller"] = caller_name()

        super().__init__(catalog=CATALOG, meta=META, **kwargs)


class ArgumentError(MolSysMTCatalogException):
    catalog_key = "ArgumentError"

    def __init__(self, argument, value=None, caller=None, message=None, code=None, cause=None):
        extra = {"argument": argument, "value": value}
        if caller:
            extra["caller"] = caller
        
        if cause is not None:
            extra["cause_exception_type"] = type(cause).__name__
            extra["cause_message"] = str(cause)

        super().__init__(message=message, code=code, extra=extra)


class ArgumentChoiceError(MolSysMTCatalogException):
    catalog_key = "ArgumentChoiceError"

    def __init__(self, argument, value, choices, caller=None, message=None):
        extra = {"argument": argument, "value": value, "choices": choices}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class ArgumentLengthError(MolSysMTCatalogException):
    catalog_key = "ArgumentLengthError"

    def __init__(self, argument, expected, actual, caller=None, message=None):
        extra = {"argument": argument, "expected": expected, "actual": actual}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class ArgumentConflictError(MolSysMTCatalogException):
    catalog_key = "ArgumentConflictError"

    def __init__(self, arg1, arg2, reason, caller=None, message=None):
        extra = {"arg1": arg1, "arg2": arg2, "reason": reason}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class StructuralInconsistencyError(InconsistencyError, MolSysMTCatalogException):
    catalog_key = "StructuralInconsistencyError"

    def __init__(self, reason, caller=None, message=None):
        extra = {"reason": reason}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class InternalAlgorithmError(MolSysMTCatalogException):
    catalog_key = "InternalAlgorithmError"

    def __init__(self, reason, caller=None, message=None):
        extra = {"reason": reason}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class IteratorError(MolSysMTCatalogException):
    catalog_key = "IteratorError"

    def __init__(self, caller=None, message=None):
        extra = {}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class LibraryNotFoundError(MolSysMTCatalogException):
    catalog_key = "LibraryNotFoundError"

    def __init__(self, library, caller=None, message=None):
        extra = {"library": library}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class MolecularSystemNeededError(MolSysMTCatalogException):
    catalog_key = "MolecularSystemNeededError"

    def __init__(self, caller=None, message=None):
        extra = {}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class MolecularSystemsNeededError(MolSysMTCatalogException):
    catalog_key = "MolecularSystemsNeededError"

    def __init__(self, caller=None, message=None):
        extra = {}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotCompatibleConversionError(MolSysMTCatalogException):
    catalog_key = "NotCompatibleConversionError"

    def __init__(self, from_form, to_form, missing_arguments, caller=None, message=None):
        extra = {
            "from_form": from_form,
            "to_form": to_form,
            "missing_arguments": missing_arguments,
        }
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotImplementedConversionError(MolSysMTCatalogException):
    catalog_key = "NotImplementedConversionError"

    def __init__(self, from_form, to_form, caller=None, message=None):
        extra = {"from_form": from_form, "to_form": to_form}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotImplementedIteratorError(MolSysMTCatalogException):
    catalog_key = "NotImplementedIteratorError"

    def __init__(self, form, caller=None, message=None):
        extra = {"form": form}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotImplementedMethodError(MolSysMTCatalogException):
    catalog_key = "NotImplementedMethodError"

    def __init__(self, method=None, arguments=None, caller=None, message=None):
        extra = {
            "method": method or "unspecified method",
            "arguments": arguments or "unspecified arguments",
        }
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotSupportedFormError(MolSysMTCatalogException):
    catalog_key = "NotSupportedFormError"

    def __init__(self, form, caller=None, message=None):
        extra = {"form": form}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotSupportedSyntaxError(MolSysMTCatalogException):
    catalog_key = "NotSupportedSyntaxError"

    def __init__(self, syntax, caller=None, message=None):
        extra = {"syntax": syntax}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class NotWithThisFormError(MolSysMTCatalogException):
    catalog_key = "NotWithThisFormError"

    def __init__(self, caller=None, form=None, requested_attribute=None, message=None):
        extra = {}
        if caller:
            extra["caller"] = caller
        if form is not None:
            extra["form"] = form
        if requested_attribute is not None:
            extra["requested_attribute"] = requested_attribute
        super().__init__(message=message, extra=extra)


class FileAlreadyHandledError(MolSysMTCatalogException):
    catalog_key = "FileAlreadyHandledError"

    def __init__(self, filename=None):
        super().__init__(extra={"filename": filename or "<unknown>"})
class FileContentError(MolSysMTCatalogException):
    catalog_key = "FileContentError"

    def __init__(self, reason, caller=None, message=None, record=None, filename=None):
        extra = {"reason": reason}
        if caller:
            extra["caller"] = caller
        if record is not None:
            extra["record"] = record
        if filename is not None:
            extra["filename"] = filename

        super().__init__(message=message, extra=extra)


class FormatError(CoreFormatError, MolSysMTCatalogException):
    catalog_key = "FormatError"

    def __init__(self, reason, caller=None, message=None):
        extra = {"reason": reason}
        if caller:
            extra["caller"] = caller

        super().__init__(message=message, extra=extra)


class UnsupportedHeavyOperationError(MolSysMTCatalogException):
    catalog_key = "UnsupportedHeavyOperationError"

    def __init__(self, operation, form, reason, caller=None, message=None):
        extra = {"operation": operation, "form": form, "reason": reason}
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


class HeavyOutputFailureError(MolSysMTCatalogException):
    catalog_key = "HeavyOutputFailureError"

    def __init__(self, reason, predicted_bytes=None, available_bytes=None, caller=None, message=None):
        extra = {"reason": reason}
        if predicted_bytes is not None:
            extra["predicted_bytes"] = predicted_bytes
        if available_bytes is not None:
            extra["available_bytes"] = available_bytes
        if caller:
            extra["caller"] = caller
        super().__init__(message=message, extra=extra)


from .warnings import NotDigestedArgumentWarning  # noqa: E402

__all__ = [
    "ArgumentError",
    "ArgumentChoiceError",
    "ArgumentLengthError",
    "ArgumentConflictError",
    "StructuralInconsistencyError",
    "InternalAlgorithmError",
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
    "FileContentError",
    "FormatError",
    "NotDigestedArgumentWarning",
    "UnsupportedHeavyOperationError",
    "HeavyOutputFailureError",
]
