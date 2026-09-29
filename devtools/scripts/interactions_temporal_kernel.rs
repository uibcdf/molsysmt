//! Exploratory temporal-run query kernel for benchmark_interactions_temporal.py.
//! This standalone C ABI is not the MolSysMT production PyO3 interface.

#[no_mangle]
pub unsafe extern "C" fn query_temporal_runs(
    frame: u32,
    block_size: u32,
    n_relations: usize,
    relation_offsets: *const u32,
    run_starts: *const u32,
    run_ends: *const u32,
    measure_starts: *const u32,
    packed_candidates: *const u8,
    bytes_per_block: usize,
    output_relations: *mut u32,
    output_measure_rows: *mut u32,
    output_capacity: usize,
) -> usize {
    if block_size == 0 || output_capacity < n_relations {
        return usize::MAX;
    }
    let block = (frame / block_size) as usize;
    let mut output_len = 0usize;
    for byte_index in 0..bytes_per_block {
        let mut bits = *packed_candidates.add(block * bytes_per_block + byte_index);
        while bits != 0 {
            let bit = bits.trailing_zeros() as usize;
            bits &= bits - 1;
            let relation = byte_index * 8 + bit;
            if relation >= n_relations {
                continue;
            }
            let first = *relation_offsets.add(relation) as usize;
            let last = *relation_offsets.add(relation + 1) as usize;
            let mut low = first;
            let mut high = last;
            while low < high {
                let middle = low + (high - low) / 2;
                if *run_starts.add(middle) <= frame {
                    low = middle + 1;
                } else {
                    high = middle;
                }
            }
            if low > first {
                let run = low - 1;
                if frame < *run_ends.add(run) {
                    *output_relations.add(output_len) = relation as u32;
                    *output_measure_rows.add(output_len) =
                        *measure_starts.add(run) + frame - *run_starts.add(run);
                    output_len += 1;
                }
            }
        }
    }
    output_len
}

#[no_mangle]
pub unsafe extern "C" fn query_temporal_runs_batch(
    frames: *const u32,
    n_frames: usize,
    block_size: u32,
    n_relations: usize,
    relation_offsets: *const u32,
    run_starts: *const u32,
    run_ends: *const u32,
    measure_starts: *const u32,
    packed_candidates: *const u8,
    bytes_per_block: usize,
    output_offsets: *mut u32,
    output_relations: *mut u32,
    output_measure_rows: *mut u32,
    output_capacity: usize,
) -> usize {
    if n_frames
        .checked_mul(n_relations)
        .is_none_or(|needed| output_capacity < needed)
    {
        return usize::MAX;
    }
    *output_offsets = 0;
    let mut total = 0usize;
    for position in 0..n_frames {
        let frame = *frames.add(position);
        let found = query_temporal_runs(
            frame,
            block_size,
            n_relations,
            relation_offsets,
            run_starts,
            run_ends,
            measure_starts,
            packed_candidates,
            bytes_per_block,
            output_relations.add(total),
            output_measure_rows.add(total),
            n_relations,
        );
        if found == usize::MAX {
            return usize::MAX;
        }
        total += found;
        *output_offsets.add(position + 1) = total as u32;
    }
    total
}
