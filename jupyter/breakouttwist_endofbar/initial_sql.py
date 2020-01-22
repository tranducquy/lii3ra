# -*- coding: utf-8 -*-


backtest_result_query = """
select 
 *
from backtest_result
where symbol in ('{}')
and rate_of_return > 100
order by rate_of_return desc
"""

b01 = "2014"
b02 = "2015"
b03 = "2016"
b04 = "2017"
b05 = "2018"
b06 = "2019"
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
,round((b01.profit
+ b02.profit
+ b03.profit
+ b04.profit
+ b05.profit
+ b06.profit)::numeric, 2) as sum
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

where b04.symbol = '{}'
and b04.entry_strategy like 'BreakoutTwist%'
and b04.exit_strategy like 'EndOfBar'

order by sum desc, 8 desc, 7 desc
"""

b01m = '2019-08'
b02m = '2019-09'
b03m = '2019-10'
b04m = '2019-11'
b05m = '2019-12'
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
,round((
b01.profit
+ b02.profit
+ b03.profit
+ b04.profit
+ b05.profit
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

where b01.symbol = '{}'
and b01.entry_strategy like 'BreakoutTwist%'
and b01.exit_strategy like 'EndOfBar'

order by sum desc
"""

