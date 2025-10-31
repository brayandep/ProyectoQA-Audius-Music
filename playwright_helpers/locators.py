# playwright_helpers/locators.py

def by_testid(value: str) -> str:
    """Selector exacto por data-testid."""
    return f'[data-testid="{value}"]'

def has_testid(fragment: str) -> str:
    """Selector por data-testid que contenga el fragmento."""
    return f'[data-testid*="{fragment}"]'

def has_class(fragment: str) -> str:
    """Selector por fragmento de clase (evita hashes dinámicos)."""
    return f'[class*="{fragment}"]'

def attr_contains(attr: str, fragment: str) -> str:
    """Selector por atributo que contenga valor."""
    return f'[{attr}*="{fragment}"]'

def any_of(*selectors: str) -> str:
    """Une varios selectores CSS con OR (coma)."""
    return ", ".join(s for s in selectors if s)

def text_exact(txt: str) -> str:
    """Selector por texto exacto (engine 'text=')."""
    # Ojo: útil en page.locator(text_exact("Your Feed"))
    return f'text="{txt}"'

def text_like(pattern_iregex: str) -> str:
    """Selector por texto (regex case-insensitive)."""
    return f'text=/{pattern_iregex}/i'
