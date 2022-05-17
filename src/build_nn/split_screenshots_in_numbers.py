from PIL.Image import open as imopen

from src.image2grid import Image2Grid
from src.utils import is_same_file, numbers_path, processed_path, remove_duplicate_images, save, screenshots_path

processed_path.mkdir(parents=True, exist_ok=True)


# Split towards numbers
def split_towards_number_directories():
    for file in screenshots_path.rglob('*.png'):
        # If already processed: don't bother doing it again
        processed = processed_path / file.name
        if processed.exists():
            assert is_same_file(file, processed)

            file.unlink()
            continue

        if file.parent.name == 'disabled_tab':
            continue

        print('Working on:', file)

        tmp = Image2Grid(imopen(file))
        calculated_grid = tmp.grid
        for x, nr_list in enumerate(calculated_grid.left):
            for y, nr in enumerate(nr_list):
                save(tmp.tabs_left.nr_imgs[x][y], f'{numbers_path.name}/{nr}', increasing=True)

        # And move file
        file.replace(processed)


if __name__ == '__main__':
    # split_towards_number_directories()

    remove_duplicate_images(numbers_path)
