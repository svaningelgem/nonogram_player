from src.fake_player import FakePlayer

app_name = "com.easybrain.nonogram"

player = FakePlayer()
try:
    while True:  # Until CTRL-C
        while player.foreground_app != app_name:
            player.start_nonogram()

        for _ in range(2):  # 2x if we're in the event levels.
            try:
                player.click_big_button_at_bottom()
            except AssertionError:
                # I'm in a level already...
                pass

        player.play_level()
except KeyboardInterrupt:
    pass
