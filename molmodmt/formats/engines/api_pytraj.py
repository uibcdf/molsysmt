from os.path import basename as _basename
#from pytraj import Trajectory as _pytraj_Trajectory

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form={
    'pytraj' : form_name
}

