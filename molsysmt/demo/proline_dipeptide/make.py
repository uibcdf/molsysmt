import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

molsys = msm.build.build_peptide('AceProNme')
molsys = msm.convert(molsys, to_form='diproline.msmpk')
shutil.move('diproline.msmpk', Path(data_dir, 'msmpk/diproline.msmpk'))


