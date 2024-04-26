backup_eval = eval
def check_eval():
    a = input('try os.system("cmd")!')
    if a.find('system') != -1:
        print('NO WAY!')
        return
    else:
        try:
            backup_eval(a, {},{})
            print('SUCCESS!')
        except:
            print('ERROR!')
            pass


del __builtins__.__dict__['eval']
check_eval()
# __import__("os").__getattribute__('\x73\x79\x73\x74\x65\x6d')("cmd")

# __import__(list(dict(os=True)).__getitem__(int(any(())))).system(list(dict(cmd=True)).__getitem__(int(any(()))))
__import__(list(dict(os=True)).__getitem__(int(any(())))).system(list(dict(cmd=True)).__getitem__(int(any(()))))
