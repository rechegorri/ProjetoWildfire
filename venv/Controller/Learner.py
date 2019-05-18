import sklearn.neural_network as neuralnetwork
from sklearn.model_selection import cross_val_score
import sklearn.metrics as metrics
from sklearn.metrics import r2_score
import Controller.DataImport as di
import Controller.Support as sup
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import datasets
import math
import pickle
import folium as fl
import Controller.DistanceMetrics as dm
import time

def MLP_trainer(X,Y):
    MLPR = neuralnetwork.MLPRegressor(activation='logistic', alpha=1e-05, batch_size='auto', beta_1=0.9,
                                          beta_2=0.999, early_stopping=False, epsilon=1e-08,
                                          hidden_layer_sizes=(9, 5), learning_rate='adaptive',
                                          learning_rate_init=0.5, max_iter=200, momentum=0.9,
                                          nesterovs_momentum=True, power_t=0.5, random_state=9, shuffle=True,
                                          solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
                                          warm_start=False)
    return MLPR

def saveNetwork(network, filename):
    with open(filename, 'wb') as fo:
        pickle.dump(network, fo)

def loadNetwork(filename):
    with open(filename,'rb') as fo:
        mlpr_loaded = pickle.load(fo)
        return mlpr_loaded

def unNormalize(norm, max, min):
    return (min+(norm*(max/min)))

def loadDataTrain(data):
    data = data.fillna(0)
    data = data.loc[~(data == 0).all(axis=1)]
    data_teste = data.tail(1000)
    ##Minimo e Maximo Valores de Lat e Long
    min_lat = data['OrigemLatitude'].min()
    max_lat = data['OrigemLatitude'].max()
    min_lon = data['OrigemLongitude'].min()
    max_lon = data['OrigemLongitude'].max()
    ##
    min_max = MinMaxScaler()
    values = min_max.fit_transform(data.values)
    data_norm = pd.DataFrame(values, columns=data.columns)
    X = data_norm.drop(['PontoLatitude', 'PontoLongitude', 'PontoDatetime', 'DistanciaDeOrigem'], axis=1)
    Y_lat = data_norm['PontoLatitude']
    Y_long = data_norm['PontoLongitude']
    mlpr_lat = MLP_trainer(X, Y_lat)
    mlpr_long = MLP_trainer(X, Y_long)
    Xlat_train, Xlat_test, Ylat_train, Ylat_test = train_test_split(X, Y_lat, test_size=0.7)
    Xlon_train, Xlon_test, Ylon_train, Ylon_test = train_test_split(X, Y_long, test_size=0.7)
    mlpr_lat.fit(Xlat_train, Ylat_train)
    mlpr_long.fit(Xlon_train, Ylon_train)
    Ylat_pred = mlpr_lat.predict(Xlat_test)
    Ylon_pred = mlpr_long.predict(Xlon_test)
    print('Medida Latitude - Entradas normalizadas')
    print(np.sqrt(metrics.mean_squared_error(Ylat_test, Ylat_pred)))
    print('Score R^2')
    print(r2_score(Ylat_test, Ylat_pred))
    print('Medida Longitude - Entradas normalizadas')
    print(np.sqrt(metrics.mean_squared_error(Ylon_test, Ylon_pred)))
    print('Score R^2')
    print(r2_score(Ylon_test, Ylon_pred))
    lat_real = []
    lon_real = []
    lat_pred = []
    lon_pred = []

    for ele in Ylat_test:
        lat_real.append(unNormalize(ele,max_lat,min_lat))
    for ele in Ylat_pred:
        lat_pred.append(unNormalize(ele,max_lat,min_lat))
    for ele in Ylat_test:
        lon_real.append(unNormalize(ele,max_lon,min_lon))
    for ele in Ylat_pred:
        lon_pred.append(unNormalize(ele,max_lat,min_lon))

    real_df = pd.DataFrame({'Latitude': lat_real,
                            'Longitude': lon_real,
                            'Class': 'Real',
                            'Datetime': Xlat_test['OrigemDatetime']}).sort_values(by='Datetime')
    pred_df = pd.DataFrame({'Latitude': lat_pred,
                            'Longitude': lon_pred,
                            'Class': 'Prediction',
                            'Datetime': Xlat_test['OrigemDatetime']}).sort_values(by='Datetime')
    return real_df, pred_df
##Inserção de dados
def import_data(arq_estacao, arq_focos):
    tempo_inicio = time.time()
    dados_df = di.importacao_dados(arq_estacao_treino, arq_focos_treino)
    tempo_decorrido = time.time()
    print('Tempo Decorrido: {:%H:%M:%S}'.format(tempo_decorrido))
    return dados_df

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacoesCorumba.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\FocosCorumba.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosFormatados.csv", encoding='utf8', index_col=None)
        #neighbours_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosVizinhos.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        csv_data = import_data(arq_focos_treino,arq_focos_treino)
        #loadDataTrain(neighbours_data)
    else:
        print(csv_data.describe())
        '''
        Delta Lat = 413.65 km
        Delta Lon = 320.15 km
        real_df,pred_df = loadDataTrain(neighbours_data)
        merged_df = pd.concat([real_df.head(200),pred_df.head(200)]).sort_values(by='Datetime')
        cores = {'Real':'red', 'Prediction':'yellow'}

        results_map = fl.Map(location=[(merged_df['Latitude'].min()+merged_df['Latitude'].max())/2,
                                       (merged_df['Longitude'].min()+merged_df['Longitude'].max())/2], zoom_start=10)
        merged_df.apply(lambda row: fl.Marker(location=[row["Latitude"], row["Longitude"]],popup=fl.Popup(row["Datetime"]),icon=fl.Icon(color=cores[row["Class"]])).add_to(results_map),axis=1)
        results_map.save('C:\\Users\Livnick\Documents\dadosFocos\corumba_results.html')
        '''