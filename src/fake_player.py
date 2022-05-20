import time
from io import BytesIO
from typing import List

import numpy as np
from PIL.Image import Image, open as imopen
from ppadb.client import Client
from ppadb.device import Device

from src.main import app_name
from src.utils import TLWH, save


class FakePlayer:
    _client: Client = None
    _device: Device = None
    _devices: List[Device] = None

    @property
    def client(self):
        if self._client is None: self._connect()

        return self._client

    @property
    def device(self):
        if self._client is None: self._connect()

        return self._device

    @property
    def devices(self):
        if self._client is None: self._connect()

        return self._devices

    def _connect(self):
        self._client = Client(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

        self._devices = self._client.devices()

        if len(self._devices) == 0:
            print('No devices')
            quit()

        self._device = self._devices[0]

        print(f'Connected to {self._device}')

    def _foreground_app(self) -> str:
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

    def is_main_screen(self) -> bool:
        tlwh = TLWH(147, 2474, 1138, 192)

        img = self.screencap()
        cropped: Image = img.crop(box=(tlwh.x, tlwh.y, tlwh.x + tlwh.w, tlwh.y + tlwh.h))
        arr: np.array = np.array(cropped).reshape((cropped.width * cropped.height, 3))
        colors = np.unique(arr, return_counts=True, axis=0)
        most_used_color = tuple(colors[0][np.argmax(colors[1])][:3])

        # Within 3%?
        blue_color = 46, 134, 237
        if most_used_color == blue_color:
            return True

        return all(
            0.96 <= m/b <= 1.04
            for m, b in zip(most_used_color, blue_color)
        )

    def click_blue_button(self):
        self.device.shell('input tap 720 2564')
        time.sleep(1)



    # if __name__ == '__main__':
    #     device, client = connect()
    #     if get_foreground_app(device) != app_name:
    #         start_nonogram(device)
    #
    #     save_screenshot(device)
    #
    #     # tap the big blue button
    #     device.shell('input tap 720 2564')
    #     time.sleep(2)
    #
    #     save_screenshot(device)
