# Retaining native calculation context in figures

This source contract implements the experimental producer
`molsysmt.figure_observation@1` for consumer B4 / uibcdf/molsysviewer#349 and
the boundary review tracked in uibcdf/molsyssuite#179. Owner integration, the current
covering hosted/installed pair and human acceptance remain separate. It adds
no public scientific detector, result store or mandatory third-party schema.

The private Analysis adapter captures the public native method path, explicitly
forwarded arguments and unprovided signature defaults, observed package versions
and the shape of the declared analysis input. Structural plots retain ordered
populations, requested structures and the explicit reference frame/population.
Selected pair/vector/tuple/extreme/SASA series also identify the selected
projection. Native and displayed units are separate. Full input coordinates,
topology and boxes are not duplicated in plot metadata: preserve those inputs
and any independent reference artifact for reproduction.

Mass-weighted GUI requests read masses through public `physchem.get_mass`,
retain the source definition/unit and forward that exact numeric vector to the
native calculation. Native digestion, admissibility and normalization remain
active; the adapter implements no weighting formula. Expert wrappers retain
their original native delegation. Uniform/default and explicit other arguments
remain native choices. Automatic resource/device defaults are requests, not a
captured execution Context or hardware certificate. Software observations do
not authenticate installed artifact bytes.

One-dimensional integer axes use `ordered_arithmetic_runs@1`: `length` and a
`runs` list of `[start, step, count]`. Expansion appends `start + step*i` for
`i=0..count-1` for each run, in order. Empty axes have no runs; negative steps
and repeated indices are retained. Plain binary64 numeric arguments use
`binary64_hex`; plain floating arrays use `binary64_array_hex@1` with dtype,
shape and flattened hexadecimal values. These encodings do not infer a
physical unit. Other arrays use `ndarray@1` with dtype, shape and recursively
encoded values.

Physical quantities and mass vectors use the existing public PyUnitWizard
`QuantityRecord` with base64 values, explicit semantic fields, unit/SI descriptor,
shape/dtype and seal. This avoids a component-specific quantity codec and keeps
two 105,000-value mass vectors within the core record bounds. Readers use
`QuantityRecord.from_dict(...).to_quantity(field=..., unit=...)` with their own
explicit expectations. Fields are `molsysmt.figure.arguments.<argument>` or
`molsysmt.figure.native_defaults.<argument>`; nested fields follow their key/index
path. Mass records declare `forwarded_as="raw_numeric_weights"` outside the
sealed quantity envelope to identify the actual numeric native call. Bare
numbers never gain an inferred unit from a field name. The provider API remains
provisional and is available at the already required PyUnitWizard 0.28.1 floor.
No population, parameter or reference is shortened to fit the display.

Figures receive detached context. Clearing or replacing a mounted report does
not erase an already adopted core figure; source edits do not recalculate it.
Its declared analysis ID and managed revision establish a recorded relationship,
not authentication or automatic observation of raw edits. Core extraction
preserves the original recipe and maps each new point to its original
observation row. Historical context is separate from current applicability.

On a core runtime without the optional `observations` argument, graphical
figure adoption reports its missing capability and keeps the scientific report
available. It does not drop provenance silently or raise the published native
capability floor to an unpublished Viewer version. Routine source callers must
pin the qualified core contribution; a source pin is not an installed package
qualification. Viewer owns generic JSON validation, persistence and literal
Calculation details; this component owns this scientific producer and its use.

Guards: `tests/molsysviewer_molsysmt/test_figure_observations.py`, existing
Analysis adoption controls, actual Jupyter/both-popup and native Qt receiving.
Scientific native choices and independent numerical controls retain their
separate scope. The current GUI reference remains an explicitly selected frame
and ordered population of the same input; this contract adds no independent
reference loading workflow to the GUI.
