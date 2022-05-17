from pathlib import Path

import cv2
import numpy as np

from PIL.Image import open as imopen

from src.utils import final_numbers_path, remove_duplicate_images, save, scale_to_100x100

white = 255


def ensure_100x100(path: Path) -> None:
    for file in path.rglob('*.png'):
        img = scale_to_100x100(file)
        cv2.imwrite(filename=str(file), img=img)


if __name__ == '__main__':
    # split_10_and_above()
    ensure_100x100(final_numbers_path)
    remove_duplicate_images(final_numbers_path)
