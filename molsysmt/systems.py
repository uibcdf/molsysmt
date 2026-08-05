import sys
from importlib.resources import files

def path(package, file):
    return files(package).joinpath(file)


class SystemsDict(dict):
    """Custom dictionary for molsysmt.systems holding pre-packaged demo systems and metadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = {}
        self.info = {}


systems = SystemsDict()

# -----------------------------------------------------------------------------
# Dipeptides & Small Peptides
# -----------------------------------------------------------------------------

systems['alanine dipeptide'] = {}
systems['alanine dipeptide']['alanine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'alanine_dipeptide.h5msm')

systems['proline dipeptide'] = {}
systems['proline dipeptide']['proline_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'proline_dipeptide.h5msm')

systems['valine dipeptide'] = {}
systems['valine dipeptide']['valine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'valine_dipeptide.h5msm')

systems['lysine dipeptide'] = {}
systems['lysine dipeptide']['lysine_dipeptide.h5msm'] = path('molsysmt.data.h5msm', 'lysine_dipeptide.h5msm')

systems['pentalanine'] = {}
systems['pentalanine']['pentalanine.inpcrd'] = path('molsysmt.data.inpcrd', 'pentalanine.inpcrd')
systems['pentalanine']['pentalanine.prmtop'] = path('molsysmt.data.prmtop', 'pentalanine.prmtop')
systems['pentalanine']['traj_pentalanine.h5'] = path('molsysmt.data.h5', 'traj_pentalanine.h5')
systems['pentalanine']['traj_pentalanine.h5msm'] = path('molsysmt.data.h5msm', 'traj_pentalanine.h5msm')

systems['Met-enkephalin'] = {}
systems['Met-enkephalin']['met_enkephalin.pdb'] = path('molsysmt.data.pdb', 'met_enkephalin.pdb')
systems['Met-enkephalin']['met_enkephalin.h5msm'] = path('molsysmt.data.h5msm', 'met_enkephalin.h5msm')


# -----------------------------------------------------------------------------
# Small & Globular Proteins
# -----------------------------------------------------------------------------

systems['Trp-Cage'] = {}
systems['Trp-Cage']['1l2y.pdb'] = path('molsysmt.data.pdb', '1l2y.pdb')
systems['Trp-Cage']['1l2y.bcif.gz'] = path('molsysmt.data.bcif_gz', '1l2y.bcif.gz')
systems['Trp-Cage']['1l2y.h5msm'] = path('molsysmt.data.h5msm', '1l2y.h5msm')

systems['chicken villin HP35'] = {}
systems['chicken villin HP35']['1vii.pdb'] = path('molsysmt.data.pdb', '1vii.pdb')
systems['chicken villin HP35']['1vii.bcif.gz'] = path('molsysmt.data.bcif_gz', '1vii.bcif.gz')
systems['chicken villin HP35']['1vii.bcif'] = path('molsysmt.data.bcif', '1vii.bcif')
systems['chicken villin HP35']['chicken_villin_HP35.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35.h5msm')
systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'] = path('molsysmt.data.h5msm', 'chicken_villin_HP35_solvated.h5msm')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'] = path('molsysmt.data.dcd', 'traj_chicken_villin_HP35_solvated.dcd')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5'] = path('molsysmt.data.h5', 'traj_chicken_villin_HP35_solvated.h5')
systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'] = path('molsysmt.data.h5msm', 'traj_chicken_villin_HP35_solvated.h5msm')

systems['T4 lysozyme L99A'] = {}
systems['T4 lysozyme L99A']['181l.pdb'] = path('molsysmt.data.pdb', '181l.pdb')
systems['T4 lysozyme L99A']['181l.bcif.gz'] = path('molsysmt.data.bcif_gz', '181l.bcif.gz')
systems['T4 lysozyme L99A']['181l.h5msm'] = path('molsysmt.data.h5msm', '181l.h5msm')
systems['T4 lysozyme L99A']['1l17.pdb'] = path('molsysmt.data.pdb', '1l17.pdb')
systems['T4 lysozyme L99A']['1l17.h5msm'] = path('molsysmt.data.h5msm', '1l17.h5msm')
systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'] = path('molsysmt.data.h5msm', 't4_lysozyme_L99A.h5msm')

systems['TcTIM'] = {}
systems['TcTIM']['1tcd.pdb'] = path('molsysmt.data.pdb', '1tcd.pdb')
systems['TcTIM']['1tcd.bcif.gz'] = path('molsysmt.data.bcif_gz', '1tcd.bcif.gz')
systems['TcTIM']['1tcd.h5msm'] = path('molsysmt.data.h5msm', '1tcd.h5msm')

systems['Hexokinase 2'] = {}
systems['Hexokinase 2']['2nzt.bcif.gz'] = path('molsysmt.data.bcif_gz', '2nzt.bcif.gz')
systems['Hexokinase 2']['2nzt.h5msm'] = path('molsysmt.data.h5msm', '2nzt.h5msm')


# -----------------------------------------------------------------------------
# Complexes & Large Assemblies
# -----------------------------------------------------------------------------

systems['Barnase-Barstar'] = {}
systems['Barnase-Barstar']['barnase_barstar.h5msm'] = path('molsysmt.data.h5msm', 'barnase_barstar.h5msm')
systems['Barnase-Barstar']['1brs.bcif'] = path('molsysmt.data.bcif', '1brs.bcif')
systems['Barnase-Barstar']['1brs.bcif.gz'] = path('molsysmt.data.bcif_gz', '1brs.bcif.gz')
systems['Barnase-Barstar']['1brs.h5msm'] = path('molsysmt.data.h5msm', '1brs.h5msm')

systems['1YCR'] = {}
systems['1YCR']['1ycr.pdb'] = path('molsysmt.data.pdb', '1ycr.pdb')
systems['1YCR']['1ycr.bcif.gz'] = path('molsysmt.data.bcif_gz', '1ycr.bcif.gz')

systems['1ATP'] = {}
systems['1ATP']['1atp.pdb'] = path('molsysmt.data.pdb', '1atp.pdb')
systems['1ATP']['1atp.bcif.gz'] = path('molsysmt.data.bcif_gz', '1atp.bcif.gz')

systems['1CEN'] = {}
systems['1CEN']['1cen.pdb'] = path('molsysmt.data.pdb', '1cen.pdb')
systems['1CEN']['1cen.bcif.gz'] = path('molsysmt.data.bcif_gz', '1cen.bcif.gz')

systems['2HGR'] = {}
systems['2HGR']['2hgr.pdb'] = path('molsysmt.data.pdb', '2hgr.pdb')

systems['4V4Z'] = {}
systems['4V4Z']['4v4z.bcif.gz'] = path('molsysmt.data.bcif_gz', '4v4z.bcif.gz')
systems['4V4Z']['4v4z_openmm.pdb'] = path('molsysmt.data.pdb', '4v4z_openmm.pdb')


# -----------------------------------------------------------------------------
# Small Molecules & Ligands
# -----------------------------------------------------------------------------

systems['benzamidine'] = {}
systems['benzamidine']['benzamidine.pdb'] = path('molsysmt.data.pdb', 'benzamidine.pdb')

systems['caffeine'] = {}
systems['caffeine']['caffeine.mol2'] = path('molsysmt.data.mol2', 'caffeine.mol2')


# -----------------------------------------------------------------------------
# Lipids & Membranes
# -----------------------------------------------------------------------------

systems['POPC'] = {}
systems['POPC']['popc.crd'] = path('molsysmt.data.crd', 'popc.crd')
systems['POPC']['popc.psf'] = path('molsysmt.data.psf', 'popc.psf')

systems['POPC membrane'] = {}
systems['POPC membrane']['popc_membrane.psf'] = path('molsysmt.data.psf', 'popc_membrane.psf')
systems['POPC membrane']['popc_membrane.dcd'] = path('molsysmt.data.dcd', 'popc_membrane.dcd')


# -----------------------------------------------------------------------------
# Toy & Synthetic Models
# -----------------------------------------------------------------------------

systems['two LJ particles'] = {}
systems['two LJ particles']['traj_two_lj_particles.trjpk'] = path('molsysmt.data.trjpk', 'traj_two_lj_particles.trjpk')

systems['particles 4'] = {}
systems['particles 4']['traj_particles_4.xyznpy'] = path('molsysmt.data.xyznpy', 'traj_particles_4.xyznpy')

systems['nglview'] = {}
systems['nglview']['ala3.pdb'] = path('molsysmt.data.pdb', 'ala3.pdb')
systems['nglview']['md_1u19.gro'] = path('molsysmt.data.gro', 'md_1u19.gro')
systems['nglview']['md_1u19.pdb'] = path('molsysmt.data.pdb', 'md_1u19.pdb')
systems['nglview']['md_1u19.traj'] = path('molsysmt.data.traj', 'md_1u19.traj')
systems['nglview']['md_1u19.trr'] = path('molsysmt.data.trr', 'md_1u19.trr')
systems['nglview']['md_1u19.xtc'] = path('molsysmt.data.xtc', 'md_1u19.xtc')


# -----------------------------------------------------------------------------
# Rich Metadata Catalog & File Descriptions
# -----------------------------------------------------------------------------

systems.info = {
    # Dipeptides & Small Peptides
    'alanine dipeptide': {
        'title': 'Alanine Dipeptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Ace-Ala-NME capped dipeptide benchmark system containing 12 heavy/hydrogen atoms.',
        'files': {
            'alanine_dipeptide.h5msm': 'Native MolSysMT HDF5 file containing full topology, 12 atoms, and coordinates.'
        }
    },
    'proline dipeptide': {
        'title': 'Proline Dipeptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Ace-Pro-NME capped dipeptide featuring a cyclic pyrrolidine sidechain.',
        'files': {
            'proline_dipeptide.h5msm': 'Native MolSysMT HDF5 file with complete topology, coordinates, and physical units.'
        }
    },
    'valine dipeptide': {
        'title': 'Valine Dipeptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Ace-Val-NME capped dipeptide featuring a branched aliphatic sidechain.',
        'files': {
            'valine_dipeptide.h5msm': 'Native MolSysMT HDF5 file with complete topology, coordinates, and physical units.'
        }
    },
    'lysine dipeptide': {
        'title': 'Lysine Dipeptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Ace-Lys-NME capped dipeptide with a positively charged sidechain.',
        'files': {
            'lysine_dipeptide.h5msm': 'Native MolSysMT HDF5 file with complete topology, coordinates, and physical units.'
        }
    },
    'pentalanine': {
        'title': 'Pentalanine Peptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Uncapped Ala5 peptide benchmark dataset with Amber topology and trajectory files.',
        'files': {
            'pentalanine.inpcrd': 'Amber initial coordinate file (INPCRD format).',
            'pentalanine.prmtop': 'Amber molecular topology and forcefield parameter file (PRMTOP format).',
            'traj_pentalanine.h5': 'HDF5 trajectory file containing coordinate frames.',
            'traj_pentalanine.h5msm': 'Native MolSysMT HDF5 trajectory file containing complete dynamics and topology.'
        }
    },
    'Met-enkephalin': {
        'title': 'Met-Enkephalin Pentapeptide',
        'category': 'Dipeptides & Small Peptides',
        'summary': 'Endogenous opioid pentapeptide (sequence Tyr-Gly-Gly-Phe-Met).',
        'files': {
            'met_enkephalin.pdb': 'Protein Data Bank structure file (PDB format).',
            'met_enkephalin.h5msm': 'Native MolSysMT HDF5 file with topology and 3D coordinates.'
        }
    },

    # Small & Globular Proteins
    'Trp-Cage': {
        'title': 'Trp-Cage TC5b Mini-Protein',
        'category': 'Small & Globular Proteins',
        'summary': '20-residue synthetic mini-protein TC5b (PDB 1L2Y) folding into a compact hydrophobic cage.',
        'files': {
            '1l2y.pdb': 'PDB file containing the 20-model NMR structure ensemble.',
            '1l2y.bcif.gz': 'Compressed Binary CIF file containing full atomic coordinates and experimental metadata.',
            '1l2y.h5msm': 'Native MolSysMT HDF5 file containing normalized topology, coordinates, and physical units for all 20 frames.'
        }
    },
    'chicken villin HP35': {
        'title': 'Chicken Villin Headpiece HP35',
        'category': 'Small & Globular Proteins',
        'summary': '35-residue fast-folding subdomain (PDB 1VII), including solvated structure and DCD trajectory.',
        'files': {
            '1vii.pdb': 'Original PDB structure file (PDB format).',
            '1vii.bcif': 'Binary CIF structure file (BCIF format).',
            '1vii.bcif.gz': 'Gzip-compressed Binary CIF structure file (BCIF.GZ format).',
            'chicken_villin_HP35.h5msm': 'Native MolSysMT HDF5 file for the vacuum protein structure.',
            'chicken_villin_HP35_solvated.h5msm': 'Native MolSysMT HDF5 file for the protein solvated in a water box.',
            'traj_chicken_villin_HP35_solvated.dcd': 'CHARMM/NAMD DCD binary trajectory file of solvated dynamics.',
            'traj_chicken_villin_HP35_solvated.h5': 'HDF5 trajectory file containing coordinate frames.',
            'traj_chicken_villin_HP35_solvated.h5msm': 'Native MolSysMT HDF5 trajectory file with solvated protein dynamics.'
        }
    },
    'T4 lysozyme L99A': {
        'title': 'T4 Lysozyme L99A Cavity Mutant',
        'category': 'Small & Globular Proteins',
        'summary': 'Engineered T4 lysozyme mutant with an internal hydrophobic cavity for ligand binding studies.',
        'files': {
            '181l.pdb': 'PDB file of the benzene-bound L99A cavity mutant (PDB 181L).',
            '181l.bcif.gz': 'Compressed Binary CIF file for structure 181L.',
            '181l.h5msm': 'Native MolSysMT HDF5 file for structure 181L.',
            '1l17.pdb': 'PDB file of the Apo L99A cavity mutant (PDB 1L17).',
            '1l17.h5msm': 'Native MolSysMT HDF5 file for structure 1L17.',
            't4_lysozyme_L99A.h5msm': 'Consolidated native MolSysMT HDF5 file for T4 lysozyme L99A.'
        }
    },
    'TcTIM': {
        'title': 'Trypanosoma cruzi Triosephosphate Isomerase',
        'category': 'Small & Globular Proteins',
        'summary': 'Homodimeric glycolytic enzyme Triosephosphate Isomerase from Trypanosoma cruzi (PDB 1TCD).',
        'files': {
            '1tcd.pdb': 'PDB crystal structure file (PDB format).',
            '1tcd.bcif.gz': 'Compressed Binary CIF file (BCIF.GZ format).',
            '1tcd.h5msm': 'Native MolSysMT HDF5 file containing homodimer topology and 3D coordinates.'
        }
    },
    'Hexokinase 2': {
        'title': 'Human Hexokinase 2',
        'category': 'Small & Globular Proteins',
        'summary': 'Key glycolytic enzyme Human Hexokinase 2 bound to glucose and inhibitor (PDB 2NZT).',
        'files': {
            '2nzt.bcif.gz': 'Compressed Binary CIF file (BCIF.GZ format).',
            '2nzt.h5msm': 'Native MolSysMT HDF5 file containing full enzyme topology and coordinates.'
        }
    },

    # Complexes & Large Assemblies
    'Barnase-Barstar': {
        'title': 'Barnase-Barstar Protein-Protein Complex',
        'category': 'Complexes & Assemblies',
        'summary': 'Ultra-high affinity complex between bacterial ribonuclease Barnase and inhibitor Barstar (PDB 1BRS).',
        'files': {
            '1brs.bcif': 'Binary CIF structure file for the 1BRS complex.',
            '1brs.bcif.gz': 'Compressed Binary CIF structure file.',
            '1brs.h5msm': 'Native MolSysMT HDF5 file for 1BRS crystal structure.',
            'barnase_barstar.h5msm': 'Consolidated native MolSysMT HDF5 file for the Barnase-Barstar complex.'
        }
    },
    '1YCR': {
        'title': 'MDM2 - p53 Peptide Complex',
        'category': 'Complexes & Assemblies',
        'summary': 'Human MDM2 oncogene bound to the p53 transactivation domain peptide (PDB 1YCR).',
        'files': {
            '1ycr.pdb': 'PDB structure file featuring SOURCE records without trailing semicolons.',
            '1ycr.bcif.gz': 'Compressed Binary CIF file for 1YCR complex.'
        }
    },
    '1ATP': {
        'title': 'PKA Kinase Complex',
        'category': 'Complexes & Assemblies',
        'summary': 'cAMP-dependent protein kinase catalytic subunit complexed with Mn2+ ATP and inhibitor (PDB 1ATP).',
        'files': {
            '1atp.pdb': 'PDB structure file with HETSYN hetero-group records.',
            '1atp.bcif.gz': 'Compressed Binary CIF file for 1ATP complex.'
        }
    },
    '1CEN': {
        'title': 'CENP-B DNA-Binding Domain',
        'category': 'Complexes & Assemblies',
        'summary': 'Centromere protein B DNA-binding domain crystal structure (PDB 1CEN).',
        'files': {
            '1cen.pdb': 'PDB structure file with HETSYN hetero-group records.',
            '1cen.bcif.gz': 'Compressed Binary CIF file for 1CEN structure.'
        }
    },
    '2HGR': {
        'title': 'Ribosome Structural Benchmark',
        'category': 'Complexes & Assemblies',
        'summary': 'Split/obsolete ribosome structural benchmark dataset (PDB 2HGR).',
        'files': {
            '2hgr.pdb': 'Original PDB structure file with OBSLTE and SPLIT records.'
        }
    },
    '4V4Z': {
        'title': 'Thermus thermophilus 70S Ribosome',
        'category': 'Complexes & Assemblies',
        'summary': 'Macromolecular 70S ribosome assembly (PDB 4V4Z) containing 149,640 atoms.',
        'files': {
            '4v4z.bcif.gz': 'Compressed Binary CIF file supporting atom counts exceeding standard PDB limits.',
            '4v4z_openmm.pdb': 'OpenMM PDB file with uppercase hex serial overflow formatting.'
        }
    },

    # Small Molecules & Ligands
    'benzamidine': {
        'title': 'Benzamidine Ligand',
        'category': 'Small Molecules & Ligands',
        'summary': 'Benzamidine synthetic aromatic inhibitor ligand.',
        'files': {
            'benzamidine.pdb': 'PDB format structure file for benzamidine.'
        }
    },
    'caffeine': {
        'title': 'Caffeine Small Molecule',
        'category': 'Small Molecules & Ligands',
        'summary': 'Caffeine xanthine alkaloid small molecule.',
        'files': {
            'caffeine.mol2': 'Tripos MOL2 format file containing bond types, atom types, and partial charges.'
        }
    },

    # Lipids & Membranes
    'POPC': {
        'title': 'POPC Lipid Molecule',
        'category': 'Lipids & Membranes',
        'summary': 'Single POPC (1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine) zwitterionic lipid molecule.',
        'files': {
            'popc.crd': 'CHARMM CRD coordinate file.',
            'popc.psf': 'CHARMM PSF protein/lipid structure file.'
        }
    },
    'POPC membrane': {
        'title': 'POPC Lipid Bilayer Membrane',
        'category': 'Lipids & Membranes',
        'summary': 'Hydrated POPC lipid bilayer membrane simulation system and trajectory.',
        'files': {
            'popc_membrane.psf': 'CHARMM PSF topology file for the lipid bilayer system.',
            'popc_membrane.dcd': 'CHARMM/NAMD DCD binary trajectory file of membrane dynamics.'
        }
    },

    # Toy & Synthetic Models
    'two LJ particles': {
        'title': 'Two Lennard-Jones Particles',
        'category': 'Toy & Synthetic Models',
        'summary': 'Minimalist 2-particle Lennard-Jones toy system trajectory.',
        'files': {
            'traj_two_lj_particles.trjpk': 'Pickled trajectory file for algorithmic unit testing.'
        }
    },
    'particles 4': {
        'title': 'Particles 4 Trajectory',
        'category': 'Toy & Synthetic Models',
        'summary': '4-particle spatial coordinate trajectory.',
        'files': {
            'traj_particles_4.xyznpy': 'NumPy NPY binary array file containing (n_frames, 4, 3) coordinates.'
        }
    },
    'nglview': {
        'title': 'NGLView Bridge Test Suite',
        'category': 'Toy & Synthetic Models',
        'summary': 'Specialized test files for NGLView, MDTraj, and GROMACS interoperability bridges.',
        'files': {
            'ala3.pdb': 'Tri-alanine peptide PDB structure file.',
            'md_1u19.gro': 'GROMACS GRO structure file for PDB 1U19.',
            'md_1u19.pdb': 'PDB structure file for PDB 1U19.',
            'md_1u19.traj': 'MDTraj trajectory file.',
            'md_1u19.trr': 'GROMACS TRR full-precision binary trajectory file.',
            'md_1u19.xtc': 'GROMACS XTC compressed binary trajectory file.'
        }
    }
}

# Group system names by category
categories = {}
for name, data in systems.info.items():
    cat = data['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(name)

systems.categories = categories
