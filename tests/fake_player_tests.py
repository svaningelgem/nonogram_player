from src.fake_player import FakePlayer


def test_tap_swipes():
    solution = [
        [-1, -1, 1, 1, 1, -1, -1, -1, -1, -1],
        [-1, 1, 1, 1, 1, 1, -1, -1, -1, -1],
        [1, 1, 1, 1, 1, 1, -1, -1, -1, -1],
        [1, 1, 1, 1, -1, 1, 1, 1, -1, -1],
        [1, 1, 1, -1, 1, 1, -1, 1, -1, -1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
        [-1, 1, 1, 1, 1, 1, -1, -1, 1, 1],
        [-1, 1, 1, 1, -1, -1, -1, -1, -1, -1],
        [-1, -1, 1, -1, 1, 1, -1, -1, -1, -1],
        [-1, -1, 1, 1, -1, 1, 1, -1, -1, -1],
    ]

    field_rect = (290, 971, 1116, 1105)

    commands = list(
        FakePlayer._adjust_solution_in_taps_and_swipes(solution, *field_rect)
    )
    assert commands == [
        "input swipe 569 1026 792 1026 225",
        "input swipe 457 1136 903 1136 375",
        "input swipe 345 1247 903 1247 450",
        "input swipe 345 1357 680 1357 300",
        "input swipe 903 1357 1126 1357 225",
        "input swipe 345 1468 569 1468 225",
        "input swipe 792 1468 903 1468 150",
        "input tap 1126 1468",
        "input swipe 345 1578 1238 1578 675",
        "input swipe 457 1689 903 1689 375",
        "input swipe 1238 1689 1350 1689 150",
        "input swipe 457 1799 680 1799 225",
        "input tap 569 1910",
        "input swipe 792 1910 903 1910 150",
        "input swipe 569 2020 680 2020 150",
        "input swipe 903 2020 1015 2020 150",
    ]
