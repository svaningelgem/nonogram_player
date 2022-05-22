import hashlib
import os
import re
from collections import defaultdict, namedtuple
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Dict, Generator, List, Union

import cv2
import numpy as np
from PIL import ImageOps
from PIL.Image import Image, fromarray
from PIL.Image import open as imopen

screenshots_path = Path(__file__).parent / "../screenshots"
screenshots_levels_path = screenshots_path / "levels"
processed_path = screenshots_path / "processed"
numbers_path = screenshots_path / "new_nr"
final_numbers_path = screenshots_path / "nr"


def natural_sort(lst):
    # https://stackoverflow.com/a/11150413/577669
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split(r"([0-9]+)", str(key))]

    return sorted(lst, key=alphanum_key)


all_final_number_files = natural_sort(final_numbers_path.rglob("*.png"))

# Create all these paths
for x in list(
    globals().values()
):  # Need to wrap it in a list because otherwise things might change during processing
    if isinstance(x, Path):
        x.mkdir(parents=True, exist_ok=True)


counter = 0

TLWH = namedtuple("TLWH", "x y w h")
pure_white = (255, 255, 255)
white = 255
tab_background = (0xEB, 0xEF, 0xF7)
magenta = (255, 0, 255)

ImageType = Union[str, Path, Image, np.ndarray]


def save(
    img: Union[Image, np.ndarray], subfolder: str = "", *, increasing: bool = False
) -> Path:
    if subfolder:
        filename = (
            Path(__file__).parent
            / f'../screenshots/{subfolder}/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'
        )
    else:
        filename = (
            Path(__file__).parent
            / f'../screenshots/{datetime.now().strftime("%Y-%m-%d %H%M%S")}'
        )

    if increasing:
        global counter
        filename = filename.parent / f"{counter}.png"
        counter += 1
        target = filename
    else:
        filename = str(filename)
        nr = ""
        n = 0
        ext = ".png"
        while os.path.exists(filename + nr + ext):
            n += 1
            nr = f"_{n}"

        target = Path(filename + nr + ext)

    target.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(img, np.ndarray):
        cv2.imwrite(str(target), img)
    else:
        img.save(str(target))

    return target


def remove_duplicate_images(from_path: Path) -> None:
    hashes: Dict[str, List[Path]] = defaultdict(list)
    for file in from_path.rglob("*.png"):
        hashes[md5hash(file)].append(file)

    for hsh, file_list in hashes.items():
        for file in natural_sort(file_list)[1:]:
            print("Removing duplicate", file)
            file.unlink()


@cache
def md5hash(file: Union[str, Path]) -> str:
    return hashlib.md5(Path(file).read_bytes()).hexdigest()


@cache
def is_same_file(file1: Union[str, Path], file2: Union[str, Path]) -> bool:
    return md5hash(file1) == md5hash(file2)


def _scale_image_to_100x100(original_image: Image, w=100, h=100) -> np.ndarray:
    """
    - enlarge the canvas to the maximum dimension
    - rescale to 100x100
    """

    # Crop it first
    mask: Image = ImageOps.invert(original_image)  # Make white -> black
    image_box = mask.getbbox()
    cropped: Image = original_image.crop(image_box)

    # Now resize it to 100x100
    im = np.array(cropped)

    max_ = max(im.shape[:2])

    # make a max_ by max_ image
    background = np.zeros(shape=(max_, max_, 3), dtype="uint8")
    # Set the background to white
    background[:] = (255, 255, 255)

    # Find the center
    center_x = (max_ - im.shape[0]) // 2
    center_y = (max_ - im.shape[1]) // 2

    # And paste the original image on it.
    background[
        center_x: center_x + im.shape[0], center_y: center_y + im.shape[1]
    ] = im

    # save(background)

    # And now resize the image from (max, max) -> (100, 100)
    new_img: Image = cv2.resize(
        background, dsize=(w, h), interpolation=cv2.INTER_NEAREST
    )
    # save(new_img)

    return new_img


def scale_to_100x100(img_path: ImageType, w=100, h=100) -> np.ndarray:
    """
    - Open the image
    - enlarge the canvas to the maximum dimension
    - rescale to 100x100
    - convert to grayscale
    """
    img = convert_image_to_pil(img_path)

    new_img = _scale_image_to_100x100(img, w=w, h=h)

    return cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)


def convert_image_to_numpy(image: ImageType) -> np.ndarray:
    if isinstance(image, Path):
        image = str(image.resolve())

    if isinstance(image, str):
        image = imopen(image)

    if isinstance(image, Image):
        image = np.array(image.convert("RGB"))

    return image.copy()


def convert_image_to_pil(image: ImageType) -> Image:
    if isinstance(image, Path):
        image = str(image.resolve())

    if isinstance(image, str):
        image = imopen(image)

    if isinstance(image, np.ndarray):
        image = fromarray(image)

    return image.copy().convert("RGB")


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


cross = -1
unknown = 0
filled = 1
