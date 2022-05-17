import cv2

from src.utils import final_numbers_path, numbers_path, remove_duplicate_images, scale_to_100x100


def move_files_to_final_dir():
    counter = 0
    for png in numbers_path.rglob('*.png'):
        tgt = final_numbers_path / png.relative_to(numbers_path)
        tgt.parent.mkdir(parents=True, exist_ok=True)

        while tgt.exists():
            tgt = tgt.parent / f'{counter}.png'
            counter += 1

        png.replace(tgt)

    remove_duplicate_images(final_numbers_path)


def rescale_files():
    for png in final_numbers_path.rglob('*.png'):
        print('Working on', png)
        img = scale_to_100x100(png)
        cv2.imwrite(str(png), img)


if __name__ == '__main__':
    move_files_to_final_dir()
    remove_duplicate_images(final_numbers_path)
