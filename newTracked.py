from state import effectState
from createDep import Dep


def newTracked(dep: Dep) -> bool:
    return (dep.n & effectState.trackOpBit) > 0
