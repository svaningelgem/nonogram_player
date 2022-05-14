from pathlib import Path
from PIL.Image import open as imopen

from src.image2grid import Image2Grid
from src.utils import save

screenshots_path = Path(__file__).parent / '../../screenshots/levels'
numbers_path = screenshots_path / '../nr'

for file in screenshots_path.rglob('*.png'):
    if file.parent.name == 'disabled_tab':
        continue

    tmp = Image2Grid(imopen(file))
    calculated_grid = tmp.grid
    for x, nr_list in enumerate(calculated_grid.left):
        for y, nr in enumerate(nr_list):
            save(tmp.tabs_left.nr_imgs[x][y], f'nr/{nr}', increasing=True)
    a = 1
