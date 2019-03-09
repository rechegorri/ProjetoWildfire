from glob import glob
import os
import csv
import datetime
import time

'''
Buscar arquivos de pasta do sistema
Leituras satelite = JSON
Leituras Estacoes = CSV
'''
arq_estacao='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacao.2017-07-01.2018-07-01.csv'
arq_focos='C:\\Users\Livnick\Documents\dadosFocos\Focos.2017-07-01.2018-07-01.csv'
estacao_reader = csv.DictReader(open(arq_estacao), delimiter = ';')
focos_reader = csv.DictReader(open(arq_focos), delimiter = ';')
estacao_list = []

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
    estacao_list.append(data_dict)

for input in focos_reader:
    data_dict = {'RiscoFog': input['RiscoFog']}
    '''model 2017/07/03 16:53:00'''
    dt = time.mktime(datetime.datetime.strptime(input['DataHora'], "%Y/%m/%d %H:%M:%S").timetuple())
    data_dict['Datetime'] = dt
    data_dict['Latitude'] = input['Latitude']
    data_dict['Longitude'] = input['Longitud']
    print(data_dict)