def signe(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


tab_width = 4


def make_tab(txt):
    i = 0
    res = ""
    for char in txt:
        if char == '\t':
            res += " " * (tab_width - i)
        else:
            res += char
        i = (i + 1) % tab_width
    return res


if __name__ == '__main__':
    print(make_tab("bon\tchien"))
