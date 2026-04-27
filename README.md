# rename_term

*Read this in other languages: [🇺🇸 English](#english) | [🇧🇷 Português](#português)*

---

<a id="english"></a>
## 🇺🇸 English

A tool that replaces terms across all files in a directory tree while **intelligently preserving the original casing** of each occurrence.

> [!WARNING]
> **UTF-8 only.** This tool only processes files encoded in UTF-8. Files with other encodings (Latin-1, UTF-16, etc.) are automatically skipped without raising an error.

---

### ⬇️ Download & Quick Start

1. Go to the **[`release/`](./release/)** folder and download `rename_term.exe`
2. Copy the `.exe` into the root folder of the project you want to process
3. Double-click the file
4. Type the term to search, the replacement, and answer the prompts
5. Done — the tool processes all `.md`, `.txt`, and `.rst` files recursively

No Python installation required.

---

### How It Works

Instead of blindly replacing every match with the same string, the tool detects the casing pattern of each occurrence and adapts accordingly:

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

### Interactive Prompts (double-click mode)

When launched by double-clicking the `.exe`, the tool will ask:

```
Term to search     : [type here]
Replace with       : [type here]

Preview only? (without changing files) [y/N]
Create .bak backups before replacing?  [y/N]
```

After running, it displays a summary and waits for you to press Enter before closing.

---

### CLI Usage (advanced)

If you prefer the command line, the tool also accepts arguments directly:

```bash
# Basic replacement
rename_term.exe oldterm newterm

# Multi-word terms (use quotes)
rename_term.exe "old phrase here" "new phrase here"

# Preview changes without writing anything
rename_term.exe oldterm newterm --dry-run

# Create backups before replacing
rename_term.exe oldterm newterm --backup

# Limit to a specific subfolder
rename_term.exe oldterm newterm --dir ./subfolder

# Process specific file types
rename_term.exe oldterm newterm --ext .md .txt .json
```

#### CLI Options

| Option | Description |
|---|---|
| `--dry-run` | Shows what would change without writing any file. |
| `--backup` | Creates a `.bak` copy of each file before overwriting. |
| `--dir DIR` | Limits the search to a specific subdirectory. Default: current directory. |
| `--ext .md .txt` | File extensions to process. Default: `.md`, `.txt`, `.rst`. |

---

### Automatically Skipped Directories

| Directory | Reason |
|---|---|
| `.git` | Version control history |
| `__pycache__`, `.venv`, `venv` | Python internal files |
| `node_modules` | JavaScript dependencies |
| `deprecated` | Archived files |

---

### Project Structure

```
rename_term/
├── README.md
├── .gitignore
├── source/                     ← source code
│   ├── rename_term.py          ← CLI / interactive entry point
│   ├── case_replace/           ← Python library
│   │   ├── __init__.py
│   │   ├── case_utils.py
│   │   └── file_replacer.py
│   └── tests/                  ← unit & integration tests
│       ├── test_case_utils.py
│       └── test_file_replacer.py
└── release/                    ← compiled executables
    └── rename_term.exe
```

---

<a id="português"></a>
## 🇧🇷 Português

Uma ferramenta que substitui termos em todos os arquivos de uma pasta de forma recursiva, **preservando inteligentemente a capitalização original** de cada ocorrência.

> [!WARNING]
> **Somente UTF-8.** Esta ferramenta processa apenas arquivos codificados em UTF-8. Arquivos com outras codificações (Latin-1, UTF-16, etc.) são ignorados automaticamente, sem gerar erros.

---

### ⬇️ Download e Início Rápido

1. Acesse a pasta **[`release/`](./release/)** e baixe o arquivo `rename_term.exe`
2. Copie o `.exe` para a pasta raiz do projeto que você quer processar
3. Clique duas vezes no arquivo
4. Digite o termo a buscar, o substituto, e responda às perguntas
5. Pronto — a ferramenta processa todos os arquivos `.md`, `.txt` e `.rst` recursivamente

Nenhuma instalação do Python é necessária.

---

### Como Funciona

Em vez de substituir todos os resultados com a mesma string, a ferramenta detecta o padrão de capitalização de cada ocorrência e se adapta:

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

### Perguntas Interativas (modo clique duplo)

Ao abrir o `.exe` com clique duplo, a ferramenta pergunta:

```
Termo a buscar     : [digite aqui]
Substituir por     : [digite aqui]

Apenas visualizar? (sem alterar arquivos) [s/N]
Criar backups .bak antes de alterar?      [s/N]
```

Ao terminar, exibe um resumo e aguarda você pressionar Enter antes de fechar.

---

### Uso via Terminal (avançado)

Para quem prefere a linha de comando, a ferramenta também aceita argumentos diretamente:

```bash
# Substituição simples
rename_term.exe oldterm newterm

# Termos com espaço (use aspas)
rename_term.exe "old phrase here" "new phrase here"

# Visualizar sem alterar nada
rename_term.exe oldterm newterm --dry-run

# Criar backups antes de substituir
rename_term.exe oldterm newterm --backup

# Limitar a uma subpasta
rename_term.exe oldterm newterm --dir ./subpasta

# Processar tipos específicos de arquivo
rename_term.exe oldterm newterm --ext .md .txt .json
```

#### Opções do Terminal

| Opção | Descrição |
|---|---|
| `--dry-run` | Mostra o que seria alterado sem escrever nenhum arquivo. |
| `--backup` | Cria uma cópia `.bak` de cada arquivo antes de sobrescrever. |
| `--dir DIR` | Limita a busca a uma subpasta específica. Padrão: pasta atual. |
| `--ext .md .txt` | Extensões de arquivo a processar. Padrão: `.md`, `.txt`, `.rst`. |

---

### Pastas Ignoradas Automaticamente

| Pasta | Motivo |
|---|---|
| `.git` | Histórico do controle de versão |
| `__pycache__`, `.venv`, `venv` | Arquivos internos do Python |
| `node_modules` | Dependências de projetos JavaScript |
| `deprecated` | Arquivos arquivados |

---

### Estrutura do Projeto

```
rename_term/
├── README.md
├── .gitignore
├── source/                     ← código fonte
│   ├── rename_term.py          ← entrypoint CLI / interativo
│   ├── case_replace/           ← biblioteca Python
│   │   ├── __init__.py
│   │   ├── case_utils.py
│   │   └── file_replacer.py
│   └── tests/                  ← testes unitários e de integração
│       ├── test_case_utils.py
│       └── test_file_replacer.py
└── release/                    ← executáveis compilados
    └── rename_term.exe
```
