def check_eval():
    payload = input('try os.system("cmd")!')
    eval(payload, {}, {})
    try:
        eval(payload, {}, {})
        print('SUCCESS!')
    except:

        print('ERROR!')
        pass
__import__("os").system("cmd")
check_eval()
#
# __import__("os").system("cmd")
