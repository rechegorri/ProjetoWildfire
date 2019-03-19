import sklearn.neural_network as neuralnetwork
from sklearn.preprocessing import MinMaxScaler
import Models.gridCell as grid
import Controller.DataImport as di
from random import triangular, random
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime
import datetime
import matplotlib.pyplot as plt
from sklearn import datasets
'''
Treino de dados da MLP, 
valor X se trata das entradas de dados para treino
valor Y são os resultados esperados a partir do dataset de treino
'''

def neural_network_treiner(X):
    print('Iniciando treino de dados: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    scaler = MinMaxScaler()
    mlpc = neuralnetwork.MLPClassifier(
        hidden_layer_sizes=(10,5), activation='tanh', solver='sgd',
        learning_rate='constant', verbose=True, momentum=0.9,
        nesterovs_momentum=True)
    x_train,x_test,y_train,y_test = None
    MLPC.fit(X2_train, Y_train)
    print('Treino de dados concluido: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    y_pred_MLPC = MLPC.predict_log_proba(X2_test)
    y_pred_MLPC = pd.DataFrame(y_pred_MLPC[:, 1:2], columns=['MLPC_predictions'])
    print('Testes realizados'.format(datetime.datetime.now()))

##Inserção de dados
def import_data(arq_estacao, arq_focos):
    print('Gerando arquivo: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    trainer_data = di.importacao_dados(arq_estacao_treino, arq_focos_treino)
    data_values = []
    for element in trainer_data:
        data_values.append(list(element.values()))
    labels = ['RiscoFogo', 'Datetime', 'Latitude', 'Longitude', 'TempBulboSeco', 'TempBulboUmido', 'UmidadeRelativa',
              'PressaoAtmEstacao', 'DirecaoVento', 'VelocidadeVentoNebulosidade','LatitudeProximo','LongitudeProximo',
              'DatetimeProximo']
    dclean_df = pd.DataFrame.from_records(data_values, columns=labels)
    dclean_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", index=False)
    return dclean_df

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacao.2017-07-01.2018-07-01.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\Focos.2017-07-01.2018-07-01.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", encoding='utf8', index_col='Datetime')
    except FileNotFoundError:
        csv_data = import_data(arq_focos_treino,arq_focos_treino)
        print("Elementos retirados: " + str(len(csv_data)))
        print('Valores extraidos: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
        csv_data = csv_data.fillna(0)
        data_y = csv_data.loc[:, 'LatitudeProximo':'DatetimeProximo']
        data_x = csv_data.loc[:, 'RiscoFogo':'DirecaoVento']
    else:
        csv_data = csv_data.fillna(0)
        data_y = csv_data.loc[:,'LatitudeProximo':'DatetimeProximo']
        data_x = csv_data.loc[:,'RiscoFogo':'DirecaoVento']
        print(data_x.describe())
