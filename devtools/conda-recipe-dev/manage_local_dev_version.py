import os
import sys
from numpy.distutils.exec_command import exec_command

def installing():

    status, output = exec_command('conda build . --no-anaconda-upload')
    status, output = exec_command('conda build . --output')
    status, output = exec_command('conda install --use-local '+output)
    status, output = exec_command('conda build purge')

def remove():

    status, output = exec_command('conda remove mdtools_uibcdf_dev --yes')

def update():

    remove()
    installing()

if '--install' in sys.argv[1:]:
    print('Building and installing local dev version via conda')
    installing()
elif '--remove' in sys.argv[1:]:
    print('Removing local dev package')
    remove()
elif '--update' in sys.argv[1:]:
    print('Updating local dev package')
    update()
