"""
test_file_replacer.py — Testes de integração para replace_in_files().

Usa diretórios temporários para garantir isolamento total.
"""

import sys
import os
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from case_replace.file_replacer import replace_in_files


def _write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def _read(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class TestBasicReplacement(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_lower_replaced(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'texto com oldterm aqui')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'texto com newterm aqui')

    def test_upper_replaced(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'TEXTO COM OLDTERM AQUI')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'TEXTO COM NEWTERM AQUI')

    def test_title_replaced(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'Texto com Oldterm aqui')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'Texto com Newterm aqui')

    def test_inconsistent_falls_back(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'texto com oLdTeRm aqui')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'texto com newterm aqui')

    def test_multiple_occurrences_mixed_case(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'oldterm, Oldterm, OLDTERM, oLdTeRm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'newterm, Newterm, NEWTERM, newterm')

    def test_stats_correct(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'oldterm Oldterm OLDTERM')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(stats['files_checked'], 1)
        self.assertEqual(stats['files_changed'], 1)
        self.assertEqual(stats['replacements'], 3)

    def test_no_match_leaves_file_unchanged(self):
        p = os.path.join(self.tmp, 'a.md')
        original = 'Nenhuma ocorrência aqui.'
        _write(p, original)
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), original)

    def test_stats_zero_when_no_match(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'nada aqui')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(stats['files_changed'], 0)
        self.assertEqual(stats['replacements'], 0)


class TestDryRun(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_dry_run_does_not_write(self):
        p = os.path.join(self.tmp, 'a.md')
        original = 'texto com oldterm aqui'
        _write(p, original)
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'], dry_run=True)
        self.assertEqual(_read(p), original)

    def test_dry_run_still_returns_correct_stats(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'oldterm Oldterm')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'], dry_run=True)
        self.assertEqual(stats['replacements'], 2)


class TestBackup(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_backup_file_created(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'oldterm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'], backup=True)
        self.assertTrue(os.path.exists(p + '.bak'))

    def test_backup_preserves_original_content(self):
        p = os.path.join(self.tmp, 'a.md')
        original = 'texto com oldterm aqui'
        _write(p, original)
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'], backup=True)
        self.assertEqual(_read(p + '.bak'), original)

    def test_no_backup_when_flag_off(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'oldterm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'], backup=False)
        self.assertFalse(os.path.exists(p + '.bak'))


class TestExtensionFilter(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_only_target_extension_modified(self):
        md  = os.path.join(self.tmp, 'a.md')
        txt = os.path.join(self.tmp, 'b.txt')
        py  = os.path.join(self.tmp, 'c.py')
        _write(md,  'oldterm')
        _write(txt, 'oldterm')
        _write(py,  'oldterm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(md),  'newterm')   # alterado
        self.assertEqual(_read(txt), 'oldterm')   # intocado
        self.assertEqual(_read(py),  'oldterm')   # intocado

    def test_multiple_extensions(self):
        md  = os.path.join(self.tmp, 'a.md')
        txt = os.path.join(self.tmp, 'b.txt')
        _write(md,  'oldterm')
        _write(txt, 'oldterm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md', '.txt'])
        self.assertEqual(_read(md),  'newterm')
        self.assertEqual(_read(txt), 'newterm')


class TestRecursionAndSkipDirs(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_recursive_into_subdirectory(self):
        sub = os.path.join(self.tmp, 'subdir', 'deep')
        p   = os.path.join(sub, 'a.md')
        _write(p, 'oldterm')
        replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(_read(p), 'newterm')

    def test_git_dir_skipped(self):
        git_file = os.path.join(self.tmp, '.git', 'COMMIT_EDITMSG')
        _write(git_file, 'oldterm')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(stats['files_checked'], 0)

    def test_deprecated_dir_skipped(self):
        dep_file = os.path.join(self.tmp, 'deprecated', 'old.md')
        _write(dep_file, 'oldterm')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(stats['files_checked'], 0)
        self.assertEqual(_read(dep_file), 'oldterm')  # intocado


class TestEdgeCases(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_multiword_search_term(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'texto com old phrase here no meio')
        replace_in_files(self.tmp, 'old phrase here', 'new phrase here', ['.md'])
        self.assertEqual(_read(p), 'texto com new phrase here no meio')

    def test_multiword_title_case(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'Texto com Old Phrase Here no meio')
        replace_in_files(self.tmp, 'old phrase here', 'new phrase here', ['.md'])
        self.assertEqual(_read(p), 'Texto com New phrase here no meio')

    def test_multiword_upper_case(self):
        p = os.path.join(self.tmp, 'a.md')
        _write(p, 'Texto com OLD PHRASE HERE no meio')
        replace_in_files(self.tmp, 'old phrase here', 'new phrase here', ['.md'])
        self.assertEqual(_read(p), 'Texto com NEW PHRASE HERE no meio')

    def test_empty_file(self):
        p = os.path.join(self.tmp, 'empty.md')
        _write(p, '')
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertEqual(stats['replacements'], 0)

    def test_invalid_search_raises(self):
        with self.assertRaises(ValueError):
            replace_in_files(self.tmp, '', 'newterm', ['.md'])

    def test_file_with_encoding_issue_skipped(self):
        """Arquivos que não são UTF-8 válidos são pulados sem erro."""
        p = os.path.join(self.tmp, 'binary.md')
        with open(p, 'wb') as f:
            f.write(b'\xff\xfe' + 'oldterm'.encode('utf-16-le'))
        stats = replace_in_files(self.tmp, 'oldterm', 'newterm', ['.md'])
        self.assertIsInstance(stats, dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
