"""Reporting native capabilities without reading or synchronizing a molecular system."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _SupportedTools:
    _NAMES = ("forms", "conversions", "dependencies", "syntaxes")

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    @_native_documentation("forms", module="supported", bind_primary=False)
    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def forms(self, form_type=None, *, output_type="styler", skip_digestion=False):
        from molsysmt.supported import forms

        self._owner._view()
        return forms(
            form_type=form_type,
            output_type=output_type,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("conversions", module="supported", bind_primary=False)
    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def conversions(
        self,
        from_form=None,
        to_form=None,
        from_form_type=None,
        to_form_type=None,
        from_viewer=None,
        to_viewer=None,
        as_rows="from",
        *,
        output_type="styler",
        skip_digestion=False,
    ):
        from molsysmt.supported import conversions

        self._owner._view()
        return conversions(
            from_form=from_form,
            to_form=to_form,
            from_form_type=from_form_type,
            to_form_type=to_form_type,
            from_viewer=from_viewer,
            to_viewer=to_viewer,
            as_rows=as_rows,
            output_type=output_type,
            skip_digestion=skip_digestion,
        )

    @_native_documentation("dependencies", module="supported", bind_primary=False)
    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def dependencies(self, *, output_type="styler", skip_digestion=False):
        from molsysmt.supported import dependencies

        self._owner._view()
        return dependencies(
            output_type=output_type,
            skip_digestion=skip_digestion,
        )

    # The canonical report keeps an explicit signature even after importing the
    # native callable compatibility module molsysmt.supported.syntaxes.
    @_native_documentation("syntaxes", module="supported.supported", bind_primary=False)
    @signal(tags=["addon", "metadata"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def syntaxes(self, *, output_type="styler", skip_digestion=False):
        from molsysmt.supported import syntaxes

        self._owner._view()
        return syntaxes(
            output_type=output_type,
            skip_digestion=skip_digestion,
        )
