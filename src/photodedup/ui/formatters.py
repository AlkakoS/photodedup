def format_size(size: int) -> str:
    """Taille lisible (ex: '2.4 Mo')."""
    if size < 1024:
        return f"{size} o"
    elif size < 1024**2:
        return f"{size / 1024:.1f} Ko"
    elif size < 1024**3:
        return f"{size / 1024**2:.1f} Mo"
    else:
        return f"{size / 1024**3:.1f} Go"
