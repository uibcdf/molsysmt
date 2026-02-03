import pytest
from molsysmt.dependencies import dep_digest
from molsysmt.form import _dict_modules
import molsysmt.config as config
from unittest.mock import patch
import sys
import depdigest

def test_dep_digest_metadata():
    """Verify that @dep_digest attaches metadata correctly."""
    @dep_digest('mdtraj')
    def dummy_func():
        pass
    assert hasattr(dummy_func, '_dependencies')
    assert dummy_func._dependencies[0]['library'] == 'mdtraj'

def test_form_registry_filtering():
    """
    Test that forms are filtered out when show_all_capabilities is False 
    and a dependency is missing.
    """
    from molsysmt import _depdigest
    from depdigest import DepConfig, register_package_config
    
    # Ensure config is registered
    register_package_config('molsysmt', DepConfig(
        libraries=_depdigest.LIBRARIES,
        mapping=_depdigest.MAPPING,
        show_all_capabilities=False,
        exception_class=_depdigest.EXCEPTION_CLASS
    ))

    # Reset registry state
    _dict_modules.clear()
    _dict_modules._initialized = False
    
    # MOCK BOTH SITES where is_installed is used
    with patch('depdigest.core.loader.is_installed', side_effect=lambda x: False if x == 'mdtraj' else True):
        _dict_modules._ensure_initialized()
        assert 'mdtraj.Trajectory' not in _dict_modules
        assert 'molsysmt.MolSys' in _dict_modules

    # Clean up
    register_package_config('molsysmt', DepConfig(
        libraries=_depdigest.LIBRARIES,
        mapping=_depdigest.MAPPING,
        show_all_capabilities=True,
        exception_class=_depdigest.EXCEPTION_CLASS
    ))
    _dict_modules.clear()
    _dict_modules._initialized = False

def test_dep_digest_runtime_error():
    """
    Verify that calling a decorated function without the library raises LibraryNotFoundError.
    """
    from molsysmt._private.exceptions import LibraryNotFoundError
    from depdigest import register_package_config, DepConfig
    
    # Use the actual module name as seen by the decorator
    module_root = __name__.split('.')[0]
    register_package_config(module_root, DepConfig(
        exception_class=LibraryNotFoundError
    ))
    
    @dep_digest('non_existent_library')
    def func_needing_missing_lib():
        pass
        
    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(LibraryNotFoundError) as excinfo:
            func_needing_missing_lib()
        assert "non_existent_library" in str(excinfo.value)

def test_dep_digest_conditional_logic():
    """
    Verify that conditional requirements (when={...}) work correctly.
    """
    from molsysmt._private.exceptions import LibraryNotFoundError
    from depdigest import register_package_config, DepConfig

    module_root = __name__.split('.')[0]
    register_package_config(module_root, DepConfig(
        exception_class=LibraryNotFoundError
    ))

    @dep_digest('openmm', when={'engine': 'OpenMM'})
    def multi_engine_func(engine='NoOpenMM'):
        return "Success"

    with patch('depdigest.core.checker.is_installed', return_value=False):
        assert multi_engine_func(engine='NoOpenMM') == "Success"

    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(LibraryNotFoundError):
            multi_engine_func(engine='OpenMM')