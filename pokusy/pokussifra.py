import math

# ASCII codes
# https://www.ge.com/digital/documentation/tracker/version11/oxy_ex-1/topics/g_cimplicity_tracker_ascii_tablefor_code39.html
IN_BLOCK = 3
OUT_BLOCK = 4


class CompResult:
    success: bool
    value: str
    error: str

    def __init__(self, success, value, error):
        self.success = success
        self.value = value
        self.error = error

    def __str__(self):
        return str((str(self.success), self.value, self.error))


def complicate(text: str) -> CompResult:
    for c in text:
        if ord(c) < 32 or ord(c) > 127:
            return CompResult(False, "", f"Char {c} ({ord(c)}) not valid.")

    blockCount = math.ceil(len(text) / IN_BLOCK)
    adjLen = blockCount * IN_BLOCK

    blockSums = [0] * blockCount
    value = 0
    for i in range(adjLen):
        if i < len(text):
            value = ord(text[i]) - 32
        else:
            value = 127

        bI = i // IN_BLOCK
        inB = i % IN_BLOCK
        blockSums[bI] += pow(128, inB) * value

    l: list = []
    for sum in blockSums:
        rest = sum
        for i in range(4):
            val = rest % 40
            rest = rest // 40
            l.append(chr(val + 64))

    result = "".join(l)
    reversion = simplify(result)
    if reversion != text:
        return CompResult(False, "", f"Invalid reversion ({reversion})")

    return CompResult(True, result, "")
# def END


def simplify(text: str) -> str:
    resultList: list = []
    blockCount = math.ceil(len(text) / 4)
    for b in range(blockCount):
        blockSum = 0
        for i in range(OUT_BLOCK):
            val = ord(text[i + b * OUT_BLOCK]) - 64
            blockSum += val * pow(40, i)
        rest = blockSum
        for j in range(IN_BLOCK):
            val = rest % 128
            rest = rest // 128
            if (val < 127):
                resultList.append(chr(val + 32))

    return "".join(resultList)
# def END


print(f"\nValid encryption example")
_input = "123456789_!@@#$_^&*() pokus_1 ABZW"
com = complicate(_input)
sim = simplify(com.value)
print(f"Input    : >{_input}<")
print(f"Encrypted: >{com.value}<")
print(f"Decrypted: >{sim}<")
print(com)

print(f"\nInvalid encryption example")
_input = "123456789_´\¨¨'"
com = complicate(_input)
sim = simplify(com.value)
print(f"Input    : >{_input}<")
print(f"Encrypted: >{com.value}<")
print(f"Decrypted: >{sim}<")
print(com)
