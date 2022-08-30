from molsysmt._private.digestion import digest

@digest()
def get_biological_assembly(molecular_system, biological_assembly_index=0, chain_indices=None, rotations=None, translations=None,
        structure_indices=0, to_form=None):

    from molsysmt.basic import get, merge

    units = []

    if (chain_indices is None) and (rotations is None) and (translations is None):

        bioassemblies = get(molecular_system, target='system', biological_assemblies=True)


        for transformation in bioassemblies[biologocial_assembly_index]:

            chains = transformation[0]
            rotation = transformation[1]
            translation = transformation[2]

            unit = msm.extract(molecular_system, selection='chain_index in @chains', syntax='molsysmt.MolSys')
            unit = msm.structure.rotate(unit, rotation=rotation)
            unit = msm.structure.translate(unit, translation=translation)

            units.append(unit)

    else:

        for chains, rotation, translation in zip(chain_indices, rotations, translations):

            unit = msm.extract(molecular_system, selection='chain_index in @chains', syntax='molsysmt.MolSys')
            unit = msm.structure.rotate(unit, rotation=rotation)
            unit = msm.structure.translate(unit, translation=translation)

            units.append(unit)

    return merge(units, to_form=to_form)

