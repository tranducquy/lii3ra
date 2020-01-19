

# Strategyの検討

## テクニカルインジケーターを使ってみる
- [x] Simple Moving Average 'SMA'
- [ ] Simple Moving Median 'SMM'
- [ ] Smoothed Simple Moving Average 'SSMA'
- [ ] Exponential Moving Average 'EMA'
  - [x] 移動平均乖離率による日足Entry寄成 一応増える
  - [x] 移動平均乖離率による日足Entry逆指値 一応寄成より増える
  - [ ] 移動平均乖離率による寄り逆張りのデイトレード
- [ ] Double Exponential Moving Average 'DEMA'
- [ ] Triple Exponential Moving Average 'TEMA'
- [x] Triangular Moving Average 'TRIMA'
- [ ] Triple Exponential Moving Average Oscillator 'TRIX'
- [ ] Volume Adjusted Moving Average 'VAMA'
- [ ] Kaufman Efficiency Indicator 'ER'
- [ ] Kaufman's Adaptive Moving Average 'KAMA'
- [ ] Zero Lag Exponential Moving Average 'ZLEMA'
- [ ] Weighted Moving Average 'WMA'
- [ ] Hull Moving Average 'HMA'
- [ ] Elastic Volume Moving Average 'EVWMA'
- [ ] Volume Weighted Average Price 'VWAP'
- [ ] Smoothed Moving Average 'SMMA'
- [ ] Moving Average Convergence Divergence 'MACD'
- [ ] Percentage Price Oscillator 'PPO'
- [ ] Volume-Weighted MACD 'VW_MACD'
- [ ] Elastic-Volume weighted MACD 'EV_MACD'
- [ ] Market Momentum 'MOM'
- [ ] Rate-of-Change 'ROC'
- [x] Relative Strenght Index 'RSI'
- [ ] Inverse Fisher Transform RSI 'IFT_RSI'
- [ ] True Range 'TR'
- [x] Average True Range 'ATR'
- [ ] Stop-and-Reverse 'SAR'
- [x] Bollinger Bands 'BBANDS'
- [ ] Bollinger Bands Width 'BBWIDTH'
- [ ] Percent B 'PERCENT_B'
- [x] Keltner Channels 'KC'
- [ ] Donchian Channel 'DO'
- [ ] Directional Movement Indicator 'DMI'
- [x] Average Directional Index 'ADX'
- [ ] Pivot Points 'PIVOT'
- [ ] Fibonacci Pivot Points 'PIVOT_FIB'
- [ ] Stochastic Oscillator %K 'STOCH'
- [ ] Stochastic oscillator %D 'STOCHD'
- [ ] Stochastic RSI 'STOCHRSI'
- [ ] Williams %R 'WILLIAMS'
- [x] Ultimate Oscillator 'UO'
- [x] Awesome Oscillator 'AO'
- [ ] Mass Index 'MI'
- [ ] Vortex Indicator 'VORTEX'
- [ ] Know Sure Thing 'KST'
- [ ] True Strength Index 'TSI'
- [ ] Typical Price 'TP'
- [ ] Accumulation-Distribution Line 'ADL'
- [ ] Chaikin Oscillator 'CHAIKIN'
- [ ] Money Flow Index 'MFI'
- [ ] On Balance Volume 'OBV'
- [ ] Weighter OBV 'WOBV'
- [ ] Volume Zone Oscillator 'VZO'
- [ ] Price Zone Oscillator 'PZO'
- [ ] Elder's Force Index 'EFI'
- [ ] Cummulative Force Index 'CFI'
- [ ] Bull power and Bear Power 'EBBP'
- [ ] Ease of Movement 'EMV'
- [ ] Commodity Channel Index 'CCI'
- [ ] Coppock Curve 'COPP'
- [ ] Buy and Sell Pressure 'BASP'
- [ ] Normalized BASP 'BASPN'
- [ ] Chande Momentum Oscillator 'CMO'
- [ ] Chandelier Exit 'CHANDELIER'
- [ ] Qstick 'QSTICK'
- [ ] Twiggs Money Index 'TMF'
- [ ] Wave Trend Oscillator 'WTO'
- [ ] Fisher Transform 'FISH'
- [ ] Ichimoku Cloud 'ICHIMOKU'
- [ ] Adaptive Price Zone 'APZ'
- [ ] Vector Size Indicator 'VR'
- [ ] Squeeze Momentum Indicator 'SQZMI'
- [ ] Volume Price Trend 'VPT'
- [ ] Finite Volume Element 'FVE'
- [ ] Volume Flow Indicator 'VFI'
- [ ] Moving Standard deviation 'MSD'

## 組み合わせ
|No.|Title|1.GAP|2.INTRO SERIAL|3.ADX|4.NewValue|5.Big Bar|6.Flow|
|---|---|---|---|---|---|---|---|
|1|Breakout Sigma1| | | | | | |
|2|Breakout KC| | | | | | |
|3|ATR Based Breakout| | | | | | |
|4|Asymmetric Again| | |x| | | |
|5|Asymmetric Triple| | | | | | |
|6|RSI Trigger| | | | | | |
|7|The Ultimate| | | | | | |
|8|Breakout Sigma1 Twice| | | | | | |
 
## Entry判定
 - ATR
   - [x] ATRブレイク ATR Based Breakout
 - Keltner Channels
   - [x] KCブレイク後の新値更新 Breakout KC
   - [x] KCブレイク2回 Breakout KC Twice
 - 新値
 - BollingerBand
   - [x] Sigma1ブレイク後の新値更新 Breakout Sigma1
   - [x] Sigma1ブレイク2回 Breakout Sigma1 Twice
 - Flow
 - Big Bar
 - RSI
 - ADX
 - 日時
 
## Entry注文
 - 逆指値
 - 指値
 - OCO逆指値,逆指値
 - 寄成
 
## Exit判定
 - 新値
 - ATR
 - TR
 - BollingerBand
 - パーセンタイル
 - 期間指定高値/安値
 - フィボナッチ
 - 利益率指定
 - OCO利益率指定,逆指値ロスカット
 - 利益率指定
 - 逆指値ロスカット
 - OCO指値固定利益,逆指値固定損失
 - 固定利益額
 - 固定損失額
 - End of Bar
 - 期間

## Exit注文
 - 逆指値指値
 - 逆指値成行
 - 指値
 - 寄成
 - 引成
 - OCO指値,逆指値

