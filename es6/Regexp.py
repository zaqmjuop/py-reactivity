import re


class Regexp:

    @property
    def isGlobal(self):
        return self._isGlobal

    @property
    def ignoreCase(self):
        return self._ignoreCase

    @property
    def lastIndex(self):
        return self._lastIndex

    @property
    def multiline(self):
        return self._multiline

    @property
    def source(self):
        return self._pattern

    def __init__(self, pattern: str, attributes: str) -> None:
        self._pattern = pattern
        self._isGlobal = bool(re.search(r'g', attributes))
        self._multiline = bool(re.search(r'm', attributes))
        self._ignoreCase = bool(re.search(r'i', attributes))
        self._lastIndex = 0
        pass

    def exec(self, text) -> None:
        searchRes = re.search(self._pattern, text)
        res = {
            "0": searchRes.group(),
            "index": searchRes.span()[0],
            "input": text,
            "groups": searchRes.groups() if len(searchRes.groups()) else None
        } if searchRes else None
        return res

    def test(self, text) -> None:
        searchRes = re.search(self._pattern, text)
        return bool(searchRes)

    def toString(self) -> None:
        re.sub(r'\\(.)', r'\1', self._pattern)
