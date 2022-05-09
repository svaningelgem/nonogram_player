import sys

from PIL.Image import open as imopen

app_name = 'com.easybrain.nonogram'

if __name__ == '__main__':
    
    sys.exit(0)
    for png in Path('../screenshots/ok').glob('*.png'):
        size = (2000, 1000)
        out_file = Path('out.txt')
        img = imopen(str(png)).convert('RGB')
        background = imnew('RGB', size, color='white')
        centered_x = (background.width - img.width) // 2
        centered_y = (background.height - img.height) // 2
        background.paste(img, box=(centered_x, centered_y))

        tmp_name = 'new.jpg'
        background.save(tmp_name)
        subprocess.run(['tesseract', tmp_name, 'out'])
        sys.exit(0)

    player = FakePlayer()

    for png in Path('../screenshots/level3').glob('*.png'):
        print(png)
        player.screencap = lambda *x: imopen(str(png)).convert('RGB')
        player.crop_numbers()
        sys.exit(0)

    # if player.is_main_screen():
    #    player.click_blue_button()
    # player.save_screenshot('level3')
    #
    # player.crop_numbers()
