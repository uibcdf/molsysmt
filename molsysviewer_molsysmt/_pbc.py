"""Native box utilities and explicitly received periodic coordinate editors."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _PbcTools:
    _NAMES = (
        "has_pbc",
        "get_lengths_from_box",
        "get_angles_from_box",
        "get_lengths_and_angles_from_box",
        "get_volume_from_box",
        "get_shape_from_box",
        "get_shape_from_angles",
        "get_volume_from_lengths_and_angles",
        "get_box_from_lengths_and_angles",
        "get_box_with_shape",
        "wrap_to_pbc",
        "wrap_to_mic",
        "unwrap",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call_explicit(self, name, parameters):
        from molsysmt import pbc

        self._owner._view()
        return getattr(pbc, name)(**parameters)

    @_native_documentation("has_pbc", module="pbc", bind_primary=True)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def has_pbc(self, skip_digestion=False):
        from molsysmt import pbc

        return self._owner._read(pbc.has_pbc, {"skip_digestion": skip_digestion})

    @_native_documentation("get_lengths_from_box", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_lengths_from_box(self, box, skip_digestion=False):
        return self._call_explicit(
            "get_lengths_from_box", {"box": box, "skip_digestion": skip_digestion}
        )

    @_native_documentation("get_angles_from_box", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_angles_from_box(self, box, skip_digestion=False):
        return self._call_explicit(
            "get_angles_from_box", {"box": box, "skip_digestion": skip_digestion}
        )

    @_native_documentation(
        "get_lengths_and_angles_from_box", module="pbc", bind_primary=False
    )
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_lengths_and_angles_from_box(self, box, skip_digestion=False):
        return self._call_explicit(
            "get_lengths_and_angles_from_box",
            {"box": box, "skip_digestion": skip_digestion},
        )

    @_native_documentation("get_volume_from_box", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_volume_from_box(self, box, *, skip_digestion=False):
        return self._call_explicit("get_volume_from_box", {"box": box})

    @_native_documentation("get_shape_from_box", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_shape_from_box(self, box, skip_digestion=False):
        return self._call_explicit(
            "get_shape_from_box", {"box": box, "skip_digestion": skip_digestion}
        )

    @_native_documentation("get_shape_from_angles", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_shape_from_angles(self, box_angles, skip_digestion=False):
        return self._call_explicit(
            "get_shape_from_angles",
            {"box_angles": box_angles, "skip_digestion": skip_digestion},
        )

    @_native_documentation(
        "get_volume_from_lengths_and_angles", module="pbc", bind_primary=False
    )
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_volume_from_lengths_and_angles(
        self, box_lengths, box_angles, *, skip_digestion=False
    ):
        return self._call_explicit(
            "get_volume_from_lengths_and_angles",
            {"box_lengths": box_lengths, "box_angles": box_angles},
        )

    @_native_documentation(
        "get_box_from_lengths_and_angles", module="pbc", bind_primary=False
    )
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_box_from_lengths_and_angles(
        self, box_lengths, box_angles=None, skip_digestion=False
    ):
        return self._call_explicit(
            "get_box_from_lengths_and_angles",
            {
                "box_lengths": box_lengths,
                "box_angles": box_angles,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_box_with_shape", module="pbc", bind_primary=False)
    @signal(tags=["addon", "pbc"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_box_with_shape(
        self, shape="cubic", length="1 nm", n_structures=1, skip_digestion=False
    ):
        return self._call_explicit(
            "get_box_with_shape",
            {
                "shape": shape,
                "length": length,
                "n_structures": n_structures,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("wrap_to_pbc", module="pbc")
    @signal(tags=["addon", "pbc", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def wrap_to_pbc(
        self,
        selection="all",
        structure_indices="all",
        box_origin="[0,0,0] nanometers",
        box_center=None,
        center_of_selection=None,
        weights=None,
        center_coordinates="[0,0,0] nanometers",
        compact="component",
        syntax="MolSysMT",
        engine="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "wrap_to_pbc",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "box_origin": box_origin,
                "box_center": box_center,
                "center_of_selection": center_of_selection,
                "weights": weights,
                "center_coordinates": center_coordinates,
                "compact": compact,
                "syntax": syntax,
                "engine": engine,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
            module="pbc",
        )

    @_native_documentation("wrap_to_mic", module="pbc")
    @signal(tags=["addon", "pbc", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def wrap_to_mic(
        self,
        selection="all",
        structure_indices="all",
        mic_origin="[0,0,0] nanometers",
        center_of_selection=None,
        center_coordinates="[0,0,0] nanometers",
        weights=None,
        compact="component",
        syntax="MolSysMT",
        engine="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "wrap_to_mic",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "mic_origin": mic_origin,
                "center_of_selection": center_of_selection,
                "center_coordinates": center_coordinates,
                "weights": weights,
                "compact": compact,
                "syntax": syntax,
                "engine": engine,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
            module="pbc",
        )

    @_native_documentation("unwrap", module="pbc")
    @signal(tags=["addon", "pbc", "edit"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def unwrap(
        self,
        selection="all",
        structure_indices="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        in_place=False,
        skip_digestion=False,
        *,
        update_view=True,
    ):
        from ._geometry import _run_geometry_transform

        return _run_geometry_transform(
            self._owner,
            "unwrap",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "syntax": syntax,
                "engine": engine,
                "in_place": in_place,
                "skip_digestion": skip_digestion,
            },
            update_view,
            module="pbc",
        )
