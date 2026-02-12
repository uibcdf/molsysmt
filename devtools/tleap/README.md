# tLEaP Bootstrap (Temporary Developer Tooling)

This directory documents how to provision `tleap` for local comparison runs
against `engine='MolSysMT'` during development.

This is temporary tooling. The `tleap` path is not part of the long-term
distribution target for MolSysMT 1.0.

## Recommended layout

Keep `AmberClassic` as a sibling repository:

```bash
cd ..
gh repo clone Amber-MD/AmberClassic
```

Expected location:

```text
../AmberClassic
```

## Build and enable `tleap`

From the `molsysmt` repository root:

```bash
bash devtools/tleap/bootstrap_tleap.sh
source ../AmberClassic/AmberClassic.sh
```

Optional build flags can be passed to `configure`:

```bash
bash devtools/tleap/bootstrap_tleap.sh --help
```

## Verify availability

```bash
bash devtools/tleap/check_tleap.sh
```

This verifies:
- `tleap` is found in `PATH`
- a minimal `tleap -f leap.in` run succeeds

## Notes

- If `gh` is not available, use:

```bash
git clone https://github.com/Amber-MD/AmberClassic ../AmberClassic
```

- If you already have an `AmberClassic` clone elsewhere, set:

```bash
export AMBERCLASSIC_DIR=/absolute/path/to/AmberClassic
bash devtools/tleap/bootstrap_tleap.sh
```
