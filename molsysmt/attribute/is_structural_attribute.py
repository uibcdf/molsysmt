from .attributes import attributes

def is_structural_attribute(attribute):

    structural_attributes = [
            'structure_index',
            'structure_id',
            'coordinates',
            'box',
            'time',
            ]

    return attribute in structural_attributes

