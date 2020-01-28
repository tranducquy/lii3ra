# -*- coding: utf-8 -*-

backtest_profit_query = """
select
 b08.symbol
,b08.entry_strategy
,b08.exit_strategy
,round(b01.profit::numeric, 2) as "{}"
,round(b02.profit::numeric, 2) as "{}"
,round(b03.profit::numeric, 2) as "{}"
,round(b04.profit::numeric, 2) as "{}"
,round(b05.profit::numeric, 2) as "{}"
,round(b06.profit::numeric, 2) as "{}"
,round(b07.profit::numeric, 2) as "{}"
,round(b08.profit::numeric, 2) as "{}"
,round(b09.profit::numeric, 2) as "{}"
,round((
coalesce(b01.profit, 0)
+ coalesce(b02.profit, 0)
+ coalesce(b03.profit, 0)
+ coalesce(b04.profit, 0)
+ coalesce(b05.profit, 0)
+ coalesce(b06.profit, 0)
+ coalesce(b07.profit, 0)
+ coalesce(b08.profit, 0)
+ coalesce(b09.profit, 0)
)::numeric, 2) as sum
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
) as b08

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
on b08.symbol = b01.symbol
and b08.entry_strategy = b01.entry_strategy
and b08.exit_strategy = b01.exit_strategy

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
on b08.symbol = b02.symbol
and b08.entry_strategy = b02.entry_strategy
and b08.exit_strategy = b02.exit_strategy

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
on b08.symbol = b03.symbol
and b08.entry_strategy = b03.entry_strategy
and b08.exit_strategy = b03.exit_strategy

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
) as b04
on b08.symbol = b04.symbol
and b08.entry_strategy = b04.entry_strategy
and b08.exit_strategy = b04.exit_strategy

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
on b08.symbol = b05.symbol
and b08.entry_strategy = b05.entry_strategy
and b08.exit_strategy = b05.exit_strategy

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
on b08.symbol = b06.symbol
and b08.entry_strategy = b06.entry_strategy
and b08.exit_strategy = b06.exit_strategy

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
) as b07
on b08.symbol = b07.symbol
and b08.entry_strategy = b07.entry_strategy
and b08.exit_strategy = b07.exit_strategy

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
) as b09
on b08.symbol = b09.symbol
and b08.entry_strategy = b09.entry_strategy
and b08.exit_strategy = b09.exit_strategy

where b08.symbol in ({})

{}

order by sum desc, 8 desc, 7 desc
"""

backtest_profit_monthry_query = """
select
 b11.symbol
,b11.entry_strategy
,b11.exit_strategy
,round(b01.profit::numeric, 2) as "{}"
,round(b02.profit::numeric, 2) as "{}"
,round(b03.profit::numeric, 2) as "{}"
,round(b04.profit::numeric, 2) as "{}"
,round(b05.profit::numeric, 2) as "{}"
,round(b06.profit::numeric, 2) as "{}"
,round(b07.profit::numeric, 2) as "{}"
,round(b08.profit::numeric, 2) as "{}"
,round(b09.profit::numeric, 2) as "{}"
,round(b10.profit::numeric, 2) as "{}"
,round(b11.profit::numeric, 2) as "{}"
,round(b12.profit::numeric, 2) as "{}"
,round((
coalesce(b01.profit, 0)
+ coalesce(b02.profit, 0)
+ coalesce(b03.profit, 0)
+ coalesce(b04.profit, 0)
+ coalesce(b05.profit, 0)
+ coalesce(b06.profit, 0)
+ coalesce(b07.profit, 0)
+ coalesce(b08.profit, 0)
+ coalesce(b09.profit, 0)
+ coalesce(b10.profit, 0)
+ coalesce(b11.profit, 0)
+ coalesce(b12.profit, 0)
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
) as b11

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
on b11.symbol = b01.symbol
and b11.entry_strategy = b01.entry_strategy
and b11.exit_strategy = b01.exit_strategy

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
on b11.symbol = b02.symbol
and b11.entry_strategy = b02.entry_strategy
and b11.exit_strategy = b02.exit_strategy

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
on b11.symbol = b03.symbol
and b11.entry_strategy = b03.entry_strategy
and b11.exit_strategy = b03.exit_strategy

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
on b11.symbol = b04.symbol
and b11.entry_strategy = b04.entry_strategy
and b11.exit_strategy = b04.exit_strategy

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
on b11.symbol = b05.symbol
and b11.entry_strategy = b05.entry_strategy
and b11.exit_strategy = b05.exit_strategy

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
on b11.symbol = b06.symbol
and b11.entry_strategy = b06.entry_strategy
and b11.exit_strategy = b06.exit_strategy

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
) as b07
on b11.symbol = b07.symbol
and b11.entry_strategy = b07.entry_strategy
and b11.exit_strategy = b07.exit_strategy

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
) as b08
on b11.symbol = b08.symbol
and b11.entry_strategy = b08.entry_strategy
and b11.exit_strategy = b08.exit_strategy

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
) as b09
on b11.symbol = b09.symbol
and b11.entry_strategy = b09.entry_strategy
and b11.exit_strategy = b09.exit_strategy

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
) as b10
on b11.symbol = b10.symbol
and b11.entry_strategy = b10.entry_strategy
and b11.exit_strategy = b10.exit_strategy

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
) as b12
on b11.symbol = b12.symbol
and b11.entry_strategy = b12.entry_strategy
and b11.exit_strategy = b12.exit_strategy

where b11.symbol  in ({})

{}

order by sum desc
"""



