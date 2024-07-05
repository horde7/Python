import msvcrt as m
import subprocess

subprocess.run('', shell=True)


def esc_setYX(row: int, col: int):
    print(f"\033[{row};{col}H", end='')  # go to coords

def esc_Bright(isSet: bool):
    if isSet:
        print("\033[1m", end='')
    else:
        print("\033[22m", end='')

def esc_ForeColor(num: int):
    col = 30+ num
    print(f"\033[{col}m", end='')

def esc_BackColor(num: int):
    col = 40+ num
    print(f"\033[{col}m", end='')



