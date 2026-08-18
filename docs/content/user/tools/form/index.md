# Form

MolSysMT is built on a form-agnostic architecture capable of ingesting, querying, and converting between dozens of data representations—including native memory containers, third-party library classes, disk file formats, and in-memory text representations.

|      |      |
| :--- | :--- |
| [Class Forms](class/index.md) | In-memory object classes from MolSysMT and external libraries |
| [File Forms](file/index.md) | On-disk file formats (PDB, H5MSM, GRO, CIF, XTC, DCD, etc.) |
| [String Forms](string/index.md) | In-memory string forms (PDB text, sequences, SMILES, IDs) |
| [Get attributes](get_attributes.ipynb) | Querying full attribute dictionaries for forms |
| [Has attribute](has_attribute.ipynb) | Checking specific attribute availability in forms |
| [Is item](is_item.ipynb) | Validating if an object is an instanced item of any form |
| [Is file](is_file.ipynb) | Checking if an item or form names an on-disk file |
| [Is string](is_string.ipynb) | Checking if an item or form names an in-memory string |
| [Close](close.ipynb) | Closing open file handlers and streams for resource forms |

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   class/index.md
   file/index.md
   string/index.md
   get_attributes.ipynb
   has_attribute.ipynb
   is_item.ipynb
   is_file.ipynb
   is_string.ipynb
   close.ipynb
```
