from src.fake_player import FakePlayer

app_name = "com.easybrain.nonogram"

player = FakePlayer()
while player.foreground_app != app_name:
    player.start_nonogram()

try:
    player.click_big_button_at_bottom()
except AssertionError:
    # I'm in a level already...
    pass

player.play_level()
