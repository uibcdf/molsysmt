http://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-environments/    

conda env export -n MolModMT_Lab -f molmodmt_lab.yml

Remove 'prefix:'

anaconda login
anaconda upload --user uibcdf molmodmt_lab.yml
anaconda logout

http://envs.anaconda.org/uibcdf

conda env create uibcdf/molmodmt_lab
source activate MolModMT_lab
