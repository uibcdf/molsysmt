"""PDB provenance identifies the imported producer without changing observations."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("version", ["0.23.0", "0+unknown", "1.0.0rc1+" + "a" * 160])
def test_pdb_producer_version_is_actual_and_format_safe(monkeypatch, version):
    source = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    baseline = msm.convert(source, to_form="string:pdb_text")
    monkeypatch.setattr(msm, "__version__", version)
    produced = msm.convert(source, to_form="string:pdb_text")
    remarks = [line for line in produced.splitlines() if line.startswith("REMARK   1 ")]
    prefix = "Created by MolSysMT version "
    pieces = []
    for line in remarks:
        payload = line[11:]
        if payload.startswith(prefix):
            pieces.append(payload[len(prefix) :])
        elif payload.startswith("Version continuation: "):
            pieces.append(payload[len("Version continuation: ") :])
    assert "".join(pieces) == version
    assert all(len(line) <= 80 for line in remarks)
    assert any(line.startswith("REMARK   1 Created on ") for line in remarks)

    def scientific(text):
        return [
            line
            for line in text.splitlines()
            if line.startswith(
                ("ATOM", "HETATM", "CONECT", "CRYST1", "MODEL", "ENDMDL")
            )
        ]

    assert scientific(produced) == scientific(baseline)
