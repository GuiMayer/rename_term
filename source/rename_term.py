#!/usr/bin/env python3
"""
rename_term.py — Replace-in-files recursivo com preservação de case.

Pode ser usado de dois modos:
  - Modo interativo: execute sem argumentos (ex: clique duplo no .exe)
  - Modo CLI:        passe argumentos diretamente no terminal
"""

import sys
import os
import argparse

# Adiciona o diretório deste arquivo ao path para encontrar case_replace/
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    from case_replace.file_replacer import replace_in_files
except ImportError as e:
    print(
        f'[ERRO] Não foi possível importar a biblioteca case_replace.\n'
        f'Detalhe: {e}',
        file=sys.stderr,
    )
    input('\nPressione Enter para fechar...')
    sys.exit(2)


def _exe_dir() -> str:
    """Retorna o diretório do executável (ou do script durante desenvolvimento)."""
    if getattr(sys, 'frozen', False):
        # Rodando como executável compilado (PyInstaller)
        return os.path.dirname(sys.executable)
    # Rodando como script Python
    return os.getcwd()


def _run(search: str, replacement: str, root: str, extensions: list,
         dry_run: bool, backup: bool) -> None:
    """Executa a substituição e imprime o resumo."""
    print()
    print(f'Buscando   : "{search}"')
    print(f'Substituto : "{replacement}"')
    print(f'Diretório  : {root}')
    print(f'Extensões  : {" ".join(extensions)}')
    if dry_run:
        print('[MODO] dry-run — nenhum arquivo será alterado')
    if backup:
        print('[MODO] backup — arquivos .bak serão criados')
    print('-' * 60)

    try:
        stats = replace_in_files(
            root=root,
            search=search,
            replacement=replacement,
            extensions=extensions,
            dry_run=dry_run,
            backup=backup,
        )
    except ValueError as e:
        print(f'[ERRO] {e}', file=sys.stderr)
        return

    print('-' * 60)
    print(f'Arquivos verificados : {stats["files_checked"]}')
    print(f'Arquivos alterados   : {stats["files_changed"]}')
    print(f'Substituições totais : {stats["replacements"]}')


# ──────────────────────────────────────────────────────────────────────────────
# Modo interativo — ativado ao rodar sem argumentos (ex: clique duplo no .exe)
# ──────────────────────────────────────────────────────────────────────────────

def interactive_mode() -> None:
    print('=' * 60)
    print('  rename_term — Substituição com preservação de case')
    print('=' * 60)
    print()
    print('Os arquivos serão processados na pasta onde este')
    print('executável está localizado.')
    print()

    search = input('Termo a buscar     : ').strip()
    if not search:
        print('[ERRO] O termo de busca não pode ser vazio.')
        input('\nPressione Enter para fechar...')
        sys.exit(1)

    replacement = input('Substituir por     : ').strip()

    print()
    dry_run_input = input('Apenas visualizar? (sem alterar arquivos) [s/N] ').strip().lower()
    dry_run = dry_run_input in ('s', 'sim', 'y', 'yes')

    backup_input = input('Criar backups .bak antes de alterar?      [s/N] ').strip().lower()
    backup = backup_input in ('s', 'sim', 'y', 'yes')

    root = _exe_dir()
    _run(search, replacement, root, ['.md', '.txt', '.rst'], dry_run, backup)
    print()
    input('Pressione Enter para fechar...')


# ──────────────────────────────────────────────────────────────────────────────
# Modo CLI — ativado ao passar argumentos no terminal
# ──────────────────────────────────────────────────────────────────────────────

def cli_mode() -> None:
    parser = argparse.ArgumentParser(
        prog='rename_term',
        description='Substituição recursiva de termos em arquivos com preservação de case.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Regras de case:
  OLDTERM  →  NEWTERM   (all caps preservado)
  Oldterm  →  Newterm   (primeira letra maiúscula preservada)
  oldterm  →  newterm   (all lower preservado)
  oLdTeRm  →  newterm   (inconsistente → fallback lower)
        """,
    )

    parser.add_argument('search',      help='Termo a buscar (case-insensitive)')
    parser.add_argument('replacement', help='Termo substituto')
    parser.add_argument(
        '--dir',
        default=None,
        metavar='DIR',
        help='Diretório raiz da busca (padrão: pasta atual onde o script é chamado)',
    )
    parser.add_argument(
        '--ext',
        nargs='+',
        default=['.md', '.txt', '.rst'],
        metavar='EXT',
        help='Extensões de arquivo a processar (padrão: .md .txt .rst)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostra o que seria alterado sem escrever nenhum arquivo',
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Cria <arquivo>.bak antes de sobrescrever cada arquivo alterado',
    )

    args = parser.parse_args()
    root = os.path.abspath(args.dir) if args.dir else os.getcwd()

    if not os.path.isdir(root):
        print(f'[ERRO] Diretório não encontrado: {root}', file=sys.stderr)
        sys.exit(2)

    _run(args.search, args.replacement, root, args.ext, args.dry_run, args.backup)


# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        cli_mode()


if __name__ == '__main__':
    main()
