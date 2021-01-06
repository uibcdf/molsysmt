from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
from molsysmt import __version__ as msm_version
#import distutils.extension

ext_math = Extension(
    name = 'molsysmt.lib.libmath',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libmath.f90'],
)

ext_pbc = Extension(
    name = 'molsysmt.lib.libpbc',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libpbc.f90'],
)

ext_com = Extension(
    name = 'molsysmt.lib.libcom',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libcom.f90'],
)

ext_box = Extension(
    name = 'molsysmt.lib.libbox',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libbox.f90','molsysmt/lib/libpbc.f90'],
)

ext_geometry = Extension(
    name = 'molsysmt.lib.libgeometry',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molsysmt/lib/libgeometry.f90', 'molsysmt/lib/libmath.f90', 'molsysmt/lib/libpbc.f90','molsysmt/lib/libbox.f90'],
)

ext_rmsd = Extension(
    name = 'molsysmt.lib.librmsd',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molsysmt/lib/librmsd.f90'],
)

ext_bonds = Extension(
    name = 'molsysmt.lib.libbonds',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molsysmt/lib/libbonds.f90'],
)

# ext_io_dcd = Extension(
#     name = 'molsysmt.moldyn.Readers.MyIOformats.libdcdfile',
#     extra_compile_args = [],
#     libraries = [],
#     language = 'f90',
#     sources = ['molsysmt/moldyn/Readers/MyIOformats/libdcdfile.f90'],
# )

extensions_list=[]
extensions_lib=[ext_com, ext_pbc, ext_box, ext_math, ext_geometry, ext_rmsd, ext_bonds]
extensions_list.extend(extensions_lib)

setup(
    name='molsysmt',
    version=msm_version,
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    package_dir={'molsysmt': 'molsysmt'},
    packages=find_packages(),
    ext_modules=extensions_list,
    package_data={'molsysmt': []},
    scripts=[],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/MolSysMT',
    license='MIT',
    description="---",
    long_description="---",
)

