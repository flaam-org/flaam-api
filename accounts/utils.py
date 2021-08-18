from pathlib import Path
from typing import Any


def avatar_path(instance: Any, filename: str) -> str:
    ext = Path(filename).suffix[1:].lower()
    return f"avatars/avatar_{instance.pk}.{ext}"
