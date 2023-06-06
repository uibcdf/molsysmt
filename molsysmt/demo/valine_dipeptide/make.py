import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

molsys = msm.build.build_peptide('AceValNme')
molsys = msm.convert(molsys, to_form='divaline.msmpk')
shutil.move('divaline.msmpk', Path(data_dir, 'msmpk/divaline.msmpk'))


