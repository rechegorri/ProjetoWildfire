from Models.Wind import Wind
from Models.gridCell import GridCell
from Controller.GridMap import GridMap

import numpy as np

def sigmoid(add):
    return 1 / (1 + np.exp(-add))

def sigmoidDerivative(sigm):
    return sigm * (1-sigm)

gridmap = GridMap(200)

class RedeNeural:

    def feedfoward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weight1))
        self.output = sigmoid(np.dot(self.layer1, self.weight2))

    def backprop(self):
        d_w2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        d_w1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))

        self.weight1 += d_w1
        self.weight2 +=d_w2