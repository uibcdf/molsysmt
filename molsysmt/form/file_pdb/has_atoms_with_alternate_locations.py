def has_atoms_with_alternate_locations(filename):

    atom_index = 0

    output = {}

    with open(filename, 'r') as fff:
        for line in fff.readlines():
            if line.startswith('ATOM ') or line.startswith('HETATM '):
                if line[16]!=' ':
                    print(line)
                atom_index += 1

    pass
