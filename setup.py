from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
#import distutils.extension

ext_math = Extension(
    name = 'molmodmt.lib.libmath',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/lib/libmath.f90'],
)

ext_pbc = Extension(
    name = 'molmodmt.lib.libpbc',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/lib/libpbc.f90'],
)

ext_box = Extension(
    name = 'molmodmt.lib.libbox',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/lib/libbox.f90','molmodmt/lib/libpbc.f90'],
)

ext_geometry = Extension(
    name = 'molmodmt.lib.libgeometry',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molmodmt/lib/libgeometry.f90','molmodmt/lib/libpbc.f90','molmodmt/lib/libmath.f90'],
)

ext_rmsd = Extension(
    name = 'molmodmt.lib.librmsd',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molmodmt/lib/librmsd.f90','molmodmt/lib/libpbc.f90'],
)

# ext_io_dcd = Extension(
#     name = 'molmodmt.moldyn.Readers.MyIOformats.libdcdfile',
#     extra_compile_args = [],
#     libraries = [],
#     language = 'f90',
#     sources = ['molmodmt/moldyn/Readers/MyIOformats/libdcdfile.f90'],
# )

extensions_list=[]
extensions_lib=[ext_box, ext_math, ext_pbc, ext_geometry]
extensions_list.extend(extensions_lib)

setup(
    name='molmodmt',
    version='0.0.3',
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    package_dir={'molmodmt': 'molmodmt'},
    packages=find_packages(),
    ext_modules=extensions_list,
    package_data={'molmodnmt': []},
    scripts=[],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/MolModMT',
    license='MIT',
    description="---",
    long_description="---",
)

