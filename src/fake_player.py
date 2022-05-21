import time
from collections import defaultdict
from functools import cache
from io import BytesIO
from pprint import pprint
from typing import List, Tuple

import cv2
import numpy as np
from PIL.Image import Image, open as imopen
from ppadb.client import Client
from ppadb.device import Device

from src.common import cross, filled
from src.playing_field import PlayingField
from src.utils import TLWH, save


app_name = 'com.easybrain.nonogram'


class FakePlayer:
    _client: Client = None
    _device: Device = None
    _devices: List[Device] = None

    @property
    def client(self):
        self._connect()
        return self._client

    @property
    def device(self):
        self._connect()
        return self._device

    @property
    def devices(self):
        self._connect()
        return self._devices

    @cache
    def _connect(self):
        self._client = Client(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

        self._devices = self._client.devices()

        if len(self._devices) == 0:
            print('No devices')
            quit()

        self._device = self._devices[0]

        print(f'Connected to {self._device}')

    @property
    def foreground_app(self) -> str:
        return (
            self.device.shell("dumpsys activity recents | grep 'Recent #0' | cut -d= -f2 | sed 's| .*||' | cut -d '/' -f1")
            .strip()
        )

    def start_nonogram(self) -> None:
        self.device.shell(f'monkey -p {app_name} 1')
        time.sleep(10)

    def screencap(self) -> Image:
        b = BytesIO(bytes(self.device.screencap()))
        return imopen(b).convert('RGB')

    def save_screenshot(self, subfolder: str = '') -> None:
        save(self.screencap(), subfolder=subfolder)

    def _get_contours(self, threshold: int = 10, screen: np.ndarray = None) -> Tuple[np.ndarray, Tuple[np.ndarray], np.ndarray]:
        src = np.array(screen or self.screencap())
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (3, 3))

        # Detect edges using Canny
        canny_output = cv2.Canny(gray, threshold, threshold * 2)

        # Find contours
        contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return src, contours, hierarchy

    def get_big_button_click_coordinates(self) -> Tuple[int, int]:
        src, contours, hierarchy = self._get_contours()
        w = src.shape[0]
        h = src.shape[0]
        bottom_part = h - (h // 3.5)
        big_button_threshold = 0.015 * w * h

        # Only keep the things at the bottom
        filtered_contours = []
        for i, c in enumerate(contours):
            minimum_y = min(c[:, :, 1])
            if minimum_y <= bottom_part:
                continue

            area = cv2.contourArea(c)
            if area <= big_button_threshold:
                continue

            filtered_contours.append((i, c, minimum_y, area))

        assert filtered_contours, f'No big buttons found?'

        # Order contours based on the order they appear.
        ordered = sorted(filtered_contours, key=lambda x: x[2])

        bottom_button = ordered[-1]
        x_coords = bottom_button[1][:, :, 0]
        y_coords = bottom_button[1][:, :, 1]

        return (
            x_coords.min() + (x_coords.max() - x_coords.min()) // 2,
            y_coords.min() + (y_coords.max() - y_coords.min()) // 2,
        )

    def click_big_button_at_bottom(self) -> bool:
        center = self.get_big_button_click_coordinates()
        self.device.shell(f'input tap {center[0]} {center[1]}')
        time.sleep(1)

    def get_playing_field_area(self, screen=None) -> Tuple[int, int, int, int]:
        """
        returns topleft-x/y, width, height
        """
        src, contours, hierarchy = self._get_contours(screen=screen)
        max_contour = max(contours, key=lambda c: cv2.contourArea(c))

        x = max_contour[:, :, 0]
        y = max_contour[:, :, 1]

        return (
            x.min(),
            y.min(),
            x.max() - x.min(),
            y.max() - y.min(),
        )

    def play_level(self):
        screen = self.screencap()
        field = PlayingField(screen)
        solution = field.solution
        x, y, w, h = self.get_playing_field_area(screen)

        row_height = h / len(solution)
        col_width = w / len(solution[0])

        for i, row in enumerate(solution):
            for j, element in enumerate(row):
                if element != filled:
                    continue

                click_x = int(x + col_width * j + col_width/2)
                click_y = int(y + row_height * i + row_height/2)
                self.device.shell(f'input tap {click_x} {click_y}')
                time.sleep(0.5)
