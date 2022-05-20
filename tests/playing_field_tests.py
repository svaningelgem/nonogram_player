import pytest
from src.playing_field import PlayingField
from tests.conftest import all_levels


def test_simple_one(first_level):
    field = PlayingField(first_level)

    assert field.solution == [
        [ 1, -1, -1, -1, -1, -1, -1, -1,  1, -1],
        [ 1,  1,  1,  1,  1, -1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1, -1, -1, -1, -1],
        [-1, -1,  1,  1, -1, -1, -1, -1, -1, -1],
        [-1, -1,  1,  1, -1, -1, -1, -1, -1, -1],
        [-1, -1,  1,  1, -1, -1, -1, -1, -1, -1],
        [-1, -1,  1,  1, -1, -1, -1, -1, -1, -1],
        [-1,  1,  1,  1,  1, -1, -1, -1, -1, -1]
    ]


@pytest.mark.parametrize('screenshot', all_levels(), ids=lambda x: f'{x.parent.name}/{x.name}')
def test_all(screenshot):
    # We're not doing anything here with it, but it shouldn't fail.
    PlayingField(screenshot).solution
