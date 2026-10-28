import itertools
import string

one_letter_chain_names = list(string.ascii_uppercase)
two_letters_chain_names = sorted(
    ["".join(pair) for pair in itertools.product(one_letter_chain_names, repeat=2)]
)
three_letters_chain_names = sorted(
    ["".join(pair) for pair in itertools.product(one_letter_chain_names, repeat=3)]
)
all_chain_names = (
    one_letter_chain_names + two_letters_chain_names + three_letters_chain_names
)

dict_chain_index_int_to_str = {ii: name for ii, name in enumerate(all_chain_names)}
dict_chain_name_str_to_int = {name: ii for ii, name in enumerate(all_chain_names)}


def _alphabetic_chain_id(index):
    """Extend the established A..Z, AA..ZZ ordering without a fixed length limit."""
    value = index + 1
    letters = []
    while value:
        value, remainder = divmod(value - 1, 26)
        letters.append(string.ascii_uppercase[remainder])
    return "".join(reversed(letters))
