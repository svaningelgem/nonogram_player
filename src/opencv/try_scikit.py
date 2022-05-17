from skimage.metrics import structural_similarity

from ..utils import all_final_number_files, final_numbers_path, scale_to_100x100


def write_all_scores_to_csv():
    with open('output.csv', 'w') as fp:
        fp.write(';'.join(str(x.relative_to(final_numbers_path)) for x in all_final_number_files))
        fp.write(";\n")

        for first in all_final_number_files:
            first_img = scale_to_100x100(first)

            fp.write(str(first.relative_to(final_numbers_path)))
            fp.write(';')

            for second in all_final_number_files:
                second_img = scale_to_100x100(second)

                x = str(structural_similarity(first_img, second_img)).replace('.', ',')
                fp.write(x)
                fp.write(';')

            fp.write('\n')


df = pd.read_csv('output.csv', sep=';', header=0, index_col=0).iloc[:,:-1]  # Chop off last column


def filter(x, y):
    return df.iloc[df.index.str.startswith(f'{x}\\')].iloc[:,df.index.str.startswith(f'{y}\\')]


def print_csv_with_comparison_metrics():
    print('current;compare;min;max;avg')
    for current_nr in range(1, 15+1):
        for compare_against in range(1, 15+1):
            filtered_df = filter(current_nr, compare_against)

            glob_min = filtered_df.min().min()
            glob_max = filtered_df[filtered_df < 0.9999].max().max()
            glob_avg = filtered_df.mean().mean()
            print(f'{current_nr};{compare_against};{glob_min};{glob_max};{glob_avg}')


x = df.iloc[df.index.str.startswith(f'2\\')]
a = 1