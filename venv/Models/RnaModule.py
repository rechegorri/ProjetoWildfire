from Models.Wind import Wind
from Models.gridCell import GridCell
from Controller.GridMap import GridMap

class RedeNeural:
    def __init__(self, grid, wind, flamability, y):
        self.input = grid
        self.wind = wind
        self.flamability = flamability
        self.weight1 = random.rand(self.input.shape[1],4)
        self.weight2 = random.rand(4,1)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def feedfoward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weight1))
        self.output = sigmoid(np.dot(self.layer1, self.weight2))
