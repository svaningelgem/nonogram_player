from split_screenshots_in_numbers import numbers_path, remove_duplicate_images

final_numbers_path = numbers_path / '../nr'
final_numbers_path.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    counter = 0
    for png in numbers_path.rglob('*.png'):
        tgt = final_numbers_path / png.relative_to(numbers_path)
        tgt.parent.mkdir(parents=True, exist_ok=True)

        while tgt.exists():
            tgt = tgt.parent / f'{counter}.png'
            counter += 1

        png.replace(tgt)

    remove_duplicate_images(final_numbers_path)
