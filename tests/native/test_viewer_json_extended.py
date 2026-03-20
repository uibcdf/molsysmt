"""
Extended tests for molsysmt.native.viewer_json.ViewerJSON covering uncovered methods:
- copy()
- dumps() with indent
- dump() to file path (plain and gzip)
- dump() to file-like object
- dump() to file-like with gzip raises ArgumentError
"""
import json
import gzip
import pytest
from molsysmt.native.viewer_json import ViewerJSON
from molsysmt._private.smonitor import ArgumentError


@pytest.fixture()
def simple_vjson():
    vj = ViewerJSON()
    vj.data['atoms']['atom_name'] = ['CA', 'CB']
    return vj


def test_copy_is_independent(simple_vjson):
    """copy() returns a deep copy — modifying it does not affect the original."""
    copy = simple_vjson.copy()
    copy.data['atoms']['atom_name'].append('CG')
    assert len(simple_vjson.data['atoms']['atom_name']) == 2
    assert len(copy.data['atoms']['atom_name']) == 3


def test_dumps_returns_valid_json(simple_vjson):
    """dumps() returns a valid JSON string."""
    s = simple_vjson.dumps()
    parsed = json.loads(s)
    assert parsed['atoms']['atom_name'] == ['CA', 'CB']


def test_dumps_with_indent(simple_vjson):
    """dumps(indent=2) returns a pretty-printed JSON string."""
    s = simple_vjson.dumps(indent=2)
    assert '\n' in s
    parsed = json.loads(s)
    assert 'atoms' in parsed


def test_dump_to_plain_file(simple_vjson, tmp_path):
    """dump() to a file path writes valid JSON."""
    out = str(tmp_path / 'out.json')
    simple_vjson.dump(out)
    with open(out) as f:
        parsed = json.load(f)
    assert parsed['atoms']['atom_name'] == ['CA', 'CB']


def test_dump_to_gzip_file(simple_vjson, tmp_path):
    """dump() to a file path with compression='gzip' writes gzipped JSON."""
    out = str(tmp_path / 'out.json.gz')
    simple_vjson.dump(out, compression='gzip')
    with gzip.open(out, 'rt', encoding='utf-8') as f:
        parsed = json.load(f)
    assert parsed['atoms']['atom_name'] == ['CA', 'CB']


def test_dump_to_filelike(simple_vjson, tmp_path):
    """dump() to a file-like object writes valid JSON."""
    out = tmp_path / 'out.json'
    with open(out, 'w') as fp:
        simple_vjson.dump(fp)
    with open(out) as f:
        parsed = json.load(f)
    assert parsed['atoms']['atom_name'] == ['CA', 'CB']


def test_dump_filelike_with_gzip_raises(simple_vjson):
    """dump() to a file-like object with gzip raises ArgumentError."""
    import io
    buf = io.StringIO()
    with pytest.raises(ArgumentError):
        simple_vjson.dump(buf, compression='gzip')
