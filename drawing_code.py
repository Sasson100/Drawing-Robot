import time
from machine import Pin, SPI
from button import Button
from joystick import Joystick
import st7789py as st7789
from xglcd_font import XglcdFont

display = st7789.ST7789(
    SPI(
        1,
        polarity=1, phase=1,
        baudrate=30000000,
        sck=Pin(18),
        mosi=Pin(5),
        miso=Pin(19)
    ),
    240,
    320,
    cs=Pin(4,Pin.OUT),
    dc=Pin(17,Pin.OUT),
    reset=Pin(16,Pin.OUT),
    rotation=2,
    color_order=st7789.BGR
)
display.inversion_mode(False)
font = XglcdFont('lib/FixedFont5x8.c', 5, 8)


joystick = Joystick(14,27,12)
button = Button(22)

x_pos = 0
y_pos = 0
size = 10
color_dict = {
    "red": 255,
    "green": 0,
    "blue": 0
}
color = st7789.color565(**color_dict)
white = st7789.WHITE
black = st7789.BLACK
size = 3
in_menu = False
menu_pos = 0

display.fill_rect(0,240,240,5,white)

display.text_xglcd(font,f"Size = {size}",10,270,white)
display.text_xglcd(font,f"Red = {color_dict["red"]}",10,280,white)
display.text_xglcd(font,f"Green = {color_dict["green"]}",10,290,white)
display.text_xglcd(font,f"Blue = {color_dict["blue"]}",10,300,white)

display.fill_rect(150,270,size,size,color)

while True:
    if (d:=joystick.direction_point) != (0,0):
        if in_menu:
            if abs(d[0]) == 0:
                display.fill_rect(5,(menu_pos+1)*10+260,3,8,black)
                menu_pos = (menu_pos-d[1])%4
                display.fill_rect(5,(menu_pos+1)*10+260,3,8,white)
                time.sleep_ms(500) 
            else:
                if menu_pos == 0:
                    if d[0] == -1:
                        display.vline(150+size-1,270,size,black)
                        display.hline(150,270+size-1,size,black)
                    size = max(1,min(50,size+d[0]))
                    display.text_xglcd(font,f"Size = {size}  ",10,270,white)
                else:
                    color_cap = ["Red","Green","Blue"][menu_pos-1]
                    color_lower = color_cap.lower()
                    color_dict[color_lower] = (color_dict[color_lower]+d[0])%256
                    color = st7789.color565(**color_dict)
                    display.text_xglcd(font,f"{color_cap} = {color_dict[color_lower]}  ",10,10*menu_pos+270,white)
                display.fill_rect(150,270,size,size,color)   
                time.sleep_ms(50)
        else:
            x_pos = (x_pos+d[0])%(241-size)
            y_pos = (y_pos-d[1])%(241-size)
            size_x = min(239,max(0,x_pos+size))-x_pos
            size_y = min(239,max(0,y_pos+size))-y_pos
            display.fill_rect(x_pos,y_pos,size,size,color)
            time.sleep_ms(50)

    if button.was_pressed():
        in_menu = not in_menu
        if in_menu:
            menu_pos = 0
            display.fill_rect(5,270,3,8,white)
        else:
            display.fill_rect(5,270,3,38,black)