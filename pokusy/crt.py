import msvcrt as m
import os as os


def move (y, x):
    print("\033[%d;%dH" % (y, x))


code = 0
# move(10,10)
os.system("")




while code != 27:
    # print('Esc')
    ch = m.getch()
    code = ord(ch)
    if code == 224:
        ch = m.getch()
        code = ord(ch)
        if code == 72:
            print('UP')
        elif code == 75:
            print('LEFT')
        elif code == 77:
            print('RIGHT')
        elif code == 80:
            print('DOWN')
        else:
            print('SomeFunction')

    elif code == 13:
        print('ENTER')
    else:
        print(chr(code))


    # hex = ch.hex()
    # print(ch.hex(), end='')
    # if ch == '\x00\x1b':
    #    print('Esc')
    # else:
    #   print('Enter')


