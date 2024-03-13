class Dep(set):

    def __init__(self, effects=None):
        super().__init__(effects or [])
        self.w = 0
        self.n = 0


def createDep(effects=None):
    dep = Dep(effects)
    dep.w = 0
    dep.n = 0
    return dep


if __name__ == '__main__':
    d = createDep()
    print(d)
    print(dir(d))
