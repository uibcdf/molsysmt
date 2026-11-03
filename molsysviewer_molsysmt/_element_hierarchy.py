"""Explicit current-system chain/entity readers; native projections stay independent."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


def _reader_documentation(name, scope, *, local_skip=False):
    def decorate(function):
        function = _native_documentation(name, module=f"element.{scope}")(function)
        function.__doc__ += (
            "\n\nView integration\n----------------\n"
            "Reads the current view.molsys through the serialized molecular reader, "
            "including pending native edits, without scene reconciliation. "
            "Native selection/output-level and redefine_* projection behavior, "
            "containers, IDs, missing values and errors remain unchanged. "
            "The returned projection is not assigned to the molecular system; "
            "there is no update_view control or automatic scene/history change. "
            "A loaded, open owner is required.\n"
        )
        if local_skip:
            function.__doc__ = function.__doc__.replace(
                "\nReturns\n-------",
                "\nskip_digestion : bool, default=False\n"
                "    Keyword-only addon validation control, not forwarded to "
                "the native reader.\n\nReturns\n-------",
                1,
            )
            function.__doc__ += (
                "The native reader has no skip_digestion argument. This local "
                "control never disables its validation.\n"
            )
        return function

    return decorate


class _HierarchyTools:
    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt import element

        native = getattr(getattr(element, self._MODULE), name)
        return self._owner._read(native, parameters)


class _ChainTools(_HierarchyTools):
    _MODULE = "chain"
    _NAMES = ("get_chain_id", "get_chain_index", "get_chain_name", "get_chain_type")

    @_reader_documentation("get_chain_id", "chain")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_chain_id(
        self,
        element="atom",
        selection="all",
        redefine_indices=False,
        redefine_ids=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_chain_id",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_ids": redefine_ids,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_chain_index", "chain")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_chain_index(
        self,
        element="atom",
        selection="all",
        redefine_indices=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_chain_index",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_chain_name", "chain")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_chain_name(
        self,
        element="atom",
        selection="all",
        redefine_indices=False,
        redefine_ids=False,
        redefine_names=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_chain_name",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_ids": redefine_ids,
                "redefine_names": redefine_names,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_chain_type", "chain")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_chain_type(
        self,
        element="atom",
        selection="all",
        redefine_indices=False,
        redefine_types=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_chain_type",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_types": redefine_types,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )


class _EntityTools(_HierarchyTools):
    _MODULE = "entity"
    _NAMES = (
        "get_entity_id",
        "get_entity_index",
        "get_entity_name",
        "get_entity_type",
        "get_n_entities",
    )

    @_reader_documentation("get_entity_id", "entity")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_entity_id(
        self,
        element="entity",
        selection="all",
        redefine_indices=False,
        redefine_ids=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_entity_id",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_ids": redefine_ids,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_entity_index", "entity")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_entity_index(
        self,
        element="entity",
        selection="all",
        redefine_indices=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_entity_index",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_entity_name", "entity")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_entity_name(
        self,
        element="entity",
        selection="all",
        redefine_indices=False,
        redefine_names=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_entity_name",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_names": redefine_names,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_entity_type", "entity")
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_entity_type(
        self,
        element="entity",
        selection="all",
        redefine_indices=False,
        redefine_types=False,
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_entity_type",
            {
                "element": element,
                "selection": selection,
                "redefine_indices": redefine_indices,
                "redefine_types": redefine_types,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_reader_documentation("get_n_entities", "entity", local_skip=True)
    @signal(tags=["addon", "element", "read"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_n_entities(
        self,
        selection="all",
        redefine_entities=False,
        syntax="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_n_entities",
            {
                "selection": selection,
                "redefine_entities": redefine_entities,
                "syntax": syntax,
            },
        )
