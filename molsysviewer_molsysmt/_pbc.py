"""Native periodic-box readers and factories with explicit scientific inputs."""

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
