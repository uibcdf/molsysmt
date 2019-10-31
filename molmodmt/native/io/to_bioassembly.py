from molmodel import BioAssembly as _BioAssembly
from molmodel import Chain as _Chain
from molmodel import Entity as _Entity
from molmodel import Segment as _Segment
from molmodel import Group as _Group
from molmodel import Atom as _Atom
import numpy as _np
from copy import deepcopy as _deepcopy

def from_mmtf(mmtf):

    bioassemblies = []
    index=0

    for mmtf_bioassembly in mmtf.bio_assembly:

        bioassembly = _BioAssembly()

        bioassembly.index = index
        bioassembly.name = mmtf_bioassembly['name']
        bioassembly.id = mmtf_bioassembly['name']
        bioassembly.type = None

        # chains

        bioassembly.chain = []
        for transform_list in mmtf_bioassembly['transformList']:
            for chain_index in transform_list['chainIndexList']:
                chain = _Chain()

                chain.bioassembly_id = bioassembly.id
                chain.bioassembly_index = bioassembly.index
                chain.bioassembly_name = bioassembly.name

                chain.index = chain_index
                chain.id = mmtf.chain_id_list[chain_index]
                chain.name = mmtf.chain_name_list[chain_index]
                chain.type = None

                chain.entity = []
                chain.segment = []
                chain.group = []
                chain.atom = []
                chain.bond = []

                bioassembly.chain.append(chain)

        # entities

        bioassembly.entity=[]
        entity_index=0
        for entity_mmtf in mmtf.entity_list:
            entity = _Entity()

            entity.bioassembly_index = bioassembly.index
            entity.bioassembly_id = bioassembly.id
            entity.bioassembly_name = bioassembly.name
            entity.bioassembly_type = bioassembly.type

            entity.chain_index = []
            entity.chain_id = []
            entity.chain_name = []
            entity.chain_type = []

            for chain_index in entity_mmtf['chainIndexList']:

                chain = bioassembly.chain[chain_index]

                entity.chain_index.append(chain.index)
                entity.chain_id.append(chain.id)
                entity.chain_name.append(chain.name)
                entity.chain_type.append(chain.type)

            entity.index = entity_index
            entity.id = None
            entity.name = entity_mmtf['description']
            entity.type = entity_mmtf['type']

            entity.segment = []
            entity.group = []
            entity.atom = []
            entity.bond = []

            bioassembly.entity.append(entity)
            entity_index+=1

        # segments

        bioassembly.segment=[]
        segment_index=0

        for segment_mmtf in []:
            segment = _Segment()

            segment.bioassembly_index = bioassembly.index
            segment.bioassembly_id = bioassembly.id
            segment.bioassembly_name = bioassembly.name
            segment.bioassembly_type = bioassembly.type

            segment.chain_index = None
            segment.chain_id = None
            segment.chain_name = None
            segment.chain_type = None

            segment.entity_index = None
            segment.entity_id = None
            segment.entity_name = None
            segment.entity_type = None

            segment.index = segment_index
            segment.id = None
            segment.name = None
            segment.type = None

            segment.index_start = 0
            segment.index_end = 0
            segment.pdb_start = 0
            segment.pdb_end = 0
            segment.uniprot_start = 0
            segment.uniprot_end = 0
            segment.length = segment.index_end - segment.index_start +1

            bio_assembly.segment.append[segment]
            segment_index+=1

        # groups, atoms and bonds.

        bioassembly.group=[]

        atom_index = 0
        group_index = 0
        chain_index = 0

        for num_groups_per_chain in mmtf.groups_per_chain:

            chain = bioassembly.chain[chain_index]
            entity = None

            for _ in range(num_groups_per_chain):

                mmtf_group_type = mmtf.group_type_list[group_index]
                mmtf_group = mmtf.group_list[mmtf_group_type]

                group = _Group()

                group.bioassembly_index = bioassembly.index
                group.bioassembly_id = bioassembly.id
                group.bioassembly_name = bioassembly.name
                group.bioassembly_type = bioassembly.type

                group.chain_index = chain.index
                group.chain_id = chain.id
                group.chain_name = chain.name
                group.chain_type = chain.type

                group.entity_index = None
                group.entity_id = None
                group.entity_name = None
                group.entity_type = None

                group.segment_index = None
                group.segment_id = None
                group.segment_name = None
                group.segment_type = None

                group.index = group_index
                group.id = mmtf.group_id_list[group_index]
                group.name = mmtf_group['groupName']
                group.type = mmtf_group['chemCompType']

                group.letter_code = mmtf_group['singleLetterCode']
                group.formal_charge = _np.sum(mmtf_group['formalChargeList'])

                group.atom=[]
                group.bond=[]

                for atom_index_in_group in range(len(mmtf_group['atomNameList'])):

                    atom = _Atom()

                    atom.bioassembly_index = bioassembly.index
                    atom.bioassembly_id = bioassembly.id
                    atom.bioassembly_name = bioassembly.name
                    atom.bioassembly_type = bioassembly.type

                    atom.chain_index = chain.index
                    atom.chain_id = chain.id
                    atom.chain_name = chain.name
                    atom.chain_type = chain.type

                    atom.entity_index = None
                    atom.entity_id = None
                    atom.entity_name = None
                    atom.entity_type = None

                    atom.segment_index = None
                    atom.segment_id = None
                    atom.segment_name = None
                    atom.segment_type = None

                    atom.group_index = group.index
                    atom.group_id = group.id
                    atom.group_name = group.name
                    atom.group_type = group.type

                    atom.index = atom_index
                    atom.id = mmtf.atom_id_list[atom_index]
                    atom.name = mmtf_group['atomNameList'][atom_index_in_group]
                    atom.type = mmtf_group['elementList'][atom_index_in_group]
                    atom.element = atom.type
                    atom.formal_charge = mmtf_group['formalChargeList'][atom_index_in_group]

                    bioassembly.atom.append(atom)
                    chain.atom.append(atom)
                    #entity.atom.append(atom)
                    #segment.atom.append(atom)
                    group.atom.append(atom)
                    atom_index+=1

                bioassembly.group.append(group)
                group_index+=1

            chain_index+=1

        bioassemblies.append(bioassembly)
        index+=1

    return bioassemblies

