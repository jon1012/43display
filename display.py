from machine import UART, Pin
import time

CMD_SIZE = 512

# frame format
FRAME_B = 0xA5
FRAME_E0 = 0xCC
FRAME_E1 = 0x33
FRAME_E2 = 0xC3
FRAME_E3 = 0x3C

# color define
WHITE = 0x03
GRAY = 0x02
DARK_GRAY = 0x01
BLACK = 0x00

# command define
CMD_HANDSHAKE = 0x00 # handshake
CMD_SET_BAUD = 0x01 # set baud
CMD_READ_BAUD = 0x02 # read baud
CMD_MEMORYMODE = 0x07 # set memory mode
CMD_STOPMODE = 0x08 # enter stop mode
CMD_UPDATE = 0x0A # update
CMD_SCREEN_ROTATION = 0x0D # set screen rotation
CMD_LOAD_FONT = 0x0E # load font
CMD_LOAD_PIC = 0x0F # load picture
CMD_SET_COLOR = 0x10 # set color
CMD_SET_EN_FONT = 0x1E # set english font
CMD_SET_CH_FONT = 0x1F # set chinese font
CMD_DRAW_PIXEL = 0x20 # set pixel
CMD_DRAW_LINE = 0x22 # draw line
CMD_FILL_RECT = 0x24 # fill rectangle
CMD_DRAW_CIRCLE = 0x26 # draw circle
CMD_FILL_CIRCLE = 0x27 # fill circle
CMD_DRAW_TRIANGLE = 0x28 # draw triangle
CMD_FILL_TRIANGLE = 0x29 # fill triangle
CMD_CLEAR = 0x2E # clear screen use back color
CMD_DRAW_STRING = 0x30 # draw string
CMD_DRAW_BITMAP = 0x70 # draw bitmap

# FONT
GBK32 = 0x01
GBK48 = 0x02
GBK64 = 0x03

ASCII32 = 0x01
ASCII48 = 0x02
ASCII64 = 0x03

# Memory Mode
MEM_NAND = 0
MEM_TF = 1

# set screen rotation
EPD_NORMAL = 0 # screen normal
EPD_INVERSION = 1 # screen inversion

class Display:
    def __init__(self, tx, rx, wake_up, reset, uart_num=1):
        self.wpin = wake_up
        self.rpin = reset
        self.uart = UART(1, baudrate=115200, tx=tx, rx=rx)
        self.wpin.value(1)
        self.rpin.value(1)

    def _verify(self, buf):
        r = 0
        for value in buf:
            r ^= value

        return r

    def reset(self):
        self.rpin.value(0)
        time.sleep(0.001)
        self.rpin.value(1)
        time.sleep(0.001)
        self.rpin.value(0)
        time.sleep(2)

    def wake(self):
        self.wpin.value(0)
        time.sleep(0.001)
        self.wpin.value(1)
        time.sleep(0.001)
        self.wpin.value(0)
        time.sleep(0.01)

    def sleep(self):
        self.send_command(CMD_STOPMODE)

    def _send_cmd(self, command):
        command = command + bytes([self._verify(command)])
        self.uart.write(command)

    def _prepare_command(self, command, data=None):
        msg_body = bytes([command])
        if data is not None:
            msg_body += data
        msg_len = len(msg_body) + 8

        msg = bytes([FRAME_B,
                    (msg_len >> 8) & 0xFF,
                    msg_len & 0xFF])

        msg += msg_body
        msg += bytes([FRAME_E0, FRAME_E1, FRAME_E2, FRAME_E3])
        return msg

    def send_command(self, command, data=None):
        self._send_cmd(
            self._prepare_command(command, data=data))

    def set_memory(self, memory_mode):
        self.send_command(CMD_MEMORYMODE,
                          data=bytes([memory_mode]))

    def set_rotation(self, rotation_mode):
        self.send_command(CMD_SCREEN_ROTATION,
                          data=bytes([rotation_mode]))

    def set_color(self, color, bg_color=WHITE):
        self.send_command(CMD_SET_COLOR,
                          data=bytes([color, bg_color]))

    def set_en_font(self, font):
        self.send_command(CMD_SET_EN_FONT,
                          data=bytes([font]))

    def set_ch_font(self, font):
        self.send_command(CMD_SET_CH_FONT,
                          data=bytes([font]))

    def clear(self):
        self.send_command(CMD_CLEAR)

    def update(self):
        self.send_command(CMD_UPDATE)

    def load_pic(self):
        self.send_command(CMD_LOAD_PIC)

    def _send_numeric_command(self, command, values):
        buf = bytes()
        for v in values:
            buf += bytes([(v >> 8) & 0xFF,
                          v & 0xFF])
        self.send_command(command, data=buf)

    def draw_pixel(self, x, y):
        self._send_numeric_command(CMD_DRAW_PIXEL, [x, y])

    def draw_line(self, x0, y0, x1, y1):
        self._send_numeric_command(CMD_DRAW_LINE,
                                   [x0, y0, x1, y1])

    def fill_rect(self, x0, y0, x1, y1):
        self._send_numeric_command(CMD_FILL_RECT,
                                   [x0, y0, x1, y1])

    def draw_circle(self, x0, y0, r):
        self._send_numeric_command(CMD_DRAW_CIRCLE,
                                   [x0, y0, r])

    def fill_circle(self, x0, y0, r):
        self._send_numeric_command(CMD_FILL_CIRCLE,
                                   [x0, y0, r])

    def draw_triangle(self, x0, y0, x1, y1, x2, y2):
        self._send_numeric_command(CMD_DRAW_TRIANGLE,
                                   [x0, y0, x1, y1, x2, y2])

    def fill_triangle(self, x0, y0, x1, y1, x2, y2):
        self._send_numeric_command(CMD_FILL_TRIANGLE,
                                   [x0, y0, x1, y1, x2, y2])

    def text(self, text, x, y):
        buf = bytes([(x >> 8) & 0xFF,
                     x & 0xFF,
                     (y >> 8) & 0xFF,
                     y & 0xFF])
        buf += text.encode('ISO-8859-1')
        self.send_command(CMD_DRAW_STRING, data=buf)

    def draw_bitmap(self, filename, x, y):
        buf = bytes([(x >> 8) & 0xFF,
                     x & 0xFF,
                     (y >> 8) & 0xFF,
                     y & 0xFF])
        buf += filename.encode('ISO-8859-1')
        self.send_command(CMD_DRAW_BITMAP, data=buf)
        
"""
from machine import Pin
from display import Display
disp = Display(tx=12, rx=13, wake_up=Pin(14), reset=Pin(15))
# disp.reset()
disp.wake()
disp.clear()
disp.update()

epd_init()
epd_wakeup()
epd_set_memory(MEM_NAND)

"""
