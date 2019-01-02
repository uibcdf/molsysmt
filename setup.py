from setuptools import setup, find_packages
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
#import distutils.extension

ext_math = Extension(
    name = 'molmodmt.moldyn.lib.libmath',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/libmath.f90'],
)

ext_cell2box = Extension(
    name = 'molmolmd.moldyn.lib.libcell2box',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/libcell2box.f90'],
)

ext_frame = Extension(
    name = 'molmodmt.moldyn.lib.libframe',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/libframe.f90'],
)

ext_geometry = Extension(
    name = 'molmodmt.moldyn.lib.libgeometry',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/libgeometry.f90','molmodmt/moldyn/lib/libpbc.f90','molmodmt/moldyn/lib/libmath.f90'],
)

ext_pbc = Extension(
    name = 'molmodmt.moldyn.lib.libpbc',
    extra_compile_args = [],
    libraries = [],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/libpbc.f90'],
)

ext_rmsd = Extension(
    name = 'molmodmt.moldyn.lib.librmsd',
    extra_compile_args = [],
    libraries = ['lapack'],
    language = 'f90',
    sources = ['molmodmt/moldyn/lib/librmsd.f90','molmodmt/moldyn/lib/libpbc.f90'],
)

# ext_io_bin = Extension(
#     name = 'molmodmt.moldyn.Readers.MyIOformats.libbinfile',
#     extra_compile_args = [],
#     libraries = [],
#     language = 'f90',
#     sources = ['molmodmt/moldyn/Readers/MyIOformats/libbinfile.f90'],
# )

# ext_io_dcd = Extension(
#     name = 'molmodmt.moldyn.Readers.MyIOformats.libdcdfile',
#     extra_compile_args = [],
#     libraries = [],
#     language = 'f90',
#     sources = ['molmodmt/moldyn/Readers/MyIOformats/libdcdfile.f90'],
# )

extensions_list=[]
# extensions_lib=[ext_math, ext_cell2box, ext_frame, ext_pbc, ext_geometry ,ext_rmsd]
# extensions_io=[ext_io_bin,ext_io_dcd]
# extensions_list.extend(extensions_lib)

setup(
    name='molmodmt',
    version='0.0.1',
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    package_dir={'molmodmt': 'molmodmt'},
    packages=find_packages(),
    ext_modules=extensions_list,
    package_data={'molmodnmt': []},
    scripts=[],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/MolDynMT',
    license='MIT',
    description="---",
    long_description="---",
)

