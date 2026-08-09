"""Testing the dependency contract required by the OpenFF form adapters."""

from pathlib import Path
import tomllib

import yaml

from devtools.scripts.validate_dependencies import (
    OPENFF_TEST_ENV_SPECS,
    SOFT_DEPENDENCIES,
)


REPO = Path(__file__).resolve().parents[1]


def _normalized_conda_dependencies(path):
    payload = yaml.safe_load(path.read_text(encoding='utf-8'))
    return {str(item).replace(' ', '') for item in payload['dependencies']}


def test_openff_runtime_bounds_are_in_ci_and_development_environments():
    for relative_path in (
        'devtools/conda-envs/test_env.yaml',
        'devtools/conda-envs/development_env.yaml',
    ):
        dependencies = _normalized_conda_dependencies(REPO / relative_path)
        assert OPENFF_TEST_ENV_SPECS <= dependencies


def test_openff_runtime_bounds_are_in_the_soft_dependency_extra():
    payload = tomllib.loads((REPO / 'pyproject.toml').read_text(encoding='utf-8'))
    dependencies = {
        item.replace(' ', '')
        for item in payload['project']['optional-dependencies']['soft']
    }

    assert {'openff-toolkit>=0.17.1', 'openff-units>=0.3.0'} <= dependencies


def test_dependency_validator_reads_openff_from_the_normative_registry():
    assert {'openff', 'rdkit'} <= SOFT_DEPENDENCIES
