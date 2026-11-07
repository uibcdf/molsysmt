# MDAnalysis

Form adapters for MDAnalysis in-memory classes and objects.

MolSysMT supports MDAnalysis **2.8.0 or newer**. This baseline supplies public
NumPy 2-compatible builds and explicit attribute-guessing controls for topology
copies. Copying declared topology does not ask the provider to fill missing
assignments. A provider version must also support your Python interpreter.

For an `MDAnalysis.AtomGroup`, `msm.copy()` duplicates the parent Universe and
returns the same ordered view, retaining unselected parent atoms as context.
This can copy substantially more data than the group represents. Use
`msm.extract()` to materialize a compact system containing only selected atoms
and structures. See {ref}`Tutorial_Form_MDAnalysis_AtomGroup` and
{ref}`Tutorial_Form_MDAnalysis_Universe` for metadata and time-axis limits.

| Class | Description |
| :--- | :--- |
| [AtomGroup](MDAnalysis_AtomGroup.ipynb) | Form adapter for `AtomGroup` |
| [Topology](MDAnalysis_Topology.ipynb) | Form adapter for `Topology` |
| [Universe](MDAnalysis_Universe.ipynb) | Form adapter for `Universe` |
| [topology_PDBParser](MDAnalysis_topology_PDBParser.ipynb) | Form adapter for `topology_PDBParser` |

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   AtomGroup <MDAnalysis_AtomGroup.ipynb>
   Topology <MDAnalysis_Topology.ipynb>
   Universe <MDAnalysis_Universe.ipynb>
   topology_PDBParser <MDAnalysis_topology_PDBParser.ipynb>
```
