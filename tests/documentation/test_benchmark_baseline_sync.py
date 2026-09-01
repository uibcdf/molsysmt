"""Guards for benchmark data published by the documentation dashboard."""

import json
import re
from pathlib import Path

import pytest


REPOSITORY = Path(__file__).resolve().parents[2]
CANONICAL_DIRECTORY = REPOSITORY / "benchmarks" / "baselines"
PUBLISHED_DIRECTORY = REPOSITORY / "docs" / "_static" / "benchmarks_data"


@pytest.mark.parametrize(
    "filename",
    ["competitor_matrix_session.json", "macro_kernels_session.json"],
)
def test_published_benchmark_data_matches_canonical_baseline(filename):
    canonical = json.loads((CANONICAL_DIRECTORY / filename).read_text())
    published = json.loads((PUBLISHED_DIRECTORY / filename).read_text())

    assert published == canonical


def test_dashboard_competitor_keys_are_delivered_by_the_baseline():
    dashboard = (REPOSITORY / "docs" / "_static" / "benchmarks_dashboard.html").read_text()
    baseline = json.loads(
        (CANONICAL_DIRECTORY / "competitor_matrix_session.json").read_text()
    )
    referenced_keys = set(re.findall(r"data\.(competitor_[a-z0-9_]+)", dashboard))

    assert referenced_keys
    assert referenced_keys <= baseline["results"].keys()
