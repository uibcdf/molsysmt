"""Testing native threading, GIL release, and panic containment."""

from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
import threading

import numpy as np

import molsysmt._rust as rust


def test_long_native_kernel_releases_the_gil():
    """Allow another Python thread to advance during native computation."""

    n_atoms = 2_500
    axis = np.arange(n_atoms, dtype=np.float64)
    coordinates = np.column_stack((axis, axis % 17, axis % 31))
    charges = np.ones(n_atoms, dtype=np.float64)
    ready = threading.Event()
    start = threading.Event()
    stop = threading.Event()
    counter = [0]

    def spin():
        ready.set()
        start.wait()
        while not stop.is_set():
            counter[0] += 1

    worker = threading.Thread(target=spin)
    worker.start()
    ready.wait()
    start.set()
    baseline = counter[0]
    output = rust.coulomb_potential_parallel(coordinates, charges)
    stop.set()
    worker.join()

    assert output.shape == (n_atoms,)
    assert counter[0] > baseline


def test_concurrent_calls_can_use_different_cached_rayon_pools():
    """Run bounded nested parallel work without corrupting native results."""

    rng = np.random.default_rng(20260728)
    coordinates = rng.random((600, 300, 3))
    weights = np.ones(300, dtype=np.float64)
    expected = coordinates.mean(axis=1, keepdims=True)
    thread_counts = (1, 2, 3, 1, 2, 3)

    def calculate(num_threads):
        return np.asarray(rust.get_center(coordinates, weights, num_threads))

    with ThreadPoolExecutor(max_workers=len(thread_counts)) as executor:
        outputs = list(executor.map(calculate, thread_counts))

    for output in outputs:
        np.testing.assert_allclose(output, expected, rtol=1e-14, atol=1e-14)


def test_rust_panic_is_contained_as_a_python_failure():
    """Keep a representative private-binding panic inside the child process."""

    code = (
        "import numpy as np\n"
        "import molsysmt._rust as rust\n"
        "rust.get_center(np.ones((1, 2, 3)), np.ones(1), 1)\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "PanicException" in result.stderr
    assert "panicked at" in result.stderr
