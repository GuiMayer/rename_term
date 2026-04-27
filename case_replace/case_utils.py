"""case_utils.py — Detecção e preservação de case para replace-in-files."""


def detect_case(match_str: str) -> str:
    """
    Analisa o padrão de case de um match e retorna uma string descrevendo-o.

    Retorna:
        'upper'        — todas as letras maiúsculas (ex: OLDTERM, OLD PHRASE HERE)
        'title'        — primeira letra upper, nenhuma letra interior de palavra é upper
                         (ex: Oldterm, Old phrase here, Old Phrase Here)
        'lower'        — todas as letras minúsculas (ex: oldterm, old phrase here)
        'inconsistent' — qualquer outro padrão (ex: oLdTeRm, OLDtErm)
                         → o caller deve usar lower como fallback
    """
    letters = [c for c in match_str if c.isalpha()]

    if not letters:
        return 'lower'  # sem letras: nenhum case para preservar

    # 1. Tudo maiúsculo
    if all(c.isupper() for c in letters):
        return 'upper'

    # 2. Tudo minúsculo
    if all(c.islower() for c in letters):
        return 'lower'

    # 3. Title: primeira letra upper; dentro de cada palavra, nenhuma letra
    #    após a primeira é maiúscula.
    if match_str[0].isupper():
        for word in match_str.split():
            word_letters = [c for c in word if c.isalpha()]
            if len(word_letters) > 1 and any(c.isupper() for c in word_letters[1:]):
                return 'inconsistent'
        return 'title'

    # 4. Qualquer outro padrão
    return 'inconsistent'


def apply_case(replacement: str, case: str) -> str:
    """
    Aplica o padrão de case ao string de substituição.

    Args:
        replacement: Termo substituto (em qualquer case)
        case:        Padrão detectado ('upper' | 'title' | 'lower' | 'inconsistent')

    Retorna:
        Replacement com o case aplicado. 'inconsistent' usa lower como fallback.
    """
    if not replacement:
        return replacement

    if case == 'upper':
        return replacement.upper()

    if case == 'title':
        # Capitaliza apenas a primeira letra do substituto; o resto em lower.
        # (Ex: "grande guerra" → "Grande guerra")
        return replacement[0].upper() + replacement[1:].lower()

    # 'lower' ou 'inconsistent' → tudo minúsculo
    return replacement.lower()
