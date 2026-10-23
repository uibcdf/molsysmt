"""Protecting document identity, block reads and independent handler lifetime."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    NotCompatibleConversionError,
)
from molsysmt.native import PDBQTFileHandler
from tests.form.file_pdbqt.test_native_contract import LIGAND, RIGID


def poses(count=5, body=RIGID):
    output = ["REMARK shared document evidence\n"]
    for index in range(count):
        lines = []
        for line in body.splitlines(keepends=True):
            if line.startswith(("ATOM", "HETATM")):
                line = line[:30] + f"{float(line[30:38]) + index * 10:8.3f}" + line[38:]
            lines.append(line)
        output.append(f"MODEL {17 + index * 10}\n" + "".join(lines) + "ENDMDL\n")
    return "".join(output)


def test_metadata_units_order_repetitions_and_snapshot_ownership(tmp_path):
    path = tmp_path / "poses.pdbqt"
    text = poses()
    path.write_text(text)
    with PDBQTFileHandler(path) as handler:
        assert msm.get_form(handler) == "molsysmt.PDBQTFileHandler"
        assert (handler.n_atoms, handler.n_structures) == (4, 5)
        copy = handler.copy()
        assert copy._document is handler._document
        path.write_text("source path replaced after snapshot")
        with msm.pyunitwizard.context(standard_units=["pm"]):
            data = handler.get(
                element="atom",
                selection=[3, 0],
                structure_indices=[4, 1, 4],
                coordinates=True,
            )
        assert data.shape == (3, 2, 3)
        xyz = msm.pyunitwizard.get_value(data, to_unit="nm")
        np.testing.assert_allclose(xyz[:, 1, 0], [4.1, 1.1, 4.1])
        assert msm.get(handler, structure_indices=[4, 1, 4], structure_id=True) == [
            "57",
            "27",
            "57",
        ]
    assert handler.closed and not copy.closed
    assert msm.convert(copy, to_form="string:pdbqt_text") == "pdbqt_text:" + text
    copy.close()
    copy.close()
    with pytest.raises(FormatError, match="closed"):
        copy.get_coordinates()


def test_torsion_tree_is_detached_and_native_loss_is_explicit():
    with PDBQTFileHandler("pdbqt_text:" + poses(2, LIGAND)) as handler:
        tree = handler.get_torsion_tree()
        tree["atom_ids"][0] = "wrong"
        assert handler.get_torsion_tree()["atom_ids"][0] == "17"
        with pytest.raises(FormatError, match="torsion"):
            msm.convert(handler, to_form="molsysmt.MolSys")
        native = msm.convert(
            handler,
            to_form="molsysmt.MolSys",
            discard_torsion_tree=True,
            structure_indices=[1, 0],
        )
        assert native.structures.coordinates.shape == (2, 4, 3)
        assert native.topology.atoms.atom_id.tolist() == ["17", "3", "45", "90"]


@pytest.mark.parametrize("kind", ["handler", "file", "text"])
def test_form_structure_iterator_and_public_facade_preserve_source_axes(kind, tmp_path):
    text = "pdbqt_text:" + poses()
    path = tmp_path / "poses.pdbqt"
    path.write_text(text[len("pdbqt_text:") :])
    handler = PDBQTFileHandler(text)
    source = handler if kind == "handler" else str(path) if kind == "file" else text
    module = msm.form._dict_modules[msm.get_form(source)]
    iterator = module.StructuresIterator(
        source,
        atom_indices=[3, 0],
        structure_indices=[4, 1, 4],
        chunk=2,
        output_type="dictionary",
        coordinates=True,
        structure_index=True,
        structure_id=True,
    )
    blocks = list(iterator)
    assert [b["coordinates"].shape for b in blocks] == [(2, 2, 3), (1, 2, 3)]
    assert [b["structure_index"].tolist() for b in blocks] == [[4, 1], [4]]
    assert [b["structure_id"].tolist() for b in blocks] == [["57", "27"], ["57"]]
    xyz = np.concatenate(
        [msm.pyunitwizard.get_value(b["coordinates"], to_unit="nm") for b in blocks]
    )
    np.testing.assert_allclose(xyz[:, 1, 0], [4.1, 1.1, 4.1])
    assert iterator._handler.closed == (kind != "handler")
    output = [
        msm.pyunitwizard.get_value(v, to_unit="nm").copy()
        for v in msm.Iterator(
            source, coordinates=True, structure_indices=[4, 1, 4], chunk=2
        )
    ]
    assert [v.shape for v in output] == [(2, 4, 3), (1, 4, 3)]
    np.testing.assert_allclose(np.concatenate(output)[:, 0, 0], [4.1, 1.1, 4.1])
    handler.close()


def test_direct_iterator_step_empty_selection_and_early_close():
    from molsysmt.form.string_pdbqt_text.iterators import StructuresIterator

    text = "pdbqt_text:" + poses(9)
    with StructuresIterator(
        text, start=1, stop=8, step=3, chunk=2, structure_index=True
    ) as iterator:
        assert next(iterator).tolist() == [1, 4]
        assert not iterator._handler.closed
    assert iterator._handler.closed
    assert list(StructuresIterator(text, structure_indices=[], coordinates=True)) == []


def test_borrowed_iterator_never_closes_caller_handler_on_failure():
    from molsysmt.form.molsysmt_PDBQTFileHandler.iterators import StructuresIterator

    handler = PDBQTFileHandler("pdbqt_text:" + poses())
    with pytest.raises(ArgumentError):
        StructuresIterator(handler, structure_indices=[99], coordinates=True)
    assert not handler.closed
    iterator = StructuresIterator(handler, coordinates=True)
    iterator.close()
    assert not handler.closed
    handler.close()


def test_current_block_reads_no_other_records_and_no_full_trajectory(
    tmp_path, monkeypatch
):
    path = tmp_path / "many.pdbqt"
    path.write_text(poses(150))
    with PDBQTFileHandler(path) as handler:
        from molsysmt.form.molsysmt_PDBQTFileHandler.iterators import StructuresIterator

        seen = []
        record = handler._document.record

        def tracked(index):
            seen.append(int(index))
            return record(index)

        monkeypatch.setattr(handler._document, "record", tracked)
        iterator = StructuresIterator(
            handler,
            structure_indices=[149, 2, 149],
            chunk=2,
            coordinates=True,
            occupancy=True,
            output_type="dictionary",
        )
        first = next(iterator)
        assert first["coordinates"].shape == (2, 4, 3)
        assert seen == [149, 2]
        iterator.close()
        # Metadata conversion must use only the atom-scale reference record.
        seen.clear()
        msm.convert(handler, to_form="molsysmt.Topology")
        assert seen == []


def test_models_with_changed_molecular_identity_are_rejected():
    text = poses(2)
    second = text.index("MODEL 27")
    with pytest.raises(FormatError, match="identity"):
        PDBQTFileHandler(
            "pdbqt_text:" + text[:second] + text[second:].replace("0.125 C", "0.225 C")
        )


def test_getters_have_shaped_empty_atom_and_structure_axes():
    with PDBQTFileHandler("pdbqt_text:" + poses()) as handler:
        assert handler.get_coordinates(indices=[]).shape == (5, 0, 3)
        assert handler.get_coordinates(structure_indices=[]).shape == (0, 4, 3)
        assert handler.get(structure_indices=[], structure_id=True) == []


def test_handler_user_guide_examples_execute():
    import re
    from pathlib import Path

    page = (
        Path(__file__).parents[2]
        / "docs/content/user/tools/form/class/molsysmt/pdbqt_file_handler.md"
    )
    scope = {}
    for code in re.findall(r"```python\n(.*?)```", page.read_text(), flags=re.S):
        exec(compile(code, str(page), "exec"), scope)
    assert scope["handler"].closed


def test_resident_text_reference_and_independent_native_metadata():
    text = "pdbqt_text:" + poses(3)
    with PDBQTFileHandler(text) as handler:
        assert handler._document._text is text
        projected = msm.convert(handler, to_form="molsysmt.Topology")
        projected.atoms.loc[0, "atom_name"] = "changed"
        assert msm.get(handler, element="atom", atom_name=True)[0] != "changed"
        assert handler.get_coordinates().shape == (3, 4, 3)


def test_optional_structure_observables_can_start_after_first_model():
    text = poses(2)
    split = text.index("MODEL 27")
    first = "\n".join(
        line[:54] + " " * 12 + line[66:]
        if line.startswith(("ATOM", "HETATM"))
        else line
        for line in text[:split].split("\n")
    )
    second = "\n".join(
        line[:54] + f"{0.25:6.2f}{20.0:6.2f}" + line[66:]
        if line.startswith(("ATOM", "HETATM"))
        else line
        for line in text[split:].split("\n")
    )
    with PDBQTFileHandler("pdbqt_text:" + first + second) as handler:
        assert msm.has_attribute(handler, "b_factor")
        assert msm.has_attribute(handler, "occupancy")
        with msm.pyunitwizard.context(standard_units=["pm"]):
            data = handler.get(
                element="atom",
                structure_indices=[1, 0],
                occupancy=True,
                b_factor=True,
                output_type="dictionary",
            )
        np.testing.assert_allclose(data["occupancy"][0], 0.25)
        assert np.isnan(data["occupancy"][1]).all()
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(data["b_factor"], to_unit="nm**2")[0], 0.2
        )
        assert np.isnan(msm.pyunitwizard.get_value(data["b_factor"])[1]).all()


def test_serialized_structure_selection_and_handler_extract_ownership():
    with PDBQTFileHandler("pdbqt_text:" + poses(4)) as handler:
        text = msm.convert(
            handler, to_form="string:pdbqt_text", structure_indices=[3, 1]
        )
        with PDBQTFileHandler(text) as selected:
            assert msm.get(selected, structure_id=True) == ["47", "27"]
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(selected.get_coordinates(), to_unit="nm")[
                    :, 0, 0
                ],
                [3.1, 1.1],
            )
        selected = msm.extract(handler, structure_indices=[2, 0])
        assert selected is not handler
        selected.close()
        assert not handler.closed
        for structures in ([1, 1], []):
            with pytest.raises(FormatError, match="nonempty and unique"):
                msm.convert(
                    handler, to_form="string:pdbqt_text", structure_indices=structures
                )


def test_iterator_releases_owned_snapshot_on_read_failure(monkeypatch):
    from molsysmt.form.string_pdbqt_text.iterators import StructuresIterator

    iterator = StructuresIterator("pdbqt_text:" + poses(3), coordinates=True)

    def broken(index):
        raise FormatError(reason="failed block read")

    monkeypatch.setattr(iterator._handler._document, "record", broken)
    with pytest.raises(FormatError, match="failed block"):
        next(iterator)
    assert iterator.closed and iterator._handler.closed
    assert list(iterator) == []


def test_handler_known_source_pose_read_preserves_order_and_plain_index_contract():
    from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
    from tests.form.file_pdbqt.test_known_source_poses import ensemble, rigid_tree

    source = declared_methanol()
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(source, [1, 0, 5, 4, 3, 2]),
        return_atom_map=True,
    )
    with PDBQTFileHandler(ensemble(text)) as handler:
        out = handler.read_poses(source, mapping, structure_indices=[2, 0, 2])
        assert out.structures.structure_id.tolist() == ["51", "9", "51"]
        expected = np.arange(18).reshape(6, 3) / 10
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(out.structures.coordinates, to_unit="nm"),
            expected[None] + np.asarray([-0.5, 0, -0.5])[:, None, None],
        )
        with pytest.raises(ArgumentError):
            handler.read_poses(
                source,
                mapping,
                structure_indices=msm.pyunitwizard.quantity([0], "dimensionless"),
            )
        assert not handler.closed


def test_handler_conversion_reports_preserve_document_identity_and_report_tree_loss():
    with PDBQTFileHandler("pdbqt_text:" + poses(3, LIGAND)) as handler:
        report = msm.get_conversion_report(handler, to_form="molsysmt.MolSys")
        assert {"pdbqt_torsion_tree", "pdbqt_remarks"} <= {
            i.attribute for i in report.issues
        }
        with pytest.raises(NotCompatibleConversionError):
            msm.convert(
                handler,
                to_form="molsysmt.MolSys",
                discard_torsion_tree=True,
                strict=True,
            )
        text, report = msm.convert(
            handler, to_form="string:pdbqt_text", strict=True, return_report=True
        )
        assert text == "pdbqt_text:" + poses(3, LIGAND)
        assert report.is_exhaustive and not report.issues
        assert not handler.closed


@pytest.mark.parametrize("output_form", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_unmodified_facade_can_yield_native_molecular_system_blocks(output_form):
    with PDBQTFileHandler("pdbqt_text:" + poses(4)) as handler:
        shapes, values = [], []
        for block in msm.Iterator(
            handler, structure_indices=[3, 1, 2], chunk=2, output_form=output_form
        ):
            assert msm.get_form(block) == output_form
            coordinates = msm.get(block, element="atom", coordinates=True)
            shapes.append(coordinates.shape)
            values.extend(
                msm.pyunitwizard.get_value(coordinates, to_unit="nm")[:, 0, 0]
            )
        assert shapes == [(2, 4, 3), (1, 4, 3)]
        np.testing.assert_allclose(values, [3.1, 1.1, 2.1])
        assert not handler.closed
