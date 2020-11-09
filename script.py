import datetime
import time
import requests

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, TINY_FONT, SINCLAIR_FONT

appid = "e8bd7521d1c97dea05da0928c20e94e4"

def int_around(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def offset_num(number):
    if number == "1":
        return 2
    return 0


def drawCelcius(draw, fromX):
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    fromX += 2
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 6), fill="white")


def drawMinus(draw, fromX):
    draw.point((fromX, 3), fill="white")
    draw.point((fromX + 1, 3), fill="white")
    draw.point((fromX + 2, 3), fill="white")


def drawCloudRain(draw, fromX):
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 7), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 7), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 7), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 6), fill="white")


def drawCloud(draw, fromX):
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX = fromX + 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")


def drawSun(draw, fromX):
    fromX += 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    fromX += 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 4), fill="white")


def drawSnow(draw, fromX):
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 5), fill="white")
    fromX += 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 4), fill="white")
    draw.point((fromX, 5), fill="white")
    fromX += 1
    draw.point((fromX, 0), fill="white")
    draw.point((fromX, 3), fill="white")
    draw.point((fromX, 6), fill="white")
    fromX += 1
    draw.point((fromX, 2), fill="white")
    draw.point((fromX, 4), fill="white")
    fromX += 1
    draw.point((fromX, 1), fill="white")
    draw.point((fromX, 5), fill="white")


weather_type = {
    "Atmosphere" : drawCloud,
    "Clouds" : drawCloud,
    "Snow" : drawSnow,
    "Thunderstorm" : drawCloudRain,
    "Drizzle" : drawCloudRain,
    "Rain" : drawCloudRain,
    "Clear" : drawSun
}

try:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=8, rotate=0, block_orientation=-90)
    device.contrast(25)
    print("Created device")

    offset = datetime.timezone(datetime.timedelta(hours=3))
    city = "Saint Petersburg"
    temp = 0
    weather = "Clear"
    count = 1800
    while True:
        now = datetime.datetime.now(offset)
        if count == 1800:
            try:
                import pymyip
                city = pymyip.get_city()
                print(city)
            except:
                print("NO INTERNET")

            try:
                response = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + appid)
                if (response.status_code != 404) :
                    temp = int_around(response.json().get("main").get("temp") - 273.15)
                    weather = response.json().get("weather")[0].get("main")
                    timezone = int(response.json().get("timezone")) / 3600
                    offset = datetime.timezone(datetime.timedelta(hours=timezone))
                count = 0
            except requests.ConnectionError:
                count = 1620

        with canvas(device) as draw:
            hourFirst = str(int(now.hour / 10))
            hourSecond = str(int(now.hour % 10))
            minuteFirst = str(int(now.minute / 10))
            minuteSecond = str(int(now.minute % 10))
            text(draw, (3 + offset_num(hourFirst), 0), hourFirst, fill="white", font=proportional(LCD_FONT))
            text(draw, (9 + offset_num(hourSecond), 0), hourSecond, fill="white", font=proportional(LCD_FONT))
            text(draw, (15, 0), ":", fill="white", font=proportional(LCD_FONT))
            text(draw, (18 + offset_num(minuteFirst), 0), minuteFirst, fill="white", font=proportional(LCD_FONT))
            text(draw, (24 + offset_num(minuteSecond), 0), minuteSecond, fill="white", font=proportional(LCD_FONT))

            weather_type[weather](draw, 32)

            i = 45
            for number in str(temp):
                if number == "-":
                    drawMinus(draw, 41)
                    continue
                text(draw, (i + offset_num(number), 0), number, fill="white", font=proportional(LCD_FONT))
                i += 6

            drawCelcius(draw, 57)

        count += 1
        time.sleep(1)

except KeyboardInterrupt:
    pass
