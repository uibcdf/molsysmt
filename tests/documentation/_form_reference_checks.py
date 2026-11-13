"""Shared source and rendered-reference checks for explicitly reviewed forms."""

import ast
import importlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
PAGES = Path("docs/content/user/tools/form/class/molsysmt")
_EXTERNAL_CLASS_OPERATIONS = {
    "biopython_Seq": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "biopython_SeqRecord": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "biopython_PDBStructure": {
        "__init__",
        "get_structural_attributes",
        "has_attribute",
        "is_form",
    },
}
_OPERATIONS = {
    "MolSys": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "add_bonds",
        "remove_bonds",
        "get_topological_attributes",
        "get_structural_attributes",
        "get_mechanical_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "Topology": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "Structures": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "MolSysDict": {
        "__init__",
        "extract",
        "copy",
        "get_topological_attributes",
        "get_structural_attributes",
        "has_attribute",
        "is_form",
    },
    "TopologyDict": {
        "__init__",
        "extract",
        "copy",
        "get_topological_attributes",
        "get_structural_attributes",
        "has_attribute",
        "is_form",
    },
    "StructuresDict": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
    "MolecularMechanicsDict": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_mechanical_attributes",
        "set",
        "has_attribute",
        "is_form",
    },
    "MolSysBuilder": {
        "__init__",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "has_attribute",
        "is_form",
    },
    "MolecularMechanics": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_mechanical_attributes",
        "set",
        "has_attribute",
        "is_form",
    },
    "ViewerJSON": {
        "__init__",
        "extract",
        "copy",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "has_attribute",
        "is_form",
    },
    "GROFileHandler": {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "get_topological_attributes",
        "get_structural_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    },
}
_FILE_HOOKS = {
    "__init__",
    "extract",
    "copy",
    "add",
    "merge",
    "append_structures",
    "get_topological_attributes",
    "get_structural_attributes",
    "set",
    "iterators",
    "has_attribute",
    "is_form",
}
_YAML_HOOKS = {
    "__init__",
    "get_topological_attributes",
    "get_structural_attributes",
    "has_attribute",
    "is_form",
}
# Explicitly reviewed file tutorials; adding an adapter does not admit it here.
_FILE_OPERATIONS = {
    "file_bcif": _FILE_HOOKS,
    "file_bcif_gz": _FILE_HOOKS,
    "file_cif": _FILE_HOOKS,
    "file_cif_gz": _FILE_HOOKS,
    "file_crd": _FILE_HOOKS,
    "file_dcd": _FILE_HOOKS,
    "file_fasta": _FILE_HOOKS - {"append_structures"},
    "file_gro": _FILE_HOOKS,
    "file_h5": _FILE_HOOKS,
    "file_h5msm": _FILE_HOOKS,
    "file_inpcrd": _FILE_HOOKS,
    "file_mdcrd": _FILE_HOOKS,
    "file_mol2": _FILE_HOOKS | {"get_mechanical_attributes"},
    "file_molsys_yaml": _YAML_HOOKS,
    "file_pdb": _FILE_HOOKS,
    "file_pir": _FILE_HOOKS - {"append_structures"},
    "file_prmtop": _FILE_HOOKS,
    "file_psf": _FILE_HOOKS | {"get_mechanical_attributes"},
    "file_smi": _FILE_HOOKS - {"append_structures"},
    "file_structures_yaml": _YAML_HOOKS,
    "file_top": _FILE_HOOKS,
    "file_topology_yaml": _YAML_HOOKS,
    "file_trjpk": _YAML_HOOKS | {"to_molsysmt_StructuresDict"},
    "file_xtc": _FILE_HOOKS,
    "file_xyz": _FILE_HOOKS,
    "file_xyznpy": _FILE_HOOKS,
}
_STRING_OPERATIONS = {
    "string_alphafold_id": _FILE_HOOKS,
    "string_amino_acids_1": _FILE_HOOKS,
    "string_amino_acids_3": _FILE_HOOKS,
    "string_pdb_id": _FILE_HOOKS,
    "string_pdb_text": _FILE_HOOKS,
    "string_smiles": _FILE_HOOKS - {"append_structures"},
    "string_uniprot_id": _FILE_HOOKS,
}
_OPENMM_CLASS_OPERATIONS = {
    "openmm_AmberInpcrdFile": _FILE_HOOKS,
    "openmm_AmberPrmtopFile": _FILE_HOOKS,
    "openmm_CharmmCrdFile": _FILE_HOOKS,
    "openmm_CharmmPsfFile": _FILE_HOOKS,
    "openmm_Context": _FILE_HOOKS,
    "openmm_GromacsGroFile": _FILE_HOOKS,
    "openmm_GromacsTopFile": _FILE_HOOKS,
    "openmm_Modeller": _FILE_HOOKS,
    "openmm_PDBFile": _FILE_HOOKS,
    "openmm_Simulation": _FILE_HOOKS,
    "openmm_State": _FILE_HOOKS,
    "openmm_System": _FILE_HOOKS,
    "openmm_Topology": _FILE_HOOKS,
}
_EXTERNAL_CLASS_OPERATIONS.update(_OPENMM_CLASS_OPERATIONS)
_MDTRAJ_CLASS_OPERATIONS = {
    "mdtraj_AmberRestartFile": _FILE_HOOKS,
    "mdtraj_DCDTrajectoryFile": _FILE_HOOKS,
    "mdtraj_GroTrajectoryFile": _FILE_HOOKS,
    "mdtraj_HDF5TrajectoryFile": _FILE_HOOKS,
    "mdtraj_PDBTrajectoryFile": _FILE_HOOKS,
    "mdtraj_Topology": _FILE_HOOKS,
    "mdtraj_Trajectory": _FILE_HOOKS,
    "mdtraj_XTCTrajectoryFile": _FILE_HOOKS,
}
_EXTERNAL_CLASS_OPERATIONS.update(_MDTRAJ_CLASS_OPERATIONS)
_MDANALYSIS_CLASS_OPERATIONS = {
    "MDAnalysis_AtomGroup": _FILE_HOOKS
    - {"add", "merge", "append_structures", "set", "iterators"},
    "MDAnalysis_Topology": _FILE_HOOKS,
    "MDAnalysis_Universe": _FILE_HOOKS,
    "MDAnalysis_topology_PDBParser": _FILE_HOOKS,
}
_EXTERNAL_CLASS_OPERATIONS.update(_MDANALYSIS_CLASS_OPERATIONS)


def _declared_converters(adapter, directory):
    if directory.name not in {
        "file_molsys_yaml",
        "file_structures_yaml",
        "file_topology_yaml",
    }:
        return adapter._convert_to
    # These three reviewed adapters condition their entire registry on PyYAML.
    # Their documentation describes the routes with that prerequisite, even in
    # a source-only receiving environment where the optional engine is absent.
    from depdigest import is_installed

    tree = ast.parse((ROOT / directory / "__init__.py").read_text())
    conditional = [node for node in tree.body if isinstance(node, ast.If)]
    assert len(conditional) == 1
    assert ast.unparse(conditional[0].test) == "is_installed('yaml')"
    assignment = conditional[0].body[0]
    assert isinstance(assignment, ast.Assign)
    assert ast.unparse(assignment.targets[0]) == "_convert_to"
    declarations = ast.literal_eval(assignment.value)
    assert adapter._convert_to == (declarations if is_installed("yaml") else {})
    return declarations


def _assert_native_form_reference_contract(name):
    is_file = name in _FILE_OPERATIONS
    is_string = name in _STRING_OPERATIONS
    is_external = name in _EXTERNAL_CLASS_OPERATIONS
    adapter_name = name if is_file or is_string or is_external else f"molsysmt_{name}"
    if is_file or is_string:
        folder = "file" if is_file else "string"
        page = ROOT / f"docs/content/user/tools/form/{folder}/{name}.ipynb"
        operations = (_FILE_OPERATIONS if is_file else _STRING_OPERATIONS)[name]
    elif is_external:
        owner = name.split("_", 1)[0].lower()
        page = ROOT / f"docs/content/user/tools/form/class/{owner}/{name}.ipynb"
        operations = _EXTERNAL_CLASS_OPERATIONS[name]
    else:
        page = ROOT / PAGES / f"{adapter_name}.ipynb"
        operations = _OPERATIONS[name]
    notebook = json.loads(page.read_text())
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    adapter = importlib.import_module(f"molsysmt.form.{adapter_name}")
    directory = Path(f"molsysmt/form/{adapter_name}")
    converters = _declared_converters(adapter, directory)
    expected = {directory / f"{item}.py" for item in operations}
    converter_files = {
        directory / f"{value if isinstance(value, str) else value.__name__}.py"
        for value in converters.values()
    }
    expected.update(converter_files)
    conversions = "".join(notebook["cells"][4]["source"])
    assert set(re.findall(r"^\| `([^`]+)` \|", conversions, re.M)) == set(converters)
    assert re.findall(
        r"\*\*(\d+) registered direct conversion routes\*\*", conversions
    ) == [str(len(converters))]
    links = re.findall(r"\]\((https://github.com/uibcdf/molsysmt/blob/[^)]+)\)", source)
    observed = set()
    for url in links:
        parsed = urlsplit(url)
        parts = parsed.path.split("/")
        assert re.fullmatch(r"[a-f0-9]{40}", parts[4])
        path = Path(*parts[5:])
        assert path in expected and (ROOT / path).is_file()
        source_lines = (ROOT / path).read_text().splitlines()
        has_content = any(line.strip() for line in source_lines)
        if path in converter_files:
            assert has_content, "An empty module cannot deliver a converter."
            module = importlib.import_module(".".join(path.with_suffix("").parts))
            assert callable(getattr(module, path.stem, None))
        if not source_lines or (not has_content and not parsed.fragment):
            # Truly empty files have no line anchor. Whitespace-only metadata
            # may also link to its header; an existing physical line stays valid.
            assert path.stem in {
                "set",
                "get_topological_attributes",
                "get_structural_attributes",
            }
            assert not parsed.fragment
            observed.add(path)
            continue
        line = re.fullmatch(r"L([1-9][0-9]*)", parsed.fragment)
        assert line is not None
        lineno = int(line[1])
        assert lineno <= len(source_lines)
        if path.stem in {
            "__init__",
            "get_topological_attributes",
            "get_structural_attributes",
            "get_mechanical_attributes",
            "set",
            "iterators",
        }:
            assert lineno == 1
        else:
            definitions = [
                node
                for node in ast.parse((ROOT / path).read_text()).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.lineno == lineno
            ]
            assert len(definitions) == 1 and definitions[0].name == path.stem
            module = importlib.import_module(".".join(path.with_suffix("").parts))
            assert callable(getattr(module, definitions[0].name))
        observed.add(path)
    assert observed == expected
    assert not re.search(
        rf"\{{(?:func|mod)\}}`~?molsysmt\.form\.{adapter_name}", source
    )
    return {
        "name": name,
        "page": page,
        "links": links,
        "source_files": expected,
        "operations": len(operations) - 1,
        "operation_names": operations,
        "converter_files": converter_files,
        "converters": len(converters),
    }


def _assert_rendered_native_form_references(html_root, name):
    from bs4 import BeautifulSoup

    contract = _assert_native_form_reference_contract(name)
    html_root = Path(html_root).resolve()
    page = html_root / contract["page"].relative_to(ROOT / "docs").with_suffix(".html")
    soup = BeautifulSoup(page.read_text(), "html.parser")
    article = soup.select_one("article.bd-article")
    assert article is not None
    hrefs = [node["href"] for node in article.find_all("a", href=True)]
    expected = set(contract["links"])
    assert expected and expected <= set(hrefs), expected - set(hrefs)
    assert sum(href in expected for href in hrefs) == len(contract["links"])
    assert all(
        node.find_parent("a") is not None for node in article.select("code.xref")
    )
    tables = article.find_all("table")
    assert len(tables[1].find_all("a", href=True)) == contract["operations"]
    assert len(tables[2].find_all("a", href=True)) == contract["converters"]
    expected_operations = {
        href
        for href in expected
        if Path(urlsplit(href).path).stem in contract["operation_names"] - {"__init__"}
    }
    assert {
        node["href"] for node in tables[1].find_all("a", href=True)
    } == expected_operations
    assert {node["href"] for node in tables[2].find_all("a", href=True)} == {
        href
        for href in expected
        if Path(*urlsplit(href).path.split("/")[5:]) in contract["converter_files"]
    }
    local = set()
    for href in hrefs:
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            continue
        target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
        if target.is_dir():
            target /= "index.html"
        assert target.is_relative_to(html_root) and target.is_file(), href
        if parsed.fragment:
            target_soup = (
                soup
                if target == page
                else BeautifulSoup(target.read_text(), "html.parser")
            )
            fragment = unquote(parsed.fragment)
            assert target_soup.find(id=fragment) or target_soup.find(
                "a", attrs={"name": fragment}
            ), href
        local.add((str(target.relative_to(html_root)), parsed.fragment))
    return {
        "name": name,
        "expected_reference_occurrences": len(contract["links"]),
        "unique_source_destinations": len(expected),
        "operations": contract["operations"],
        "converters": contract["converters"],
        "local_destinations": len(local),
        "no_unlinked_python_roles": True,
    }
