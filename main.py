### Author: core
### Description: Simple visual morse widget
### Category: morse
### License: MIT
### Appname: cw_flash

import ugfx, pyb, buttons

ugfx.init()
ugfx.clear()
ugfx.area(0,0,320,240,ugfx.html_color(0x00FF00))
buttons.init()
ugfx.set_default_font(ugfx.FONT_NAME)

t4 = pyb.Timer(4, freq=300, mode=pyb.Timer.CENTER)

SIGN_SCALING = 100
DOT = 1
DASH = 3
PAUSE_ELEMENT = DOT
PAUSE_CHARACTER = 3 * DOT - DOT
PAUSE_WORD = 7 * DOT - DOT

AF = True

def dot():
    if AF:
        ch1 = t4.channel(1, pyb.Timer.PWM, pin=pyb.Pin("BUZZ"), pulse_width=(t4.period() + 1) // 2)
    ugfx.area(100,75,90,90,ugfx.BLACK)
    pyb.delay(SIGN_SCALING*DOT)
    if AF:
        pyb.Pin("BUZZ",pyb.Pin.OUT).low()
    ugfx.area(0,0,320,240,ugfx.html_color(0x00FF00))
    pyb.delay(SIGN_SCALING*PAUSE_ELEMENT)

def dash():
    if AF:
        ch1 = t4.channel(1, pyb.Timer.PWM, pin=pyb.Pin("BUZZ"), pulse_width=(t4.period() + 1) // 2)
    ugfx.area(25,75,270,90,ugfx.BLACK)
    pyb.delay(SIGN_SCALING*DASH)
    if AF:
        pyb.Pin("BUZZ",pyb.Pin.OUT).low()
    ugfx.area(0,0,320,240,ugfx.html_color(0x00FF00))
    pyb.delay(SIGN_SCALING*PAUSE_ELEMENT)

CODEBOOK = {
        ' ': ' ',
        'a': '.-',
        'b': '-...',
        'c': '-.-.',
        'd': '-..',
        'e': '.',
        'f': '..-.',
        'g': '--.',
        'h': '....',
        'i': '..',
        'j': '.---',
        'k': '-.-',
        'l': '.-..',
        'm': '--',
        'n': '-.',
        'o': '---',
        'p': '.--.',
        'q': '--.-',
        'r': '.-.',
        's': '...',
        't': '-',
        'u': '..-',
        'v': '...-',
        'w': '.--',
        'x': '-..-',
        'y': '-.--',
        'z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '.': '.-.-.-', 
        ',': '--..--', 
        '?': '..--..', 
        '/': '-..-.',
        '@': '.--.-.',
        '=': '-...-',
        }

MSG = 'core'

character_buffer = ''
msg_pointer = 0
while True:
    if character_buffer is '': # fill new character
        pyb.delay(SIGN_SCALING*PAUSE_CHARACTER)
        character_buffer = CODEBOOK[MSG[msg_pointer]]
        msg_pointer = (msg_pointer + 1) % len(MSG)

    # send character

    if character_buffer[0] is '-':
        dash()
    elif character_buffer[0] is '.':
        dot()
    else:
        pyb.delay(SIGN_SCALING*PAUSE_WORD)

    if len(character_buffer) > 1:
        character_buffer = character_buffer[1:]
    else:
        character_buffer = ''

    pyb.wfi()
    if buttons.is_triggered("BTN_MENU") or buttons.is_triggered("BTN_B") or buttons.is_triggered("JOY_CENTER"):
        break;
    if buttons.is_triggered("BTN_A"):
        AF = not AF
    if buttons.is_triggered("JOY_DOWN"):
        SIGN_SCALING += 20
    if buttons.is_triggered("JOY_UP"):
        SIGN_SCALING -= 20

ugfx.clear()
