"""
Code adopted from: https://stackoverflow.com/a/46500300/577669
"""
from pathlib import Path

import cv2
import numpy as np

cwd = Path(__file__).parent
src = cwd / '2022-05-24 063706.png'
out = cwd / 'out'


image = cv2.imread(str(src))
orig_image = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
circles = None

# radius! not diameter!
minimum_circle_radius = 230 // 2
maximum_circle_radius = 250 // 2

guess_dp = 1.0

min_circles_expected = 10
max_circles_expected = 20
breakout = False

max_guess_accumulator_array_threshold = 100     # minimum of 1, no maximum, (max 300?) the quantity of votes
# needed to qualify for a circle to be found.
circleLog = []

guess_accumulator_array_threshold = max_guess_accumulator_array_threshold

while guess_accumulator_array_threshold > 1 and breakout == False:
    # start out with smallest resolution possible, to find the most precise circle, then creep bigger if none found
    guess_dp = 1.0
    print("resetting guess_dp:" + str(guess_dp))
    while guess_dp < 9 and breakout is False:
        guess_radius = maximum_circle_radius
        # print("setting guess_radius: " + str(guess_radius))
        # print(circles is None)
        while True:

            # HoughCircles algorithm isn't strong enough to stand on its own if you don't
            # know EXACTLY what radius the circle in the image is, (accurate to within 3 pixels)
            # If you don't know radius, you need lots of guess and check and lots of post-processing
            # verification.  Luckily HoughCircles is pretty quick so we can brute force.

            print(f"guessing radius: {guess_radius} and dp: {guess_dp} vote threshold: {guess_accumulator_array_threshold}")

            circles = cv2.HoughCircles(gray,
                                       cv2.HOUGH_GRADIENT,
                                       dp=guess_dp,                # resolution of accumulator array.
                                       minDist=100,                # number of pixels center of circles should be from each other, hardcode
                                       param1=50,
                                       param2=guess_accumulator_array_threshold,
                                       minRadius=(guess_radius-3),    # HoughCircles will look for circles at minimum this size
                                       maxRadius=(guess_radius+3)     # HoughCircles will look for circles at maximum this size
                                       )

            if circles is not None:
                if min_circles_expected <= len(circles[0]) <= max_circles_expected:
                    print(f"len of circles: {len(circles)}")
                    circleLog.append((circles.copy(), guess_dp, guess_accumulator_array_threshold, guess_radius))
                break
            guess_radius -= 5
            if guess_radius < minimum_circle_radius:
                break

        guess_dp += 1.5

    guess_accumulator_array_threshold -= 2

# Return the circleLog with the highest accumulator threshold

# ensure at least some circles were found
counter = 0
for cir, guess_dp, guess_accumulator_array_threshold, guess_radius in circleLog:
    # convert the (x, y) coordinates and radius of the circles to integers
    output = orig_image.copy()

    if len(cir) > 1:
        print("FAIL before")
        exit()

    print(cir[0, :])

    cir = np.round(cir[0, :]).astype("int")

    for (x, y, r) in cir:
        cv2.circle(output, (x, y), r, (0, 0, 255), 2)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    cv2.imwrite(str(out) + f'_{counter}.png', output)
    print(f' >> {counter}: {guess_dp}, {guess_accumulator_array_threshold}, {guess_radius}')
    counter += 1
