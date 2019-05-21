from glob import glob
import os
import csv
import datetime
import time
from operator import itemgetter
import Controller.DistanceMetrics as dm
import pandas as pd

def run_end_failure():
    print('Erro ao iniciar a leitura: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    exit(1)

'''
Buscar arquivos de pasta do sistema
Leituras satelite = JSON
Leituras Estacoes = CSV

INICIO
'''
def determinarGridPosicao(list):
    '''
    Determina posição de grid para todos os elementos
    :param list:
    :return:
    '''
    seq_lat = [x['Latitude'] for x in list]
    seq_lon = [x['Longitude'] for x in list]
    max_lat = max(seq_lat)
    max_lon = max(seq_lon)
    min_lat = min(seq_lat)
    min_lon = min(seq_lon)
    for element in list:
        coordenadas_or = {'Latitude': element['Latitude'],
                          'Longitude': element['Longitude']}
        element['PosicaoGrid'] = dm.coordanadasParaGrid(coordenadas_or, min_lat, max_lat, min_lon, max_lon)
    return list

def getNeighboursData(input_list):
    '''
    A partir de um dado ponto P, determinar a vizinhança de pontos na região (12 horas x velocidade do vento)
    Mapear por vizinhos no tempo, dentro do espaço de 12 horas
                Q0 Q1 Q2
                Q3 DT Q4
                Q5 Q6 Q7
    '''
    for element in input_list:
        quad0, quad1, quad2, quad3, quad4, quad5, quad6, quad7 = 0, 0, 0, 0, 0, 0, 0, 0
        next_element_id = input_list.index(element) + 1
        try:
            next_element = input_list[next_element_id]
        except (ValueError, IndexError):
            next_element = None
        while (next_element is not None and next_element['Datetime'] - element['Datetime'] <= 28800 and next_element['Datetime'] > element['Datetime']):##86900=24hrs
            coord_ponto = element['PosicaoGrid']
            coord_next = next_element['PosicaoGrid']
            if (coord_next['y'] - coord_ponto['y'] == -1):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    quad0 = 1
                if (coord_next['x'] - coord_ponto['x'] == 0):
                    quad1 = 1
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    quad2 = 1
            if (coord_next['y'] - coord_ponto['y'] == 0):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    quad3 = 1
                ##0,0 é o ponto em si
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    quad4 = 1
            if (coord_next['y'] - coord_ponto['y'] == 1):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    quad5 = 1
                if (coord_next['x'] - coord_ponto['x'] == 0):
                    quad6 = 1
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    quad7 = 1
            next_element_id += 1
            try:
                next_element = input_list[next_element_id]
            except IndexError:
                break
        element['quad0'] = quad0
        element['quad1'] = quad1
        element['quad2'] = quad2
        element['quad3'] = quad3
        element['quad4'] = quad4
        element['quad5'] = quad5
        element['quad6'] = quad6
        element['quad7'] = quad7

def importacao_dados(arq_estacao, arq_focos):
    print('Inicio da importação: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    estacao_reader = csv.DictReader(open(arq_estacao), delimiter = ';')
    focos_reader = csv.DictReader(open(arq_focos), delimiter = ';')
    estacao_list = []
    focos_list = []
    estacao_datetime = []
    if arq_estacao == None or arq_focos == None:
        run_end_failure()
    for input in estacao_reader:
        '''Indexar dados em datetime'''
        data_aux = input['Data'].split('/')
        dt = time.mktime(datetime.datetime(day=int(data_aux[0]), month=int(data_aux[1]), year=int(data_aux[2]),hour=int(input['Hora'][0:2]), minute=int(input['Hora'][2:4])).timetuple())
        data_dict = {'Datetime': dt}
        data_dict['TempBulboSeco'] = input['TempBulboSeco']
        data_dict['TempBulboUmido'] = input['TempBulboUmido']
        data_dict['UmidadeRelativa'] = input['UmidadeRelativa']
        data_dict['PressaoAtmEstacao'] = input['PressaoAtmEstacao']
        data_dict['DirecaoVento'] =  input['DirecaoVento']
        data_dict['VelocidadeVentoNebulosidade'] =  input['VelocidadeVentoNebulosidade']
        estacao_datetime.append(dt)
        estacao_list.append(data_dict)
    print("Leitura de estações: " + str(len(estacao_list)))
    for input in focos_reader:
        data_dict = {'RiscoFog': input['RiscoFog']}
        '''model 2017/07/03 16:53:00'''
        dt = time.mktime(datetime.datetime.strptime(input['DataHora'], "%Y/%m/%d %H:%M:%S").timetuple())
        data_dict['Datetime'] = dt
        data_dict['Latitude'] = input['Latitude']
        data_dict['Longitude'] = input['Longitud']
        data_dict['DiaSemCh'] = input['DiaSemCh']
        data_dict['Precipit'] = input['Precipit']
        data_dict['RiscoFog'] = input['RiscoFog']
        focos_list.append(data_dict)
    print("Registros de satélite: " + str(len(focos_list)))
    estacao_list = sorted(estacao_list, key=itemgetter('Datetime'))
    focos_list = sorted(focos_list, key=itemgetter('Datetime'))
    '''
    Lista de Dict com valores de estação e satélite
    '''
    data_output = []
    index=0

    for element in focos_list:
        '''
        Varre por dados de tempo dentro da ocorrencia do ponto e concatena os mesmos
        '''
        ##Busca de datetime anterior mais proximo do foco para vincular os dados de tempo.
        index, leitura_recente_dt = min(enumerate(estacao_datetime),  key=lambda x: abs(x[1]-element['Datetime']))
        ##Valores focos incendio
        data_dict ={'Datetime' : element['Datetime']}
        data_dict['Coordenadas'] = {'Latitude':element['Latitude'], 'Longitude': element['Longitude']}
        data_dict['Latitude'] = element['Latitude']
        data_dict['Longitude'] = element['Longitude']
        data_dict['DiaSemChuva'] = element['DiaSemCh']
        data_dict['Precipitacao'] = element['Precipit']
        data_dict['RiscoFogo'] = element['RiscoFog']
        ##valores leituras tempo
        data_dict['TempBulboSeco'] = estacao_list[index]['TempBulboSeco']
        data_dict['TempBulboUmido'] = estacao_list[index]['TempBulboUmido']
        data_dict['UmidadeRelativa'] = estacao_list[index]['UmidadeRelativa']
        data_dict['PressaoAtmEstacao'] = estacao_list[index]['PressaoAtmEstacao']
        data_dict['DirecaoVento'] = estacao_list[index]['DirecaoVento']
        data_dict['VelocidadeVentoNebulosidade'] = estacao_list[index]['VelocidadeVentoNebulosidade']
        data_output.append(data_dict)
        index = index + 1
    print('Concatenação de dados: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    data_output = determinarGridPosicao(data_output)
    getNeighboursData(data_output)
    dados_filtrados = []
    for element in data_output:
        if(element['quad0'] + element['quad1'] + element['quad2'] + element['quad3'] +
        element['quad4'] + element['quad5'] + element['quad6'] + element['quad7']>0):
            dados_filtrados.append(element)
    print('Processo de mapeamento de vizinhos concluido: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    output_labels = ['Datetime', 'Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSeco','TempBulboUmido',
                     'UmidadeRelativa', 'PressaoAtmEstacao', 'DirecaoVento', 'VelocidadeVentoNebulosidade',
                      'PosicaoGrid', 'quad0', 'quad1', 'quad2', 'quad3',
                      'quad4', 'quad5', 'quad6', 'quad7']
    output_df = pd.DataFrame(dados_filtrados, columns=output_labels)
    output_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosFormatados.csv", index=False)
    print("Numero de valores com vizinhos: "+str(len(dados_filtrados)))
    print('Arquivo Gerado: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    return output_df