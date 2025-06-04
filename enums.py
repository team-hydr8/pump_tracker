from enum import Enum

class PumpStatus(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3

class UserLanguage(Enum):
    AFRIKAANS = 0
    ENGLISH = 1
    SEPEDI = 2
    SOUTHERN_NDEBELE = 3
    SOUTHERN_SOTHO = 4
    SWAZI = 5
    TSONGA = 6
    TSWANA = 7
    XHOSA = 8
    VENDA = 9
    ZULU = 10

class ViewMode(Enum):
    DARK = 0
    LIGHT = 1

class MeasureSystem(Enum):
    METRIC = 0
    IMPERIAL = 1