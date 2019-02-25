# Cell model with basic attributes to be consumed by the NAN
# Coordenadas:
# 1 Grau Latitude: 111,12km
# 1 Grau Longitude: 0 - 111,12km
# precisão de 3 casas (aprox 111m)
# Status: consumed, flamable, non-flamable, in-flames
from enum import Enum

CellStatusEnum = Enum('CellStatusEnum','CONSUMED FLAMABLE NONFLAMABLE BEINGCONSUMED')

class GridCell:
    def __init__(self, x, y, altitude, time_reading, wind_direction, wind_speed, air_humidity):
        self.x=x
        self.y=y
        self.altitude=altitude
        self.time_reading=time_reading
        self.wind_direction=wind_direction
        self.wind_speed=wind_speed
        self.air_humidity=air_humidity
        self.flam_state_last=None
        self.flam_state_current=None
        self.flam_state_next=None

    ##Funcoes para normalizacao de dados para MLP
    def getLastCellStatusInt(self):
        if self.flam_state_last == CellStatusEnum.NONFLAMABLE:
            return 0.25
        if self.flam_state_last == CellStatusEnum.FLAMABLE:
            return 0.50
        if self.flam_state_last == CellStatusEnum.BEINGCONSUMED:
            return 0.75
        else:
            return 1.0

    def getCurrentCellStatusInt(self):
        if self.flam_state_last == CellStatusEnum.NONFLAMABLE:
            return 0.25
        if self.flam_state_last == CellStatusEnum.FLAMABLE:
            return 0.50
        if self.flam_state_last == CellStatusEnum.BEINGCONSUMED:
            return 0.75
        else:
            return 1.0

    def getNextCellStatusInt(self):
        if self.flam_state_last == CellStatusEnum.NONFLAMABLE:
            return 0.25
        if self.flam_state_last == CellStatusEnum.FLAMABLE:
            return 0.50
        if self.flam_state_last == CellStatusEnum.BEINGCONSUMED:
            return 0.75
        else:
            return 1.0

##Funcao para normalizar valores em ENUM de status
    def setNextCellStatusInt(self, value):
        if value >0 and value <= 0.25:
            self.flam_state_next = CellStatusEnum.NONFLAMABLE
            return
        if value <= 0.50:
            self.flam_state_next = CellStatusEnum.FLAMABLE
            return
        if value <= 0.75:
            self.flam_state_next = CellStatusEnum.BEINGCONSUMED
            return
        if value <= 1.00:
            self.flam_state_next = CellStatusEnum.CONSUMED
            return

    def setLastCellStatusInt(self, value):
        if value >0 and value <= 0.25:
            self.flam_state_last = CellStatusEnum.NONFLAMABLE
            return
        if value <= 0.50:
            self.flam_state_last = CellStatusEnum.FLAMABLE
            return
        if value <= 0.75:
            self.flam_state_last = CellStatusEnum.BEINGCONSUMED
            return
        if value <= 1.00:
            self.flam_state_last = CellStatusEnum.CONSUMED
            return

    def setCurrentCellStatusInt(self, value):
        if value >0 and value <= 0.25:
            self.flam_state_current = CellStatusEnum.NONFLAMABLE
            return
        if value <= 0.50:
            self.flam_state_current = CellStatusEnum.FLAMABLE
            return
        if value <= 0.75:
            self.flam_state_current = CellStatusEnum.BEINGCONSUMED
            return
        if value <= 1.00:
            self.flam_state_current = CellStatusEnum.CONSUMED
            return