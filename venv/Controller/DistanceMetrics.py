from math import sin, cos, sqrt, atan2, radians, degrees, pi
from haversine import haversine, Units

# raio aprox da terra em km
R = 6371.0

def getDistanceBetweenPoints(o_lat ,o_long ,d_lat ,d_long):
    origin = (o_lat,o_long)
    destination = (d_lat,d_long)
    return haversine(origin,destination,unit=Units.KILOMETERS)

def getBearingBetweenPoints(o_lat ,o_long ,d_lat ,d_long):
    o_lat, o_long, d_lat, d_long = map(radians, [o_lat, o_long, d_lat, d_long])
    dlat = d_lat - o_lat
    dlong = d_long - o_long
    x = cos(d_lat)*sin(dlong)
    y = cos(o_lat)*sin(d_lat)-sin(o_lat)*cos(d_lat)*cos(dlong)
    bearing = atan2(x,y)
    return degrees(bearing)

def getBearingFromInmet(value):
    if(value==0):
        return 0
    if (value==99):
        return 0
    else:
        return value*10
