import sklearn.neural_network as neuralnetwork
import sklearn.svm as svm
from sklearn import model_selection as model
import sklearn.metrics as metrics
import Controller.DataImport as di
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
import datetime as dt
import matplotlib.pyplot as plt
from sklearn import datasets
import seaborn as sns
import matplotlib.pyplot as plt
import math
import pickle
import folium as fl
import time
import Controller.BuscaGridCV as buscaCV

def matriz_confusao(Y_true,Y_pred):
    labels = ['Quad0','Quad1','Quad2','Quad3','Quad4','Quad5','Quad6','Quad7']
    conf_mat_dict = {}
    for label_col in range(len(labels)):
        y_true_lbl = Y_true[:,label_col]
        y_pred_lbl = Y_pred[:,label_col]
        conf_mat_dict[labels[label_col]] = metrics.confusion_matrix(y_pred=y_pred_lbl,y_true=y_true_lbl)
    return conf_mat_dict
    #for label, matrix in conf_mat_dict.items():
        #sns.set()
        #ax = sns.heatmap(matrix)
        #plt.show(ax)
        #print("Matrix de confusão para {}:".format(label))
        #print(matrix)
    #sns.set(font_scale=1.4)
    #sns.heatmap(data=)
    #plt.show()


def kfold_classif(X,Y, splits, method):
    methods = {'Acurácia': 'accuracy', 'LogLoss': 'neg_log_loss', 'AUC': 'roc_auc'}
    kfold = model.KFold(n_splits=splits, random_state=1828)
    acuracia = model.cross_val_score(method, X, Y, cv=kfold, scoring='accuracy')#Acertos sobre erros balanceado
    avg_precision = model.cross_val_score(method, X, Y, cv=kfold, scoring='average_precision')
    recall_score = model.cross_val_score(method, X, Y, cv=kfold, scoring='recall')#True Pos/ (True Pos + False Pos)
    auc_score = model.cross_val_score(method, X, Y, cv=kfold, scoring='roc_auc')#Area sobre a curva que entre TP e FP, quanto mais positivo melhor
    return {'Acuracia Media':acuracia.mean(),'Acuracia Desvio': acuracia.std(),
            'Precisao Media': avg_precision.mean(), 'Precisao Desvio': avg_precision.std(),
            'AUC Media':auc_score.mean(), 'AUC Desvio': auc_score.std(),
            'Recall Media': recall_score.mean(), 'Recall Desvio':recall_score.std()
            }

def treino_binarizacao(X,Y):
    labels = ['Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSecoEst1','TempBulboUmidoEst1',
                     'UmidadeRelativaEst1', 'DirecaoVentoEst1', 'VelocidadeVentoNebulosidadeEst1','DistanciaParaEst1',
                     'TempBulboSecoEst2', 'TempBulboUmidoEst2','UmidadeRelativaEst2', 'DirecaoVentoEst2',
                     'VelocidadeVentoNebulosidadeEst2', 'DistanciaParaEst2']
    mlb = MultiLabelBinarizer()
    Ybin = mlb.fit_transform(Y)
    mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(10,4), activation='tanh', solver='lbfgs',
    learning_rate='invscaling', random_state=2818, max_iter=400,early_stopping=True)
    x_train,x_test,y_train,y_test = model.train_test_split(X,Y,train_size=0.33)
    mlp.fit(x_train,y_train)
    y_pred = mlp.predict(x_test)
    print("Erro de cobertura:"+str(metrics.coverage_error(y_test,y_pred)))
    print("Precisão média de labels:"+str(metrics.label_ranking_average_precision_score(y_test,y_pred)))
    print("Perda de ranks:"+str(metrics.label_ranking_loss(y_test,y_pred)))
    matriz = matriz_confusao(y_test, y_pred)
    results = {
        "Erro de cobertura": metrics.coverage_error(y_test,y_pred),
        "Precisão média de labels": metrics.label_ranking_average_precision_score(y_test,y_pred),
        "Perda de ranks":metrics.label_ranking_loss(y_test,y_pred),
        "Matrizes": matriz
    }
    res_df = pd.DataFrame(results)
    res_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\ResultadosMAcomMatriz2.csv")

def executar_treino(csv_data):
    n_iteracoes = 3
    labels = ['Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSecoEst1','TempBulboUmidoEst1',
                     'UmidadeRelativaEst1', 'DirecaoVentoEst1', 'VelocidadeVentoNebulosidadeEst1','DistanciaParaEst1',
                     'TempBulboSecoEst2', 'TempBulboUmidoEst2','UmidadeRelativaEst2', 'DirecaoVentoEst2',
                     'VelocidadeVentoNebulosidadeEst2', 'DistanciaParaEst2']
    ##Drop coluna com valores Zerados e remove NAN (representam menos de 1% da base)
    csv_data.drop(labels=['Datetime', 'PosicaoGrid'], axis=1, inplace=True)
    csv_data = csv_data.fillna(0)
    X = csv_data[labels]
    Y = csv_data['Vizinhos']
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(data=scaler.fit_transform(X), columns=labels)
    #results_df = pd.DataFrame(buscaCV.rodarGridCV(X_scaled,Y))
    #results_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\ResultadosGridCV.csv")
    #treino_binarizacao(X_scaled,Y)
    #.values.ravel()

def preprocessamento(csv_data, y_splits):
    labels = ['DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSecoEst1',
              'TempBulboUmidoEst1',
              'UmidadeRelativaEst1', 'DirecaoVentoEst1', 'VelocidadeVentoNebulosidadeEst1', 'DistanciaParaEst1',
              'TempBulboSecoEst2', 'TempBulboUmidoEst2', 'UmidadeRelativaEst2', 'DirecaoVentoEst2',
              'VelocidadeVentoNebulosidadeEst2', 'DistanciaParaEst2', 'GridPosicao_x', 'GridPosicao_y', 'Quad0',
              'Quad1', 'Quad2', 'Quad3', 'Quad4', 'Quad5', 'Quad6', 'Quad7']
    scaler = MinMaxScaler()
    data_normalized = pd.DataFrame(scaler.fit_transform(csv_data), columns=labels)
    X = data_normalized[['DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSecoEst1',
                         'TempBulboUmidoEst1',
                         'UmidadeRelativaEst1', 'DirecaoVentoEst1', 'VelocidadeVentoNebulosidadeEst1',
                         'DistanciaParaEst1',
                         'TempBulboSecoEst2', 'TempBulboUmidoEst2', 'UmidadeRelativaEst2', 'DirecaoVentoEst2',
                         'VelocidadeVentoNebulosidadeEst2', 'DistanciaParaEst2', 'GridPosicao_x', 'GridPosicao_y']]
    if(y_splits==1):
        Y = []
        Y.append(data_normalized[['Quad0','Quad1', 'Quad2', 'Quad3', 'Quad4', 'Quad5', 'Quad6', 'Quad7']])
    if(y_splits==2):
        Y = []
        Y.append(data_normalized[['Quad0','Quad1', 'Quad2', 'Quad3']])
        Y.append(data_normalized[['Quad4','Quad5', 'Quad6', 'Quad7']])
    if(y_splits==4):
        Y = []
        Y.append(data_normalized[['Quad0', 'Quad1']])
        Y.append(data_normalized[['Quad2', 'Quad3']])
        Y.append(data_normalized[['Quad4', 'Quad5']])
        Y.append(data_normalized[['Quad6', 'Quad7']])
    if(y_splits==8):
        Y = []
        Y.append(data_normalized[['Quad0']].values.ravel())
        Y.append(data_normalized[['Quad1']].values.ravel())
        Y.append(data_normalized[['Quad2']].values.ravel())
        Y.append(data_normalized[['Quad3']].values.ravel())
        Y.append(data_normalized[['Quad4']].values.ravel())
        Y.append(data_normalized[['Quad5']].values.ravel())
        Y.append(data_normalized[['Quad6']].values.ravel())
        Y.append(data_normalized[['Quad7']].values.ravel())
    return X,Y

def treino_MLPC(csv_data):
    mlp = neuralnetwork.MLPClassifier(hidden_layer_sizes=(10, 4), activation='tanh', solver='lbfgs',
                                      learning_rate='invscaling', random_state=2818, max_iter=400, early_stopping=True)
    X,Y_list = preprocessamento(csv_data,8)
    lst_dc = []
    for aux in Y_list:
        lst_dc.append(kfold_classif(X,aux,3,mlp))
    lst_df = pd.DataFrame(lst_dc)
    lst_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\MLPC ResultadosGrajau8Redes.csv")

def treino_SVM(csv_data):
    '''
    Uso de método SVM para comparativo de resultados com o MLPC
    '''
    clf = svm.SVC(gamma='auto')
    X,Y_list = preprocessamento(csv_data,8)

    lst_dc = []
    for aux in Y_list:
        lst_dc.append(kfold_classif(X,aux,3,clf))
    lst_df = pd.DataFrame(lst_dc)
    lst_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\SVC_ResultadosGrajau8RedesGrid.csv")

##Inserção de dados
def import_data(arq_estacao0, arq_estacao1, arq_focos):
    tempo_inicio = time.time()
    dados_df = di.importacao_dados(arq_estacao0, arq_estacao1, arq_focos)
    tempo_decorrido = time.time() - tempo_inicio
    print('Tempo Decorrido: '+str(dt.timedelta(seconds=tempo_decorrido)))
    return dados_df

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(dt.datetime.now()))
    arq_estacao0_importar='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacaoBarraDoCordaMA.csv'
    arq_estacao1_importar='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacaoImperatrizMA.csv'
    arq_focos_importar='C:\\Users\Livnick\Documents\dadosFocos\FocosGrajauMA.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosFormatados.csv", encoding='utf8', index_col=None)
    except FileNotFoundError:
        #Acurácia, LogLoss, AUC
        csv_data = import_data(arq_estacao0_importar, arq_estacao1_importar,arq_focos_importar)
        #treino_MLPC(csv_data)
        #executar_treino(csv_data)
    else:
        csv_data.drop(labels=['Datetime', 'Latitude', 'Longitude'], axis=1, inplace=True)
        csv_data = csv_data.fillna(0)
        treino_SVM(csv_data)
        treino_MLPC(csv_data)
        #executar_treino(csv_data)
