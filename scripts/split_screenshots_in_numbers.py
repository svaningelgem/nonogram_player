from pathlib import Path
from typing import Generator

import cv2
import numpy as np
from PIL.Image import open as imopen

from src.hint_tab import HintTab
from src.image2grid import Image2Grid
from src.interpret_number import InterpretNumber
from src.utils import md5hash, numbers_path, processed_path, remove_duplicate_images, save, \
    scale_to_100x100, screenshots_levels_path

processed_path.mkdir(parents=True, exist_ok=True)


white = 255


def skip_whites(img: np.ndarray, start_row: int = 0) -> int:
    while start_row < img.shape[1]:
        if not np.all(img[:, start_row] == white):
            break

        start_row += 1

    return start_row


def split_in_separate_numbers(img: np.ndarray) -> Generator[np.ndarray, None, None]:
    start = end = skip_whites(img)

    while start < img.shape[1]:
        end += 1
        if end >= img.shape[1]:
            break

        if np.all(img[:, end] == white):
            yield img[:, start:end]

            start = end = skip_whites(img, start_row=end)

    if start != end:
        yield img[:, start:end]


# Split towards numbers
def split_towards_number_directories(to_path):
    previous_file_hashes = {
        md5hash(filename)
        for filename in processed_path.rglob('*.png')
    }

    for file in screenshots_levels_path.rglob('*.png'):
        if file.parent.name in ['disabled_tab', 'empty tab']:
            continue

        current_hash = md5hash(file)
        if current_hash in previous_file_hashes:
            file.unlink()
            continue

        previous_file_hashes.add(current_hash)

        # If already processed: don't bother doing it again
        processed = processed_path / file.name
        counter = 0
        while processed.exists():
            processed = processed_path / f'{file.stem}_{counter}.png'
            counter += 1

        print('Working on:', file)

        tmp = Image2Grid(file)
        try:
            calculated_grid = tmp.grid
        except ValueError as ex:  # ValueError: Can't do this yet! Got 1 tabs. File saved as: E:\nonogram_player\src\..\screenshots\2022-05-17 202756.png.
            print(ex)
            continue

        def process_imgs(direction: HintTab) -> None:
            for nr_images in direction.nr_imgs:
                for nr_img in nr_images:
                    # Can be > 10 here still!
                    for additional_number in split_in_separate_numbers(nr_img):
                        which_number_is_it = InterpretNumber(additional_number).most_likely
                        save(additional_number, f'{to_path.name}/{which_number_is_it}', increasing=True)

        process_imgs(calculated_grid.left)
        process_imgs(calculated_grid.top)

        # And move file
        file.replace(processed)


def convert_all_to_100x100(p: Path) -> None:
    for img in p.rglob('*.png'):
        cv2.imwrite(str(img), scale_to_100x100(img))


if __name__ == '__main__':
    split_towards_number_directories(numbers_path)
    convert_all_to_100x100(numbers_path)
    remove_duplicate_images(numbers_path)
