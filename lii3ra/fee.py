
class Fee:
    @staticmethod
    def get_fee(symbol):
        """売買の往復手数料"""
        fee = 0
        if '.T' in symbol:
            fee = 1500 # 仮
        elif ('USD' in symbol
                or 'JPY' in symbol):
            fee = 0
        elif ('N225mini' in symbol):
            fee = 0
        else:
            fee = 0
        return fee

    @staticmethod
    def get_fee_per_unit(symbol):
        """ユニット毎の売買往復手数料"""
        fee = 0
        if '.T' in symbol:
            fee = 0
        elif ('USD' in symbol
                or 'JPY' in symbol):
            fee = 0
        elif ('N225f' in symbol):
            fee = 600 / 1000
        elif ('N225minif' in symbol):
            fee = 80 / 100
        else:
            fee = 0
        return fee

    @staticmethod
    def get_spread(symbol):
        """仮で固定のスプレッド"""
        spread = 0.0
        if 'USDJPY' == symbol:
            spread = 0.008
        elif 'EURJPY' == symbol:
            spread = 0.013
        elif 'GBPJPY' == symbol:
            spread = 0.028
        elif 'EURUSD' == symbol:
            spread = 0.00008
        elif 'GBPUSD' == symbol:
            spread = 0.00013
        return spread
