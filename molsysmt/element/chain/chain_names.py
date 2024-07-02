import itertools
import string

one_letter_chain_names = list(string.ascii_uppercase)
two_letters_chain_names = [''.join(pair) for pair in itertools.product(one_letter_chain_names, repeat=2)]
three_letters_chain_names = [''.join(pair) for pair in itertools.product(one_letter_chain_names, repeat=3)]
all_chain_names = one_letter_chain_names + two_letters_chain_names + three_letters_chain_names
