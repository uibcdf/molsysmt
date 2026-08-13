"""Structural guards for the published API reference."""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
API_ROOT = REPOSITORY_ROOT / 'docs' / 'api'


def test_published_api_reference_excludes_private_modules():
    assert not any(path.is_file() for path in (API_ROOT / '_private').rglob('*'))

    offenders = []
    for source in API_ROOT.rglob('*'):
        if source.suffix not in {'.md', '.rst'}:
            continue
        if 'molsysmt._private' in source.read_text(encoding='utf-8'):
            offenders.append(source.relative_to(REPOSITORY_ROOT).as_posix())

    assert offenders == []
