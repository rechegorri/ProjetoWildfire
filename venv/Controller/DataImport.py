from glob import glob
import numpy as np
import os
import csv
import datetime
import time
from operator import itemgetter
import Controller.DistanceMetrics as dm

def run_end_failure():
    print('Erro ao iniciar a leitura: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    exit(1)

'''
Buscar arquivos de pasta do sistema
Leituras satelite = JSON
Leituras Estacoes = CSV

INICIO
'''

def getNeighboursData(input_list):
    output_list = []
    for element in input_list:
        ##Separar registros até 72 posteriores ao ocorrido
        ##72 hrs = 259200
        next_element_id = input_list.index(element) + 1
        try:
            next_element = input_list[next_element_id]
        except IndexError:
            next_element = None
        neighbours_list = []
        while (next_element != None and element['Datetime'] - next_element['Datetime'] <= 259200):
            ##Busca distancia que o vizinho temporal está do ponto em km
            next_element['DistanciaDoPonto'] = dm.getDistanceBetweenPoints(float(element['Latitude']),
                                                                           float(element['Longitude']),
                                                                           float(next_element['Latitude']),
                                                                           float(next_element['Longitude']))
            neighbours_list.append(next_element)
            next_element_id = next_element_id + 1
            try:
                next_element = input_list[next_element_id]
            except IndexError:
                next_element = None
        out_neighbours = {'OrigemLatitude':element['Latitude']}
        out_neighbours['OrigemDotLongitude'] = element['Longitude']
        out_neighbours['OrigemDatetime'] = element['Datetime']
        out_neighbours['Vizinhos'] = neighbours_list
        output_list.append(element)
    return output_list


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
        ##Busca de datetime anterior mais proximo do foco para vincular os dados de tempo.
        index, leitura_recente_dt = min(enumerate(estacao_datetime),  key=lambda x: abs(x[1]-element['Datetime']))
        ##Valores focos incendio
        data_dict = {'RiscoFogo': element['RiscoFog']}
        data_dict['Datetime'] = element['Datetime']
        data_dict['Latitude'] = element['Latitude']
        data_dict['Longitude'] = element['Longitude']
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
    neighbours_list = getNeighboursData(data_output)
    print('Processo de importação concluido: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    return data_output,output_list