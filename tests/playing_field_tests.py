from pathlib import Path

import pytest

from src.playing_field import PlayingField
from tests.conftest import all_levels


def test_simple_one(first_level):
    field = PlayingField(first_level)

    assert field.solution == [
        [1, -1, -1, -1, -1, -1, -1, -1, 1, -1],
        [1, 1, 1, 1, 1, -1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
        [-1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
    ]


@pytest.mark.parametrize(
    "screenshot", all_levels(), ids=lambda x: f"{x.parent.name}/{x.name}"
)
def test_all(screenshot):
    # We're not doing anything here with it, but it shouldn't fail.
    PlayingField(screenshot).solution


def test_failing_screenshots():
    source = Path(__file__).parent / 'resources/failing_screenshots/2022-05-21 204409.png'

    field = PlayingField(source)

    # This was failing to provide the correct solution
    assert field.left == [[3, 1], [3, 1], [4, 2], [2, 1, 1, 1], [1, 3, 2], [6, 3], [10], [3, 1, 1, 1], [3, 2, 2, 2], [3, 1, 2], [5, 1, 1, 3], [14], [8, 5], [3, 6, 1], [7]]
    # But the 2nd iteration would be fine
    assert PlayingField(source, iteration=1).left == [[3, 1], [3, 1], [4, 2], [2, 1, 1, 1], [1, 3, 2], [6, 3], [10], [3, 1, 1, 1], [3, 2, 2, 2], [3, 1, 2], [5, 1, 1, 3], [14], [8, 5], [3, 8, 1], [7]]

    assert PlayingField(source).solution == [
        [-1, -1, -1, -1, -1, -1,  1,  1,  1, -1,  1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1,  1,  1,  1, -1, -1, -1,  1, -1, -1, -1],
        [-1, -1, -1, -1,  1,  1,  1,  1, -1, -1, -1,  1,  1, -1, -1],
        [-1, -1, -1, -1,  1,  1, -1, -1,  1, -1,  1, -1,  1, -1, -1],
        [-1, -1, -1,  1, -1, -1,  1,  1,  1, -1,  1,  1, -1, -1, -1],
        [-1, -1, -1,  1,  1,  1,  1,  1,  1, -1,  1,  1,  1, -1, -1],
        [-1, -1, -1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, -1, -1],
        [-1, -1,  1,  1,  1, -1, -1,  1, -1,  1, -1, -1,  1, -1, -1],
        [-1, -1,  1,  1,  1, -1,  1,  1, -1,  1,  1, -1,  1,  1, -1],
        [-1, -1,  1,  1,  1, -1, -1, -1, -1,  1, -1, -1,  1,  1, -1],
        [-1,  1,  1,  1,  1,  1, -1,  1, -1,  1, -1,  1,  1,  1, -1],
        [-1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1, -1, -1,  1,  1,  1,  1,  1],
        [ 1,  1,  1, -1,  1,  1,  1,  1,  1,  1,  1,  1, -1, -1,  1],
        [-1, -1, -1, -1, -1,  1,  1,  1,  1,  1,  1,  1, -1, -1, -1],
    ]
