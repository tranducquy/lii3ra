# -*- coding: utf-8 -*-


backtest_result_query = """
select 
 *
from backtest_result
where symbol in ({})
and rate_of_return > {}
order by rate_of_return desc
"""


backtest_profit_monthry_query = """
select
 b01.symbol
,b01.entry_strategy
,b01.exit_strategy
,round(b01.profit::numeric, 2) as "{}"
,round(b02.profit::numeric, 2) as "{}"
,round(b03.profit::numeric, 2) as "{}"
,round((
coalesce(b01.profit, 0)
+ coalesce(b02.profit, 0)
+ coalesce(b03.profit, 0)
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
) as b02

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
) as b01
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
on b02.symbol = b03.symbol
and b02.entry_strategy = b03.entry_strategy
and b02.exit_strategy = b03.exit_strategy

where b02.symbol in ({})
and b02.entry_strategy like 'BreakoutKC%'
and b02.exit_strategy like 'EndOfBar'

and round((
coalesce(b01.profit, 0)
+ coalesce(b02.profit, 0)
+ coalesce(b03.profit, 0)
)::numeric, 2) > 0.0

order by sum desc
"""

