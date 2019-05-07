from math import sin, cos, sqrt, atan2, radians, pi

# raio aprox da terra em km
R = 6371.0

def getDistanceBetweenPoints(o_lat ,o_long ,d_lat ,d_long):
    dlat = deg2rad(d_lat - o_lat)
    dlong = deg2rad(d_long - o_long)
    a = sin(dlat / 2) ** 2 + cos(deg2rad(o_lat)) * cos(deg2rad(d_long)) * sin(dlong / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c ##Em km

def deg2rad(deg):
    return deg*(pi/180)
