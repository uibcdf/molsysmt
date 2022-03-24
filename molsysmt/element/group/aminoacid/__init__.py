from .name_to_type import name_to_type
from terminals import n_terminal, c_terminal
from aminoacids_1letter_code import aa3_to_aa1

names = list(name_to_type.keys())
types = list(name_to_type.values())
terminals = n_terminals + c_terminals
