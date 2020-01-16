class Unit:

    @staticmethod
    def get_unit(symbol):
        if ('^N225'
                or '1570.T' in symbol
                or '1357.T' in symbol
                or '1568.T' in symbol
                or '1356.T' in symbol
                or '1617.T' in symbol
                or '1618.T' in symbol
                or '1619.T' in symbol
                or '1620.T' in symbol
                or '1621.T' in symbol
                or '1622.T' in symbol
                or '1623.T' in symbol
                or '1624.T' in symbol
                or '1625.T' in symbol
                or '1626.T' in symbol
                or '1627.T' in symbol
                or '1628.T' in symbol
                or '1629.T' in symbol
                or '1630.T' in symbol
                or '1631.T' in symbol
                or '1632.T' in symbol
                or '1633.T' in symbol):
            unit = 1
        elif '.T' in symbol:
            unit = 100
        elif 'N225minif' in symbol:
            unit = 100
        elif 'N225f' in symbol:
            unit = 1000
        elif 'JPX400f' in symbol:
            unit = 1000
        elif 'Mothersf' in symbol:
            unit = 1000
        else:
            unit = 1
        return unit

    @staticmethod
    def is_order_vol_infinity(symbol):
        if ('XBTUSD' == symbol
                or 'ETHUSD' == symbol
                or 'USDJPY' == symbol
                or 'GBPJPY' == symbol
                or 'EURJPY' == symbol
                or 'EURUSD' == symbol
                or 'N225f' == symbol
                or 'N225minif' == symbol
                or '^N225' == symbol
                or '1321.T' == symbol
                or 'Topixf' == symbol
                or 'Topixminif' == symbol
                or 'Topix' == symbol
                or 'JPX400f' == symbol
                or 'JPX400' == symbol
                or 'Mothersf' == symbol
                or 'Mothers' == symbol):
            return True
        else:
            return False
