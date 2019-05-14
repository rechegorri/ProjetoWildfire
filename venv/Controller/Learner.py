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
    values = min_max.fit_transform(data)
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
    focos_df, neighbours_df = di.importacao_dados(arq_estacao_treino, arq_focos_treino)
    return focos_df, neighbours_df

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacoesCorumba.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\FocosCorumba.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", encoding='utf8', index_col=None)
        neighbours_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosVizinhos.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        csv_data, neighbours_data = import_data(arq_focos_treino,arq_focos_treino)
        loadDataTrain(neighbours_data)
    else:
        real_df,pred_df = loadDataTrain(neighbours_data)
        merged_df = pd.concat([real_df,pred_df]).sort_values(by='Datetime').head(500)
        cores = {'Real':'red', 'Prediction':'yellow'}
        '''
        real_map = fl.Map(location=[(real_df['Latitude'].min() + real_df['Latitude'].max()) / 2,
                                    (real_df['Longitude'].min() + real_df['Longitude'].max()) / 2],
                                    tiles="Cartodb dark_matter", zoom_start=10)
        real_df.head(500).apply(lambda row:fl.CircleMarker(location=[row["Latitude"],row["Longitude"]],radius=7,fill_color=cores[row['Class']]).add_to(real_map),axis=1)
        real_map.save('C:\\Users\Livnick\Documents\dadosFocos\corumba_real.html')
        '''
        results_map = fl.Map(location=[(merged_df['Latitude'].min()+merged_df['Latitude'].max())/2,
                                       (merged_df['Longitude'].min()+merged_df['Longitude'].max())/2],
                                        tiles="Cartodb dark_matter", zoom_start=10)
        merged_df.apply(lambda row: fl.CircleMarker(location=[row["Latitude"], row["Longitude"]], radius=7,
                                                            fill_color=cores[row['Class']]).add_to(results_map), axis=1)
        results_map.save('C:\\Users\Livnick\Documents\dadosFocos\corumba_results.html')