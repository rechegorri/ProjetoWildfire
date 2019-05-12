import sklearn.neural_network as neuralnetwork
from sklearn.model_selection import cross_val_score
import sklearn.metrics as metrics
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
import Controller.DataImport as di
from sklearn.model_selection import train_test_split
import numpy as np
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
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacoesCorumba.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\FocosCorumba.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", encoding='utf8', index_col=None)
        neighbours_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosVizinhos.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        csv_data, neighbours_data = import_data(arq_focos_treino,arq_focos_treino)
        print(len(neighbours_data))
        print(len(neighbours_data['PontoDatetime'].unique()))
        print(len(neighbours_data['OrigemDatetime'].unique()))
        print(neighbours_data.describe())
        ##tratamento_data(csv_data)
    else:
        neighbours_labels = ['OrigemLatitude', 'OrigemLongitude', 'OrigemDatetime', 'OrigemTempBulboSeco',
                             'OrigemTempBulboUmido', 'OrigemUmidadeRelativa', 'OrigemPressaoAtmEstacao',
                             'OrigemDirecaoVento', 'OrigemVelocidadeVentoNebulosidade', 'PontoLatitude',
                             'PontoLongitude', 'PontoDatetime', 'DistanciaDeOrigem']
        neighbours_cleaned = neighbours_data.fillna(0)
        neighbours_cleaned = neighbours_cleaned.loc[~(neighbours_data == 0).all(axis=1)]

        print(neighbours_cleaned.isna().sum()/neighbours_cleaned.shape[0])
        print(neighbours_cleaned.describe())
        if True:
            min_max_scaler = MinMaxScaler()
            data = min_max_scaler.fit_transform(neighbours_cleaned)
            neighbours_norm = pd.DataFrame(data, columns=neighbours_labels)
            X = neighbours_norm.drop(['PontoLatitude', 'PontoLongitude', 'PontoDatetime', 'DistanciaDeOrigem'], axis=1)
            Y_lat = neighbours_norm['PontoLatitude']
            Y_long = neighbours_norm['PontoLongitude']

            MLPC_lat = neuralnetwork.MLPRegressor(activation='logistic', alpha=1e-05, batch_size='auto', beta_1=0.9,
                                              beta_2=0.999, early_stopping=False, epsilon=1e-08,
                                              hidden_layer_sizes=(9, 5), learning_rate='adaptive',
                                              learning_rate_init=0.5, max_iter=200, momentum=0.9,
                                              nesterovs_momentum=True, power_t=0.5, random_state=9, shuffle=True,
                                              solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
                                              warm_start=False)
            MLPC_long = neuralnetwork.MLPRegressor(activation='logistic', alpha=1e-05, batch_size='auto', beta_1=0.9,
                                              beta_2=0.999, early_stopping=False, epsilon=1e-08,
                                              hidden_layer_sizes=(9, 5), learning_rate='adaptive',
                                              learning_rate_init=0.5, max_iter=200, momentum=0.9,
                                              nesterovs_momentum=True, power_t=0.5, random_state=9, shuffle=True,
                                              solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
                                              warm_start=False)
            Xlat_train, Xlat_test, Ylat_train, Ylat_test = train_test_split(X, Y_lat, test_size=0.7)
            Xlong_train, Xlong_test, Ylong_train, Ylong_test = train_test_split(X, Y_long, test_size=0.7)
            ##TestLat
            MLPC_lat.fit(Xlat_train,Ylat_train)
            Ylat_pred = MLPC_lat.predict(Xlat_test)
            print('Medida Latitude - Entradas normalizadas')
            print(np.sqrt(metrics.mean_squared_error(Ylat_test, Ylat_pred)))
            print('Score R^2')
            print(r2_score(Ylat_test, Ylat_pred))
            MLPC_long.fit(Xlong_train,Ylong_train)
            print('Medida Longitude - Entradas normalizadas')
            Ylong_pred = MLPC_long.predict(Xlong_test)
            print(np.sqrt(metrics.mean_squared_error(Ylong_test, Ylong_pred)))
            print('Score R^2')
            print(r2_score(Ylong_test, Ylong_pred))