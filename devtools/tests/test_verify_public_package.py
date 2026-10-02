"""Protect actual adoption of the shared, read-only public Conda verifier."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = "uibcdf/molsyssuite/.github/actions/verify-public-conda@399d33a4ee0da148571cba7cfc004e3f3a2e71e7"


def test_workflows_call_the_pinned_common_verifier_and_retain_evidence():
    for workflow in ("promote_conda_package.yaml", "verify_public_conda_package.yaml"):
        data = yaml.safe_load((ROOT / ".github/workflows" / workflow).read_text())
        job = data["jobs"]["promote" if workflow.startswith("promote") else "verify"]
        steps = job["steps"]
        calls = [step for step in steps if step.get("uses") == PROVIDER]
        assert len(calls) == 1
        call = calls[0]
        assert call["id"] == "public_verification"
        assert call["with"] == {"package": "molsysmt", "version": "${{ inputs.version }}",
                                "subdir": "${{ inputs.target }}", "filename": "${{ inputs.filename }}",
                                "sha256": "${{ inputs.sha256 }}"}
        receipts = [step for step in steps if step.get("with", {}).get("path") ==
                    "${{ steps.public_verification.outputs.evidence-path }}"]
        assert len(receipts) == 1
        assert "always()" in receipts[0]["if"]
        assert "outputs.evidence-path != ''" in receipts[0]["if"]
        assert receipts[0]["with"]["if-no-files-found"] == "error"


def test_independent_recheck_has_no_mutation_credentials_or_promotion():
    data = yaml.safe_load((ROOT / ".github/workflows/verify_public_conda_package.yaml").read_text())
    assert data["permissions"] == {"contents": "read"}
    steps = data["jobs"]["verify"]["steps"]
    assert all("/promote@" not in step.get("uses", "") for step in steps)
    assert all("ANACONDA_UIBCDF_TOKEN" not in str(step) for step in steps)
    assert not (ROOT / "devtools/conda-build/verify_public_package.py").exists()


def test_publication_guard_is_pinned_and_runs_without_scientific_jobs():
    data = yaml.load((ROOT / ".github/workflows/check-conda-publication.yml").read_text(), Loader=yaml.BaseLoader)
    assert set(data["on"]) == {"push", "pull_request", "workflow_dispatch"}
    assert data["permissions"] == {"contents": "read"}
    assert data["jobs"] == {"publication": {"uses": "uibcdf/molsyssuite/.github/workflows/check-conda-publication.yaml@2a63a15d67d2e72724b6349e89f9f026b25e860f"}}


def test_promotion_checks_native_cells_and_steps_instead_of_a_job_count():
    import json
    data = yaml.safe_load((ROOT / ".github/workflows/promote_conda_package.yaml").read_text())
    steps = data["jobs"]["promote"]["steps"]
    source = "uibcdf/molsyssuite/.github/actions/verify-installed-matrix@778c918b37a1c2c2fa03ed387a000bff0edf1b3d"
    calls = [step for step in steps if step.get("uses") == source]
    assert len(calls) == 1
    call = calls[0]
    assert call["with"]["candidate-sha"] == "${{ inputs.candidate_sha }}"
    assert call["with"]["run-id"] == "${{ inputs.pair_run_id }}"
    assert call["with"]["title"] == "MT ${{ inputs.version }} build ${{ inputs.build_number }} + Viewer ${{ inputs.molsysviewer_version }} build ${{ inputs.molsysviewer_build_number }} | Python 3.14 | all"
    profile = json.loads(call["with"]["profile"])
    assert profile["platforms"] == ["linux-64", "linux-aarch64", "osx-arm64", "win-64"]
    assert profile["python_versions"] == ["3.11", "3.12", "3.13", "3.14"]
    assert len(profile["required_steps"]) == 4
    assert "--jq .total_count" not in str(steps)
    assert any("always()" in step.get("if", "") and
               "steps.installed_matrix.outputs.evidence-path" in str(step.get("with", {}).get("path", ""))
               for step in steps)
    recheck = yaml.safe_load((ROOT / ".github/workflows/verify_installed_conda_pair.yaml").read_text())
    assert any(step.get("uses") == source for step in recheck["jobs"]["verify"]["steps"])
    assert "ANACONDA_UIBCDF_TOKEN" not in str(recheck)
