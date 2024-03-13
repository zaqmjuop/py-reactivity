from es6.Object import Object
##
# Make a map and return a function for checking if a key
# is in that map.
# IMPORTANT: all calls of this function must be prefixed with
# \/\##\_\_PURE\_\_\#\/
# So that rollup can tree-shake them if necessary.
# /


def makeMap(text: str,  expectsLowerCase=False):
    map = Object()
    charList = text.split(',')
    for i in range(0, len(charList)):
        map[charList[i]] = True

    def _check(val: str):
        if (expectsLowerCase):
            val = val.lower()
        res = bool(map[val]) if map.hasattr(val) else False
        return res
    return _check
