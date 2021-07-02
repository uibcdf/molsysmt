"""
ProjectName
A short description of the project.
"""
import sys
from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
import versioneer

short_description = __doc__.split("\n")

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = "\n".join(short_description[2:])

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
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_dir={'molsysmt': 'molsysmt'},
    packages=find_packages(),
    ext_modules=extensions_list,
    include_package_data=True,
    package_data={'molsysmt': ['data']},
    scripts=[],
    setup_requires=[] + pytest_runner,
    platforms=['Linux',
                'Mac OS-X',
                'Unix',
                'Windows',
    ],
    python_requires=">=3.7",
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/MolSysMT',
    license='MIT',
    description=short_description[0],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

