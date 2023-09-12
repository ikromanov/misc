# Implementation of examples from OneTickQueryTrainingHandsOnExercices.pdf
# with 'quersive' package

import quersive as q
import pandas as pd
from datetime import datetime
import os

os.environ['ONE_TICK_CONFIG'] = 'C:/OMD/client_data/config/one_tick_config.txt'
# os.environ['ONE_TICK_CONFIG'] = 'C:/CloudMail/Projects/Vanguard/TCA/client_data/config/one_tick_config.txt'
# os.environ['OMD_BASE'] = 'C:/CloudMail/Projects/Vanguard/TCA'
# os.environ['OMD_ROOT'] = 'C:/OMD'

context = 'DEFAULT'


def display_results(data, symbols=None, n=5):
    if symbols is not None:
        for sym in symbols:
            print(sym)
            df = pd.DataFrame(data[sym])
            print(df.head(n))
    else:
        df = pd.DataFrame(data[''])
        print(df.head(n))


def main():
    symbols = ['FULL_DEMO_L1::IBM']
    start_time, end_time = datetime(2006, 6, 1, 9, 30), datetime(2006, 6, 1, 16)

    # 1. Check prices points N ticks before and after and event (with FIELD_NAME[+/-N] and TIME_SHIFT built-in function)
    # n = 10
    # time_shift_msec = 120000
    # add_fields = q.add_fields(fields='PRICE_BEFORE_TICK_1 double=PRICE[-1],'
    #                                  'PRICE_AFTER_TICK_1 double=PRICE[1],'
    #                                  'PRICE_BEFORE_TICK_{0} double=PRICE[{0}],'
    #                                  'PRICE_AFTER_TICK_{0} double=PRICE[-{0}],'
    #                                  'PRICE_BEFORE_SEC_30 double=TIME_SHIFT("PRICE",-30000,"LAST_AT_OR_BEFORE"),'
    #                                  'PRICE_AFTER_SEC_30 double=TIME_SHIFT("PRICE",30000,"FIRST_AT_OR_AFTER"),'
    #                                  'PRICE_BEFORE_SEC_{1} double=TIME_SHIFT("PRICE",-{1},"LAST_AT_OR_BEFORE"),'
    #                                  'PRICE_AFTER_SEC_{1} double=TIME_SHIFT("PRICE",{1},"FIRST_AT_OR_AFTER")'.format(n, time_shift_msec))
    # graph = q.Graph(q.passthrough(ticktype='TRD', fields='PRICE'))
    # graph >> add_fields

    # 2. Compute aggregated values over a period of exactly N seconds before and after an event
    # interval1 = 60
    # interval2 = 300
    # graph = q.Graph(q.passthrough(ticktype='TRD', fields='PRICE,SIZE'))
    # graph >> q.vwap(bucket_interval=interval1, is_running_aggr=True, all_fields_for_sliding=True,
    #                 output_field_name='VWAP_{}'.format(interval1)) >> \
    #          q.vwap(bucket_interval=interval2, is_running_aggr=True, all_fields_for_sliding=True,
    #                 output_field_name='VWAP_{}'.format(interval2))

    # 3. Compute ASK and BID VWAP & Volume over N seconds before and after each trade
    # calculate QTE stats and save query to a file
    get_qte_stats = q.Graph(q.passthrough(ticktype='QTE'))
    get_qte_stats >> q.compute(compute='VWAP(PRICE_FIELD_NAME=ASK_PRICE,SIZE_FIELD_NAME=ASK_SIZE) ASK_VWAP,'
                                       'VWAP(PRICE_FIELD_NAME=BID_PRICE,SIZE_FIELD_NAME=BID_SIZE) BID_VWAP,'
                                       'SUM(INPUT_FIELD_NAME=ASK_SIZE) ASK_VOLUME,'
                                       'SUM(INPUT_FIELD_NAME=ASK_SIZE) BID_VOLUME',
                               append_output_field_name=False)
    get_qte_stats = get_qte_stats.save(symbols, start_time, end_time, otq_file='C:/temp/temp.otq', query_name='get_qte_stats')

    # main query
    time_window_sec = 300
    graph = q.Graph(q.passthrough(ticktype='TRD', fields='PRICE,SIZE,EXCHANGE'))
    graph >> q.join_with_query(otq_query='"{}"'.format(get_qte_stats), symbol_name='_SYMBOL_NAME',
                               start_timestamp='TIMESTAMP-{}*1000'.format(time_window_sec),
                               end_timestamp='TIMESTAMP',
                               prefix_for_output_ticks='BEFORE_')\
          >> q.join_with_query(otq_query='"{}"'.format(get_qte_stats), symbol_name='_SYMBOL_NAME',
                               start_timestamp='TIMESTAMP',
                               end_timestamp='TIMESTAMP+{}*1000'.format(time_window_sec),
                               prefix_for_output_ticks='AFTER_')

    # Process results
    # Save graph
    graph.save(symbols, start_time, end_time, otq_file='C:/temp/market_cond.otq', query_name='main')

    # Print results
    data = q.run_query(graph, symbols, start_time, end_time)
    display_results(data, symbols)


if __name__ == '__main__': main()
