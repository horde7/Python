import subprocess
subprocess.run('', shell=True)

# Dokumentation for escape sequences
# https://www2.math.upenn.edu/~kazdan/210/computer/ansi.html
# https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
print('\033[10;15H', end='')  # go to coords
print("aaaaaaaaaaaa")
print("aaaaaaaaaaaa")
print("aaaaaaaaaaaa")
print("aaaaaaaaaaaa")
print('aaaaaaaaaaaa')
print('aaaaaaaaaaaa')
print('\033[3A', end='')  # 3 rows up

print(' enter password : \0337', end='')
print('\n\n\t2 attempts remaining .\0338', end='')
x = input()