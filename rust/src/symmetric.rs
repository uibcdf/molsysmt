//! Filling symmetric (self) distance matrices.
//!
//! The natural way to fill an `n x n` symmetric matrix is to store both `out[j][k]`
//! and `out[k][j]` as each pair is computed. That mirror store is a column walk
//! (stride `n * 8` bytes) but, more importantly, it makes the pair loop
//! *unvectorisable*: the compiler cannot emit a vector store for a scattered
//! destination, so the whole inner loop stays scalar no matter how wide the
//! available registers are. Filling the strict upper triangle with unit-stride
//! stores and mirroring afterwards in a cache-blocked pass is both faster on the
//! baseline build and, unlike the interleaved form, able to vectorise.
//!
//! Measured at n = 4000, identical arithmetic, only the store pattern differing:
//!
//! | form | baseline ortho | AVX2 ortho | baseline triclinic | AVX2 triclinic |
//! |---|---|---|---|---|
//! | mirror store per pair | 271 ms | 197 ms | 528 ms | 468 ms |
//! | upper triangle + this pass | 262 ms | 129 ms | 342 ms | 158 ms |
//!
//! See `devguide/pending_proposals/rust_kernel_redesign_beyond_faithful_ports.md`
//! sections 4.D and 4.F.

/// Tile side for the mirror pass. A `TILE x TILE` block and its transpose together
/// are `2 * 64 * 64 * 8 B = 64 KB`, so both stay resident while the block is copied.
const TILE: usize = 64;

/// Mirror the strict upper triangle of a row-major `n x n` matrix onto its strict
/// lower triangle. The diagonal is left untouched.
///
/// Tiled so that each block is transposed while both its source rows and its
/// destination rows are still in cache; the untiled version degenerates into one
/// cache miss per element for large `n`.
pub(crate) fn mirror_upper_to_lower(m: &mut [f64], n: usize) {
    debug_assert_eq!(m.len(), n * n);
    let mut jb = 0;
    while jb < n {
        let jhi = (jb + TILE).min(n);
        let mut kb = jb;
        while kb < n {
            let khi = (kb + TILE).min(n);
            for j in jb..jhi {
                // Skip the part of this tile that lies on or below the diagonal.
                let kstart = if kb <= j { j + 1 } else { kb };
                for k in kstart..khi {
                    m[k * n + j] = m[j * n + k];
                }
            }
            kb += TILE;
        }
        jb += TILE;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The reference: mirror element by element, no tiling.
    fn mirror_naive(m: &mut [f64], n: usize) {
        for j in 0..n {
            for k in (j + 1)..n {
                m[k * n + j] = m[j * n + k];
            }
        }
    }

    fn upper_only(n: usize) -> Vec<f64> {
        let mut m = vec![0.0f64; n * n];
        for j in 0..n {
            for k in (j + 1)..n {
                m[j * n + k] = (j * 31 + k * 7) as f64 * 0.5 + 1.0;
            }
        }
        m
    }

    #[test]
    fn tiled_mirror_matches_the_naive_mirror() {
        // Sizes below, at, and straddling the tile side, including the awkward ones.
        for n in [0usize, 1, 2, 3, 5, 63, 64, 65, 127, 128, 129, 200] {
            let mut tiled = upper_only(n);
            let mut naive = upper_only(n);
            mirror_upper_to_lower(&mut tiled, n);
            mirror_naive(&mut naive, n);
            assert_eq!(tiled, naive, "tiled mirror differs from naive at n={n}");
        }
    }

    #[test]
    fn mirror_is_symmetric_and_preserves_the_diagonal() {
        let n = 129;
        let mut m = upper_only(n);
        for j in 0..n {
            m[j * n + j] = -7.0;
        }
        mirror_upper_to_lower(&mut m, n);
        for j in 0..n {
            assert_eq!(m[j * n + j], -7.0, "diagonal touched at j={j}");
            for k in 0..n {
                assert_eq!(m[j * n + k], m[k * n + j], "asymmetric at ({j},{k})");
            }
        }
    }

    #[test]
    fn mirror_leaves_the_upper_triangle_unchanged() {
        let n = 100;
        let original = upper_only(n);
        let mut m = original.clone();
        mirror_upper_to_lower(&mut m, n);
        for j in 0..n {
            for k in (j + 1)..n {
                assert_eq!(m[j * n + k], original[j * n + k], "upper changed at ({j},{k})");
            }
        }
    }
}
