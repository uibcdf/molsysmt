import itertools
import string

one_letter_chain_names = list(string.ascii_uppercase)
two_letters_chain_names = sorted([''.join(pair) for pair in itertools.product(one_letter_chain_names, repeat=2)])
three_letters_chain_names = sorted([''.join(pair) for pair in itertools.product(one_letter_chain_names, repeat=3)])
all_chain_names = one_letter_chain_names + two_letters_chain_names + three_letters_chain_names

dict_chain_index_int_to_str = {ii: name for ii, name in enumerate(all_chain_names)}
dict_chain_name_str_to_int = {name: ii for ii, name in enumerate(all_chain_names)}

