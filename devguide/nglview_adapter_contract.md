# NGLView Adapter Contract

**Status:** normative for the `nglview.NGLWidget` form and MolSysMT's NGLView
integration.

## Instance-dependent coverage

`nglview.NGLWidget` is a visualization container, not a topology type. Its
form declaration describes attributes that an instance may deliver; actual
availability must be determined by the instance-aware `has_attribute()`
adapter.

MolSysMT recognizes the following cases:

1. A single-component widget created through MolSysMT carries an exact private
   topology snapshot.
2. An external widget with a structure string uses the existing PDB fallback
   and therefore exposes only the semantics demonstrable through that route.
3. A coordinate-only or empty widget does not acquire an invented topology.
4. A multicomponent widget does not claim the private snapshot of one
   component as the topology of the complete widget.

## Private topology snapshot

`MolSysMTTrajectory` stores a private copy of the selected native topology.
The snapshot belongs to the trajectory component, not to the global
`NGLWidget` class. It is used only when the widget contains that one component.

This snapshot prevents MolSysMT from discarding information merely because
NGLView consumes PDB text for rendering. It preserves identifiers, hierarchy,
bond order, bond type, and other native topological semantics that PDB cannot
represent faithfully.

The snapshot is isolated from the source molecular system. Mutating the source
after creating the widget must not change a later conversion from the widget.

## External-widget fallback

Widgets without the private snapshot continue through their structure-string
fallback. PDB-derived atom inventory may be available, but the adapter must
not claim `bond_id`, `bond_order`, or `bond_type` as faithfully available from
that route.

The fallback remains useful for ordinary external widgets; the sidecar is an
optional fidelity enhancement, never an assumption about every NGLView
instance.

## Structural information

Coordinates are read from the NGL trajectory itself. A structure string
describes only one structure and cannot provide complete per-structure
metadata for a multi-structure trajectory.

When coordinate count and parsed PDB metadata count differ, MolSysMT retains
the complete coordinate series and discards the partial metadata. It must not
repeat a first-structure identifier, box, B factor, occupancy, or alternate
location across structures without evidence.

## Ordered pair consumers

MolSysMT atom selections are returned in canonical sorted order. NGL helpers
that consume ordered pairs, including group-level hydrogen bonds, must not use
a selection result as a positional permutation of the input pairs. They must
retrieve an aligned complete attribute array and index it with the original
pair order.

## Required evidence

Changes to this adapter require tests covering:

- exact IDs and chemical bond metadata for MolSysMT-created widgets;
- snapshot isolation from later source mutation;
- external PDB widgets without a sidecar;
- empty widgets;
- multicomponent widgets;
- multi-structure coordinates without partial structural metadata;
- group-level hydrogen-bond endpoint order;
- the complete NGLView form, view, get, and helper surface.
