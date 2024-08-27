from .base_split import BaseSplit
from .equal_split import EqualSplit
from .exact_split import ExactSplit
from .percentage_split import PercentageSplit

split_type = {
    "EQUAL":EqualSplit,
    "EXACT":ExactSplit,
    "PERCENT":PercentageSplit
}