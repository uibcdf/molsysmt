from . import cosolute
from . import ion
from . import lipid
from . import peptide
from . import protein
from . import dna
from . import rna
from . import small_molecule
from . import water

catalog={}
mmtf_translator={}

# cosolute.py

for name in cosolute.name:
    catalog[name]='cosolute'

mmtf_translator.update(cosolute.mmtf_translator)

# ion.py

for name in ion.name:
    catalog[name]='ion'

mmtf_translator.update(ion.mmtf_translator)

#lipid.py

for name in lipid.name:
    catalog[name]='lipid'

mmtf_translator.update(lipid.mmtf_translator)

#peptide.py

for name in peptide.name:
    catalog[name]='peptide'

mmtf_translator.update(peptide.mmtf_translator)

#protein.py

for name in protein.name:
    catalog[name]='protein'

mmtf_translator.update(protein.mmtf_translator)

# rna.py

for name in rna.name:
    catalog[name]='rna'

mmtf_translator.update(rna.mmtf_translator)

# small_molecule.py

for name in small_molecule.name:
    catalog[name]='small molecule'

mmtf_translator.update(small_molecule.mmtf_translator)

# water.py

for name in water.name:
    catalog[name]='water'

mmtf_translator.update(water.mmtf_translator)


del(ion, cosolute, peptide, protein, lipid, dna, rna, small_molecule, water)


