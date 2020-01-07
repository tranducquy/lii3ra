# -*- coding: utf-8 -*-


class OandaUtils:
    MAX_COUNT = 5000

    def get_count(self, count):
        c = count
        if count > OandaUtils.MAX_COUNT:
            c = OandaUtils.MAX_COUNT
        return c


class OandaSymbol():
    USDJPY = "USD_JPY"
    EURJPY = "EUR_JPY"
    GBPJPY = "GBP_JPY"
    EURUSD = "EUR_USD"
    GBPUSD = "GBP_USD"
    EURGBP = "EUR_GBP"

    @staticmethod
    def get_symbol(symbol):
        i = symbol
        if symbol == "USDJPY":
            i = OandaSymbol.USDJPY
        elif symbol == "EURJPY":
            i = OandaSymbol.EURJPY
        elif symbol == "GBPJPY":
            i = OandaSymbol.GBPJPY
        elif symbol == "EURUSD":
            i = OandaSymbol.EURUSD
        elif symbol == "GBPUSD":
            i = OandaSymbol.GBPUSD
        elif symbol == "EURGBP":
            i = OandaSymbol.EURGBP
        return i


class OandaLeg():
    S5 = "S5"
    S10 = "S10"
    S15 = "S15"
    S30 = "S30"
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    M5 = "M5"
    M10 = "M10"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"
    H4 = "H4"
    H6 = "H6"
    H8 = "H8"
    H12 = "H12"
    D = "D"
    W = "W"
    M = "M"

    @staticmethod
    def get_leg(leg):
        l = leg
        if leg == '5s':
            l = OandaLeg.S5
        elif leg == '10s':
            l = OandaLeg.S10
        elif leg == '15s':
            l = OandaLeg.S15
        elif leg == '30s':
            l = OandaLeg.S30
        elif leg == '1m':
            l = OandaLeg.M1
        elif leg == '2m':
            l = OandaLeg.M2
        elif leg == '3m':
            l = OandaLeg.M3
        elif leg == '4m':
            l = OandaLeg.M4
        elif leg == '5m':
            l = OandaLeg.M5
        elif leg == '10m':
            l = OandaLeg.M10
        elif leg == '15m':
            l = OandaLeg.M15
        elif leg == '30m':
            l = OandaLeg.M30
        elif leg == '1h':
            l = OandaLeg.H1
        elif leg == '2h':
            l = OandaLeg.H2
        elif leg == '3h':
            l = OandaLeg.H3
        elif leg == '4h':
            l = OandaLeg.H4
        elif leg == '6h':
            l = OandaLeg.H6
        elif leg == '8h':
            l = OandaLeg.H8
        elif leg == '12h':
            l = OandaLeg.H12
        elif leg == '1d' or leg == 'd' or leg == 'daily':
            l = OandaLeg.D
        elif leg == '1w' or leg == 'w' or leg == 'weekly':
            l = OandaLeg.W
        elif leg == '1m' or leg == 'm' or leg == 'monthly':
            l = OandaLeg.M
        return l
