catalog={}
mmtf_translator={}

# cosolute.py
from molsysmt.elements.entities import cosolute as entity_module

for name in entity_module.name:
    catalog[name]='cosolute'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

# ion.py
from molsysmt.elements.entities import ion as entity_module

for name in entity_module.name:
    catalog[name]='ion'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

#lipid.py
from molsysmt.elements.entities import lipid as entity_module

for name in entity_module.name:
    catalog[name]='lipid'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

#peptide.py
from molsysmt.elements.entities import peptide as entity_module

for name in entity_module.name:
    catalog[name]='peptide'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

#protein.py
from molsysmt.elements.entities import protein as entity_module

for name in entity_module.name:
    catalog[name]='protein'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

# rna.py
from molsysmt.elements.entities import dna as entity_module

for name in entity_module.name:
    catalog[name]='rna'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

# small_molecule.py
from molsysmt.elements.entities import small_molecule as entity_module

for name in entity_module.name:
    catalog[name]='small molecule'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)

# water.py
from molsysmt.elements.entities import water as entity_module

for name in entity_module.name:
    catalog[name]='water'

mmtf_translator.update(entity_module.mmtf_translator)

del(entity_module)






