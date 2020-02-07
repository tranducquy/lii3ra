# -*- coding: utf-8 -*-


ohlcv_query = """
select 
 symbol
,min(time)
,max(time)
,count(*)
from ohlcv
where symbol in ({})
and leg = '1d'
group by symbol
order by 1
"""

backtest_result_query = """
select 
 *
from backtest_result
where symbol in ({})
order by symbol
"""

b01 = "2015"
b02 = "2016"
b03 = "2017"
b04 = "2018"
b05 = "2019"
b06 = "2020"
backtest_profit_query = """
select
b04.symbol
,b04.entry_strategy
,b04.exit_strategy
,round(b01.profit::numeric, 2) as "{}"
,round(b02.profit::numeric, 2) as "{}"
,round(b03.profit::numeric, 2) as "{}"
,round(b04.profit::numeric, 2) as "{}"
,round(b05.profit::numeric, 2) as "{}"
,round(b06.profit::numeric, 2) as "{}"
,round((coalesce(b01.profit, 0)
+ coalesce(b02.profit, 0)
+ coalesce(b03.profit, 0)
+ coalesce(b04.profit, 0)
+ coalesce(b05.profit, 0)
+ coalesce(b06.profit, 0))::numeric, 2) as sum
from 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history 
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b04

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b01
on b04.symbol = b01.symbol
and b04.entry_strategy = b01.entry_strategy
and b04.exit_strategy = b01.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b02
on b04.symbol = b02.symbol
and b04.entry_strategy = b02.entry_strategy
and b04.exit_strategy = b02.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b03
on b04.symbol = b03.symbol
and b04.entry_strategy = b03.entry_strategy
and b04.exit_strategy = b03.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b05
on b04.symbol = b05.symbol
and b04.entry_strategy = b05.entry_strategy
and b04.exit_strategy = b05.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 5) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b06
on b04.symbol = b06.symbol
and b04.entry_strategy = b06.entry_strategy
and b04.exit_strategy = b06.exit_strategy

where b04.symbol in ({})

order by sum desc, 8 desc, 7 desc
"""

b01m = '2019-09'
b02m = '2019-10'
b03m = '2019-11'
b04m = '2019-12'
b05m = '2020-01'
b06m = '2020-02'
backtest_profit_monthry_query = """
select
 b01.symbol
,b01.entry_strategy
,b01.exit_strategy
,round(b01.profit::numeric, 2) as "{}"
,round(b02.profit::numeric, 2) as "{}"
,round(b03.profit::numeric, 2) as "{}"
,round(b04.profit::numeric, 2) as "{}"
,round(b05.profit::numeric, 2) as "{}"
,round(b06.profit::numeric, 2) as "{}"
,round((
b01.profit
+ b02.profit
+ b03.profit
+ b04.profit
+ b05.profit
+ b06.profit
)::numeric, 2) as sum
from 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history 
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b01

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b02
on b01.symbol = b02.symbol
and b01.entry_strategy = b02.entry_strategy
and b01.exit_strategy = b02.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b03
on b01.symbol = b03.symbol
and b01.entry_strategy = b03.entry_strategy
and b01.exit_strategy = b03.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b04
on b01.symbol = b04.symbol
and b01.entry_strategy = b04.entry_strategy
and b01.exit_strategy = b04.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b05
on b01.symbol = b05.symbol
and b01.entry_strategy = b05.entry_strategy
and b01.exit_strategy = b05.exit_strategy

left outer join 
(
select
 symbol
,entry_strategy
,exit_strategy
,sum(profit_rate) as profit
from backtest_history
where substr(text(time), 0, 8) = '{}'
group by symbol, entry_strategy, exit_strategy
) as b06
on b01.symbol = b06.symbol
and b01.entry_strategy = b06.entry_strategy
and b01.exit_strategy = b06.exit_strategy

where b05.symbol  in ({})

order by sum desc
"""

position_query = """
select
 symbol
,substr(text(time), 1, 10)
,leg
,entry_strategy
,exit_strategy
,mp.positiontype_name
,pos_price
,open
,high
,low
,close
,volume
from backtest_history as bh
inner join m_ordertype as mo
    on bh.order_type = mo.ordertype_id
inner join m_positiontype as mp
    on bh.position = mp.positiontype_id
where symbol in ({})
and date(time) = '{}'
order by symbol
"""

entrysignal_query = """
select
 symbol
,substr(text(time), 1, 10)
,leg
,mp.positiontype_name as ポジション
,substr(text(order_create_time), 1, 10) as 注文作成日時
,mo.ordertype_name as 注文方法
,order_vol as 注文数量
,order_price as 注文価格
,case 
    when order_type in (1,3,5,7) then order_price + (order_price * {})
    when order_type in (2,4,6,8) then order_price - (order_price * {})
end as 逆指値指値

,mo_oco1.ordertype_name as 注文方法oco1
,order_vol_oco1 as 注文数量oco1
,order_price_oco1 as 注文価格oco1
,case 
    when order_type_oco1 in (1,3,5,7) then order_price_oco1 + (order_price_oco1 * {})
    when order_type_oco1 in (2,4,6,8) then order_price_oco1 - (order_price_oco1 * {})
end as 逆指値指値oco1
,mo_oco2.ordertype_name as 注文方法oco2
,order_vol_oco2 as 注文数量oco2
,order_price_oco2 as 注文価格oco2
,case 
    when order_type_oco2 in (1,3,5,7) then order_price_oco2 + (order_price_oco2 * {})
    when order_type_oco2 in (2,4,6,8) then order_price_oco2 - (order_price_oco2 * {})
end as 逆指値指値oco2

,open
,high
,low
,close
,entry_strategy
,exit_strategy
from backtest_history as bh
inner join m_ordertype as mo
    on bh.order_type = mo.ordertype_id
inner join m_positiontype as mp
    on bh.position = mp.positiontype_id
inner join m_ordertype as mo_oco1
    on bh.order_type_oco1 = mo_oco1.ordertype_id
inner join m_ordertype as mo_oco2
    on bh.order_type_oco2 = mo_oco2.ordertype_id
where symbol in ({})
and position = 0
and date(time) = '{}'
order by symbol
"""

exitsignal_query = """
select
symbol
,substr(text(time), 1, 10)
,leg
,mp.positiontype_name
,mo.ordertype_name as 注文方法
,bh.order_price as 注文価格
,case 
    when position = 1 and bh.order_type = 9 then (low-1) - ((low-1)*{})
    when position = 2 and bh.order_type = 10 then (high+1) + ((high+1)*{})
end as 逆指値指値
,pos_price as ポジション価格
,case 
    when position = 1 then pos_price - (pos_price*{})
    when position = 2 then pos_price + (pos_price*{})
end as ロスカット1
,case 
    when position = 1 then pos_price - (pos_price*{})
    when position = 2 then pos_price + (pos_price*{})
end as ロスカット2
,open
,high
,low
,close
,entry_strategy
,exit_strategy
from backtest_history as bh
inner join m_ordertype as mo
    on bh.order_type = mo.ordertype_id
inner join m_positiontype as mp
    on bh.position = mp.positiontype_id
where symbol in ({})
and position <> 0
and date(time) = '{}'
order by symbol
"""

backtest_history_detail_query = """
select
 symbol
,leg
,time
,open
,high
,low
,close
,volume
,entry_indicator1
,entry_indicator2
,entry_indicator3
,entry_indicator4
,entry_indicator5
,entry_indicator6
,entry_indicator7
,exit_indicator1
,exit_indicator2
,exit_indicator3
,exit_indicator4
,exit_indicator5
,exit_indicator6
,exit_indicator7
,order_create_time
,mot1.ordertype_name as create_ordertype
,order_vol
,order_price

,mot1_oco1.ordertype_name as ordertype_oco1
,order_vol_oco1
,order_price_oco1
,mot1_oco2.ordertype_name as ordertype_oco2
,order_vol_oco2
,order_price_oco2

,call_order_time
,mot2.ordertype_name as call_ordertype
,call_order_vol
,call_order_price
,execution_order_time
,mot3.ordertype_name as execution_ordertype
,execution_order_type as e_ordertype
,mos.orderstatus_name as execution_order_status
,execution_order_vol
,execution_order_price
,mpt.positiontype_name
,cash
,pos_vol
,pos_price
,total_value
,profit_value
,profit_rate
,leverage
,max_drawdown
,fee
,spread_fee
,regist_time
,entry_strategy
,exit_strategy
from backtest_history as bh
inner join m_ordertype as mot1
    on bh.order_type = mot1.ordertype_id
inner join m_ordertype as mot2
    on bh.call_order_type = mot2.ordertype_id
inner join m_ordertype as mot3
    on bh.execution_order_type = mot3.ordertype_id
inner join m_positiontype as mpt
    on bh.position = mpt.positiontype_id
inner join m_orderstatus as mos
    on bh.execution_order_status = mos.orderstatus_id
inner join m_ordertype as mot1_oco1
    on bh.order_type_oco1 = mot1_oco1.ordertype_id
inner join m_ordertype as mot1_oco2
    on bh.order_type_oco2 = mot1_oco2.ordertype_id
where symbol = '{}'
and leg = '1d'
and date(time) between '{}' and '{}'
order by time
"""

