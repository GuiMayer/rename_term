# rename_term — Substituição de Termos em Massa

> Troque um termo por outro em todos os seus arquivos de uma vez, sem perder maiúsculas e minúsculas.

---

## O Problema que Isso Resolve

Imagine que você escreveu centenas de páginas de um projeto e só agora percebeu que um nome está errado — `oldterm` deveria ser `newterm`. Esse nome aparece em dezenas de arquivos, em vários formatos:

- `oldterm` no meio de uma frase normal
- `Oldterm` no início de uma frase
- `OLDTERM` em um título em caixa alta

Se você simplesmente fizer um "substituir tudo" com qualquer editor, vai perder as maiúsculas e minúsculas originais. Tudo vai virar `newterm` (ou `Newterm`, ou qualquer coisa que você digitou), independente do contexto.

**Este script resolve isso.** Ele detecta automaticamente como a palavra estava escrita em cada lugar e adapta a substituição.

---

## Como Funciona

O script analisa cada ocorrência do termo que você quer trocar e aplica uma de quatro regras:

| Como estava no arquivo | Como fica depois |
|---|---|
| `oldterm` (tudo minúsculo) | `newterm` |
| `Oldterm` (começa com maiúscula) | `Newterm` |
| `OLDTERM` (tudo maiúsculo) | `NEWTERM` |
| `oLdTeRm` (misturado sem padrão) | `newterm` *(vira minúsculo — a opção mais segura)* |

Isso funciona também com **termos de mais de uma palavra**:

| Como estava | Como fica |
|---|---|
| `old phrase here` | `new phrase here` |
| `Old phrase here` | `New phrase here` |
| `OLD PHRASE HERE` | `NEW PHRASE HERE` |

---

## Como Usar

Abra o terminal **na pasta que você quer processar** e execute:

```bash
python caminho/para/rename_term.py <termo-antigo> <termo-novo>
```

> O script processa todos os arquivos da pasta onde você está quando o executa.

### Exemplos práticos

```bash
# Troca simples
python rename_term.py oldterm newterm

# Termos com espaço: use aspas
python rename_term.py "old phrase here" "new phrase here"

# Testar ANTES de fazer qualquer mudança (recomendado!)
python rename_term.py oldterm newterm --dry-run

# Criar backup de segurança antes de substituir
python rename_term.py oldterm newterm --backup

# Processar apenas uma subpasta específica
python rename_term.py oldterm newterm --dir ./subfolder
```

---

## Opções Disponíveis

| Opção | O que faz |
|---|---|
| `--dry-run` | **Mostra** o que seria alterado sem mudar nada. Use sempre primeiro para conferir. |
| `--backup` | Antes de alterar cada arquivo, cria uma cópia com extensão `.bak`. Segurança extra. |
| `--dir PASTA` | Limita a busca a uma subpasta específica. Padrão: a pasta atual. |
| `--ext .md .txt` | Define quais tipos de arquivo serão processados. Padrão: `.md`, `.txt`, `.rst`. |

---

## Fluxo Recomendado

```
1. Navegue até a pasta raiz do seu projeto no terminal
2. Rode com --dry-run para ver o que vai mudar
3. Se parecer certo, rode com --backup para segurança
4. Confirme o resultado
5. Se algo deu errado, os arquivos .bak têm o conteúdo original
```

---

## O que o Script Ignora

Para não bagunçar o projeto, algumas pastas são ignoradas automaticamente:

- `.git` — histórico do controle de versão
- `__pycache__`, `.venv` — arquivos internos do Python
- `node_modules` — dependências de projetos JavaScript
- `deprecated` — pasta de arquivos arquivados

---

## Estrutura Técnica (para quem quiser entender)

```
python/
└── case_replace/
    ├── README.md           ← este arquivo
    ├── __init__.py         ← ponto de entrada do pacote
    ├── case_utils.py       ← lógica de detecção e aplicação de case
    └── file_replacer.py    ← varredura recursiva e substituição

rename_term.py              ← interface de linha de comando (coloque na raiz do projeto)
```
