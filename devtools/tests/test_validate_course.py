"""Executable contract for the Four Paths course structure."""

import json
import re
import subprocess
import sys
from io import StringIO

import pytest

from devtools.scripts import validate_course

ENTRYPOINTS = (
    "devtools/scripts/validate_course.py",
    "docs/content/course/devtools/validate_course.py",
)


def test_legacy_course_entrypoint_matches_the_maintained_checker(tmp_path):
    results = [
        subprocess.run(
            [sys.executable, str(validate_course.REPO / relative)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        for relative in ENTRYPOINTS
    ]
    assert results[0].returncode == 0, results[0].stderr
    assert "Course structure valid:" in results[0].stdout
    assert results[1].returncode == results[0].returncode, results[1].stdout
    assert results[1].stdout == results[0].stdout
    assert results[1].stderr == results[0].stderr


@pytest.mark.parametrize("relative", ENTRYPOINTS)
def test_course_entrypoint_help_does_not_run_the_checker(relative, tmp_path):
    result = subprocess.run(
        [sys.executable, str(validate_course.REPO / relative), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout
    assert "Course structure valid:" not in result.stdout
    assert "modules compliant" not in result.stdout


@pytest.mark.parametrize("relative", ENTRYPOINTS)
def test_course_entrypoint_rejects_unknown_options(relative, tmp_path):
    result = subprocess.run(
        [sys.executable, str(validate_course.REPO / relative), "--not-a-course-option"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr
    assert "Course structure valid:" not in result.stdout


def test_common_core_identity_and_numbering_are_fully_consolidated():
    assert validate_course.SECTIONS["Common_Core"] == ("core", range(1, 21))
    assert validate_course.main() == 0


def test_common_core_navigation_links_reach_real_module_and_foundations_targets(
    tmp_path,
):
    """Render stored navigation text against stored page labels and curriculum order."""
    pytest.importorskip("myst_nb")
    from sphinx.testing.util import SphinxTestApp

    source = tmp_path / "source"
    core = source / "course/Common_Core"
    core.mkdir(parents=True)
    foundations = source / "user/foundations"
    foundations.mkdir(parents=True)
    pages = sorted(validate_course.notebooks(validate_course.COURSE / "Common_Core"))
    assert len(pages) == 20
    (source / "conf.py").write_text(
        "extensions = ['myst_nb']\nmaster_doc = 'index'\nnb_execution_mode = 'off'\n"
        "source_suffix = {'.rst': 'restructuredtext', '.md': 'myst-nb', '.ipynb': 'myst-nb'}\n",
        encoding="utf-8",
    )
    (foundations / "index.md").write_text(
        "\n".join(
            (validate_course.REPO / "docs/content/user/foundations/index.md")
            .read_text(encoding="utf-8")
            .splitlines()[:2]
        )
        + "\n",
        encoding="utf-8",
    )
    support = foundations / "support"
    support.mkdir()
    (support / "selection_syntaxes.md").write_text(
        "\n".join(
            (
                validate_course.REPO
                / "docs/content/user/foundations/support/selection_syntaxes.md"
            )
            .read_text(encoding="utf-8")
            .splitlines()[:2]
        )
        + "\n",
        encoding="utf-8",
    )
    naming = foundations / "molecular_system/naming_schemes.md"
    naming.parent.mkdir()
    naming.write_text(
        "\n".join(
            (
                validate_course.REPO
                / "docs/content/user/foundations/molecular_system/naming_schemes.md"
            )
            .read_text(encoding="utf-8")
            .splitlines()[:2]
        )
        + "\n",
        encoding="utf-8",
    )
    extra_targets = (
        "user/tools/build/infer_covalent_bonds.md",
        "user/foundations/native_world/file_handlers/molsysmt_GROFileHandler.md",
        "user/foundations/governance/configuration_options.md",
        "user/foundations/governance/precision_and_types.md",
    )
    for relative in extra_targets:
        original = validate_course.REPO / "docs/content" / relative
        header = original.read_text(encoding="utf-8").splitlines()[:2]
        assert header[0].startswith("(") and header[0].endswith(")=")
        assert header[1].startswith("# ")
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(header) + "\n", encoding="utf-8")
    (core / "index.md").write_text(
        (validate_course.COURSE / "Common_Core/index.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    naming_pages = set()
    for page in pages:
        notebook = json.loads(page.read_text(encoding="utf-8"))
        markdown = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        ]
        navigation = [
            line
            for cell in markdown
            for line in cell.splitlines()
            if "{ref}`user-foundations" in line
            or "[Module " in line
            or "{ref}`Module " in line
        ]
        if any("user-foundations-group-naming-schemes" in line for line in navigation):
            naming_pages.add(page.name)
        heading = re.search(r"^# .+$", markdown[0], re.MULTILINE)
        assert heading is not None
        excerpt = markdown[0][: heading.end()] + "\n\n" + "\n\n".join(navigation)
        (core / page.name).write_text(
            json.dumps(
                {
                    "nbformat": 4,
                    "nbformat_minor": 5,
                    "metadata": {},
                    "cells": [
                        {
                            "cell_type": "markdown",
                            "id": "navigation",
                            "metadata": {},
                            "source": excerpt,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
    (source / "index.rst").write_text(
        "Course navigation\n=================\n\n.. toctree::\n\n"
        + "   course/Common_Core/index\n"
        + "   user/foundations/index\n   user/foundations/support/selection_syntaxes\n"
        + "   user/foundations/molecular_system/naming_schemes\n"
        + "".join("   " + path.removesuffix(".md") + "\n" for path in extra_targets),
        encoding="utf-8",
    )
    assert {
        "04_Native_Forms.ipynb",
        "12_Building_Repairing_and_Auditing_Systems.ipynb",
    } <= naming_pages
    warnings = StringIO()
    app = SphinxTestApp(
        srcdir=source,
        builddir=tmp_path,
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
    )
    try:
        app.build(force_all=True)
        assert app.statuscode == 0, warnings.getvalue()
        assert warnings.getvalue() == ""
        for index, page in enumerate(pages):
            rendered = (
                tmp_path / f"html/course/Common_Core/{page.stem}.html"
            ).read_text(encoding="utf-8")
            assert 'href="../../user/foundations/index.html#' in rendered
            if page.name in naming_pages:
                assert (
                    'href="../../user/foundations/molecular_system/naming_schemes.html#user-foundations-group-naming-schemes"'
                    in rendered
                )
            if page.name == "12_Building_Repairing_and_Auditing_Systems.ipynb":
                assert (
                    'href="../../user/tools/build/infer_covalent_bonds.html#tutorial-infer-covalent-bonds"'
                    in rendered
                )
                assert (
                    'href="../../user/foundations/native_world/file_handlers/molsysmt_GROFileHandler.html#user-foundations-native-world-file-handlers-molsysmt-grofilehandler"'
                    in rendered
                )
            if index < len(pages) - 1:
                following = pages[index + 1]
                next_link = re.search(
                    r'Next Module:.*?href="([^"]+)"', rendered, re.DOTALL
                )
                assert next_link is not None
                assert next_link[1].startswith(f"{following.stem}.html")
    finally:
        app.cleanup()
