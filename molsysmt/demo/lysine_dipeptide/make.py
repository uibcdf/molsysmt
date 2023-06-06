import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

molsys = msm.build.build_peptide('AceLysNme')
molsys = msm.convert(molsys, to_form='dilysine.msmpk')
shutil.move('dilysine.msmpk', Path(data_dir, 'msmpk/dilysine.msmpk'))


