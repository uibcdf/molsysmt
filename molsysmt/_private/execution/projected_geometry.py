"""Deliver projected coordinate blocks to geometry reducers under a shared budget."""

from molsysmt._private.smonitor import (
    MemoryBudgetExceededError,
    UnsupportedHeavyOperationError,
)


def execute_projected_geometry(
    source, *, universe, frames, reducer, per_frame_bytes, pbc, heavy_mode, caller
):
    """Choose a declared streaming route or a bounded ordinary-getter route."""
    from molsysmt import configure
    from molsysmt._private.execution import ChunkedExecutor
    from molsysmt._private.execution.memory_policy import decide_mode
    from molsysmt.basic import get, get_form
    from molsysmt.form import _dict_modules

    block_budget = configure.max_ram_usage // 4
    max_chunk_size = min(configure.chunk_size, block_budget // per_frame_bytes)
    if max_chunk_size < 1:
        raise UnsupportedHeavyOperationError(
            operation=caller,
            form="projected geometry blocks",
            reason="One projected coordinate/geometry frame exceeds the block working estimate.",
        )
    mode = decide_mode(per_frame_bytes * len(frames) * 4, heavy_mode)
    if mode == "eager" and per_frame_bytes * len(frames) > block_budget:
        raise MemoryBudgetExceededError(
            reason="Selected eager geometry work exceeds the block budget; use streaming.",
            predicted_bytes=per_frame_bytes * len(frames),
            available_bytes=block_budget,
            caller=caller,
        )
    reducer.metadata["execution"]["execution"] = (
        "chunked" if mode == "heavy" else "eager"
    )
    form = get_form(source)
    attributes = ["coordinates", "box"] if pbc else ["coordinates"]
    if isinstance(form, str) and getattr(_dict_modules[form], "_heavy_support", {}).get(
        "coordinates", False
    ):
        return ChunkedExecutor(
            source,
            form,
            caller,
            reducer=reducer,
            atom_indices=universe,
            structure_indices=frames,
            attributes=attributes,
            heavy_mode="force" if mode == "heavy" else "off",
            max_chunk_size=max_chunk_size,
        ).execute()
    if mode == "heavy":
        raise UnsupportedHeavyOperationError(
            operation=caller,
            form=str(form),
            reason="No streamed coordinate delivery route.",
        )
    reducer.initialize({})
    coordinates = get(
        source, selection=universe, structure_indices=frames, coordinates=True
    )
    box = get(source, structure_indices=frames, box=True) if pbc else None
    reducer.consume(
        ChunkedExecutor._build_chunk(
            {"coordinates": coordinates, "box": box, "structure_indices": frames}
        )
    )
    return reducer.finalize()
