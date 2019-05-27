from glob import glob
import os
import csv
import datetime
import time
from operator import itemgetter
import Controller.DistanceMetrics as dm
import pandas as pd

'''
Codigo;Local;Latitude;Longitude
82571;BARRA DO CORDA - MA;-5.5;-45.23
82564;IMPERATRIZ - MA;-5.53;-47.48
'''
estacao_82571 = {'Codigo':'82571',
                 'Local':'Barra do Corda - MA',
                 'Latitude':-5.50,
                 'Longitude':-45.23}

estacao_82564 = {'Codigo':'82564',
                 'Local':'Imperatriz - MA',
                 'Latitude':-5.53,
                 'Longitude':-47.48}

def run_end_failure():
    print('Erro - Arquivo não encontrado: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
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

def importClimaData(estacao_reader, estacao_datetime):
    estacao_list = []
    for input in estacao_reader:
        '''Indexar dados em datetime'''
        data_aux = input['Data'].split('/')
        #data_aux = input[1].split('/')
        dt = time.mktime(datetime.datetime(day=int(data_aux[0]), month=int(data_aux[1]),
        year=int(data_aux[2]),hour=int(input['Hora'][0:2]), minute=int(input['Hora'][2:4])).timetuple())
        data_dict = {'Datetime': dt}
        data_dict['CodEstacao'] = input['Estacao']
        data_dict['TempBulboSeco'] = input['TempBulboSeco']
        data_dict['TempBulboUmido'] = input['TempBulboUmido']
        data_dict['UmidadeRelativa'] = input['UmidadeRelativa']
        data_dict['DirecaoVento'] =  input['DirecaoVento']
        data_dict['VelocidadeVentoNebulosidade'] =  input['VelocidadeVentoNebulosidade']
        estacao_datetime.append(dt)
        estacao_list.append(data_dict)
    estacao_datetime.sort()
    estacao_list = sorted(estacao_list, key=itemgetter('Datetime'))
    print("Leitura de estação: " + str(len(estacao_list)))
    return estacao_list, estacao_datetime

def getNeighboursData(input_list):
    '''
    A partir de um dado ponto P, determinar a vizinhança de pontos na região (12 horas x velocidade do vento)
    Mapear por vizinhos no tempo, dentro do espaço de 12 horas
                Q0 Q1 Q2
                Q3 DT Q4
                Q5 Q6 Q7
    '''
    for element in input_list:
        next_element_id = input_list.index(element) + 1
        neighbours_lst = []
        try:
            next_element = input_list[next_element_id]
        except (ValueError, IndexError):
            next_element = None
        while (next_element is not None and next_element['Datetime'] - element['Datetime'] <= 43450 and next_element['Datetime'] > element['Datetime']):##86900=24hrs
            coord_ponto = element['PosicaoGrid']
            coord_next = next_element['PosicaoGrid']
            if (coord_next['y'] - coord_ponto['y'] == -1):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    if 'quad0' not in neighbours_lst:
                        neighbours_lst.append('quad0')
                if (coord_next['x'] - coord_ponto['x'] == 0):
                    if 'quad1' not in neighbours_lst:
                        neighbours_lst.append('quad1')
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    if 'quad2' not in neighbours_lst:
                        neighbours_lst.append('quad2')
            if (coord_next['y'] - coord_ponto['y'] == 0):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    if 'quad3' not in neighbours_lst:
                        neighbours_lst.append('quad3')
                ##0,0 é o ponto em si
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    if 'quad4' not in neighbours_lst:
                        neighbours_lst.append('quad4')
            if (coord_next['y'] - coord_ponto['y'] == 1):
                if (coord_next['x'] - coord_ponto['x'] == 1):
                    if 'quad5' not in neighbours_lst:
                        neighbours_lst.append('quad5')
                if (coord_next['x'] - coord_ponto['x'] == 0):
                    if 'quad6' not in neighbours_lst:
                        neighbours_lst.append('quad6')
                if (coord_next['x'] - coord_ponto['x'] == -1):
                    if 'quad7' not in neighbours_lst:
                        neighbours_lst.append('quad7')
            next_element_id += 1
            try:
                next_element = input_list[next_element_id]
            except IndexError:
                break
        element['Vizinhos'] = neighbours_lst


def importacao_dados(arq_estacao_82571, arq_estacao_82564, arq_focos):
    print('Inicio da importação: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    estacao_reader_82571 = csv.DictReader(open(arq_estacao_82571), delimiter = ';')
    estacao_reader_82564 = csv.DictReader(open(arq_estacao_82564), delimiter = ';')
    focos_reader = csv.DictReader(open(arq_focos), delimiter = ';')
    focos_list = []
    estacao_datetime_82571 = []
    estacao_datetime_82564 = []
    if arq_estacao_82571 == None or arq_estacao_82564 == None or arq_focos == None:
        run_end_failure()

    '''
    Coleta dados de estações metereológicas
    '''
    estacao_lst_82571, estacao_datetime_82571 = importClimaData(estacao_reader_82571,estacao_datetime_82571)
    estacao_lst_82564, estacao_datetime_82564 = importClimaData(estacao_reader_82564,estacao_datetime_82564)

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
    #estacao_list = sorted(estacao_list, key=itemgetter('Datetime'))
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
        index_82564, leitura_recente_dt0 = min(enumerate(estacao_datetime_82564),  key=lambda x: abs(x[1]-element['Datetime']))
        index_82571, leitura_redente_dt1 = min(enumerate(estacao_datetime_82571), key=lambda x: abs(x[1]-element['Datetime']))
        ##Valores focos incendio
        data_dict ={'Datetime' : element['Datetime']}
        data_dict['Coordenadas'] = {'Latitude':element['Latitude'], 'Longitude': element['Longitude']}
        data_dict['Latitude'] = element['Latitude']
        data_dict['Longitude'] = element['Longitude']
        data_dict['DiaSemChuva'] = element['DiaSemCh']
        data_dict['Precipitacao'] = element['Precipit']
        data_dict['RiscoFogo'] = element['RiscoFog']
        ##valores leituras tempo
        data_dict['TempBulboSecoEst1'] = estacao_lst_82564[index_82564]['TempBulboSeco']
        data_dict['TempBulboUmidoEst1'] = estacao_lst_82564[index_82564]['TempBulboUmido']
        data_dict['UmidadeRelativaEst1'] = estacao_lst_82564[index_82564]['UmidadeRelativa']
        data_dict['DirecaoVentoEst1'] = estacao_lst_82564[index_82564]['DirecaoVento']
        data_dict['VelocidadeVentoNebulosidadeEst1'] = estacao_lst_82564[index_82564]['VelocidadeVentoNebulosidade']
        data_dict['DistanciaParaEst1'] = dm.getDistanceBetweenPoints(float(element['Latitude']),
                                                                     float(element['Longitude']),
                                                                     float(estacao_82564['Latitude']),
                                                                     float(estacao_82564['Longitude']))
        data_dict['TempBulboSecoEst2'] = estacao_lst_82571[index_82571]['TempBulboSeco']
        data_dict['TempBulboUmidoEst2'] = estacao_lst_82571[index_82571]['TempBulboUmido']
        data_dict['UmidadeRelativaEst2'] = estacao_lst_82571[index_82571]['UmidadeRelativa']
        data_dict['DirecaoVentoEst2'] = estacao_lst_82571[index_82571]['DirecaoVento']
        data_dict['VelocidadeVentoNebulosidadeEst2'] = estacao_lst_82571[index_82571]['VelocidadeVentoNebulosidade']
        data_dict['DistanciaParaEst2'] = dm.getDistanceBetweenPoints(float(element['Latitude']),
                                                                     float(element['Longitude']),
                                                                     float(estacao_82571['Latitude']),
                                                                     float(estacao_82571['Longitude']))
        data_output.append(data_dict)
        index_82564 = index_82564 + 1
    print('Concatenação de dados: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    data_output = determinarGridPosicao(data_output)
    getNeighboursData(data_output)
    dados_filtrados = []
    for element in data_output:
        if(len(element['Vizinhos'])>0):
            dados_filtrados.append(element)
    print('Processo de mapeamento de vizinhos concluido: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    output_labels = ['Datetime', 'Latitude', 'Longitude', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'TempBulboSecoEst1','TempBulboUmidoEst1',
                     'UmidadeRelativaEst1', 'DirecaoVentoEst1', 'VelocidadeVentoNebulosidadeEst1','DistanciaParaEst1',
                     'TempBulboSecoEst2', 'TempBulboUmidoEst2','UmidadeRelativaEst2', 'DirecaoVentoEst2',
                     'VelocidadeVentoNebulosidadeEst2', 'DistanciaParaEst2',
                      'PosicaoGrid', 'Vizinhos']
    output_df = pd.DataFrame(dados_filtrados, columns=output_labels)
    output_df.to_csv("C:\\Users\Livnick\Documents\dadosFocos\DadosFormatados.csv", index=False)
    print("Numero de valores com vizinhos: "+str(len(dados_filtrados)))
    print('Arquivo Gerado: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    return output_df