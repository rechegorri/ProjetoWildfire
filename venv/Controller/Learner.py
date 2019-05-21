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

def matriz_confusao(X,Y, mlp):
    if(mlp == None):
        mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(10, 8), activation='identity', solver='adam',
                                      learning_rate='constant', random_state=2818, max_iter=400,
                                      early_stopping=True)
    x_train, x_test, y_train, y_test = model.train_test_split(X,Y,test_size=0.3, random_state=42)
    mlp.fit(x_train,y_train)
    y_pred = mlp.predict(x_test)
    matrix = metrics.confusion_matrix(y_test.values.argmax(axis=1),y_pred.argmax(axis=1))
    df_matrix = pd.DataFrame(matrix, columns=Y.columns.values)
    sns.set(font_scale=1.4)
    sns.heatmap(df_matrix, annot=True)
    plt.show()


def kfold_classif(X,Y, splits, mlp):
    methods = {'Acurácia': 'accuracy', 'LogLoss': 'neg_log_loss', 'AUC': 'roc_auc'}
    kfold = model.KFold(n_splits=splits, random_state=1828)
    if (mlp == None):
        mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(8, 4), activation='logistic', solver='adam',
                                      learning_rate='constant', random_state=2818, max_iter=400,
                                      early_stopping=True)
    '''
    if (tipo_metodo=="Classification Report"):
        x_train, x_test, y_train, y_test = model.train_test_split(X,Y,test_size=0.33)
        mlp.fit(x_train,y_train)
        y_pred = mlp.predict(x_test)
        return(metrics.classification_report(y_test, y_pred))
    else:
    '''
    acuracia = model.cross_val_score(mlp, X, Y, cv=kfold, scoring='accuracy')
    logloss = model.cross_val_score(mlp, X, Y, cv=kfold, scoring='neg_log_loss')
    auc = model.cross_val_score(mlp, X, Y, cv=kfold, scoring='roc_auc')
    return {'Acurácia Média':acuracia.mean(),'Acurácia Desvio': acuracia.std(),
                'LogLoss Média': logloss.mean(), 'LogLoss Desvio': logloss.std(),
                'AUC Média': auc.mean(), 'AUC Desvio': auc.std()}

def executar_treino(csv_data, tipo_analise):
    n_iteracoes = 5
    labels = ['Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSeco', 'TempBulboUmido',
              'UmidadeRelativa', 'DirecaoVento', 'VelocidadeVentoNebulosidade', 'quad0', 'quad1', 'quad2', 'quad3',
              'quad4', 'quad5', 'quad6', 'quad7']
    ##Drop coluna com valores Zerados e remove NAN (representam menos de 1% da base)
    csv_data.drop(labels=['Datetime', 'PressaoAtmEstacao', 'PosicaoGrid'], axis=1, inplace=True)
    csv_data = csv_data.dropna(axis=0)
    scaler = MinMaxScaler()
    scaler.fit(csv_data)
    data_scaled = scaler.transform(csv_data)
    scaled_df = pd.DataFrame(data_scaled, columns=labels)
    X = scaled_df[
        ['Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSeco', 'TempBulboUmido',
         'UmidadeRelativa', 'DirecaoVento', 'VelocidadeVentoNebulosidade']]
    #.values.ravel()
    mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(6, 2), activation='logistic', solver='adam',learning_rate='constant', random_state=2818, max_iter=400,early_stopping=True)

    result1 = kfold_classif(X, scaled_df[['quad0']].values.ravel(),n_iteracoes,None)
    result2 = kfold_classif(X, scaled_df[['quad1']].values.ravel(),n_iteracoes,None)
    result3 = kfold_classif(X, scaled_df[['quad2']].values.ravel(),n_iteracoes,None)
    result4 = kfold_classif(X, scaled_df[['quad3']].values.ravel(),n_iteracoes,None)
    result5 = kfold_classif(X, scaled_df[['quad4']].values.ravel(),n_iteracoes,None)
    result6 = kfold_classif(X, scaled_df[['quad5']].values.ravel(),n_iteracoes,None)
    result7 = kfold_classif(X, scaled_df[['quad6']].values.ravel(),n_iteracoes,None)
    result8 = kfold_classif(X, scaled_df[['quad6']].values.ravel(),n_iteracoes,None)
    lst_res = [result1,result2,result3,result4,result5,result6,result7,result8]
    res_df = pd.DataFrame(lst_res,columns=result1.keys())
    res_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\Resultados8RedesIguais.csv", index=True, index_label='Quadrante')
    # matriz_confusao(X,Y)

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
    except FileNotFoundError:
        #Acurácia, LogLoss, AUC
        csv_data = import_data(arq_estacao_importar,arq_focos_importar)
        executar_treino(csv_data, 'Acurácia')
    else:
        executar_treino(csv_data, 'LogLoss')
