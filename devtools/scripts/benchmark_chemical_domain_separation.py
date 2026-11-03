"""Compare #255 native/domain paths in independent source-root processes."""

import argparse
import gc
import hashlib
import json
import platform
import resource
import statistics
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--scenario",
        choices=["inventory", "structural", "group_only", "h5msm"],
        required=True,
    )
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--states", type=int, default=1)
    parser.add_argument("--structures", type=int, default=1000)
    parser.add_argument(
        "--partition", choices=["reused", "differing"], default="reused"
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    root = args.source_root.resolve()
    sys.path.insert(0, str(root))
    import h5py
    import numpy as np
    import pandas as pd

    import molsysmt as msm
    from molsysmt.native import MolSys, Topology

    assert Path(msm.__file__).resolve().is_relative_to(root)

    def peak():
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

    def measure(name, operation, check):
        warm = operation()
        check(warm)
        del warm
        timings = []
        before = peak()
        for _ in range(7):
            gc.collect()
            start = time.perf_counter()
            result = operation()
            timings.append(time.perf_counter() - start)
            check(result)
            del result
        return dict(
            operation=name,
            samples_seconds=timings,
            median_seconds=statistics.median(timings),
            minimum_seconds=min(timings),
            maximum_seconds=max(timings),
            peak_rss_before_bytes=before,
            peak_rss_after_bytes=peak(),
        )

    def fixture():
        source = MolSys(n_atoms=args.atoms)
        source.topology.atoms["atom_id"] = pd.array(
            np.arange(args.atoms).astype(str), dtype="string"
        )
        source.topology.atoms["atom_type"] = "C"
        for j in range(args.states):
            if j:
                source.chemical_states.append_state(skip_digestion=True)
            record = source.chemical_states._states[j]
            first = np.arange(args.atoms - 1, dtype=np.int64)
            split = args.partition == "differing" and j % 2 and args.atoms > 2
            if split:
                first = first[first != args.atoms // 2 - 1]
            record.bonds = pd.DataFrame(
                dict(
                    bond_id=pd.array(np.arange(len(first)).astype(str), dtype="string"),
                    atom1_index=first,
                    atom2_index=first + 1,
                    bond_type="covalent",
                )
            )
            record.component_indices = pd.Series(
                np.arange(args.atoms) >= args.atoms // 2
                if split
                else np.zeros(args.atoms),
                dtype="Int64",
            )
            record.components = type(record.components)(n_components=2 if split else 1)
            record.components["component_id"] = pd.array(
                np.arange(len(record.components)).astype(str), dtype="string"
            )
            record.connectivity_completeness = "complete"
            record.component_completeness = "complete"
            record.state_id = f"s-{j}"
        source.chemical_states._set_reference_index(0)
        if args.scenario in {"structural", "h5msm"}:
            xyz = (
                np.arange(args.structures * args.atoms * 3, dtype=np.float64).reshape(
                    args.structures, args.atoms, 3
                )
                * 1e-5
            )
            source.structures.coordinates = msm.pyunitwizard.quantity(xyz, "nm")
            source.structures.time = msm.pyunitwizard.quantity(
                np.arange(args.structures), "ps"
            )
        return source

    results = []
    setup_peak = peak()
    if args.scenario == "group_only":
        source = Topology(n_groups=30, n_chains=3)

        def check_counts(value):
            assert value == [0, 30, 3]

        results.append(
            measure(
                "group_only_counts",
                lambda: source.get(n_atoms=True, n_groups=True, n_chains=True),
                check_counts,
            )
        )
    else:
        source = fixture()
        setup_peak = peak()
        count = args.atoms

        def check_counts(value):
            assert value == [count, 0]

        results.append(
            measure(
                "stable_counts",
                lambda: source.topology.get(n_atoms=True, n_groups=True),
                check_counts,
            )
        )

        def check_topology(value):
            assert value.n_atoms == count
            assert value is not source.topology

        results.append(measure("topology_copy", source.topology.copy, check_topology))
        subset = np.arange(0, count, 2, dtype=np.int64)

        def check_subset(value):
            assert value.n_atoms == len(subset)
            assert value.atoms.atom_id.tolist() == subset.astype(str).tolist()

        results.append(
            measure(
                "topology_extract",
                lambda: source.topology.extract(atom_indices=subset),
                check_subset,
            )
        )
        if args.scenario == "inventory":

            def check_system(value):
                assert value.topology.n_atoms == count
                assert value.chemical_states.n_chemical_states == args.states
                assert value.chemical_states is not source.chemical_states

            results.append(measure("molsys_copy", source.copy, check_system))
        if args.scenario == "structural":
            storage = source.structures._coordinates
            records = list(source.chemical_states._states)
            counter = [0]

            def edit():
                counter[0] += 1
                msm.set(
                    source,
                    element="atom",
                    selection=[0],
                    chemical_state=0,
                    formal_charge=counter[0] % 2,
                )
                return source

            def check_edit(value):
                assert value.structures._coordinates is storage
                assert value.chemical_states.n_chemical_states == args.states
                assert all(
                    "formal_charge" not in record.atom_attributes
                    or record.atom_attributes["formal_charge"].isna().all()
                    for record in value.chemical_states._states[1:]
                )
                assert msm.get(
                    value,
                    element="atom",
                    selection=[0],
                    chemical_state=0,
                    formal_charge=True,
                ) == [counter[0] % 2]

            results.append(measure("chemical_edit_with_coordinates", edit, check_edit))
            results[-1]["unaffected_state_records_shared"] = all(
                a is b for a, b in zip(records[1:], source.chemical_states._states[1:])
            )
            frames = [args.structures - 1, 0]

            def check_extract(value):
                assert value.structures.coordinates.shape == (2, len(subset), 3)
                np.testing.assert_allclose(
                    msm.pyunitwizard.get_value(
                        value.structures.coordinates, to_unit="nm"
                    ),
                    msm.pyunitwizard.get_value(
                        source.structures.coordinates, to_unit="nm"
                    )[frames][:, subset],
                )

            results.append(
                measure(
                    "molsys_extract_two_structures",
                    lambda: source.extract(
                        atom_indices=subset, structure_indices=frames
                    ),
                    check_extract,
                )
            )
        if args.scenario == "h5msm":
            source.interactions = {
                "empty": msm.Interactions.from_records(
                    [],
                    n_atoms=count,
                    n_structures=args.structures,
                    evaluated_structure_indices=[0, args.structures - 1],
                    method="domain_separation_benchmark",
                )
            }
            filename = args.output.with_suffix(".h5msm")
            assert not filename.exists()
            msm.h5msm.write(source, str(filename))

            def check_topology_layer(value):
                assert value["topology"].n_atoms == count
                assert set(value) == {"topology"}

            results.append(
                measure(
                    "h5_topology_layer",
                    lambda: msm.h5msm.read_layers(str(filename), layers=["topology"]),
                    check_topology_layer,
                )
            )
            from molsysmt.form._h5msm05_structures import read_independent_structures

            def read_block():
                with h5py.File(filename) as file:
                    return read_independent_structures(
                        file,
                        structure_indices=[args.structures - 1, 0],
                        atom_indices=[count - 1, 0],
                    )

            def check_block(value):
                assert value.coordinates.shape == (2, 2, 3)
                np.testing.assert_allclose(
                    msm.pyunitwizard.get_value(value.coordinates, to_unit="nm"),
                    msm.pyunitwizard.get_value(
                        source.structures.coordinates, to_unit="nm"
                    )[[args.structures - 1, 0]][:, [count - 1, 0]],
                )

            results.append(
                measure(
                    "h5_nonconsecutive_block_private_codec", read_block, check_block
                )
            )
            results[-1]["file_size_bytes"] = filename.stat().st_size
            filename.unlink()

    source_digest = hashlib.sha256()
    for filename in sorted((root / "molsysmt").rglob("*.py")):
        source_digest.update(str(filename.relative_to(root)).encode())
        source_digest.update(filename.read_bytes())
    with (root / "molsysmt/_rust.abi3.so").open("rb") as extension:
        extension_digest = hashlib.file_digest(extension, "sha256").hexdigest()
    payload = dict(
        schema="molsysmt.chemical-domain-benchmark@1",
        source_root=str(root),
        module=str(Path(msm.__file__).resolve()),
        scenario=args.scenario,
        atoms=args.atoms,
        states=args.states,
        structures=args.structures,
        partition=args.partition,
        python=sys.version,
        platform=platform.platform(),
        numpy=np.__version__,
        pandas=pd.__version__,
        h5py=h5py.__version__,
        warmups=1,
        repetitions=7,
        setup_peak_rss_bytes=setup_peak,
        final_peak_rss_bytes=peak(),
        results=results,
        source_python_sha256=source_digest.hexdigest(),
        native_extension_sha256=extension_digest,
        harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print("BENCHMARK_COMPLETE", args.output, flush=True)


if __name__ == "__main__":
    main()
