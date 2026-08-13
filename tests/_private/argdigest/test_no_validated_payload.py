from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "molsysmt"


def test_runtime_does_not_depend_on_the_removed_validated_payload_protocol():
    forbidden_fragments = (
        "ValidatedPayload",
        "argdigest.core.contract",
    )
    offenders = {}

    for source_file in PACKAGE_ROOT.rglob("*.py"):
        source = source_file.read_text(encoding="utf-8")
        matches = [fragment for fragment in forbidden_fragments if fragment in source]
        if matches:
            offenders[str(source_file.relative_to(PACKAGE_ROOT))] = matches

    assert offenders == {}
