# Cell model with basic attributes to be consumed by the NAN
# Coordenadas:
# 1 Grau Latitude: 111,12km
# 1 Grau Longitude: 0 - 111,12km
# precisão de 3 casas (aprox 111m)
# Status: consumed, flamable, non-flamable, in-flames
from enum import Enum

CellStatus = Enum('CellStatus','CONSUMED FLAMABLE NONFLAMABLE BEINGCONSUMED')


def CellStatusValue(cellstatus: CellStatus):
    return cellstatus.value


class GridCell:
    def __init__(self, x, y):
        self.CellStatus = CellStatus
        self.x = x
        self.y = y
        self.elevation = 0.00


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
