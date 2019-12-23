from enum import IntEnum


class OrderType(IntEnum):
    NONE_ORDER = 0
    STOP_MARKET_LONG = 1  # 逆指値 成行 新規買
    STOP_MARKET_SHORT = 2  # 逆指値 成行 新規売
    STOP_LIMIT_LONG = 3  # 逆指値 指値 新規買
    STOP_LIMIT_SHORT = 4  # 逆指値 指値 新規売
    LIMIT_LONG = 5  # 指値 新規買
    LIMIT_SHORT = 6  # 指値 新規売
    MARKET_LONG = 7  # 成行 新規買
    MARKET_SHORT = 8  # 成行 新規売
    CLOSE_LONG_STOP_MARKET = 9  # 逆指値 成行 返売(longを返済)
    CLOSE_SHORT_STOP_MARKET = 10  # 逆指値 成行 返買(shortを返済)
    CLOSE_LONG_MARKET = 11  # 成行 返売(longを返済)
    CLOSE_SHORT_MARKET = 12  # 成行 返買(shortを返済)
    CLOSE_LONG_LIMIT = 13  # 指値 返売(longを返済)
    CLOSE_SHORT_LIMIT = 14  # 指値 返買(shortを返済)
    CLOSE_LONG_STOP_LIMIT = 15  # 逆指値 指値 返売(longを返済)
    CLOSE_SHORT_STOP_LIMIT = 16  # 逆指値 指値 返買(shortを返済)
    CLOSE_LONG_OCO = 17  # OCO 返売
    CLOSE_SHORT_OCO = 18  # OCO 返買
    OCO = 19  # OCO 新規買 and 新規売
