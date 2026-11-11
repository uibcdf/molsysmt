"""Keep the unavailable live-handler copy distinct from supported file copies."""

import hashlib
from pathlib import Path

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.form.molsysmt_H5MSMFileHandler.copy import copy as adapter_copy
from molsysmt.native import H5MSMFileHandler


@pytest.mark.parametrize("direct", [False, True])
@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_unavailable_handler_copy_refuses_without_touching_source_or_destination(
    tmp_path, direct, explicit, skip
):
    source = Path(msm.systems["pentalanine"]["traj_pentalanine.h5msm"])
    original = hashlib.sha256(source.read_bytes()).hexdigest()
    destination = tmp_path / "copy.h5msm"
    kwargs = dict(skip_digestion=skip)
    if explicit:
        kwargs["output_filename"] = destination
    with H5MSMFileHandler(source) as handler:
        source_handle = handler.file
        with pytest.raises(NotImplementedMethodError):
            (adapter_copy if direct else msm.copy)(handler, **kwargs)
        assert handler.file is source_handle and source_handle.id.valid
        assert hashlib.sha256(source.read_bytes()).hexdigest() == original
        assert not destination.exists()
