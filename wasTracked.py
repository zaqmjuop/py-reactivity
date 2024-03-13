from state import effectState
from createDep import Dep


def wasTracked(dep: Dep) -> bool:
    return (dep.w & effectState.trackOpBit) > 0
