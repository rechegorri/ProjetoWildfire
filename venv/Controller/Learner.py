import sklearn.neural_network
from sklearn.preprocessing import MinMaxScaler
import Models.gridCell as grid
from random import triangular, random
import pandas as pd
from datetime import datetime
'''
Treino de dados da MLP, 
valor X se trata das entradas de dados para treino
valor Y são os resultados esperados a partir do dataset de treino
'''
def neural_network_treiner(X,Y):
    now = datetime.now()
    print("Iniciando aprendizado de rede neural " + now.strftime('%Y-%m-%d %H:%M:%S'))
    scaler = MinMaxScaler()
    X2 = scaler.fit_transform(X)
    Y2 = scaler.fit_transform(Y)
    ##X2 = X
    ##Y2 = Y
    now = datetime.now()
    print("Dados normalizados " + now.strftime('%Y-%m-%d %H:%M:%S'))
    MLPC = sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=500)
    X2_train = X2[:300]
    X2_test = X2[300:]
    Y_train = Y2[:300]
    Y_test = Y2[300:]
    MLPC.fit(X2_train, Y_train)
    now = datetime.now()
    print("Treino realizado " + now.strftime('%Y-%m-%d %H:%M:%S'))
    y_pred_MLPC = MLPC.predict_log_proba(X2_test)
    y_pred_MLPC = pd.DataFrame(y_pred_MLPC[:, 1:2], columns=['MLPC_predictions'])
    now = datetime.now()
    print("Teste realizado " + now.strftime('%Y-%m-%d %H:%M:%S'))

##Inserção de dados
##Por ora, random
if __name__ == '__main__':
    now = datetime.now()
    print("INICIO " + now.strftime('%Y-%m-%d %H:%M:%S'))
    input = []
    for i in range (300):
        for j in range (300):
            alt = triangular(300,800,500)
            wind_d = triangular(0,359,120)
            wind_s = triangular(0,30,20)
            air_h = triangular(25,100,55)
            gc = grid.GridCell(i, j, alt, None, wind_d, wind_s, air_h)
            gc.setLastCellStatusInt(random())
            gc.setCurrentCellStatusInt(random())
            input.append(gc)
    now = datetime.now()
    print("Objetos criados" + now.strftime('%Y-%m-%d %H:%M:%S'))
    ##Select relevant data from object
    input_test = []
    input_res_test = []
    for obj in input:
        aux = [obj.altitude, obj.wind_direction, obj.wind_speed, obj.air_humidity, obj.getLastCellStatusInt(), obj.getCurrentCellStatusInt()]
        aux_res = [obj.getCurrentCellStatusInt(), random()]
        input_test.append(aux)
        input_res_test.append(aux_res)
    now = datetime.now()
    print("Lista de Inputs criada " + now.strftime('%Y-%m-%d %H:%M:%S'))
    neural_network_treiner(input_test, input_res_test)


