import molsysmt as msm

molsys = msm.convert('1tcd_solv_min.pdb')
molsys = msm.remove(molsys, structure_indices='all')
traj = msm.get('traj_eq.h5', structure_indices=range(10), time=True, coordinates=True,
               box=True, temperature=True, potential_energy=True, kinetic_energy=True,
               output_type='dictionary')

msm.append_structures(molsys, traj)

msm.info(molsys)

structures = msm.convert(molsys, 'molsysmt.Structures')
