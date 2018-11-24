from Models.gridCell import GridCell
from Models.gridCell import CellStatus
from Models.Wind import Wind
import numpy as np

def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))

def sigmoidDerivada(sig):
    return sig * (1 - sig)

def createCell(x,y):
    cell = GridCell(x,y)
    cell.elevation = np.random.randint(0, 450, 1)
    cell.cellStatus = np.random.choice(list(CellStatus))
    return cell
#input cell
inputCell: GridCell = createCell(1,1)
inputCell.cellStatus = CellStatus.FLAMABLE
#Wind
inputWind = Wind(np.random.randint(0,45,1), np.random.randint(0, 359, 1),0)
#Neighbours
neighbours: GridCell = []

for i in range(3):
    for j in range(3):
        if not (i==1 and j==1):
            cell = createCell(i, j)
            neighbours.append(cell)

#Multi-Input: Gathers all inputs
input = np.array([inputCell.cellStatus.value, inputCell.elevation, inputWind.speed, inputWind.direction])
for cell in neighbours:
    input  = np.append(input, ([cell.cellStatus.value, cell.elevation]) )

#Output
output = np.array([CellStatus.BEINGCONSUMED.value])
for cell in neighbours:
    output = np.append(output, [cell.cellStatus.value])

pesos0 = 2*np.random.random((20,9)) - 1
pesos1 = 2*np.random.random((9,1)) - 1

epoch = 1000
learningRate = 0.3
moment = 1

#Learning
for j in range(epoch):
    entryLayer = input
    addSinap0 = np.dot(entryLayer,pesos0)

    hiddenLayer = sigmoid(addSinap0)
    addSinap1 = np.dot(hiddenLayer,pesos1)

    outputLayer = sigmoid(addSinap1)
    errOutput = output - outputLayer
    avgAbs = np.mean(np.abs(errOutput))
    print('Erro: ' + str(avgAbs))

    sigmoidOutput = sigmoidDerivada(outputLayer)
    outputDelta = errOutput * sigmoidOutput

    transWeight1 = pesos1[np.newaxis]
    transWeight1 = transWeight1.T
    deltaOutputXWeight = outputDelta.dot(transWeight1)
    deltaHiddenLayer = deltaOutputXWeight * sigmoidDerivada(hiddenLayer)

    transHiddenLayer = hiddenLayer.T
    newWeight1 = transHiddenLayer.dot(outputDelta)
    pesos1 = (pesos1 * moment) + (newWeight1 + learningRate)

    transEntryLayer = entryLayer.T
    newWeight0 = transEntryLayer.dot(deltaHiddenLayer)
    pesos0 = (pesos0 * moment) + (newWeight0 + learningRate)