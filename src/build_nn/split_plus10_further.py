from pathlib import Path

import cv2
import numpy as np

from PIL.Image import open as imopen

from src.utils import final_numbers_path, remove_duplicate_images, save, scale_image_to_100x100, scale_to_100x100

white = 255


def skip_whites(img: np.ndarray, start_row: int = 0) -> int:
    while start_row < len(img):
        if not np.all(img[:, start_row] == white):
            break

        start_row += 1

    return start_row


def split_10_and_above():
    for file in final_numbers_path.rglob('1?/*.png'):
        img = np.array(imopen(str(file)))
        start = end = skip_whites(img)

        while start < len(img):
            end += 1
            if end >= len(img):
                break

            if np.all(img[:, end] == white):
                save(img[:, start:end], 'splitted_further', increasing=True)
                start = end = skip_whites(img, start_row=end)

        if start == end:
            continue

        save(img[:, start:end], 'splitted_further', increasing=True)


def ensure_100x100(path: Path) -> None:
    for file in path.rglob('*.png'):
        img = scale_to_100x100(file)
        cv2.imwrite(filename=str(file), img=img)


if __name__ == '__main__':
    # split_10_and_above()
    ensure_100x100(final_numbers_path)
    remove_duplicate_images(final_numbers_path)
