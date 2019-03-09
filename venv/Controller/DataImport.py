from glob import glob
import os
import csv
import datetime

'''
Buscar arquivos de pasta do sistema
Leituras satelite = JSON
Leituras Estacoes = CSV
'''
arq_estacao='C:\\Users\Livnick\Documents\dadosFocos\DadosEstacao.2017-07-01.2018-07-01.csv'
arq_focos='C:\\Users\Livnick\Documents\dadosFocos\Focos.2017-07-01.2018-07-01.csv'
estacao_reader = csv.DictReader(open(arq_estacao), delimiter = ';')
focos_reader = csv.DictReader(open(arq_focos), delimiter = ';')
for input in estacao_reader:
    data_aux = input['Data'].split('/')
    dt = datetime.datetime(day=int(data_aux[0]), month=int(data_aux[1]), year=int(data_aux[2]),hour=int(input['Hora'][0:2]), minute=int(input['Hora'][2:4]))
    print(dt)
