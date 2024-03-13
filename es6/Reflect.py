from rawAttr import getRawAttr, setRawAttr
from .Object import Object
import sys
sys.path.append('../')


class Reflect:

    @classmethod
    def get(cls, target: Object, name: str, receiver):
        Object._validate(target)
        return getRawAttr(target, name)

    @classmethod
    def set(cls, target: Object, name: str, value, receiver):
        Object._validate(target)
        setRawAttr(target, name, value)
        pass

    @classmethod
    def defineProperty(cls, target: Object, name: str, desc):
        Object._validate(target)
        Object.defineProperty(target, name, desc)

    @classmethod
    def deleteProperty(cls, target: Object, name: str):
        Object._validate(target)
        delattr(target, name)

    @classmethod
    def has(cls, target: Object, name: str):
        Object._validate(target)
        return target.hasattr(name)

    @classmethod
    def ownKeys(cls, target: Object):
        Object._validate(target)
        return target.keys()

    @classmethod
    def getPrototypeOf(cls, target: Object):
        Object._validate(target)
        return target.__proto__ or None

    def __init__(self) -> None:
        pass
