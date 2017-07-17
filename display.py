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


WAKE_UP = 2
RESET = 3

COMMANDS = {
    "handshake": [0xA5, 0x00, 0x09, CMD_HANDSHAKE, 0xCC, 0x33, 0xC3, 0x3C],
    "read_baud": [0xA5, 0x00, 0x09, CMD_READ_BAUD, 0xCC, 0x33, 0xC3, 0x3C],
    "stopmode": [0xA5, 0x00, 0x09, CMD_STOPMODE, 0xCC, 0x33, 0xC3, 0x3C],
    "update": [0xA5, 0x00, 0x09, CMD_UPDATE, 0xCC, 0x33, 0xC3, 0x3C],
    "load_font": [0xA5, 0x00, 0x09, CMD_LOAD_FONT, 0xCC, 0x33, 0xC3, 0x3C],
    "load_pic": [0xA5, 0x00, 0x09, CMD_LOAD_PIC, 0xCC, 0x33, 0xC3, 0x3C]
}

class Display:
    def __init__(self, tx, rx, wake_up, reset, uart_num=1):
        self.wpin = wake_up
        self.rpin = reset
        self.uart = machine.UART(1, baudrate=115200, tx=tx, rx=rx)
        self.wpin.set(1)
        self.rpin.set(1)

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

    def _send_cmd(command):
        command = command + self._verify(command)
        self.uart.write(command)

    def _prepare_command(command, data=None):
        msg_body = bytes([command])
        if data is not None:
            msg_body += data
        msg_len = len(msg_body) + 8

        msg = bytes([FRAME_B,
                    (msg_len >> 8) & 0xFF,
                    msg_len & 0xFF])


    def update():

epd_init();
epd_wakeup();
epd_set_memory(MEM_NAND);
