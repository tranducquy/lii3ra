
-- drop table ohlcv;
create table ohlcv
(
    symbol text,
    leg text,
    time timestamp,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    primary key(symbol, leg, time)
)
;

drop table backtest_result;
create table backtest_result 
(
    symbol text,
    leg text,
    entry_strategy text,
    exit_strategy text,
    start_time timestamp,
    end_time timestamp,
    market_start_time timestamp,
    market_end_time timestamp,
    initial_assets double precision,
    last_assets double precision,
    rate_of_return double precision,
    win_count integer,
    loss_count integer,
    win_value double precision,
    loss_value double precision,
    win_rate double precision,
    payoffratio double precision,
    profit_rate_per_trade double precision,
    long_win_count integer,
    long_loss_count integer,
    long_win_value double precision,
    long_loss_value double precision,
    long_win_rate double precision,
    long_payoffratio double precision,
    long_profit_rate_per_trade double precision,
    short_win_count integer,
    short_loss_count integer,
    short_win_value double precision,
    short_loss_value double precision,
    short_win_rate double precision,
    short_payoffratio double precision,
    short_profit_rate_per_trade double precision,
    max_drawdown double precision,
    fee double precision,
    spread_fee double precision,
    regist_time timestamp,
    primary key(symbol, leg, entry_strategy, exit_strategy)
)
;

drop table backtest_history;
create table backtest_history
(
    symbol text,
    leg text,
    entry_strategy text,
    exit_strategy text,
    time timestamp,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    entry_indicator1 double precision,
    entry_indicator2 double precision,
    entry_indicator3 double precision,
    entry_indicator4 double precision,
    entry_indicator5 double precision,
    entry_indicator6 double precision,
    entry_indicator7 double precision,
    exit_indicator1 double precision,
    exit_indicator2 double precision,
    exit_indicator3 double precision,
    exit_indicator4 double precision,
    exit_indicator5 double precision,
    exit_indicator6 double precision,
    exit_indicator7 double precision,
    vol_indicator1 double precision,
    vol_indicator2 double precision,
    vol_indicator3 double precision,
    vol_indicator4 double precision,
    vol_indicator5 double precision,
    order_create_time timestamp,
    order_type integer,
    order_vol double precision,
    order_price double precision,
    call_order_time timestamp,
    call_order_type integer,
    call_order_vol double precision,
    call_order_price double precision,
    execution_order_time timestamp,
    execution_order_type integer,
    execution_order_status integer,
    execution_order_vol double precision,
    execution_order_price double precision,
    execution_order_time2 timestamp,
    execution_order_type2 integer,
    execution_order_status2 integer,
    execution_order_vol2 double precision,
    execution_order_price2 double precision,
    position integer,
    cash double precision,
    pos_vol double precision,
    pos_price double precision,
    total_value double precision,
    profit_value double precision,
    profit_rate double precision,
    max_drawdown double precision,
    leverage double precision,
    fee double precision,
    spread_fee double precision,
    regist_time timestamp,
    primary key(symbol, leg, entry_strategy, exit_strategy, time)
);

drop table m_positiontype;
create table m_positiontype
(
    positiontype_id integer,
    positiontype_name text,
    primary key(positiontype_id)
)
;
insert into m_positiontype (positiontype_id, positiontype_name) values (0, 'NOTHING');
insert into m_positiontype (positiontype_id, positiontype_name) values (1, 'LONG');
insert into m_positiontype (positiontype_id, positiontype_name) values (2, 'SHORT');

drop table m_orderstatus;
create table m_orderstatus
(
    orderstatus_id integer,
    orderstatus_name text,
    primary key(orderstatus_id)
)
;
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (0, '注文なし');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (1, '注文中');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (2, '失効');
insert into m_orderstatus (orderstatus_id, orderstatus_name) values (3, '約定');

drop table m_ordertype;
create table m_ordertype
(
    ordertype_id integer,
    ordertype_name text,
    primary key(ordertype_id)
)
;
insert into m_ordertype (ordertype_id, ordertype_name) values (0, '注文なし');
insert into m_ordertype (ordertype_id, ordertype_name) values (1, '逆指値成行新規買');
insert into m_ordertype (ordertype_id, ordertype_name) values (2, '逆指値成行新規売');
insert into m_ordertype (ordertype_id, ordertype_name) values (3, '逆指値指値新規買');
insert into m_ordertype (ordertype_id, ordertype_name) values (4, '逆指値指値新規売');
insert into m_ordertype (ordertype_id, ordertype_name) values (5, '指値新規買');
insert into m_ordertype (ordertype_id, ordertype_name) values (6, '指値新規売');
insert into m_ordertype (ordertype_id, ordertype_name) values (7, '成行新規買');
insert into m_ordertype (ordertype_id, ordertype_name) values (8, '成行新規売');
insert into m_ordertype (ordertype_id, ordertype_name) values (9, '逆指値成行返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (10, '逆指値成行返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (11, '成行返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (12, '成行返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (13, '指値返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (14, '指値返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (15, '逆指値指値返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (16, '逆指値指値返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (17, 'OCO返売');
insert into m_ordertype (ordertype_id, ordertype_name) values (18, 'OCO返買');
insert into m_ordertype (ordertype_id, ordertype_name) values (19, 'OCO新規');
