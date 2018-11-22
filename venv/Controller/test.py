from Models.gridCell import GridCell
from Controller.GridMap import GridMap

cg = GridMap(100)
for cell in cg.grid:
    print(cell.cellValue)