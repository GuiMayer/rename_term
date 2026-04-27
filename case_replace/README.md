# rename_term

*Read this in other languages: [🇺🇸 English](#english) | [🇧🇷 Português](#português)*

---

<a id="english"></a>
## 🇺🇸 English

A command-line tool that replaces terms across all files in a directory tree while **intelligently preserving the original casing** of each occurrence.

> [!WARNING]
> **UTF-8 only.** This script only processes files encoded in UTF-8. Files with other encodings (Latin-1, UTF-16, etc.) are automatically skipped without raising an error.

---

### How It Works

Instead of blindly replacing every match with the same string, the script detects the casing pattern of each occurrence and adapts the replacement accordingly:

| Found in file | Result |
|---|---|
| `oldterm` (all lowercase) | `newterm` |
| `Oldterm` (first letter capitalized) | `Newterm` |
| `OLDTERM` (all uppercase) | `NEWTERM` |
| `oLdTeRm` (inconsistent pattern) | `newterm` *(falls back to lowercase)* |

This also works with **multi-word terms**:

| Found in file | Result |
|---|---|
| `old phrase here` | `new phrase here` |
| `Old phrase here` | `New phrase here` |
| `OLD PHRASE HERE` | `NEW PHRASE HERE` |

---

### Usage

Open a terminal **in the folder you want to process** and run:

```bash
python path/to/rename_term.py <search> <replacement>
```

The script processes all matching files starting from the directory where it is called.

### Examples

```bash
# Basic replacement
python rename_term.py oldterm newterm

# Multi-word terms (use quotes)
python rename_term.py "old phrase here" "new phrase here"

# Preview changes without writing anything (recommended first step)
python rename_term.py oldterm newterm --dry-run

# Create backups before replacing
python rename_term.py oldterm newterm --backup

# Limit to a specific subfolder
python rename_term.py oldterm newterm --dir ./subfolder
```

---

### Options

| Option | Description |
|---|---|
| `--dry-run` | Shows what would change without writing any file. Always run this first. |
| `--backup` | Creates a `.bak` copy of each file before overwriting it. |
| `--dir DIR` | Limits the search to a specific subdirectory. Default: current directory. |
| `--ext .md .txt` | File extensions to process. Default: `.md`, `.txt`, `.rst`. |

---

### Recommended Workflow

```
1. Navigate to the root of the folder you want to process
2. Run with --dry-run to preview what will change
3. If it looks correct, run with --backup for safety
4. Verify the results
5. If something went wrong, the .bak files hold the original content
```

---

### Automatically Skipped Directories

The following directories are always ignored during the recursive scan:

| Directory | Reason |
|---|---|
| `.git` | Version control history |
| `__pycache__`, `.venv`, `venv` | Python internal files |
| `node_modules` | JavaScript dependencies |
| `deprecated` | Archived files |

---

### Project Structure

```
rename_term/                ← project root (git repository)
├── case_replace/           ← Python library package
│   ├── __init__.py
│   ├── case_utils.py       ← case detection and application logic
│   ├── file_replacer.py    ← recursive file scanning and replacement
│   └── README.md           ← this file
└── tests/
    ├── test_case_utils.py  ← unit tests for case logic
    └── test_file_replacer.py  ← integration tests for file operations

rename_term.py              ← CLI entry point (place at your project root)
```

---

<a id="português"></a>
## 🇧🇷 Português

Uma ferramenta de linha de comando que substitui termos em todos os arquivos de uma pasta de forma recursiva, **preservando inteligentemente a capitalização original** de cada ocorrência.

> [!WARNING]
> **Somente UTF-8.** Este script processa apenas arquivos codificados em UTF-8. Arquivos com outras codificações (Latin-1, UTF-16, etc.) são ignorados automaticamente, sem gerar erros.

---

### Como Funciona

Em vez de substituir todos os resultados com a mesma string, o script detecta o padrão de capitalização de cada ocorrência e adapta a substituição:

| Encontrado no arquivo | Resultado |
|---|---|
| `oldterm` (tudo minúsculo) | `newterm` |
| `Oldterm` (primeira letra maiúscula) | `Newterm` |
| `OLDTERM` (tudo maiúsculo) | `NEWTERM` |
| `oLdTeRm` (padrão inconsistente) | `newterm` *(usa minúsculo como fallback)* |

Também funciona com **termos de mais de uma palavra**:

| Encontrado no arquivo | Resultado |
|---|---|
| `old phrase here` | `new phrase here` |
| `Old phrase here` | `New phrase here` |
| `OLD PHRASE HERE` | `NEW PHRASE HERE` |

---

### Como Usar

Abra o terminal **na pasta que você quer processar** e execute:

```bash
python caminho/para/rename_term.py <busca> <substituição>
```

O script processa todos os arquivos correspondentes a partir do diretório onde é chamado.

### Exemplos

```bash
# Substituição simples
python rename_term.py oldterm newterm

# Termos com espaço (use aspas)
python rename_term.py "old phrase here" "new phrase here"

# Visualizar as mudanças sem escrever nada (passo recomendado)
python rename_term.py oldterm newterm --dry-run

# Criar backups antes de substituir
python rename_term.py oldterm newterm --backup

# Limitar a uma subpasta específica
python rename_term.py oldterm newterm --dir ./subpasta
```

---

### Opções

| Opção | Descrição |
|---|---|
| `--dry-run` | Mostra o que seria alterado sem escrever nenhum arquivo. Use sempre primeiro. |
| `--backup` | Cria uma cópia `.bak` de cada arquivo antes de sobrescrever. |
| `--dir DIR` | Limita a busca a uma subpasta específica. Padrão: pasta atual. |
| `--ext .md .txt` | Extensões de arquivo a processar. Padrão: `.md`, `.txt`, `.rst`. |

---

### Fluxo Recomendado

```
1. Navegue até a pasta raiz do projeto no terminal
2. Rode com --dry-run para visualizar o que vai mudar
3. Se parecer correto, rode com --backup para segurança
4. Verifique o resultado
5. Se algo deu errado, os arquivos .bak têm o conteúdo original
```

---

### Pastas Ignoradas Automaticamente

As seguintes pastas são sempre ignoradas durante a varredura recursiva:

| Pasta | Motivo |
|---|---|
| `.git` | Histórico do controle de versão |
| `__pycache__`, `.venv`, `venv` | Arquivos internos do Python |
| `node_modules` | Dependências de projetos JavaScript |
| `deprecated` | Arquivos arquivados |

---

### Estrutura do Projeto

```
rename_term/                ← raiz do projeto (repositório git)
├── case_replace/           ← pacote Python da biblioteca
│   ├── __init__.py
│   ├── case_utils.py       ← lógica de detecção e aplicação de case
│   ├── file_replacer.py    ← varredura recursiva e substituição
│   └── README.md           ← este arquivo
└── tests/
    ├── test_case_utils.py  ← testes unitários da lógica de case
    └── test_file_replacer.py  ← testes de integração das operações em arquivo

rename_term.py              ← CLI (coloque na raiz do seu projeto)
```
