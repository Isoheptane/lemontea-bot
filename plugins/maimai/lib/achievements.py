import math

def compute_rate(achievements: float) -> str:
    if (achievements < 50.0):
        return "d"
    elif (achievements < 60.0):
        return "c"
    elif (achievements < 70.0):
        return "b"
    elif (achievements < 75.0):
        return "bb"
    elif (achievements < 80.0):
        return "bbb"
    elif (achievements < 90.0):
        return "a"
    elif (achievements < 94.0):
        return "aa"
    elif (achievements < 97.0):
        return "aaa"
    elif (achievements < 98.0):
        return "s"
    elif (achievements < 99.0):
        return "sp"
    elif (achievements < 99.5):
        return "ss"
    elif (achievements < 100.0):
        return "ssp"
    elif (achievements < 100.5):
        return "sss"
    else:
        return "sssp"

def compute_rating(level: float, achievements: float) -> int:
    if (achievements < 50.0):
        rating = 0.0
    elif (achievements < 60.0):
        rating = 5.0
    elif (achievements < 70.0):
        rating = 6.0
    elif (achievements < 75.0):
        rating = 7.0
    elif (achievements < 80.0):
        rating = 7.5
    elif (achievements < 90.0):
        rating = 8.5
    elif (achievements < 94.0):
        rating = 9.5
    elif (achievements < 97.0):
        rating = 10.5
    elif (achievements < 98.0):
        rating = 12.5
    elif (achievements < 99.0):
        rating = 12.7
    elif (achievements < 99.5):
        rating = 13.0
    elif (achievements < 100.0):
        rating = 13.2
    elif (achievements < 100.5):
        rating = 13.5
    else:
        rating = 14.0
    return math.floor(level * (min(100.5, achievements) / 100) * rating)

def compute_rating_new(level: float, achievements: float) -> int:
    if (achievements < 50.0):
        rating = 0.0
    elif (achievements < 60.0):
        rating = 8.0
    elif (achievements < 70.0):
        rating = 9.6
    elif (achievements < 75.0):
        rating = 11.2
    elif (achievements < 80.0):
        rating = 12.0
    elif (achievements < 90.0):
        rating = 13.6
    elif (achievements < 94.0):
        rating = 15.2
    elif (achievements < 97.0):
        rating = 16.8
    elif (achievements < 98.0):
        rating = 20.0
    elif (achievements < 99.0):
        rating = 20.0
    elif (achievements < 99.5):
        rating = 20.8
    elif (achievements < 100.0):
        rating = 21.1
    elif (achievements < 100.5):
        rating = 21.6
    else:
        rating = 22.4
    return math.floor(level * (min(100.5, achievements) / 100) * rating)