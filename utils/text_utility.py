from unicodedata import normalize


def accent_remover(text: str):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').upper()
