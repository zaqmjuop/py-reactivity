class Symbol:

    def __init__(self, description: str = '') -> None:
        self.description = description
        pass

    def __str__(self):
        return f"Symbol({self.description})"

    def toString(self):
        return self.__str__()
