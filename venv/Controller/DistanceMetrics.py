from math import sin, cos, sqrt, atan2, radians, degrees, pi
from haversine import haversine, Units
import operator

# raio aprox da terra em km
R = 6371.0

def getDistanceBetweenPoints(o_lat ,o_long ,d_lat ,d_long):
    origin = (o_lat,o_long)
    destination = (d_lat,d_long)
    return haversine(origin,destination,unit=Units.KILOMETERS)

def getBearingBetweenPoints(origin, destination):
    '''
    :param origin: ponto de partida
    :param destination: ponto de destino
    :return: angulo em graus entre dois pontos.
    '''
    o_lat = float(origin['Latitude'])
    o_long = float(origin['Longitude'])
    d_lat = float(destination['Latitude'])
    d_long = float(destination['Longitude'])
    o_lat, o_long, d_lat, d_long = map(radians, [o_lat, o_long, d_lat, d_long])
    dlat = d_lat - o_lat
    dlong = d_long - o_long
    x = cos(d_lat)*sin(dlong)
    y = cos(o_lat)*sin(d_lat)-sin(o_lat)*cos(d_lat)*cos(dlong)
    bearing = atan2(x,y)
    return operator.mod(degrees(bearing),360)

def getBearingFromInmet(value):
    if(value==0):
        return 0
    if (value==99):
        return 0
    else:
        return value*10

def get_valor_normalizado(valor, min, max):
    ##Regra de 3
    return ((valor - min)/(max - min))

def coordanadasParaGrid(coordenadas, min_lat, max_lat, min_lon, max_lon):
    '''
    :param coordenadas: valores de ponto em lat e long
    :param min_lat:
    :param max_lat:
    :param min_lon:
    :param max_lon:
    :return: grid referente a latitude e longitude do ponto. (42 x 33 - aprox. quadrado de 10km de lado)
    '''
    x = (float(coordenadas['Latitude']) - float(min_lat))/ (float(max_lat) - float(min_lat))
    grid_x = int(x*42)#413.54 km entre min e max
    y = (float(coordenadas['Longitude']) - float(min_lon))/ (float(max_lon) - float(min_lon))
    grid_y = int(y*33)#320.15 km entre min e max
    return {'x':grid_x,
            'y':grid_y}