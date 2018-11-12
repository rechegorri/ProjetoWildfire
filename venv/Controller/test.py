from Models.gridCell import CellValue
from Models.gridCell import GridCell

class main:
    def __init__(self):
        cell = Cell(0,0)
        cell.cellValue = CellValue.FLAMABLE
        print(cell.cellValue.value)

MyMain = main()