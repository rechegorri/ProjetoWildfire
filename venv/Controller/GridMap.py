from Models.gridCell import CellValue
from Models.gridCell import GridCell
import random

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
            print("Row: "+str(cell.x)+" Column: "+str(cell.y)+" Status: "+str(cell.cellValue)+" Elevation: "+str(cell.elevation))

myGrid = GridMap(200)