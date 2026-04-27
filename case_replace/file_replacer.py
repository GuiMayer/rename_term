"""
file_replacer.py — Substituição recursiva em arquivos com preservação de case.
"""

import re
import os
import shutil
from typing import List

from .case_utils import detect_case, apply_case

# Pastas sempre ignoradas durante a varredura recursiva
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', 'deprecated', '.venv', 'venv', '.mypy_cache'}


def replace_in_files(
    root: str,
    search: str,
    replacement: str,
    extensions: List[str],
    dry_run: bool = False,
    backup: bool = False,
) -> dict:
    """
    Substitui `search` por `replacement` em todos os arquivos com extensão
    em `extensions`, a partir de `root`, de forma recursiva.

    Args:
        root:        Diretório raiz da busca.
        search:      Termo a buscar (case-insensitive, busca literal).
        replacement: Substituto — o case de cada ocorrência é preservado.
        extensions:  Lista de extensões, ex: ['.md', '.txt'].
        dry_run:     Se True, apenas reporta sem escrever nada.
        backup:      Se True, cria `<arquivo>.bak` antes de sobrescrever.

    Retorna:
        dict com chaves 'files_checked', 'files_changed', 'replacements'.
    """
    if not search:
        raise ValueError("O termo de busca não pode ser vazio.")

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    stats = {'files_checked': 0, 'files_changed': 0, 'replacements': 0}

    for dirpath, dirnames, filenames in os.walk(root):
        # Poda pastas ignoradas in-place (afeta os filhos do os.walk)
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)

        for filename in filenames:
            if not any(filename.endswith(ext) for ext in extensions):
                continue

            filepath = os.path.join(dirpath, filename)
            stats['files_checked'] += 1

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, PermissionError, OSError):
                continue  # pula arquivos ilegíveis ou binários

            def _replace(m):
                case = detect_case(m.group(0))
                return apply_case(replacement, case)

            new_content, n = pattern.subn(_replace, content)

            if n > 0:
                stats['files_changed'] += 1
                stats['replacements'] += n

                if dry_run:
                    print(f'[DRY-RUN] {filepath}: {n} substituição(ões)')
                else:
                    if backup:
                        shutil.copy2(filepath, filepath + '.bak')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'[OK] {filepath}: {n} substituição(ões)')

    return stats
