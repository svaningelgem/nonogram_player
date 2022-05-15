import hashlib
from collections import defaultdict
from functools import cache
from pathlib import Path
from typing import Dict, List, Union

from PIL.Image import open as imopen

from src.image2grid import Image2Grid
from src.utils import save

screenshots_path = Path(__file__).parent / '../../screenshots/levels'
processed_path = Path(__file__).parent / '../../screenshots/processed'
numbers_path = screenshots_path / '../new_nr'

processed_path.mkdir(parents=True, exist_ok=True)


@cache
def md5hash(file: Union[str, Path]) -> str:
    return hashlib.md5(Path(file).read_bytes()).hexdigest()


@cache
def is_same_file(file1: Union[str, Path], file2: Union[str, Path]) -> bool:
    return md5hash(file1) == md5hash(file2)


# Split towards numbers
def split_towards_number_directories():
    for file in screenshots_path.rglob('*.png'):
        # If already processed: don't bother doing it again
        processed = processed_path / file.name
        if processed.exists():
            assert is_same_file(file, processed)

            file.unlink()
            continue

        print('Working on:', file)

        if file.parent.name == 'disabled_tab':
            continue

        tmp = Image2Grid(imopen(file))
        calculated_grid = tmp.grid
        for x, nr_list in enumerate(calculated_grid.left):
            for y, nr in enumerate(nr_list):
                save(tmp.tabs_left.nr_imgs[x][y], f'{numbers_path.name}/{nr}', increasing=True)

        # And move file
        processed.write_bytes(file.read_bytes())
        file.unlink()


def remove_duplicate_images(from_path: Path) -> None:
    hashes: Dict[str, List[Path]] = defaultdict(list)
    for file in from_path.rglob('*.png'):
        hashes[md5hash(file)].append(file)

    for hsh, file_list in hashes.items():
        for file in file_list[1:]:
            file.unlink()


if __name__ == '__main__':
    split_towards_number_directories()
    remove_duplicate_images(numbers_path)
