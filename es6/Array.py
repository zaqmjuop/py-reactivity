
class Array(list):
    @property
    def length(self):
        return len(self)

    @length.setter
    def length(self, newVal: int):
        keeps = self[0:newVal]
        self.clear()
        self.extend(keeps)
        pass

    def __init__(self, data: list = []) -> None:
        super().__init__(data)
        pass
    # concat 连接两个或多个数组，并返回已连接数组的副本。

    def concat(self, ary2):
        return self + ary2
    # entries()	返回键/值对数组迭代对象。

    def entries(self):
        def generateIterator():
            i = 0
            while True:
                if (i < len(self)):
                    yield {"value": [i, self[i]], "done": False}
                else:
                    yield {"value": None, "done": True}
                i += 1

        it = generateIterator()
        return it
    # every()	检查数组中的每个元素是否通过测试。

    def every(self, func):
        for i in range(0, len(self)):
            if (bool(func(self[i], i, self)) == True):
                return False
        return True
    # fill()	用静态值填充数组中的元素。

    def fill(self, value, start=0, end=-1):
        if (end == -1):
            end = len(self)
        for i in range(start, end):
            self[i] = value
    # filter()	使用数组中通过测试的每个元素创建新数组。

    def filter(self, func):
        res = []
        for i in range(0, len(self)):
            if (bool(func(self[i], i, self)) == True):
                res.append(self[i])
        return res
    # find()	返回数组中第一个通过测试的元素的值。

    def find(self, func):
        for i in range(0, len(self)):
            if (bool(func(self[i], i, self)) == True):
                return self[i]
        return None
    # findIndex()	返回数组中通过测试的第一个元素的索引。

    def findIndex(self, func):
        for i in range(0, len(self)):
            if (bool(func(self[i], i, self)) == True):
                return i
        return -1
    # forEach()	为每个数组元素调用函数。

    def forEach(self, func):
        for i in range(0, len(self)):
            func(self[i], i, self)
        return None
    # includes()	检查数组是否包含指定的元素。

    def includes(self, element, start=0):
        for i in range(start, len(self)):
            if (self[i] == element):
                return True
        return False
    # indexOf()	在数组中搜索元素并返回其位置。

    def indexOf(self, item, start=0):
        for i in range(start, len(self)):
            if (self[i] == item):
                return i
        return -1
    # join(): string	将数组的所有元素连接成一个字符串。

    def join(self, separator=''):
        length = len(self)
        if (length == 0):
            return ''
        res = self[0]
        for i in range(1, length):
            res += separator
            res += self[i]
        return res
    # keys()	返回 Array Iteration 对象，包含原始数组的键.

    def keys(self):
        def generateIterator():
            i = 0
            while True:
                if (i < len(self)):
                    yield {"value": i, "done": False}
                else:
                    yield {"value": None, "done": True}
                i += 1

        it = generateIterator()
        return it
    # lastIndexOf(): number	在数组中搜索元素，从末尾开始，并返回其位置。

    def lastIndexOf(self, item, start=0):
        for i in range(len(self) - 1, start - 1, -1):  # -1 是遍历步长, start - 1遍历结束标识
            if (self[i] == item):
                return i
        return -1
    # map(): any[]	使用为每个数组元素调用函数的结果创建新数组。

    def map(self, func):
        resAry = self.copy()
        for i in range(0, len(resAry)):
            resAry[i] = func(self[i], i, self)
        return resAry
    # pop(): any	删除数组的最后一个元素，并返回该元素。

    # push(): number	将新元素添加到数组的末尾，并返回新的长度。

    def push(self, *args):
        for item in args:
            self.append(item)
        return len(self)
    # reduce(): any	将数组的值减为单个值（从左到右）。

    def reduce(self, func, initialValue=None):
        total = initialValue
        for i in range(0, len(self)):
            total = func(total, self[i], i, self)
        return total
    # reduceRight(): any	将数组的值减为单个值（从右到左）。

    def reduceRight(self, func, initialValue=None):
        total = initialValue
        for i in range(len(self) - 1, -1, -1):
            total = func(total, self[i], i, self)
        return total
    # reverse(): any[]	反转数组中元素的顺序。

    def reverse(self):
        length = len(self)
        for i in range(0, int(length / 2)):
            itemLeft = self[i]
            self[i] = self[length - 1 - i]
            self[length - 1 - i] = itemLeft
        return self
    # shift(): any	删除数组的第一个元素，并返回该元素。

    def shift(self):
        res = self[0]
        del self[0]
        return res
    # slice(): any[]	选择数组的一部分，并返回新数组

    def slice(self, start=0, end=None):
        if (end == None):
            end = len(self) - 1
        return self[start: end]
    # some(): boolean	检查数组中的任何元素是否通过测试。

    def some(self, func):
        for i in range(0, len(self)):
            if (bool(func(self[i], i, self)) == True):
                return True
        return False
    # sort(): any[]	对数组的元素进行排序。

    def sort(self, func=lambda a, b: a-b):
        n = len(self)
        for i in range(1, n):
            itemI = self[i]
            j = i - 1
            while j >= 0 and int(func(self[j], itemI)) > 0:
                self[j + 1] = self[j]
                j -= 1
            self[j + 1] = itemI
        return self
    # splice(): any[]	从数组中添加/删除元素。

    def splice(self, index, howmany=0, *args):
        for i in range(0, howmany):
            del self[index]
        for i in range(len(args) - 1, -1, -1):
            self.insert(index, args[i])
        return self
    # toString(): string	将数组转换为字符串，并返回结果。

    def toString(self):
        if (len(self) == 0):
            return ''
        res = self[0]
        for i in range(1, len(self)):
            res += ','
            res += self[i]
        return res
    # unshift():number	将新元素添加到数组的开头，并返回新的长度。

    def unshift(self, *args):
        for i in range(len(args) - 1, -1, -1):
            self.insert(0, args[i])
        return len(self)


if __name__ == '__main__':
    print([None] * 0)
    a1 = Array([1, 2, 3, 4, 5])
    a2 = [2, 3, 4]
    a1.length = 3
    print(a1)
