from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from Models.gridCell import GridCell
from Models.gridCell import CellStatusEnum as cellstatus
import random


##Inserção de dados
##Por ora, random
input = []
for i in range (300):
    input.append([])
    for j in range (300):
        alt = random.triangular(300,800,500)
        wind_d = random.triangular(0,359,120)
        wind_s = random.triangular(0,30,20)
        air_h = random.triangular(25,100,55)
        gc = GridCell(i, j, alt, None, wind_d, wind_s, air_h)
        gc.setLastCellStatusInt(random.random())
        gc.setCurrentCellStatusInt(random.random())
        input[i]=gc



##Treino de dados da MLP
def neural_network_treiner(X,Y):
    print("Iniciando aprendizado de rede neural")

    scaler = MinMaxScaler()
    X2 = scaler.fit(X)
