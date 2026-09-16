from functools import cache
from pathlib import Path

import pytest


@cache
def all_levels() -> list[Path]:
    return [
        png
        for directory in ["levels", "processed*"]
        for path in (Path(__file__).parent / "../screenshots").rglob(directory)
        if path.exists()
        for png in path.rglob("*.png")
        if png.parent.name not in ["disabled_tab", "empty_tab"]
    ]


@pytest.fixture(scope="session")
def first_level() -> Path:
    yield all_levels()[0]
