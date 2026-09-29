"""Compare pair-site sparse storage skeletons, excluding scientific metadata.

Run with optional ``--pydata``, ``--torch``, and ``--tensorflow`` flags only
when those packages are available. Reported bytes count numeric payloads,
not Python runtime, dependency imports, input arrays, or inverse indexes.
"""

import argparse
import gc
import json
import platform
import statistics
import time

import numpy as np


def make_events(frames, sites, per_frame, churn):
    rng = np.random.default_rng(251)
    frame = np.repeat(np.arange(frames, dtype=np.int32), per_frame)
    pair = np.empty(frames * per_frame, dtype=np.int32)
    pool = rng.choice(sites * sites, size=400, replace=False).astype(np.int32)
    for f in range(frames):
        start = f * per_frame
        pair[start:start + per_frame] = rng.choice(
            sites * sites if churn else pool,
            size=per_frame, replace=False,
        )
    first = pair // sites
    second = pair % sites
    event_id = np.arange(1, len(pair) + 1, dtype=np.int32)
    return frame, pair, first, second, event_id


def sizes(value):
    if isinstance(value, dict):
        return sum(sizes(item) for item in value.values())
    if isinstance(value, (tuple, list)):
        return sum(sizes(item) for item in value)
    if isinstance(value, np.ndarray):
        return value.nbytes
    return 0


def timed(call, requests):
    call(requests[0])
    samples = []
    for request in requests:
        before = time.perf_counter_ns()
        ids = call(request)
        samples.append((time.perf_counter_ns() - before) / 1e6)
        assert ids.ndim == 1
    return round(statistics.median(samples), 4), round(sorted(samples)[189], 4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--sites", type=int, default=1000)
    parser.add_argument("--per-frame", type=int, default=10)
    parser.add_argument("--churn", action="store_true")
    parser.add_argument("--pydata", action="store_true")
    parser.add_argument("--torch", action="store_true")
    parser.add_argument("--tensorflow", action="store_true")
    args = parser.parse_args()
    if (args.frames < 1 or args.sites < 20 or args.per_frame < 1
            or args.per_frame > 400 or args.frames * args.per_frame >= 2**31
            or args.sites * args.sites >= 2**31):
        parser.error("frames and per-frame must be positive; sites >= 20; "
                     "per-frame <= 400; indices must fit int32")
    frame, pair, first, second, event_id = make_events(
        args.frames, args.sites, args.per_frame, args.churn,
    )
    requests = np.random.default_rng(26).integers(0, args.frames, size=200)
    def expected(f):
        return event_id[frame == f]
    results = {}

    start = time.perf_counter()
    numpy_coo = dict(frame=frame.copy(), first=first.copy(),
                     second=second.copy(), event_id=event_id.copy())
    build = time.perf_counter() - start
    offsets = np.searchsorted(numpy_coo["frame"], np.arange(args.frames + 1))
    def numpy_query(f):
        return numpy_coo["event_id"][offsets[f]:offsets[f + 1]]
    for f in (0, args.frames // 2, args.frames - 1):
        np.testing.assert_array_equal(np.sort(numpy_query(f)), np.sort(expected(f)))
    results["numpy_coo"] = dict(build_s=round(build, 4),
                                payload_bytes=sizes(numpy_coo),
                                frame_index_bytes=offsets.nbytes,
                                frame_query_ms=timed(numpy_query, requests))

    start = time.perf_counter()
    numpy_compressed = dict(
        frame_offsets=np.bincount(frame, minlength=args.frames).cumsum(
            dtype=np.int32
        ),
        pair=pair.copy(), event_id=event_id.copy(),
    )
    numpy_compressed["frame_offsets"] = np.concatenate((
        np.zeros(1, dtype=np.int32), numpy_compressed["frame_offsets"]
    ))
    build = time.perf_counter() - start
    def compressed_query(f):
        start = numpy_compressed["frame_offsets"][f]
        end = numpy_compressed["frame_offsets"][f + 1]
        return numpy_compressed["event_id"][start:end]
    for f in (0, args.frames // 2, args.frames - 1):
        np.testing.assert_array_equal(np.sort(compressed_query(f)),
                                      np.sort(expected(f)))
    results["numpy_compressed_frame_pair"] = dict(
        build_s=round(build, 4), payload_bytes=sizes(numpy_compressed),
        frame_query_ms=timed(compressed_query, requests),
    )

    start = time.perf_counter()
    unique_pair, relation = np.unique(pair, return_inverse=True)
    relation = relation.astype(np.int32)
    numpy_factorized = dict(frame=frame.copy(),
                            pair=unique_pair.astype(np.int32),
                            relation=relation, event_id=event_id.copy())
    build = time.perf_counter() - start
    def factorized_query(f):
        return numpy_factorized["event_id"][offsets[f]:offsets[f + 1]]
    results["numpy_factorized"] = dict(build_s=round(build, 4),
                                       payload_bytes=sizes(numpy_factorized),
                                       frame_index_bytes=offsets.nbytes,
                                       distinct_relations=len(unique_pair),
                                       frame_query_ms=timed(factorized_query, requests))

    start = time.perf_counter()
    compressed_pairs, compressed_relations = np.unique(pair, return_inverse=True)
    numpy_factorized_compressed = dict(
        frame_offsets=numpy_compressed["frame_offsets"].copy(),
        pair=compressed_pairs.astype(np.int32),
        relation=compressed_relations.astype(np.int32),
        event_id=event_id.copy(),
    )
    build = time.perf_counter() - start
    def factorized_compressed_query(f):
        first_event = numpy_factorized_compressed["frame_offsets"][f]
        last_event = numpy_factorized_compressed["frame_offsets"][f + 1]
        return numpy_factorized_compressed["event_id"][first_event:last_event]
    for f in (0, args.frames // 2, args.frames - 1):
        np.testing.assert_array_equal(
            np.sort(factorized_compressed_query(f)), np.sort(expected(f))
        )
    results["numpy_factorized_compressed"] = dict(
        build_s=round(build, 4),
        payload_bytes=sizes(numpy_factorized_compressed),
        distinct_relations=len(compressed_pairs),
        frame_query_ms=timed(factorized_compressed_query, requests),
    )

    import scipy
    from scipy.sparse import csr_array
    start = time.perf_counter()
    csr = csr_array((event_id, (frame, pair)),
                    shape=(args.frames, args.sites * args.sites))
    build = time.perf_counter() - start
    def scipy_query(f):
        return csr.data[csr.indptr[f]:csr.indptr[f + 1]]
    for f in (0, args.frames // 2, args.frames - 1):
        np.testing.assert_array_equal(np.sort(scipy_query(f)), np.sort(expected(f)))
    results["scipy_csr_frame_pair"] = dict(
        version=scipy.__version__, build_s=round(build, 4),
        payload_bytes=csr.data.nbytes + csr.indices.nbytes + csr.indptr.nbytes,
        frame_query_ms=timed(scipy_query, requests),
    )

    coords = np.stack((frame, first, second))
    if args.pydata:
        import sparse
        start = time.perf_counter()
        coo = sparse.COO(coords, event_id,
                         shape=(args.frames, args.sites, args.sites),
                         has_duplicates=False)
        build = time.perf_counter() - start
        def coo_query(f):
            return coo[f].data
        for f in (0, args.frames // 2, args.frames - 1):
            np.testing.assert_array_equal(np.sort(coo_query(f)), np.sort(expected(f)))
        results["pydata_coo"] = dict(
            version=sparse.__version__, build_s=round(build, 4),
            payload_bytes=coo.coords.nbytes + coo.data.nbytes,
            coord_dtype=str(coo.coords.dtype),
            frame_query_ms=timed(coo_query, requests),
        )

        start = time.perf_counter()
        gcxs = sparse.GCXS.from_coo(coo, compressed_axes=(0,))
        build = time.perf_counter() - start
        def gcxs_query(f):
            return gcxs[f].data
        for f in (0, args.frames // 2, args.frames - 1):
            np.testing.assert_array_equal(np.sort(gcxs_query(f)), np.sort(expected(f)))
        results["pydata_gcxs_frame"] = dict(
            version=sparse.__version__, build_s=round(build, 4),
            payload_bytes=gcxs.indptr.nbytes + gcxs.indices.nbytes + gcxs.data.nbytes,
            index_dtype=str(gcxs.indices.dtype),
            frame_query_ms=timed(gcxs_query, requests),
        )
        def gcxs_direct_query(f):
            return gcxs.data[gcxs.indptr[f]:gcxs.indptr[f + 1]]
        for f in (0, args.frames // 2, args.frames - 1):
            np.testing.assert_array_equal(np.sort(gcxs_direct_query(f)),
                                          np.sort(expected(f)))
        results["pydata_gcxs_frame"]["direct_frame_query_ms"] = timed(
            gcxs_direct_query, requests,
        )

    if args.torch:
        import torch
        start = time.perf_counter()
        torch_coo = torch.sparse_coo_tensor(
            torch.from_numpy(coords.astype(np.int64)),
            torch.from_numpy(event_id.copy()),
            size=(args.frames, args.sites, args.sites),
            check_invariants=True,
        ).coalesce()
        build = time.perf_counter() - start
        def torch_query(f):
            return torch.index_select(
                torch_coo, 0, torch.tensor([f], dtype=torch.int64)
            )._values().numpy()
        for f in (0, args.frames // 2, args.frames - 1):
            np.testing.assert_array_equal(np.sort(torch_query(f)),
                                          np.sort(expected(f)))
        torch_offsets = np.searchsorted(
            torch_coo.indices()[0].numpy(), np.arange(args.frames + 1)
        )
        def torch_direct_query(f):
            return torch_coo.values().numpy()[
                torch_offsets[f]:torch_offsets[f + 1]
            ]
        results["torch_coo"] = dict(
            version=torch.__version__, build_s=round(build, 4),
            payload_bytes=(torch_coo.indices().numel() *
                           torch_coo.indices().element_size() +
                           torch_coo.values().numel() *
                           torch_coo.values().element_size()),
            index_dtype=str(torch_coo.indices().dtype),
            frame_query_ms=timed(torch_query, requests),
            direct_frame_query_ms=timed(torch_direct_query, requests),
            direct_frame_index_bytes=torch_offsets.nbytes,
        )

    if args.tensorflow:
        import tensorflow as tf
        start = time.perf_counter()
        tf_coo = tf.sparse.reorder(tf.sparse.SparseTensor(
            indices=np.stack((frame, first, second), axis=1).astype(np.int64),
            values=event_id.copy(),
            dense_shape=(args.frames, args.sites, args.sites),
        ))
        build = time.perf_counter() - start
        def tf_query(f):
            return tf.sparse.slice(
                tf_coo, start=(int(f), 0, 0),
                size=(1, args.sites, args.sites),
            ).values.numpy()
        for f in (0, args.frames // 2, args.frames - 1):
            np.testing.assert_array_equal(np.sort(tf_query(f)),
                                          np.sort(expected(f)))
        def tf_retain_query(f):
            return tf.sparse.retain(
                tf_coo, tf.equal(tf_coo.indices[:, 0], int(f))
            ).values.numpy()
        results["tensorflow_coo"] = dict(
            version=tf.__version__, build_s=round(build, 4),
            payload_bytes=tf_coo.indices.numpy().nbytes +
                          tf_coo.values.numpy().nbytes,
            index_dtype=str(tf_coo.indices.dtype),
            frame_query_ms=timed(tf_query, requests),
            retain_frame_query_ms=timed(tf_retain_query, requests),
        )

    gc.collect()
    print(json.dumps(dict(platform=platform.platform(),
                          python=platform.python_version(), numpy=np.__version__,
                          frames=args.frames, sites=args.sites,
                          events=len(frame), churn=args.churn,
                          comparison=results), indent=2))


if __name__ == "__main__":
    main()
