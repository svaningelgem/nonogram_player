import re

cross = -1
unknown = 0
filled = 1


def natural_sort(lst):
    # https://stackoverflow.com/a/11150413/577669
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split(r'([0-9]+)', str(key))]

    return sorted(lst, key=alphanum_key)
