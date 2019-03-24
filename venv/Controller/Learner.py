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

def neural_network_treiner(data_input):
    print('Iniciando treino de dados: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    MLPC = neuralnetwork.MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto', beta_1=0.9,
           beta_2=0.999, early_stopping=False, epsilon=1e-08,
           hidden_layer_sizes=(9, 3), learning_rate='constant',
           learning_rate_init=0.001, max_iter=200, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=9, shuffle=True,
           solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=True,
           warm_start=False)
    Y = data_input.loc[:,'LatitudeProximo':'DatetimeProximo']
    X = data_input.loc[:,:'VelocidadeVentoNebulosidade']
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.7)
    MLPC.fit(x_train, y_train)
    print('Treino de dados concluido: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    #y_pred_MLPC = MLPC.predict(x_test)
    #y_score = MLPC.score(x_test, y_test)
    print("Valor pred: ".format(MLPC.predict(x_test)))
    print('Media do score: '.format(MLPC.score(x_test, y_test)))
    print('Testes realizados {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))

##Inserção de dados
def import_data(arq_estacao, arq_focos):
    print('Gerando arquivo: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    trainer_data = di.importacao_dados(arq_estacao_treino, arq_focos_treino)
    data_values = []
    #for element in trainer_data:
    #    data_values.append(list(element.values()))
    labels = ['RiscoFogo', 'Datetime', 'Latitude', 'Longitude', 'TempBulboSeco', 'TempBulboUmido', 'UmidadeRelativa',
              'PressaoAtmEstacao', 'DirecaoVento', 'VelocidadeVentoNebulosidade','LatitudeProximo','LongitudeProximo',
              'DatetimeProximo']
    dclean_df = pd.DataFrame(trainer_data, columns=labels, index='Datetime')
    dclean_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", index=False)
    return dclean_df

def prepare_train(csv_data):
    del csv_data['RiscoFogo']#Cerca de 68% dos dados vazios afeta os resultados
    data_semzeros = csv_data[csv_data['DatetimeProximo'] > 0]
    min_max_scaler = MinMaxScaler()
    data_pronto = pd.DataFrame(min_max_scaler.fit_transform(csv_data.values), columns=csv_data.columns, index=csv_data.index)
    #print(data_pronto.isna().sum()/data_pronto.shape[0])
    neural_network_treiner(data_pronto)

if __name__ == '__main__':
    print('Inicio fluxo: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    arq_estacao_treino='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacao.2017-07-01.2018-07-01.csv'
    arq_focos_treino='C:\\Users\Livnick\Documents\dadosFocos\Focos.2017-07-01.2018-07-01.csv'
    try:
        csv_data = pd.read_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosLimpos.csv", encoding='utf8', index_col='Datetime')
    except FileNotFoundError:
        csv_data = import_data(arq_focos_treino,arq_focos_treino)
        prepare_train(csv_data)
    else:
        prepare_train(csv_data)


