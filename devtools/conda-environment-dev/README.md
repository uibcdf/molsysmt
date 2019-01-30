http://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-environments/    

conda env export -n MolModMT_devel -f molmodmt_devel.yml
head -n -1 molmodmt_devel.yml > tmp.yml
mv tmp.yml molmodmt_devel.yml


anaconda login
anaconda upload --user uibcdf molmodmt_devel.yml
anaconda logout

http://envs.anaconda.org/uibcdf

conda env create uibcdf/molmodmt_devel
source activate MolModMT_devel

If you want to work with your local devel version from github/uibcdf:
conda uninstall molmodmt
cd PATH_REPO_MOLMODMT
git clone git@github.com:uibcdf/MolModMT.git
cd MolModMT
python setup.py develop
