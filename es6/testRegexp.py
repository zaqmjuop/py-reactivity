from Regexp import Regexp
import re


def main():

    # Python3中「正则表达式」是一个特殊的「字符序列」
    # 一个正则表达式
    reg1 = r"hello"
    print(reg1, type(reg1))  # hello <class 'str'>

    # 正则表达式的方法
    def regExec(regexp, text):
        searchRes = re.search(regexp, text)
        res = {
            "0": searchRes.group(),
            "index": searchRes.span()[0],
            "input": text,
            "groups": searchRes.groups() if len(searchRes.groups()) else None
        } if searchRes else None
        return res

    # {'0': 'e', 'index': 2, 'input': 'The best things in life are free', 'groups': None}
    print(regExec(r'e', "The best things in life are free"))
    # {'0': 'free', 'index': 28, 'input': 'The best things in life are free', 'groups': ('e',)}
    print(regExec(r'fr(e)e', "The best things in life are free"))
    print(regExec(r'1', "The best things in life are free"))  # None

    def regTest(regexp, text):
        searchRes = re.search(regexp, text)
        return bool(searchRes)

    print(regTest(r'e', "The best things in life are free"))  # True
    print(regTest(r'fr(e)e', "The best things in life are free"))  # True
    print(regTest(r'1', "The best things in life are free"))  # False

    # toString()	返回正则表达式的字符串值。
    def regToString(regexp):
        return re.sub(r'\\(.)', r'\1', regexp)

    print(regToString(r'hello\.world'))  # hello.world

    def strToReg(text):
        return re.escape(text)

    print(strToReg('hello.world'))  # hello\.world

    # global	检查是否设置了 "g" 修饰符。
    # 没有在python里找到这个修饰符。
    # 可以用 re.findall(regexp, text) 进行全局匹配
    text1 = 'hello world, hello python, hello regex'
    reg1 = r'hello (\w+)'
    matches = re.findall(reg1, text1)
    print(matches)  # ['world', 'python', 'regex']

    # ignoreCase	检查是否设置了 "i" 修饰符。
    def regHasI(regexp):
        flags = re.compile(regexp).flags
        return bool(flags & re.IGNORECASE)

    print(regHasI(r'(?im)^hello$'))  # True
    print(regHasI(r'^hello$'))  # False
    # <re.Match object; span=(0, 5), match='hello'>
    print(re.search(r'(?im)^hello$', 'hello'))
    # <re.Match object; span=(0, 5), match='Hello'>
    print(re.search(r'(?im)^hello$', 'Hello'))
    # <re.Match object; span=(0, 5), match='hEllo'>
    print(re.search(r'(?im)^hello$', 'hEllo'))
    # <re.Match object; span=(0, 5), match='heLlo'>
    print(re.search(r'(?im)^hello$', 'heLlo'))
    # <re.Match object; span=(0, 5), match='helLo'>
    print(re.search(r'(?im)^hello$', 'helLo'))
    print(re.search(r'(?im)^hello$', 'qhelLo'))  # None
    print(re.search(r'(?im)^hello$', 'helLoq'))  # None

    # multiline	检查是否设置了 "m" 修饰符。
    def regHasM(regexp):
        flags = re.compile(regexp).flags
        return bool(flags & re.MULTILINE)

    print(regHasM(r'(?im)^hello$'))  # True
    print(regHasM(r'^hello$'))  # False

    # 正则语法

    # [abc]	查找括号之间的任何字符。
    # <re.Match object; span=(1, 2), match='b'>
    print(re.search(r"[abc]", "qbbb"))
    print(re.search(r"[abc]", "qqq"))  # None

    # [^abc]	查找任何不在方括号之间的字符。
    print(re.search(r"[^abc]", "bbbb"))  # None
    # <re.Match object; span=(0, 1), match='q'>
    print(re.search(r"[^abc]", "qqq"))

    # [0-9]	查找任何从 0 至 9 的数字。
    # <re.Match object; span=(1, 2), match='2'>
    print(re.search(r"[0-9]", "b2bb"))
    print(re.search(r"[0-9]", "qqq"))  # None

    # [^0-9]	查找任何不在括号内的字符（任何非数字）。
    print(re.search(r"[^0-9]", "4444"))  # None
    # <re.Match object; span=(0, 1), match='q'>
    print(re.search(r"[^0-9]", "qqq"))

    # (x|y)	查找任何指定的选项。
    # <re.Match object; span=(4, 9), match='green'>
    print(re.search(r"(red|green)", "re, green, red, green, gren, gr, blue, yellow"))
    print(re.search(r"(qqqq|www)",
          "re, green, red, green, gren, gr, blue, yellow"))  # None

    # .	查找单个字符，除了换行符或行终止符。
    # <re.Match object; span=(1, 4), match='hat'>
    print(re.search(r"h.t", "That's hot!"))
    # <re.Match object; span=(7, 10), match='hot'>
    print(re.search(r"h.t", "Th\nt's hot!"))

    # \w	查找单词字符。单词字符是字符 a-z、A-Z、0-9，包括 _（下划线）。
    # ['G', 'i', 'v', 'e', '1', '0', '0']
    print(re.findall(r"\w", "Give 100%!"))

    # \W	查找非单词字符
    print(re.findall(r"\W", "Give 100%!"))  # [' ', '%', '!']

    # \d	查找数字。
    print(re.findall(r"\d", "Give 100%!"))  # ['1', '0', '0']

    # \D	查找非数字字符。
    # ['G', 'i', 'v', 'e', ' ', '%', '!']
    print(re.findall(r"\D", "Give 100%!"))

    # \s	查找空白字符。
    print(re.findall(r"\s", "Give 100%!"))  # [' ']

    # \S	查找非空白字符。
    # ['G', 'i', 'v', 'e', '1', '0', '0', '%', '!']
    print(re.findall(r"\S", "Give 100%!"))

    # \b	在单词的开头/结尾查找匹配项，开头如下：\bHI，结尾如下：HI\b。
    # 在单词开头搜索模式 LO：
    # <re.Match object; span=(7, 9), match='LO'>
    print(re.search(r"\bLO", "HELLO, LOOK AT YOU"))
    # 在单词末尾搜索模式 LO
    # <re.Match object; span=(3, 5), match='LO'>
    print(re.search(r"LO\b", "HELLO, LOOK AT YOU"))

    # \B	查找匹配项，但不在单词的开头/结尾处。
    # 搜索模式 LO，不在单词开头
    # <re.Match object; span=(3, 5), match='LO'>
    print(re.search(r"\BLO", "HELLO, LOOK AT YOU"))
    # 搜索模式 LO，不在单词末尾：
    # <re.Match object; span=(7, 9), match='LO'>
    print(re.search(r"LO\B", "HELLO, LOOK AT YOU"))

    # \n	查找换行符。
    # <re.Match object; span=(15, 16), match='\n'>
    print(re.search(r"\n", "Visit w3school.\nLearn Javascript."))

    # \f	查找换页符。
    # <re.Match object; span=(15, 16), match='\x0c'>
    print(re.search(r"\f", "Visit w3school.\fLearn Javascript."))

    # \r	查找回车符。
    # <re.Match object; span=(15, 16), match='\r'>
    print(re.search(r"\r", "Visit w3school.\rLearn Javascript."))

    # \t	查找制表符。
    # <re.Match object; span=(15, 16), match='\t'>
    print(re.search(r"\t", "Visit w3school.\tLearn Javascript."))

    # \v	查找垂直制表符。
    # <re.Match object; span=(15, 16), match='\x0b'>
    print(re.search(r"\v", "Visit w3school.\vLearn Javascript."))

    # \xxx	查找以八进制数 xxx 规定的字符
    print(re.findall(r"\127", "Visit W3School. Hello World!"))  # ['W', 'W']

    # \xdd	查找以十六进制数 dd 规定的字符。
    print(re.findall(r"\x57", "Visit W3School. Hello World!"))  # ['W', 'W']

    # \uxxxx	查找以十六进制数 xxxx 规定的 Unicode 字符。
    print(re.findall(r"\u0057", "Visit W3School. Hello World!"))  # ['W', 'W']

    # n+	匹配任何包含至少一个 n 的字符串。
    # ['Hellooo', 'World', 'Hello', 'W3School']
    print(re.findall(r"\w+", "Hellooo World! Hello W3School!"))

    # n*	匹配任何包含零个或多个 n 的字符串。
    # ['l', 'looo', 'l', 'l', 'lo', 'l']
    print(re.findall(r"lo*", "Hellooo World! Hello W3School!"))

    # n?	匹配任何包含零个或一个 n 的字符串。
    print(re.findall(r"10?", "1, 100 or 1000?"))  # ['1', '10', '10']

    # n{X}	匹配包含 X 个 n 的序列的字符串。
    print(re.findall(r"\d{4}", "1, 100 or 1000?"))  # ['1000']

    # n{X,Y}	匹配包含 X 至 Y 个 n 的序列的字符串。
    print(re.findall(r"\d{3,4}", "1, 100 or 1000?"))  # ['100', '1000']

    # n{X,}	匹配包含至少 X 个 n 的序列的字符串。
    print(re.findall(r"\d{3,}", "1, 100 or 1000?"))  # ['100', '1000']

    # n$	匹配任何以 n 结尾的字符串。
    # <re.Match object; span=(9, 11), match='is'>
    print(re.search(r"is$", "Is this his"))

    # ^n	匹配任何以 n 开头的字符串。
    # <re.Match object; span=(0, 2), match='Is'>
    print(re.search(r"^Is", "Is this his"))

    # ?=n	匹配任何其后紧接指定字符串 n 的字符串。
    print(re.findall(r"is(?= all)", "Is this all there is"))  # ['is']

    # ?!n	匹配任何其后没有紧接指定字符串 n 的字符串。
    # ['Is', 'is']
    print(re.findall(r"(?i)is(?! all)", "Is this all there is"))


if __name__ == "__main__":
    main()
