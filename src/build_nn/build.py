"""
Script to convert the cropped numbers (which were manually labeled) into appropriate directories.
"""
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from PIL import Image

from src.image2grid import Image2Grid

nr_dir = Path(__file__).parent / 'nr'


def load_file_with_numbers():
    final = []
    for line in (nr_dir / 'nrs.txt').read_text().splitlines():
        if len(line) <= 2:
            final.append(int(line))
            continue

        take_next_2 = False
        tmp = ''
        for char in line:
            if char == '*':
                take_next_2 = True

            elif take_next_2:
                tmp += char
                if len(tmp) == 2:
                    final.append(int(tmp))
                    take_next_2 = False
                    tmp = ''

            else:
                final.append(int(char))
    return final


def natural_sort(lst):
    # https://stackoverflow.com/a/11150413/577669
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split(r'([0-9]+)', str(key))]

    return sorted(lst, key=alphanum_key)


def move_numbers_into_right_directory(nrs, files):
    number_counter = defaultdict(int)

    for nr, file in zip(nrs, files):
        img: Image.Image = Image.open(file).convert('RGB')

        background = Image.new('RGB', size=(100, 100), color='white')
        background.paste(img, box=(
            (100-img.width)//2,
            (100-img.height)//2,
        ))

        tgt = Path(__file__).parent / 'images' / str(nr) / f'{number_counter[nr]}.png'
        tgt.parent.mkdir(parents=True, exist_ok=True)

        background.save(tgt)

        number_counter[nr] += 1
        print(nr, tgt, file)

    return number_counter


def crop_numbers():
    for level in [2, 3, 4]:
        for png in (Path(__file__).parent / f'../../screenshots/level{level}').glob('*.png'):
            Image2Grid(Image.open(png)).interpret()


if __name__ == '1__main__':
    # crop_numbers()

    input('create a nrs.txt file now!')

    nrs = load_file_with_numbers()
    files = natural_sort(nr_dir.glob('*.png'))

    assert len(nrs) == len(files)

    move_numbers_into_right_directory(
        nrs,
        files
    )


def move_images_from_generation_dir_to_final_dir():
    in_ = Path(__file__).parent / 'images2'
    out_ = Path(__file__).parent / 'images'
    for file in in_.rglob('*.png'):
        tgt = out_ / file.parent.stem
        counter = 0
        while (tgt / f'{counter}.png').exists():
            counter += 1

        tgt = tgt / f'{counter}.png'

        tgt.write_bytes(file.read_bytes())

    remove_duplicate_images(out_)


def remove_duplicate_images(images_dir):
    def md5hash(file: Path) -> str:
        import hashlib

        return hashlib.md5(file.read_bytes()).hexdigest()

    hashes: Dict[str, List[Path]] = defaultdict(list)
    for file in images_dir.rglob('*.png'):
        hashes[md5hash(file)].append(file)

    for hsh, file_list in hashes.items():
        for file in file_list[1:]:
            file.unlink()


