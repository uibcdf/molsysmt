"""Regression tests for bounded extension detection."""

from molsysmt.form import catalogue


class _TrackedString(str):
    slices = []

    def __getitem__(self, key):
        if isinstance(key, slice):
            self.slices.append(key)
        return super().__getitem__(key)

    def lower(self):
        raise AssertionError('The complete candidate must not be lowercased')


def test_molecular_text_does_not_enter_extension_matching():
    molecular_text = _TrackedString('ATOM      1  CA  ALA A   1      1.000  2.000  3.000\nEND\n')

    assert catalogue.form_of_extension(molecular_text) is None
    assert molecular_text.slices == []


def test_extension_matching_copies_only_extension_sized_slices():
    candidate = _TrackedString(('coordinate.1234567890' * 50_000) + '.bcif.gz')
    candidate.slices = []

    assert catalogue.form_of_extension(candidate) == 'file:bcif.gz'

    longest_extension = max(catalogue._load()['extension_index'], key=len)
    copied_lengths = [len(str.__getitem__(candidate, key)) for key in candidate.slices]
    assert copied_lengths
    assert max(copied_lengths) <= len(longest_extension) + 1


def test_compact_paths_and_compressed_extensions_keep_their_classification():
    assert catalogue.form_of_extension('1l2y.pdb') == 'file:pdb'
    assert catalogue.form_of_extension('/tmp/1l2y.bcif.gz') == 'file:bcif.gz'
    assert catalogue.form_of_extension('1L2Y') is None
