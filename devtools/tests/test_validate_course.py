"""Executable contract for the Four Paths course structure."""

import json
import re
from io import StringIO

import pytest

from devtools.scripts import validate_course


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
        "extensions = ['myst_nb']\nmaster_doc = 'index'\nnb_execution_mode = 'off'\n",
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
    (core / "index.md").write_text(
        (validate_course.COURSE / "Common_Core/index.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
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
        + "   user/foundations/index\n   user/foundations/support/selection_syntaxes\n",
        encoding="utf-8",
    )
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
            if index < len(pages) - 1:
                following = pages[index + 1]
                next_link = re.search(
                    r'Next Module:.*?href="([^"]+)"', rendered, re.DOTALL
                )
                assert next_link is not None
                assert next_link[1].startswith(f"{following.stem}.html")
    finally:
        app.cleanup()
