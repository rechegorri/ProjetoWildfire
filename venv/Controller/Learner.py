import sklearn.neural_network as neuralnetwork
from sklearn import model_selection as model
import sklearn.metrics as metrics
import Controller.DataImport as di
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import datetime as dt
import matplotlib.pyplot as plt
from sklearn import datasets
import seaborn as sns
import matplotlib.pyplot as plt
import math
import pickle
import folium as fl
import time

def matriz_confusao(X,Y):
    mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(10, 8), activation='identity', solver='adam',
                                      learning_rate='constant', random_state=2818, max_iter=400,
                                      early_stopping=True, alpha=1000)
    x_train, x_test, y_train, y_test = model.train_test_split(X,Y,test_size=0.3, random_state=42)
    mlp.fit(x_train,y_train)
    y_pred = mlp.predict(x_test)
    matrix = metrics.confusion_matrix(y_test.values.argmax(axis=1),y_pred.argmax(axis=1))
    df_matrix = pd.DataFrame(matrix, columns=['quad0','quad1','quad2','quad3','quad4','quad5','quad6','quad7'])
    #plt.figure(10,7)
    sns.set(font_scale=1.4)
    sns.heatmap(df_matrix, annot=True)
    plt.show()


def executar_kfold(X,Y,tipo_metodo, splits):
    methods = {'Acurácia': 'accuracy', 'LogLoss': 'neg_log_loss', 'AUC': 'roc_auc'}
    kfold = model.KFold(n_splits=splits, random_state=1828)
    mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(10, 8), activation='identity', solver='adam',
                                      learning_rate='constant', random_state=2818, max_iter=400,
                                      early_stopping=True, alpha=1000)
    resultados = model.cross_val_score(mlp, X, Y, cv=kfold, scoring=methods[tipo_metodo])
    print(str(tipo_metodo)+":" + str(resultados.mean()) + " (" + str(resultados.std()) + ")")

def saveNetwork(network, filename):
    with open(filename, 'wb') as fo:
        pickle.dump(network, fo)

def loadNetwork(filename):
    with open(filename,'rb') as fo:
        mlpr_loaded = pickle.load(fo)
        return mlpr_loaded

def unNormalize(norm, max, min):
    return (min+(norm*(max/min)))

##Inserção de dados
def import_data(arq_estacao, arq_focos):
    tempo_inicio = time.time()
    dados_df = di.importacao_dados(arq_estacao, arq_focos)
    tempo_decorrido = time.time() - tempo_inicio
    print('Tempo Decorrido: '+str(dt.timedelta(seconds=tempo_decorrido)))
    return dados_df

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    arq_estacao_importar='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacoesCorumba.csv'
    arq_focos_importar='C:\\Users\Livnick\Documents\dadosFocos\FocosCorumba.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosFormatados.csv", encoding='utf8', index_col=None)
        #neighbours_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosVizinhos.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        csv_data = import_data(arq_estacao_importar,arq_focos_importar)
        #loadDataTrain(neighbours_data)
    else:
        labels = ['Latitude', 'Longitude','DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSeco','TempBulboUmido',
                     'UmidadeRelativa', 'DirecaoVento', 'VelocidadeVentoNebulosidade', 'quad0', 'quad1', 'quad2', 'quad3', 'quad4', 'quad5', 'quad6', 'quad7']
        ##Drop coluna com valores Zerados e remove NAN (representam menos de 1% da base)
        csv_data.drop(labels=['Datetime', 'PressaoAtmEstacao','PosicaoGrid'], axis=1, inplace=True)
        csv_data = csv_data.dropna(axis=0)
        scaler = MinMaxScaler()
        scaler.fit(csv_data)
        n_iteracoes = 10
        data_scaled = scaler.transform(csv_data)
        scaled_df = pd.DataFrame(data_scaled, columns=labels)
        X = scaled_df[['Latitude', 'Longitude','DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSeco','TempBulboUmido',
                     'UmidadeRelativa', 'DirecaoVento', 'VelocidadeVentoNebulosidade']]
        Y = scaled_df[['quad0', 'quad1', 'quad2', 'quad3', 'quad4', 'quad5', 'quad6', 'quad7']]
        executar_kfold(X, Y, 'Acurácia', n_iteracoes)
        executar_kfold(X, Y, 'LogLoss', n_iteracoes)
        executar_kfold(X,Y,'AUC',n_iteracoes)
        matriz_confusao(X,Y)
