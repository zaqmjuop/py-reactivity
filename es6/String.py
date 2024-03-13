import re


class String(str):
    @property
    def length(self):
        return len(self)

    # charAt()	返回指定位置处的字符。
    def charAt(self, index=0):
        return self[index]

    # charCodeAt()	返回指定位置处字符编码。
    def charCodeAt(self, index=0):
        return ord(self[index])

    # codePointAt()	返回字符串中索引（位置）处的 Unicode 值。
    def codePointAt(self, index=0):
        return ord(self[index])

    # concat()	返回两个或多个连接的字符串。
    def concat(str1, str2):
        return str1 + str2

    # endsWith()	返回字符串是否以指定值结尾。
    def endsWith(self, searchValue, length=None):
        if (length == None):
            length = len(self)
        return super().endswith(searchValue, 0, length)

    # fromCharCode()	将 Unicode 值作为字符返回。
    @classmethod
    def fromCharCode(cls, unicode):
        return chr(unicode)

    # includes()	返回字符串是否包含指定值。
    def includes(self, searchvalue, start=0):
        resIndex = super().find(searchvalue, start)
        return resIndex != -1

    # indexOf()	返回值在字符串中第一次出现的位置。
    def indexOf(self, searchvalue, start=0):
        resIndex = super().find(searchvalue, start)
        return resIndex

    # lastIndexOf()	返回值在字符串中最后一次出现的位置。
    def lastIndexOf(self, searchvalue, end=None):
        if (end == None):
            end = len(self)
        return super().rfind(searchvalue, 0, end)

    # match()	在字符串中搜索值或正则表达式，并返回匹配项。
    def match(self, regexp):
        searchRes = re.search(regexp, self)
        res = {
            "0": searchRes.group(),
            "index": searchRes.span()[0],
            "input": self,
            "groups": searchRes.groups() if len(searchRes.groups()) > 0 else None
        } if searchRes else searchRes
        return res

    # repeat()	返回拥有多个字符串副本的新字符串。
    def repeat(self, count=1):
        res = ''
        for i in range(0, count):  # for (let i = 0; i < count; i++)
            res += self
        return res

    # replace()	在字符串中搜索值或正则表达式，并返回替换值的字符串。
    def replace(self, regexp, replacement, maxTimes=None):
        return super().replace(regexp, replacement, maxTimes) if isinstance(maxTimes, int) else super().replace(regexp, replacement)

    # search()	检索字符串中与正则表达式匹配的子串。
    def search(self, regexp):
        searchRes = re.search(regexp, self)
        return searchRes.span()[0] if searchRes else -1

    # slice()	提取字符串的一部分并返回新字符串。
    def slice(self, start, end=None):
        if (end == None):
            end = len(self)
        return self[start:end]

    # split()	将字符串拆分为子字符串数组。
    def split(self, separator='', limit=None):
        if (separator == None):
            return [self]
        if (separator == ''):
            return list(self[0: limit]) + [self[limit:]] if isinstance(limit, int) else list(self)
        else:
            return super().split(separator, limit) if isinstance(limit, int) else super().split(separator)

    # startsWith()	检查字符串是否以指定字符开头。
    def startsWith(self, searchValue, start=0):
        return super().startswith(searchValue, start)

    # substr()	从字符串中抽取子串，该方法是 substring() 的变种。
    def substr(self, start, length):
        start = start if start >= 0 else start + len(self)
        return self[start:start + length]

    # substring()	从字符串中抽取子串。
    def substring(self, start, end=None):
        end = end if end != None else len(self)
        end = end if end >= 0 else end + len(self)
        start = start if start >= 0 else start + len(self)
        return self[start:end]

    # toLowerCase()	返回转换为小写字母的字符串。
    def toLowerCase(self):
        return super().lower()

    # toUpperCase()	返回转换为大写字母的字符串。
    def toUpperCase(self):
        return super().upper()

    # trim()	返回删除了空格的字符串。
    def trim(self):
        return super().lstrip().rstrip()

    # trimEnd()	返回从末尾删除空格的字符串。
    def trimEnd(self):
        return super().rstrip()

    # trimStart()	返回从开头删除空格的字符串。
    def trimStart(self):
        return super().lstrip()
