#!/usr/bin/env python

import os
import shutil

def delete_autosummary_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'autosummary' in dirnames:
            autosummary_dir = os.path.join(dirpath, 'autosummary')
            print(f"Deleting directory: {autosummary_dir}")
            shutil.rmtree(autosummary_dir)
            dirnames.remove('autosummary')  # Avoid descending into this directory

if __name__ == "__main__":
    api_directory = 'api'  # Ruta del directorio "api"
    delete_autosummary_dirs(api_directory)

