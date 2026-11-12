from molsysmt._private.argdigest import arg_digest
from molsysmt._private.indices import indices_iterator
from molsysmt._private.smonitor import NotWithThisFormError

_INVENTORY_DIGEST = {
    "digestion_source": "molsysmt._private.argdigest.native_inventory_iterator",
    "digestion_style": "registry",
    "function_source": "molsysmt._private.argdigest.native_inventory_iterator",
    "normalization_source": "molsysmt._private.argdigest.native_inventory_iterator",
}


class TopologyIterator:
    """Iterating selected native inventory values in bounded result chunks.

    Explicit indices select positions on the requested stable element axis,
    preserving order and repetitions. The traversal window applies to those
    selected positions. Values are queried once through the validated native
    get boundary; no coordinates or chemical state is constructed. Query arrays
    and the traversal plan are resident, so this is not an out-of-core reader.
    """

    @arg_digest(form="molsysmt.Topology", **_INVENTORY_DIGEST)
    def __init__(
        self,
        molecular_system,
        element="atom",
        indices="all",
        start=0,
        stop=None,
        step=1,
        chunk=1,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):

        self.molecular_system = molecular_system
        self.element = element
        self.indices = indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.index = 0
        self._output_type = output_type

        if element not in {"atom", "group", "molecule", "chain", "entity"}:
            raise NotWithThisFormError(
                form="molsysmt.Topology", requested_attribute=f"{element}_index"
            )

        # Attribute aliases, Boolean flags and index bounds are validated by the
        # native query boundary. Keep its canonical keys and requested order.
        self._get_result = molecular_system.get(
            element=element,
            selection=indices,
            output_type="dictionary",
            **kwargs,
        )
        self.arguments = list(self._get_result)
        self._output_dictionary = dict.fromkeys(self.arguments)

        if self.arguments:
            selected_count = None
            for attribute, values in self._get_result.items():
                try:
                    count = len(values)
                except TypeError:
                    raise NotWithThisFormError(
                        form="molsysmt.Topology",
                        requested_attribute=attribute,
                        message="Inventory iteration requires one value per selected element.",
                    ) from None
                if selected_count is not None and count != selected_count:
                    raise NotWithThisFormError(
                        form="molsysmt.Topology", requested_attribute=attribute
                    )
                selected_count = count
        else:
            selected_count = len(
                molecular_system.get(element=element, selection=indices, index=True)
            )

        if self.stop is None:
            self.stop = selected_count
        self._indices_iterator = indices_iterator(
            indices=range(selected_count),
            start=self.start,
            stop=self.stop,
            step=self.step,
            chunk=self.chunk,
        )

    def __iter__(self):

        return self

    def __next__(self):
        positions = next(self._indices_iterator)
        if isinstance(positions, int):
            output = {key: self._get_result[key][positions] for key in self.arguments}
        else:
            output = {
                key: [self._get_result[key][index] for index in positions]
                for key in self.arguments
            }
        self._output_dictionary = output
        if self._output_type == "dictionary":
            return output
        values = list(output.values())
        return values[0] if len(values) == 1 else values
