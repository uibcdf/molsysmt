from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

        # EXT:
        #      (i10,2x,a)  natoms,'EXT'
        #      (2I10,2X,A8,2X,A8,3F20.10,2X,A8,2X,A8,F20.10)
        #      iatom,ires,resn,typr,x,y,z,segid,rid,wmain
        # standard:
        #      (i5) natoms
        #      (2I5,1X,A4,1X,A4,3F10.5,1X,A4,1X,A4,F10.5)
        #      iatom,ires,resn,typr,x,y,z,segid,orig_resid,wmain

    from molsysmt.native.topology import Topology

    tmp_item = Topology()

    atom_id = []
    atom_name = []
    group_id = []
    group_name = []
    chain_id = []
    bfactor = []

    extended = False

    with open(item) as fff:
        for line in fff:
            if line.strip().startswith('*') or line.strip() == "":
                continue
            field = line.split()
            if len(fields)=1:
                n_atoms = int(field[0])
            elif len(fields)==1:
                n_atoms = int(field[0])
                extended = True
            else:
                atom_id.append(int(field[0]))
                group_id.append(int(field[1]))
                group_name.append(field[2])
                atom_name.append(field[3])
                chain_id.append(field[7])
                bfactor.append(field[9])

    if len(atom_id)!=n_atoms:
        raise ValueError

    atom_id = np.array(atom_id, dtype=int)
    atom_name = np.array(atom_name, dtype=object)
    group_id = np.array(group_id, dtype=int)
    group_name = np.array(group_name, dtype=object)
    chain_id = np.array(chain_id, dtype=object)
    bfactor = np.array(bfactor, dtype=float)

    b_factor_array = puw.quantity(np.array(item.b_factor_list), unit='angstroms**2', standardized=True)
    

    return tmp_item
