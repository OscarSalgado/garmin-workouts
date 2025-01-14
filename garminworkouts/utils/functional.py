from typing import Any
import numpy as np
from numpy.typing import NDArray


def flatten(xs) -> Any:
    return [item for sublist in xs for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]


def fill(x, n) -> Any:
    return np.full(n, x)


def filter_empty(value) -> Any:
    if isinstance(value, list):
        return [filter_empty(val) for val in value if val]
    elif isinstance(value, dict):
        return {key: filter_empty(val) for key, val in value.items() if val}
    return value


def concatenate(x, y) -> NDArray[Any]:
    return np.concatenate((x, y))
