import pytest
from depdigest import is_installed, dep_digest, DepConfig, register_package_config
from molsysmt.form import _dict_modules
import molsysmt.config as config
from unittest.mock import patch
from molsysmt._private.exceptions import LibraryNotFoundError

def test_dependencies_architecture():
    """
    Unified test for dependency management architecture.
    """
    
    # 1. Test Metadata
    @dep_digest('mdtraj')
    def dummy_func():
        pass
    assert hasattr(dummy_func, '_dependencies')
    assert dummy_func._dependencies[0]['library'] == 'mdtraj'

    # 2. Test Registry Filtering
    from molsysmt import _depdigest
    # Mock 'mdtraj' missing and force filtering
    register_package_config('molsysmt', DepConfig(
        libraries=_depdigest.LIBRARIES,
        mapping=_depdigest.MAPPING,
        show_all_capabilities=False,
        exception_class=LibraryNotFoundError
    ))
    _dict_modules.clear()
    _dict_modules._initialized = False
    
    with patch('depdigest.core.loader.is_installed', side_effect=lambda x: False if x == 'mdtraj' else True):
        _dict_modules._ensure_initialized()
        assert 'mdtraj.Trajectory' not in _dict_modules
        assert 'molsysmt.MolSys' in _dict_modules

    # 3. Test Runtime Errors (with correct exception)
    # Register for this module's root
    module_root = __name__.split('.')[0]
    register_package_config(module_root, DepConfig(exception_class=LibraryNotFoundError))
    
    @dep_digest('non_existent_lib')
    def fail_func():
        pass
        
    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(LibraryNotFoundError):
            fail_func()

    # 4. Test Conditional Logic
    @dep_digest('some_lib', when={'engine': 'Special'})
    def cond_func(engine='Normal'):
        return "OK"

    with patch('depdigest.core.checker.is_installed', return_value=False):
        # Should NOT fail when condition is not met
        assert cond_func(engine='Normal') == "OK"
        # Should fail when condition is met
        with pytest.raises(LibraryNotFoundError):
            cond_func(engine='Special')

    # CLEANUP: Restore MolSysMT default config
    register_package_config('molsysmt', DepConfig(
        libraries=_depdigest.LIBRARIES,
        mapping=_depdigest.MAPPING,
        show_all_capabilities=True,
        exception_class=LibraryNotFoundError
    ))
    _dict_modules.clear()
    _dict_modules._initialized = False
