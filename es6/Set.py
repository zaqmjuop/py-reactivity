class Set(set):

    def __init__(self, value=None):
        super().__init__(value)

    @property
    def size(self):
        return len(self)

    def delete(self, value):
        return self.remove(value)

    def has(self, value):
        return value in self
