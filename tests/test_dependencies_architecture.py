import pytest
from depdigest import (
    DepConfig,
    dep_digest,
    get_info,
    is_installed,
    register_package_config,
    resolve_config,
    temporary_package_config,
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
        _dict_modules.refresh()
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
        _dict_modules.refresh()


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


@pytest.mark.parametrize(
    ("library", "dependency_type"),
    [("ackredit", "soft"), ("molsysviewer", "hard")],
)
def test_missing_suite_provider_offers_only_its_uibcdf_conda_route(
    monkeypatch, library, dependency_type
):
    from depdigest.core import checker

    from molsysmt._depdigest import LIBRARIES

    metadata = LIBRARIES[library]
    assert metadata == {
        "type": dependency_type,
        "pypi": None,
        "conda": library,
        "channel": "uibcdf",
    }
    monkeypatch.setattr(checker, "is_installed", lambda name: False)

    def operation():
        raise AssertionError("an absent provider must not execute its consumer")

    operation.__module__ = "suite_installation_probe.consumer"
    guarded = dep_digest(library)(operation)
    with temporary_package_config(
        "suite_installation_probe",
        DepConfig(libraries={library: metadata}, exception_class=LibraryNotFoundError),
    ):
        info = get_info("suite_installation_probe", format="dict")["dependencies"][0]
        with pytest.raises(LibraryNotFoundError) as missing:
            guarded()

    command = f"conda install -c uibcdf {library}"
    assert info["installed"] is False
    assert info["package_name"] == {"pypi": None, "conda": library}
    assert info["install"] == {"pypi": None, "conda": command}
    assert command in str(missing.value)
    assert "pip install" not in str(missing.value)
