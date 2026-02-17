#!/usr/bin/env bash
set -euo pipefail

TIER="${1:-smoke}"

run_smoke() {
  pytest -q \
    tests/element/component/test_get_component_index.py \
    tests/topology/get_covalent_blocks/test_get_covalent_blocks_from_molsysmt_MolSys.py \
    tests/pbc/get_lengths_and_angles_from_box/test_get_lengths_and_angles_from_box.py \
    tests/structure/get_rmsd/test_get_rmsd_from_molsysmt_MolSys.py
}

run_build_topology() {
  pytest -q \
    tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py \
    tests/topology/get_bondgraph/test_get_bondgraph_from_molsysmt_MolSys.py \
    tests/topology/get_covalent_chains/test_get_covalent_chains_from_molsysmt_MolSys.py
}

run_peptide_extended() {
  MSM_RUN_EXTENDED_PEPTIDE_PARITY=1 \
    pytest -q tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py
}

case "${TIER}" in
  smoke)
    run_smoke
    ;;
  build_topology)
    run_build_topology
    ;;
  peptide_extended)
    run_peptide_extended
    ;;
  *)
    echo "Unknown tier: ${TIER}"
    echo "Usage: $0 [smoke|build_topology|peptide_extended]"
    exit 2
    ;;
esac
