"""
test_case_utils.py — Testes unitários para detect_case() e apply_case().
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from case_replace.case_utils import detect_case, apply_case


class TestDetectCase(unittest.TestCase):

    # ------------------------------------------------------------------ UPPER
    def test_upper_single_word(self):
        self.assertEqual(detect_case('OLDTERM'), 'upper')

    def test_upper_multiword(self):
        self.assertEqual(detect_case('OLD PHRASE HERE'), 'upper')

    def test_upper_single_letter(self):
        self.assertEqual(detect_case('A'), 'upper')

    # ------------------------------------------------------------------ LOWER
    def test_lower_single_word(self):
        self.assertEqual(detect_case('oldterm'), 'lower')

    def test_lower_multiword(self):
        self.assertEqual(detect_case('old phrase here'), 'lower')

    def test_lower_single_letter(self):
        self.assertEqual(detect_case('a'), 'lower')

    def test_no_letters_returns_lower(self):
        """Strings sem letras (apenas números/espaços) retornam 'lower'."""
        self.assertEqual(detect_case('123'), 'lower')
        self.assertEqual(detect_case('   '), 'lower')

    # ------------------------------------------------------------------ TITLE
    def test_title_single_word(self):
        self.assertEqual(detect_case('Oldterm'), 'title')

    def test_title_multiword_first_only(self):
        """Apenas a primeira palavra começa com upper — sentence case."""
        self.assertEqual(detect_case('Old phrase here'), 'title')

    def test_title_multiword_each_word(self):
        """Cada palavra começa com upper — proper title case."""
        self.assertEqual(detect_case('Old Phrase Here'), 'title')

    def test_title_mixed_prepositions(self):
        """Preposições em lower no meio de título ainda é title."""
        self.assertEqual(detect_case('The Old Term'), 'title')

    # ---------------------------------------------------------- INCONSISTENT
    def test_inconsistent_mid_caps(self):
        self.assertEqual(detect_case('oLdTeRm'), 'inconsistent')

    def test_inconsistent_starts_lower_has_upper(self):
        self.assertEqual(detect_case('oLDterm'), 'inconsistent')

    def test_inconsistent_interior_uppercase(self):
        """Letra não-inicial de uma palavra em upper → inconsistente."""
        self.assertEqual(detect_case('OlD phrase here'), 'inconsistent')

    def test_inconsistent_camel_like(self):
        self.assertEqual(detect_case('oldPhraseHere'), 'inconsistent')


class TestApplyCase(unittest.TestCase):

    # ------------------------------------------------------------------ UPPER
    def test_apply_upper_from_lower(self):
        self.assertEqual(apply_case('newterm', 'upper'), 'NEWTERM')

    def test_apply_upper_from_mixed(self):
        self.assertEqual(apply_case('new phrase here', 'upper'), 'NEW PHRASE HERE')

    # ------------------------------------------------------------------ LOWER
    def test_apply_lower_from_upper(self):
        self.assertEqual(apply_case('NEWTERM', 'lower'), 'newterm')

    def test_apply_lower_from_mixed(self):
        self.assertEqual(apply_case('New Phrase Here', 'lower'), 'new phrase here')

    # ------------------------------------------------------------------ TITLE
    def test_apply_title_from_lower(self):
        self.assertEqual(apply_case('newterm', 'title'), 'Newterm')

    def test_apply_title_from_upper(self):
        """Title aplica apenas na primeira letra; resto em lower."""
        self.assertEqual(apply_case('NEWTERM', 'title'), 'Newterm')

    def test_apply_title_multiword(self):
        """Title capitaliza apenas a primeira letra do substituto inteiro."""
        self.assertEqual(apply_case('new phrase here', 'title'), 'New phrase here')

    # ---------------------------------------------------------- INCONSISTENT
    def test_apply_inconsistent_uses_lower(self):
        self.assertEqual(apply_case('nEwTeRm', 'inconsistent'), 'newterm')

    def test_apply_inconsistent_from_upper(self):
        self.assertEqual(apply_case('NEWTERM', 'inconsistent'), 'newterm')

    # ---------------------------------------------------------------- EDGE
    def test_apply_empty_string(self):
        self.assertEqual(apply_case('', 'upper'), '')
        self.assertEqual(apply_case('', 'title'), '')
        self.assertEqual(apply_case('', 'lower'), '')


class TestRoundTrip(unittest.TestCase):
    """
    Testa o pipeline completo: detect_case(match) → apply_case(replacement).
    Verifica que a case do match original é corretamente transferida ao substituto.
    """

    def _rt(self, original_match, replacement, expected):
        case = detect_case(original_match)
        result = apply_case(replacement, case)
        self.assertEqual(result, expected, f'detect_case({original_match!r})={case!r}')

    def test_upper_preserved(self):
        self._rt('OLDTERM', 'newterm', 'NEWTERM')

    def test_lower_preserved(self):
        self._rt('oldterm', 'NEWTERM', 'newterm')

    def test_title_preserved(self):
        self._rt('Oldterm', 'newterm', 'Newterm')

    def test_inconsistent_falls_back_to_lower(self):
        self._rt('oLdTeRm', 'NEWTERM', 'newterm')

    def test_upper_multiword(self):
        self._rt('OLD PHRASE HERE', 'new phrase here', 'NEW PHRASE HERE')

    def test_lower_multiword(self):
        self._rt('old phrase here', 'NEW PHRASE HERE', 'new phrase here')

    def test_title_multiword(self):
        self._rt('Old phrase here', 'new phrase here', 'New phrase here')

    def test_title_each_word(self):
        self._rt('Old Phrase Here', 'new phrase here', 'New phrase here')


if __name__ == '__main__':
    unittest.main(verbosity=2)
