In `play_level` add `save_screenshot`:
```python
for command in self._adjust_solution_in_taps_and_swipes(solution, *field_rect):
    self.save_screenshot('to_gif')
```

After this for-loop:
Add:
```python
self.save_screenshot('to_gif')
```


In `play.py` (basically add every other line the `save_screenshot` command):
```python
from src.fake_player import FakePlayer

app_name = 'com.easybrain.nonogram'

player = FakePlayer()
player.save_screenshot('to_gif')
while player.foreground_app != app_name:
    player.start_nonogram()
player.save_screenshot('to_gif')

try:
    player.click_big_button_at_bottom()
    player.save_screenshot('to_gif')
except AssertionError:
    # I'm in a level already...
    pass

player.play_level()
```

Now set your homescreen to show the app (so the gif shows opening up the app as well).

Run the `play.py` file once to generate all the pngs inside 'to_gif'.

Now in the 'to_gif' folder, I did a rename of all the files to 01.png, 02.png etc etc (I did it manually as that would be the fastest in my case).


Notice how some images in the next command are repeated a few times to give the impression that the delay there is longer.

This command will generate the animated gif:
```commandline
magick -delay 25 -loop 0 01.png 01.png 01.png 02.png 02.png 02.png 03.png 04.png 05.png 06.png 07.png 08.png 09.png 10.png 11.png 12.png 13.png 14.png 15.png 16.png 17.png 18.png 19.png 20.png 21.png 22.png 23.png 24.png 25.png 26.png 27.png 28.png 29.png 30.png 31.png 32.png 33.png 34.png 35.png 36.png 37.png 38.png 39.png 40.png 41.png 42.png 43.png 44.png 45.png 46.png 47.png 48.png 49.png 50.png 51.png 52.png 53.png 54.png 54.png 54.png 54.png 54.png animated.gif
```
(I got a 24.2MB gif file)

And this command will optimize and resize it:
```commandline
gifsicle --resize 360x780 --colors 512 animated.gif > optimized.gif
```

(And now I got a 1.77 MB file)

**Urls:**
- Imagick: https://imagemagick.org/script/download.php
- Gifsicle: https://github.com/kohler/gifsicle
