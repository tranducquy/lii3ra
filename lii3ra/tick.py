
class Tick:
    @staticmethod
    def get_tick(symbol):
        if "JPY" in symbol:
            tick = 0.01
        elif symbol == 'EURUSD' or symbol == 'GBPUSD':
            tick = 0.00001
        elif ".T" in symbol:  # 東証
            tick = 1
        elif "^N225" in symbol:  # 日経225
            tick = 1
        elif "N225mini" in symbol:  # ミニ日経225先物
            tick = 5
        elif "N225f" in symbol:  # 日経225先物
            tick = 10
        else:  # 未知
            tick = 0.01
        return tick
