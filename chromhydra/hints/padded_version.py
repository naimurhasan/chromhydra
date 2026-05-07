def padded_version(version: str, parts: int = 3) -> str:
    numbers = [piece for piece in version.split(".") if piece.isdigit()][:parts]
    return ".".join(numbers + ["0"] * (parts - len(numbers)))
