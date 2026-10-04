from devtools.scripts.validate_public_api_stability import (
    compare_signatures,
)


def test_compare_signatures_detects_parameter_inserted_in_middle():
    old_sig = {
        "pos_args": ["a", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a", "b", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Positional parameters altered" in d for d in diffs)


def test_compare_signatures_detects_default_list_to_tuple():
    old_sig = {
        "pos_args": ["forcefield"],
        "pos_defaults": {"forcefield": "['AMBER99SB-ILDN', 'TIP3P']"},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["forcefield"],
        "pos_defaults": {"forcefield": "('AMBER99SB-ILDN', 'TIP3P')"},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Default value changed for 'forcefield'" in d for d in diffs)


def test_compare_signatures_detects_parameter_added_at_end():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a", "b", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Added positional parameter(s)" in d for d in diffs)


def test_compare_signatures_detects_parameter_dropped():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Dropped positional parameter 'b'" in d for d in diffs)


def test_compare_signatures_detects_order_swap():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["b", "a"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Positional parameters altered" in d for d in diffs)


def test_compare_signatures_identical_passes():
    sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {"b": "None"},
        "kwonly_args": ["c"],
        "kwonly_defaults": {"c": "True"},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(sig, sig, "dummy_fn")
    assert diffs == []


def test_public_signatures_exclude_local_closures_and_qualify_class_methods():
    import ast

    from devtools.scripts.validate_public_api_stability import (
        extract_function_signatures,
    )

    source = """
def calculate(source):
    def table(frame):
        return frame
    class Local:
        def copy(self, value):
            return value
    return source
class First:
    def copy(self, value=None):
        return value
class Second:
    def copy(self, count):
        return count
class _Private:
    def helper(self):
        pass
if True:
    def conditional_public(value):
        pass
"""
    signatures = extract_function_signatures(ast.parse(source))
    assert set(signatures) == {
        "calculate",
        "First.copy",
        "Second.copy",
        "conditional_public",
    }
    assert signatures["First.copy"]["pos_defaults"] == {"value": "None"}
    assert signatures["Second.copy"]["pos_args"] == ["self", "count"]


def test_private_refactor_passes_but_public_parameter_removal_fails(
    tmp_path, monkeypatch
):
    from devtools.scripts import validate_public_api_stability as guard

    private = tmp_path / "molsysmt/_private/charges.py"
    public = tmp_path / "molsysmt/physchem/charges.py"
    private.parent.mkdir(parents=True)
    public.parent.mkdir(parents=True)
    private.write_text("def changed_private_helper(): pass\n")
    public.write_text("def calculate(source): return source\n")
    monkeypatch.setattr(
        guard, "get_changed_python_files", lambda *args: [private, public]
    )
    old = "def calculate(source):\n    def table(frame): return frame\n    return source\n"
    monkeypatch.setattr(guard, "get_git_file_content", lambda *args: old)
    assert guard.validate_api_stability(repo_root=tmp_path)[0] == 0
    public.write_text("def calculate(): return None\n")
    status, messages = guard.validate_api_stability(repo_root=tmp_path)
    assert status == 1
    assert any(
        "Dropped positional parameter 'source'" in message for message in messages
    )
    assert not any(
        "charges.py: Public function 'table'" in message for message in messages
    )


def test_private_module_is_not_frozen_and_public_method_remains_protected(
    tmp_path, monkeypatch
):
    from devtools.scripts import validate_public_api_stability as guard

    private = tmp_path / "molsysmt/topology/_chemical_graph.py"
    public = tmp_path / "molsysmt/native/molsys.py"
    private.parent.mkdir(parents=True)
    public.parent.mkdir(parents=True)
    private.write_text("def renamed_internal(): pass\n")
    public.write_text("class MolSys:\n    def copy(self): pass\n")
    monkeypatch.setattr(
        guard, "get_changed_python_files", lambda *args: [private, public]
    )
    monkeypatch.setattr(
        guard,
        "get_git_file_content",
        lambda ref, path: (
            "def old_helper(value): pass\n"
            if path.endswith("_chemical_graph.py")
            else "class MolSys:\n    def copy(self, value): pass\n"
        ),
    )
    status, messages = guard.validate_api_stability(repo_root=tmp_path)
    assert status == 1
    assert all("_chemical_graph" not in message for message in messages)
    assert any(
        "MolSys.copy" in message and "Dropped positional" in message
        for message in messages
    )
