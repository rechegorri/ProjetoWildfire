from Models.gridCell import CellValue
from Models.gridCell import GridCell
from Models.Wind import Wind
import random
import datetime

##Arrumar RN par plotar modelo

class GridMap:
    def __init__(self, size):
        #Creates 2D Grid and fills with random parameters
        grid = []
        for row in range(0,size):
            for column in range(0,size):
                cell = GridCell(row, column)
                cell.cellValue =  random.choice(list(CellValue))
                cell.elevation = random.choice(range(775, 850))
                grid.append(cell)

        for cell in grid:
            windDirection = random.choice(range(0,359))
            windSpeed = random.choice(range(0,30))
            ts = datetime.datetime.now().timestamp()
            #neighboursCellValue = getNeighboursCellValue(cell)
            #
            wind = Wind(windSpeed,windDirection,ts)

    def getGrid(self):
        return self.grid

    def getNeighboursCellValue(self, outerCell):
        returnList = []
        for innerCell in grid:
            if(innerCell.x != outerCell.x and innerCell.y != outerCell.x):
                if(innerCell.x >= outerCell.x-1 and innerCell.x <= outerCell.x+1 and outerCell.x-1 >=0 and outerCell.x+1<=size):
                    if(innerCell.y >= outerCell.y-1 and innerCell.y <= outerCell.y+1 and outerCell.y-1 >=0 and outerCell.y+1<=size):
                        returnList.append(innerCell.cellValue)
        return returnList

gc = GridMap(100)
for cell in gc:
    print(cell.x)