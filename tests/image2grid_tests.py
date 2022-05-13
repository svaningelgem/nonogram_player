from PIL.Image import open as imopen

from src.grid import Grid
from src.image2grid import Image2Grid
from src.utils import save


def test_interpret_simple_10x10_grid():
    """Simple 10x10 grid."""

    convertor = Image2Grid(imopen("../screenshots/levels/10/2022-05-09 140127.png"))
    sut = convertor.grid
    assert sut == Grid(
        left=[[3], [2, 2], [1, 4], [1, 5], [2, 2, 1, 1], [5, 1], [5, 1], [2, 1], [1, 2], [6]],
        top=[[3, 1], [3, 1], [3, 1], [9], [2, 3, 1], [1, 2, 2], [9], [3], [2], [2]],
    )


def test_interpret_15x15_grid():
    """15x15 grid."""
    convertor = Image2Grid(imopen("../screenshots/levels/15/Screenshot_20220512-215823.png"))
    sut = convertor.grid
    assert sut == Grid(
        left=[[4, 1], [6, 3], [1, 1, 5], [1, 3, 3], [7, 3], [3, 3, 2], [3, 5], [10], [12], [10], [5, 4], [4, 1, 1], [6, 1, 4], [6, 6], [5]],
        top=[[3], [1, 3], [1, 8], [15], [2, 11], [2, 10], [5, 4], [1, 7], [8], [10], [1, 5, 1], [13], [6, 1, 2], [4, 2], [1, 2]]
    )
