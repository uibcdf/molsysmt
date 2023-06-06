import molsysmt as msm
import numpy as np
from pathlib import Path
import os
import shutil

data_dir = Path('../../data/.')

molsys = msm.build.build_peptide('AceAlaNme')
molsys = msm.convert(molsys, to_form='dialanine.msmpk')
shutil.move('dialanine.msmpk', Path(data_dir, 'msmpk/dialanine.msmpk'))


