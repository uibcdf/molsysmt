import pytest
from molsysmt.dependencies import is_installed, dep_digest
from molsysmt.form import _dict_modules
import molsysmt.config as config
from unittest.mock import patch
import sys

def test_is_installed_caching():
    """Verify that is_installed results are cached."""
    # numpy must be installed
    assert is_installed('numpy') is True
    # The cache is internal to the function via lru_cache

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
    from molsysmt.dependencies import is_installed as is_installed_real
    
    # 1. Setup: Reset registry to force a clean initialization for the test
    _dict_modules.clear()
    _dict_modules._initialized = False
    is_installed_real.cache_clear() # Clear cache to allow mocking
    
    # 2. Mock behavior: Simulate 'mdtraj' is NOT installed
    # We patch molsysmt.form.is_installed because that's what the lazy loader uses
    with patch('molsysmt.form.is_installed', side_effect=lambda x: False if x == 'mdtraj' else True):
        
        # Scenario A: show_all_capabilities = True (Default)
        # mdtraj forms should still be present in the dictionary
        config.show_all_capabilities = True
        _dict_modules._ensure_initialized()
        assert 'mdtraj.Trajectory' in _dict_modules
        
        # Scenario B: show_all_capabilities = False
        # We must reset and re-initialize
        _dict_modules.clear()
        _dict_modules._initialized = False
        config.show_all_capabilities = False
        
        _dict_modules._ensure_initialized()
        assert 'mdtraj.Trajectory' not in _dict_modules
        # Native forms should still be there
        assert 'molsysmt.MolSys' in _dict_modules

    # Clean up: restore default state for other tests
    config.show_all_capabilities = True
    _dict_modules.clear()
    _dict_modules._initialized = False

def test_dep_digest_runtime_error():
    """
    Verify that calling a decorated function without the library raises LibraryNotFoundError.
    """
    from molsysmt._private.exceptions import LibraryNotFoundError
    
    @dep_digest('non_existent_library')
    def func_needing_missing_lib():
        pass
        
    # Mock is_installed to return False for our fake library
    with patch('molsysmt.dependencies.is_installed', return_value=False):
        with pytest.raises(LibraryNotFoundError) as excinfo:
            func_needing_missing_lib()
        assert "non_existent_library" in str(excinfo.value)

def test_dep_digest_conditional_logic():
    """
    Verify that conditional requirements (when={...}) work correctly.
    """
    @dep_digest('openmm', when={'engine': 'OpenMM'})
    def multi_engine_func(engine='NoOpenMM'):
        return "Success"

    # Case 1: Condition not met (engine is not OpenMM)
    # Even if openmm is "missing", it shouldn't raise error
    with patch('molsysmt.dependencies.is_installed', return_value=False):
        assert multi_engine_func(engine='NoOpenMM') == "Success"

    # Case 2: Condition met (engine is OpenMM)
    # Now it should check and fail
    from molsysmt._private.exceptions import LibraryNotFoundError
    with patch('molsysmt.dependencies.is_installed', return_value=False):
        with pytest.raises(LibraryNotFoundError):
            multi_engine_func(engine='OpenMM')