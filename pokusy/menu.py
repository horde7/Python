from console import *
# BORDER = '#'
BORDER = '■'
SPACE = " "
def start_menu(row: int, col: int, items: list):
    if (items.count == 0):
        pass

    maxLen = 0
    for i in items:
        if len(i) > maxLen:
            maxLen = len(i)

    borderWidth = maxLen + 6
    esc_ForeColor(2)
    cursor = 2

    key = ""
    while key != "ESC":
        esc_setYX(row, col)
        print(BORDER * borderWidth)

        itemRow = row
        itemIndex = 0
        for i in items:
            itemRow = itemRow +1
            itemIndex = itemIndex + 1
            esc_setYX(itemRow, col)
            spaces = maxLen - len(i) + 1

            if itemIndex == cursor:
                esc_Bright(True)
                print(f"{BORDER} ={i}={SPACE * spaces}{BORDER}")
                esc_Bright(False)
            else:
                print(f"{BORDER}  {i} {SPACE * spaces}{BORDER}")

        esc_setYX(row+len(items)+1, col)
        print(BORDER * borderWidth)
        key = get_key()
        print(key)
        if key == "UP" and cursor > 1:
            cursor = cursor - 1
        elif key == "DOWN" and cursor < len(items):
            cursor = cursor + 1

    # end while


def get_key():
    code = 0
    key = "?"
    while key == "?":
        # print('Esc')
        ch = m.getch()
        code = ord(ch)
        if code == 224:
            ch = m.getch()
            code = ord(ch)
            if code == 72:
                key = "UP"
            elif code == 75:
                key = "LEFT"
            elif code == 77:
                key = "RIGHT"
            elif code == 80:
                key = "DOWN"
            else:
                key = "?"

        elif code == 13:
            key = "ENTER"
        else:
            key = "?"
    # while end
    return key









