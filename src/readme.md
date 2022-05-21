ADB input keys:
==
https://forum.xda-developers.com/t/q-adb-input-keyevent-for-long-press-on-power-button.2063741/#post-64890206
https://elementalx.org/button-mapper/android-key-codes/

Example:
--
```bash
# press buttons on the device
adb shell input keyevent 26 # --> Turn power on/off
adb shell input keyevent 66 # --> enter
adb shell input keyevent --longpress KEYCODE_POWER  # --> press long on a certain key

# click somewhere
adb shell input tap '440 200'  # 440 = x, 200 = y coordinates

# type text
adb shell input text "{text_to_type}"  # make sure you have the quotation marks around your text

# Swipe
adb shell input swipe x1 y1 x2 y2 [duration in ms]  # Swipe from (x1, y1) -> (x2, y2)
# Simulating longpress
adb shell input swipe x1 y1 x1 y1 [250]  # coord1 == coord2, but duration is longer  
```

Complete list of ADB keycodes:
--
| Name | Nr | Explanation |
|---|---|---|
| KEYCODE_UNKNOWN | 0 | Unknown key code |
| KEYCODE_SOFT_LEFT | 1 | Soft Left key |
| KEYCODE_SOFT_RIGHT | 2 | Soft Right key |
| KEYCODE_HOME | 3 | Home key |
| KEYCODE_BACK | 4 | Back key |
| KEYCODE_CALL | 5 | Call key |
| KEYCODE_ENDCALL | 6 | End Call key |
| KEYCODE_0 | 7 | '0' key |
| KEYCODE_1 | 8 | '1' key |
| KEYCODE_2 | 9 | '2' key |
| KEYCODE_3 | 10 | '3' key |
| KEYCODE_4 | 11 | '4' key |
| KEYCODE_5 | 12 | '5' key |
| KEYCODE_6 | 13 | '6' key |
| KEYCODE_7 | 14 | '7' key |
| KEYCODE_8 | 15 | '8' key |
| KEYCODE_9 | 16 | '9' key |
| KEYCODE_STAR | 17 | '*' key |
| KEYCODE_POUND | 18 | '#' key |
| KEYCODE_DPAD_UP | 19 | Directional Pad Up key |
| KEYCODE_DPAD_DOWN | 20 | Directional Pad Down key |
| KEYCODE_DPAD_LEFT | 21 | Directional Pad Left key |
| KEYCODE_DPAD_RIGHT | 22 | Directional Pad Right key |
| KEYCODE_DPAD_CENTER | 23 | Directional Pad Center key |
| KEYCODE_VOLUME_UP | 24 | Volume Up key |
| KEYCODE_VOLUME_DOWN | 25 | Volume Down key |
| KEYCODE_POWER | 26 | Power key |
| KEYCODE_CAMERA | 27 | Camera key |
| KEYCODE_CLEAR | 28 | Clear key |
| KEYCODE_A | 29 | 'A' key |
| KEYCODE_B | 30 | 'B' key |
| KEYCODE_C | 31 | 'C' key |
| KEYCODE_D | 32 | 'D' key |
| KEYCODE_E | 33 | 'E' key |
| KEYCODE_F | 34 | 'F' key |
| KEYCODE_G | 35 | 'G' key |
| KEYCODE_H | 36 | 'H' key |
| KEYCODE_I | 37 | 'I' key |
| KEYCODE_J | 38 | 'J' key |
| KEYCODE_K | 39 | 'K' key |
| KEYCODE_L | 40 | 'L' key |
| KEYCODE_M | 41 | 'M' key |
| KEYCODE_N | 42 | 'N' key |
| KEYCODE_O | 43 | 'O' key |
| KEYCODE_P | 44 | 'P' key |
| KEYCODE_Q | 45 | 'Q' key |
| KEYCODE_R | 46 | 'R' key |
| KEYCODE_S | 47 | 'S' key |
| KEYCODE_T | 48 | 'T' key |
| KEYCODE_U | 49 | 'U' key |
| KEYCODE_V | 50 | 'V' key |
| KEYCODE_W | 51 | 'W' key |
| KEYCODE_X | 52 | 'X' key |
| KEYCODE_Y | 53 | 'Y' key |
| KEYCODE_Z | 54 | 'Z' key |
| KEYCODE_COMMA | 55 | ',' key |
| KEYCODE_PERIOD | 56 | '.' key |
| KEYCODE_ALT_LEFT | 57 | Left Alt modifier key |
| KEYCODE_ALT_RIGHT | 58 | Right Alt modifier key |
| KEYCODE_SHIFT_LEFT | 59 | Left Shift modifier key |
| KEYCODE_SHIFT_RIGHT | 60 | Right Shift modifier key |
| KEYCODE_TAB | 61 | Tab key |
| KEYCODE_SPACE | 62 | Space key |
| KEYCODE_SYM | 63 | Symbol modifier key |
| KEYCODE_EXPLORER | 64 | Explorer special function key |
| KEYCODE_ENVELOPE | 65 | Envelope special function key |
| KEYCODE_ENTER | 66 | Enter key |
| KEYCODE_DEL | 67 | Backspace key |
| KEYCODE_GRAVE | 68 | '`' (backtick) key |
| KEYCODE_MINUS | 69 | '-' |
| KEYCODE_EQUALS | 70 | ' = ' key |
| KEYCODE_LEFT_BRACKET | 71 | '[' key |
| KEYCODE_RIGHT_BRACKET | 72 | ']' key |
| KEYCODE_BACKSLASH | 73 | '\' key |
| KEYCODE_SEMICOLON | 74 | ';' key |
| KEYCODE_APOSTROPHE | 75 | ”' (apostrophe) key |
| KEYCODE_SLASH | 76 | '/' key |
| KEYCODE_AT | 77 | '@' key |
| KEYCODE_NUM | 78 | Number modifier key |
| KEYCODE_HEADSETHOOK | 79 | Headset Hook key |
| KEYCODE_FOCUS | 80 | Camera Focus key |
| KEYCODE_PLUS | 81 | '+' key |
| KEYCODE_MENU | 82 | Menu key |
| KEYCODE_NOTIFICATION | 83 | Notification key |
| KEYCODE_SEARCH | 84 | Search key |
| KEYCODE_MEDIA_PLAY_PAUSE | 85 | Play/Pause media key |
| KEYCODE_MEDIA_STOP | 86 | Stop media key |
| KEYCODE_MEDIA_NEXT | 87 | Play Next media key |
| KEYCODE_MEDIA_PREVIOUS | 88 | Play Previous media key |
| KEYCODE_MEDIA_REWIND | 89 | Rewind media key |
| KEYCODE_MEDIA_FAST_FORWARD | 90 | Fast Forward media key |
| KEYCODE_MUTE | 91 | Mute key |
| KEYCODE_PAGE_UP | 92 | Page Up key |
| KEYCODE_PAGE_DOWN | 93 | Page Down key |
| KEYCODE_PICTSYMBOLS | 94 | Picture Symbols modifier key |
| KEYCODE_SWITCH_CHARSET | 95 | Switch Charset modifier key |
| KEYCODE_BUTTON_A | 96 | A Button key |
| KEYCODE_BUTTON_B | 97 | B Button key |
| KEYCODE_BUTTON_C | 98 | C Button key |
| KEYCODE_BUTTON_X | 99 | X Button key |
| KEYCODE_BUTTON_Y | 100 | Y Button key |
| KEYCODE_BUTTON_Z | 101 | Z Button key |
| KEYCODE_BUTTON_L1 | 102 | L1 Button key |
| KEYCODE_BUTTON_R1 | 103 | R1 Button key |
| KEYCODE_BUTTON_L2 | 104 | L2 Button key |
| KEYCODE_BUTTON_R2 | 105 | R2 Button key |
| KEYCODE_BUTTON_THUMBL | 106 | Left Thumb Button key |
| KEYCODE_BUTTON_THUMBR | 107 | Right Thumb Button key |
| KEYCODE_BUTTON_START | 108 | Start Button key |
| KEYCODE_BUTTON_SELECT | 109 | Select Button key |
| KEYCODE_BUTTON_MODE | 110 | Mode Button key |
| KEYCODE_ESCAPE | 111 | Escape key |
| KEYCODE_FORWARD_DEL | 112 | Forward Delete key |
| KEYCODE_CTRL_LEFT | 113 | Left Control modifier key |
| KEYCODE_CTRL_RIGHT | 114 | Right Control modifier key |
| KEYCODE_CAPS_LOCK | 115 | Caps Lock key |
| KEYCODE_SCROLL_LOCK | 116 | Scroll Lock key |
| KEYCODE_META_LEFT | 117 | Left Meta modifier key |
| KEYCODE_META_RIGHT | 118 | Right Meta modifier key |
| KEYCODE_FUNCTION | 119 | Function modifier key |
| KEYCODE_SYSRQ | 120 | System Request / Print Screen key |
| KEYCODE_BREAK | 121 | Break / Pause key |
| KEYCODE_MOVE_HOME | 122 | Home Movement key |
| KEYCODE_MOVE_END | 123 | End Movement key |
| KEYCODE_INSERT | 124 | Insert key |
| KEYCODE_FORWARD | 125 | Forward key |
| KEYCODE_MEDIA_PLAY | 126 | Play media key |
| KEYCODE_MEDIA_PAUSE | 127 | Pause media key |
| KEYCODE_MEDIA_CLOSE | 128 | Close media key |
| KEYCODE_MEDIA_EJECT | 129 | Eject media key |
| KEYCODE_MEDIA_RECORD | 130 | Record media key |
| KEYCODE_F1 | 131 | F1 key |
| KEYCODE_F2 | 132 | F2 key |
| KEYCODE_F3 | 133 | F3 key |
| KEYCODE_F4 | 134 | F4 key |
| KEYCODE_F5 | 135 | F5 key |
| KEYCODE_F6 | 136 | F6 key |
| KEYCODE_F7 | 137 | F7 key |
| KEYCODE_F8 | 138 | F8 key |
| KEYCODE_F9 | 139 | F9 key |
| KEYCODE_F10 | 140 | F10 key |
| KEYCODE_F11 | 141 | F11 key |
| KEYCODE_F12 | 142 | F12 key |
| KEYCODE_NUM_LOCK | 143 | Num Lock key |
| KEYCODE_NUMPAD_0 | 144 | Numeric keypad '0' key |
| KEYCODE_NUMPAD_1 | 145 | Numeric keypad '1' key |
| KEYCODE_NUMPAD_2 | 146 | Numeric keypad '2' key |
| KEYCODE_NUMPAD_3 | 147 | Numeric keypad '3' key |
| KEYCODE_NUMPAD_4 | 148 | Numeric keypad '4' key |
| KEYCODE_NUMPAD_5 | 149 | Numeric keypad '5' key |
| KEYCODE_NUMPAD_6 | 150 | Numeric keypad '6' key |
| KEYCODE_NUMPAD_7 | 151 | Numeric keypad '7' key |
| KEYCODE_NUMPAD_8 | 152 | Numeric keypad '8' key |
| KEYCODE_NUMPAD_9 | 153 | Numeric keypad '9' key |
| KEYCODE_NUMPAD_DIVIDE | 154 | Numeric keypad '/' key (for division) |
| KEYCODE_NUMPAD_MULTIPLY | 155 | Numeric keypad '*' key (for multiplication) |
| KEYCODE_NUMPAD_SUBTRACT | 156 | Numeric keypad '-' key (for subtraction) |
| KEYCODE_NUMPAD_ADD | 157 | Numeric keypad '+' key (for addition) |
| KEYCODE_NUMPAD_DOT | 158 | Numeric keypad '.' key (for decimals or digit grouping) |
| KEYCODE_NUMPAD_COMMA | 159 | Numeric keypad ',' key (for decimals or digit grouping) |
| KEYCODE_NUMPAD_ENTER | 160 | Numeric keypad Enter key |
| KEYCODE_NUMPAD_EQUALS | 161 | Numeric keypad ' = ' key |
| KEYCODE_NUMPAD_LEFT_PAREN | 162 | Numeric keypad '(' key |
| KEYCODE_NUMPAD_RIGHT_PAREN | 163 | Numeric keypad ')' key |
| KEYCODE_VOLUME_MUTE | 164 | Volume Mute key |
| KEYCODE_INFO | 165 | Info key |
| KEYCODE_CHANNEL_UP | 166 | Channel up key |
| KEYCODE_CHANNEL_DOWN | 167 | Channel down key |
| KEYCODE_ZOOM_IN | 168 | Zoom in key |
| KEYCODE_ZOOM_OUT | 169 | Zoom out key |
| KEYCODE_TV | 170 | TV key |
| KEYCODE_WINDOW | 171 | Window key |
| KEYCODE_GUIDE | 172 | Guide key |
| KEYCODE_DVR | 173 | DVR key |
| KEYCODE_BOOKMARK | 174 | Bookmark key |
| KEYCODE_CAPTIONS | 175 | Toggle captions key |
| KEYCODE_SETTINGS | 176 | Settings key |
| KEYCODE_TV_POWER | 177 | TV power key |
| KEYCODE_TV_INPUT | 178 | TV input key |
| KEYCODE_STB_POWER | 179 | Set-top-box power key |
| KEYCODE_STB_INPUT | 180 | Set-top-box input key |
| KEYCODE_AVR_POWER | 181 | A/V Receiver power key |
| KEYCODE_AVR_INPUT | 182 | A/V Receiver input key |
| KEYCODE_PROG_RED | 183 | Red “programmable” key |
| KEYCODE_PROG_GREEN | 184 | Green “programmable” key |
| KEYCODE_PROG_YELLOW | 185 | Yellow “programmable” key |
| KEYCODE_PROG_BLUE | 186 | Blue “programmable” key |
| KEYCODE_APP_SWITCH | 187 | App switch key |
| KEYCODE_BUTTON_1 | 188 | Generic Game Pad Button #1 |
| KEYCODE_BUTTON_2 | 189 | Generic Game Pad Button #2 |
| KEYCODE_BUTTON_3 | 190 | Generic Game Pad Button #3 |
| KEYCODE_BUTTON_4 | 191 | Generic Game Pad Button #4 |
| KEYCODE_BUTTON_5 | 192 | Generic Game Pad Button #5 |
| KEYCODE_BUTTON_6 | 193 | Generic Game Pad Button #6 |
| KEYCODE_BUTTON_7 | 194 | Generic Game Pad Button #7 |
| KEYCODE_BUTTON_8 | 195 | Generic Game Pad Button #8 |
| KEYCODE_BUTTON_9 | 196 | Generic Game Pad Button #9 |
| KEYCODE_BUTTON_10 | 197 | Generic Game Pad Button #10 |
| KEYCODE_BUTTON_11 | 198 | Generic Game Pad Button #11 |
| KEYCODE_BUTTON_12 | 199 | Generic Game Pad Button #12 |
| KEYCODE_BUTTON_13 | 200 | Generic Game Pad Button #13 |
| KEYCODE_BUTTON_14 | 201 | Generic Game Pad Button #14 |
| KEYCODE_BUTTON_15 | 202 | Generic Game Pad Button #15 |
| KEYCODE_BUTTON_16 | 203 | Generic Game Pad Button #16 |
| KEYCODE_LANGUAGE_SWITCH | 204 | Language Switch key |
| KEYCODE_MANNER_MODE | 205 | Manner Mode key |
| KEYCODE_3D_MODE | 206 | 3D Mode key |
| KEYCODE_CONTACTS | 207 | Contacts special function key |
| KEYCODE_CALENDAR | 208 | Calendar special function key |
| KEYCODE_MUSIC | 209 | Music special function key |
| KEYCODE_CALCULATOR | 210 | Calculator special function key |
| KEYCODE_ZENKAKU_HANKAKU | 211 | Japanese full-width / half-width key |
| KEYCODE_EISU | 212 | Japanese alphanumeric key |
| KEYCODE_MUHENKAN | 213 | Japanese non-conversion key |
| KEYCODE_HENKAN | 214 | Japanese conversion key |
| KEYCODE_KATAKANA_HIRAGANA | 215 | Japanese katakana / hiragana key |
| KEYCODE_YEN | 216 | Japanese Yen key |
| KEYCODE_RO | 217 | Japanese Ro key |
| KEYCODE_KANA | 218 | Japanese kana key |
| KEYCODE_ASSIST | 219 | Assist key |
| KEYCODE_BRIGHTNESS_DOWN | 220 | Brightness Down key |
| KEYCODE_BRIGHTNESS_UP | 221 | Brightness Up key |
| KEYCODE_MEDIA_AUDIO_TRACK | 222 | Audio Track key |
| KEYCODE_SLEEP | 223 | Sleep key |
| KEYCODE_WAKEUP | 224 | Wakeup key |
| KEYCODE_PAIRING | 225 | Pairing key |
| KEYCODE_MEDIA_TOP_MENU | 226 | Media Top Menu key |
| KEYCODE_11 | 227 | '11' key |
| KEYCODE_12 | 228 | '12' key |
| KEYCODE_LAST_CHANNEL | 229 | Last Channel key |
| KEYCODE_TV_DATA_SERVICE | 230 | TV data service key |
| KEYCODE_VOICE_ASSIST | 231 | Voice Assist key |
| KEYCODE_TV_RADIO_SERVICE | 232 | Radio key |
| KEYCODE_TV_TELETEXT | 233 | Teletext key |
| KEYCODE_TV_NUMBER_ENTRY | 234 | Number entry key |
| KEYCODE_TV_TERRESTRIAL_ANALOG | 235 | Analog Terrestrial key |
| KEYCODE_TV_TERRESTRIAL_DIGITAL | 236 | Digital Terrestrial key |
| KEYCODE_TV_SATELLITE | 237 | Satellite key |
| KEYCODE_TV_SATELLITE_BS | 238 | BS key |
| KEYCODE_TV_SATELLITE_CS | 239 | CS key |
| KEYCODE_TV_SATELLITE_SERVICE | 240 | BS/CS key |
| KEYCODE_TV_NETWORK | 241 | Toggle Network key |
| KEYCODE_TV_ANTENNA_CABLE | 242 | Antenna/Cable key |
| KEYCODE_TV_INPUT_HDMI_1 | 243 | HDMI #1 key |
| KEYCODE_TV_INPUT_HDMI_2 | 244 | HDMI #2 key |
| KEYCODE_TV_INPUT_HDMI_3 | 245 | HDMI #3 key |
| KEYCODE_TV_INPUT_HDMI_4 | 246 | HDMI #4 key |
| KEYCODE_TV_INPUT_COMPOSITE_1 | 247 | Composite #1 key |
| KEYCODE_TV_INPUT_COMPOSITE_2 | 248 | Composite #2 key |
| KEYCODE_TV_INPUT_COMPONENT_1 | 249 | Component #1 key |
| KEYCODE_TV_INPUT_COMPONENT_2 | 250 | Component #2 key |
| KEYCODE_TV_INPUT_VGA_1 | 251 | VGA #1 key |
| KEYCODE_TV_AUDIO_DESCRIPTION | 252 | Audio description key |
| KEYCODE_TV_AUDIO_DESCRIPTION_MIX_UP | 253 | Audio description mixing volume up key |
| KEYCODE_TV_AUDIO_DESCRIPTION_MIX_DOWN | 254 | Audio description mixing volume down key |
| KEYCODE_TV_ZOOM_MODE | 255 | Zoom mode key |
| KEYCODE_TV_CONTENTS_MENU | 256 | Contents menu key |
| KEYCODE_TV_MEDIA_CONTEXT_MENU | 257 | Media context menu key |
| KEYCODE_TV_TIMER_PROGRAMMING | 258 | Timer programming key |
| KEYCODE_HELP | 259 | Help key |
| KEYCODE_NAVIGATE_PREVIOUS | 260 | Navigate to previous key |
| KEYCODE_NAVIGATE_NEXT | 261 | Navigate to next key |
| KEYCODE_NAVIGATE_IN | 262 | Navigate in key |
| KEYCODE_NAVIGATE_OUT | 263 | Navigate out key |
| KEYCODE_STEM_PRIMARY | 264 | Primary stem key for Wear |
| KEYCODE_STEM_1 | 265 | Generic stem key 1 for Wear |
| KEYCODE_STEM_2 | 266 | Generic stem key 2 for Wear |
| KEYCODE_STEM_3 | 267 | Generic stem key 3 for Wear |
| KEYCODE_DPAD_UP_LEFT | 268 | Directional Pad Up-Left |
| KEYCODE_DPAD_DOWN_LEFT | 269 | Directional Pad Down-Left |
| KEYCODE_DPAD_UP_RIGHT | 270 | Directional Pad Up-Right |
| KEYCODE_DPAD_DOWN_RIGHT | 271 | Directional Pad Down-Right |
| KEYCODE_MEDIA_SKIP_FORWARD | 272 | Skip forward media key |
| KEYCODE_MEDIA_SKIP_BACKWARD | 273 | Skip backward media key |
| KEYCODE_MEDIA_STEP_FORWARD | 274 | Step forward media key |
| KEYCODE_MEDIA_STEP_BACKWARD | 275 | Step backward media key |
| KEYCODE_SOFT_SLEEP | 276 | Put device to sleep unless a wakelock is held |
| KEYCODE_CUT | 277 | Cut key |
| KEYCODE_COPY | 278 | Copy key |
| KEYCODE_PASTE | 279 | Paste key |
| KEYCODE_SYSTEM_NAVIGATION_UP | 280 | Consumed by the system for navigation up |
| KEYCODE_SYSTEM_NAVIGATION_DOWN | 281 | Consumed by the system for navigation down |
| KEYCODE_SYSTEM_NAVIGATION_LEFT | 282 | Consumed by the system for navigation left |
| KEYCODE_SYSTEM_NAVIGATION_RIGHT | 283 | Consumed by the system for navigation right |
