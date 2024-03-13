from String import String

if __name__ == "__main__":
    print(String('qwertyuiop').charAt(2))  # e
    pass
    print(String('A').charCodeAt())  # 65
    print(String('𠮷').length)  # 1

    print(String('𠮷').codePointAt())  # 134071
    print(String('hel').concat('lo'))  # hello
    # 前11个字符是否以world结尾
    print(String("Hello world, welcome to the universe.").endsWith(
        "world", 11))  # True
    print(String.fromCharCode(65))  # A
    print(String.fromCharCode(134071))  # 𠮷
    print(String.fromCharCode(20013))  # 中

    print(String("Hello world, welcome to the universe.").includes(
        "world", 12))  # False
    print(String("Hello world, welcome to the universe.").includes(
        "world", 1))  # True
    print(String("Hello world, welcome to the universe.").indexOf("world", 12))  # -1
    print(String("Hello world, welcome to the universe.").indexOf("world", 1))  # 6
    print(String("Hello planet earth, you are a great planet.").lastIndexOf(
        'planet'))  # 36
    print(String("Hello planet earth, you are a great planet.").lastIndexOf(
        'planet', 20))  # 6
    print(String('hell').length)  # 4
    print(String('www.w3cschool.cn').match('qq'))  # None
    # {'0': '3cschoo', 'index': 5, 'input': 'www.w3cschool.cn', 'groups': None}
    print(String('www.w3cschool.cn').match('3cschoo'))
    # {'0': '3cschoo', 'index': 5, 'input': 'www.w3cschool.cn', 'groups': ('c', 'h')}
    print(String('www.w3cschool.cn').match('3(c)sc(h)oo'))
    print(String('hell').repeat(0))  # ''
    print(String('hell').repeat())  # hell
    print(String('hell').repeat(2))  # hellhell
    print(String('hell').repeat(3))  # hellhellhell
    print(String("Blue blue blue").replace(
        r'blue', 'green'))  # Blue green green
    print(String("Blue blue blue").replace(
        r'blue', 'green', 0))  # Blue blue blue
    print(String("Blue blue blue").replace(
        r'blue', 'green', 1))  # Blue green blue
    print(String("Mr. Blue has a blue house").search(
        'Blue'))  # 4
    print(String("Mr. Blue has a blue house").search(
        'blue'))  # 15
    print(String("Mr. Blue has a blue house").search(
        r'has'))  # 9
    print(String("Hello world!").slice(0, 5))  # Hello
    print(String("Hello world!").slice(1))  # ello world!
    print(String("Hello world!").slice(-1))  # !
    # ['How', 'are', 'you', 'doing', 'today?']
    print(String("How are you doing today?").split(' '))
    # ['How', 'are you doing today?']
    print(String("How are you doing today?").split(' ', 1))
    # ['How', 'are', 'you doing today?']
    print(String("How are you doing today?").split(' ', 2))
    # ['H', 'o', 'w', ' ', 'a', 'r', 'e', ' ', 'y', 'o', 'u', ' ', 'd', 'o', 'i', 'n', 'g', ' ', 't', 'o', 'd', 'a', 'y', '?']
    print(String("How are you doing today?").split(''))
    # ['H', 'ow are you doing today?']
    print(String("How are you doing today?").split('', 1))
    # ['H', 'o', 'w are you doing today?']
    print(String("How are you doing today?").split('', 2))
    print(String("Hello world, welcome to the universe.",).startsWith(
        "world", 6))  # True
    print(String("Hello world, welcome to the universe."
                 ).startsWith("world",   1))  # False
    print(String("Hello world, welcome to the universe.").startsWith(
        "Hell"))  # True
    print(String("Hello world!").substr(1, 4))  # ello
    print(String("Hello world!").substr(1, 3))  # ell
    print(String("Hello world!").substr(-5, 4))  # orld
    print(String("Hello world!").substring(6))  # world!
    print(String("Hello world!").substring(6, 9))  # wor
    print(String("Hello world!").substring(-5, -3))  # or
    print(String("Hello world!").substring(-5, 9))  # or
    print(String('我不叫Wiz 我叫Khalifa').toLowerCase())  # 我不叫wiz 我叫khalifa
    print(String('我不叫Wiz 我叫Khalifa').toUpperCase())  # 我不叫WIZ 我叫KHALIFA
    print(String('   我不叫Wiz 我叫Khalifa  ').trim())  # 我不叫Wiz 我叫Khalifa
    print(String('   我不叫Wiz 我叫Khalifa  ').trimEnd())  # 我不叫Wiz 我叫Khalifa
    print(String('   我不叫Wiz 我叫Khalifa  ').trimStart())  # 我不叫Wiz 我叫Khalifa
