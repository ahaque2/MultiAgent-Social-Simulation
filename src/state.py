import time, enum, math

class State(enum.IntEnum):
    ORIGIN = 0   #author    #orange
    RECEIVED = 1   #lightblue
    NOT_RECEIVED = 2
    SPREADER = 3
    DISINTERESTED = 4