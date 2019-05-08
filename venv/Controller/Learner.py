import sklearn.neural_network as neuralnetwork
from sklearn.model_selection import cross_val_score
import sklearn.metrics as metrics
from sklearn.preprocessing import MinMaxScaler
import Controller.DataImport as di
from sklearn.model_selection import train_test_split
import pandas as pd
#from datetime import datetime
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import datasets
import math
import folium as fl
'''
Treino de dados da MLP, 
valor X se trata das entradas de dados para treino
valor Y são os resultados esperados a partir do dataset de treino
'''
def neural_network_treiner(data_input):
    print('Iniciando treino de dados: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    MLPC = neuralnetwork.MLPRegressor(activation='logistic', alpha=1e-05, batch_size='auto', beta_1=0.9,
           beta_2=0.999, early_stopping=False, epsilon=1e-08,
           hidden_layer_sizes=(9, 5), learning_rate='adaptive',
           learning_rate_init=0.5, max_iter=200, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=9, shuffle=True,
           solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
           warm_start=False)
    Y = data_input.loc[:,'LatitudeProximo':'DatetimeProximo']
    X = data_input.loc[:,:'VelocidadeVentoNebulosidade']
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.7)
    MLPC.fit(x_train, y_train)
    print('Treino de dados concluido: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    print('------------------------------------')
    print('Erro Medio Absoluto Test DS:')
    pred = MLPC.predict(x_test)
    MAE_test_data = (y_test-pred).sum()/y_test.shape[0]
    #Valor medio normalizado do erro.
    print(MAE_test_data)
    print('------------------------------------')
    print('Erro Medio Absoluto Train DS:')
    pred2 = MLPC.predict(x_train)
    MAE_train_data = (y_train-pred2).sum()/y_train.shape[0]
    print(MAE_train_data)
    print('------------------------------------')
    print('R Squared:')
    score = MLPC.score(x_test, y_test)
    print(score)
    print('------------------------------------')
    print('Testes realizados {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))

##Inserção de dados
def import_data(arq_estacao, arq_focos):
    focos_df, neighbours_df = di.importacao_dados(arq_estacao_treino, arq_focos_treino)
    return focos_df, neighbours_df

def tratamento_data(csv_data):
    del csv_data['RiscoFogo']#Cerca de 68% dos dados vazios afeta os resultados
    min_lat = csv_data['Latitude'].min()
    max_lat = csv_data['Latitude'].max()
    min_long = csv_data['Longitude'].min()
    max_long = csv_data['Longitude'].max()
    min_max_scaler = MinMaxScaler()
    #print(data_semzeros.isna().sum() / data_semzeros.shape[0])
    data_pronto = pd.DataFrame(min_max_scaler.fit_transform(csv_data.values), columns=csv_data.columns, index=csv_data.index)
    map = fl.Map(location=[(min_lat+max_lat)/2,(min_long+max_long)/2],
                     tiles="Stamen Terrain", zoom_start=10)
    for element in csv_data.tail(50).values:
        fl.Marker([element[1],element[2]],
                  popup=dt.datetime.fromtimestamp(int(element[0])).strftime("{%d-%m-%Y %H:%M:%S}'")
                  ).add_to(map)

    map.save('C:\\Users\Livnick\Documents\dadosFocos\map001.html')


if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacao.2017-07-01.2018-07-01.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\Focos.2017-07-01.2018-07-01.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", encoding='utf8', index_col=None)
        neighbours_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosVizinhos.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        csv_data, neighbours_data = import_data(arq_focos_treino,arq_focos_treino)
        print(neighbours_data)
        ##tratamento_data(csv_data)
    else:
        print(neighbours_data)
        ##tratamento_data(csv_data)


