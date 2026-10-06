import pytest
from depdigest import (
    DepConfig,
    dep_digest,
    is_installed,
    register_package_config,
    resolve_config,
)

from molsysmt._private.smonitor import LibraryNotFoundError
from molsysmt.form import _dict_modules


def test_dependencies_architecture(monkeypatch):
    """
    Unified test for dependency management architecture.
    """

    # 1. Test Metadata
    @dep_digest("mdtraj")
    def dummy_func():
        pass

    assert hasattr(dummy_func, "_dependencies")
    assert dummy_func._dependencies[0]["library"] == "mdtraj"

    # Model absent modules at discovery, so both current and older provider
    # loaders use the real dependency checker rather than a loader-local alias.
    from depdigest.core import checker

    from molsysmt import _depdigest

    original_find_spec = checker.find_spec
    original_config = resolve_config("molsysmt")
    module_root = __name__.split(".")[0]
    original_test_config = resolve_config(module_root)

    def missing_spec(name, *args, **kwargs):
        if name in {"mdtraj", "non_existent_lib", "some_lib"}:
            return None
        return original_find_spec(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", missing_spec)
        is_installed.cache_clear()
        register_package_config(
            "molsysmt",
            DepConfig(
                libraries=_depdigest.LIBRARIES,
                mapping=_depdigest.MAPPING,
                show_all_capabilities=False,
                exception_class=LibraryNotFoundError,
            ),
        )
        _dict_modules.clear()
        _dict_modules._initialized = False
        _dict_modules._ensure_initialized()
        assert not is_installed("mdtraj")
        assert "mdtraj.Trajectory" not in _dict_modules
        assert "molsysmt.MolSys" in _dict_modules

        register_package_config(
            module_root, DepConfig(exception_class=LibraryNotFoundError)
        )

        @dep_digest("non_existent_lib")
        def fail_func():
            pass

        with pytest.raises(LibraryNotFoundError):
            fail_func()

        @dep_digest("some_lib", when={"engine": "Special"})
        def cond_func(engine="Normal"):
            return "OK"

        assert cond_func(engine="Normal") == "OK"
        with pytest.raises(LibraryNotFoundError):
            cond_func(engine="Special")
    finally:
        monkeypatch.setattr(checker, "find_spec", original_find_spec)
        is_installed.cache_clear()
        register_package_config("molsysmt", original_config)
        register_package_config(module_root, original_test_config)
        _dict_modules.clear()
        _dict_modules._initialized = False


def test_mmcif_is_registered_as_a_hard_dependency():
    from molsysmt import _depdigest

    assert _depdigest.LIBRARIES["mmcif"] == {
        "type": "hard",
        "pypi": "mmcif",
    }
    assert _depdigest.MAPPING["mmcif_PdbxContainers_DataContainer"] == "mmcif"
    assert _depdigest.MAPPING["file_cif"] == "mmcif"
    assert _depdigest.MAPPING["file_cif_gz"] == "mmcif"
    assert _depdigest.MAPPING["file_bcif"] == "mmcif"
    assert _depdigest.MAPPING["file_bcif_gz"] == "mmcif"
