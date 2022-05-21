from pathlib import Path

import cv2

from src.hint_tab import HintTab
from src.image2grid import Image2Grid
from src.interpret_number import InterpretNumber
from src.utils import (
    md5hash, numbers_path, processed_path, remove_duplicate_images, save, scale_to_100x100, screenshots_levels_path,
    split_in_separate_numbers
)


# Split towards numbers
def split_towards_number_directories(to_path):
    previous_file_hashes = {
        md5hash(filename) for filename in processed_path.rglob("*.png")
    }

    for file in screenshots_levels_path.rglob("*.png"):
        if file.parent.name in ["disabled_tab", "empty tab"]:
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
            processed = processed_path / f"{file.stem}_{counter}.png"
            counter += 1

        print("Working on:", file)

        tmp = Image2Grid(file)
        try:
            calculated_grid = tmp.grid
        except ValueError as ex:  # ValueError: Can't do this yet! Got 1 tabs. File saved as: ...
            print(ex)
            continue

        def process_imgs(direction: HintTab) -> None:
            for nr_images in direction.nr_imgs:
                for nr_img in nr_images:
                    # Can be > 10 here still!
                    for additional_number in split_in_separate_numbers(nr_img):
                        which_number_is_it = InterpretNumber(
                            additional_number
                        ).most_likely
                        save(
                            additional_number,
                            f"{to_path.name}/{which_number_is_it}",
                            increasing=True,
                        )

        process_imgs(calculated_grid.left)
        process_imgs(calculated_grid.top)

        # And move file
        file.replace(processed)


def convert_all_to_100x100(p: Path) -> None:
    for img in p.rglob("*.png"):
        cv2.imwrite(str(img), scale_to_100x100(img))


if __name__ == "__main__":
    split_towards_number_directories(numbers_path)
    convert_all_to_100x100(numbers_path)
    remove_duplicate_images(numbers_path)
