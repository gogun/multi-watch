import datetime
import time

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, TINY_FONT, SINCLAIR_FONT


def offset_num(number):
    if number == "1":
        return 2
    return 0


try:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=8, rotate=0, block_orientation=-90)
    print("Created device")

    offset = datetime.timezone(datetime.timedelta(hours=3))
    while True:
        now = datetime.datetime.now(offset)
        with canvas(device) as draw:
            # draw.rectangle(device.bounding_box, outline="white")
            hourFirst = str(int(now.hour / 10))
            hourSecond = str(int(now.hour % 10))
            minuteFirst = str(int(now.minute / 10))
            minuteSecond = str(int(now.minute % 10))
            text(draw, (3 + offset_num(hourFirst), 1), hourFirst, fill="white", font=proportional(LCD_FONT))
            text(draw, (9 + offset_num(hourSecond), 1), hourSecond, fill="white", font=proportional(LCD_FONT))
            text(draw, (15, 1), ":", fill="white", font=proportional(LCD_FONT))
            text(draw, (18 + offset_num(minuteFirst), 1), minuteFirst, fill="white", font=proportional(LCD_FONT))
            text(draw, (24 + offset_num(minuteSecond), 1), minuteSecond, fill="white", font=proportional(LCD_FONT))
        time.sleep(1)

except KeyboardInterrupt:
    pass