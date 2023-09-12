# Implementation of examples from OneTickQueryTrainingHandsOnExercices.pdf
# with 'quersive' package
import os
#os.environ['ONE_TICK_CONFIG'] = 'C:/OMD/client_data/config/one_tick_config.txt'

import quersive as q
import pandas as pd
from datetime import datetime
#import os


#os.environ['ONE_TICK_CONFIG'] = 'C:/CloudMail/Projects/Vanguard/TCA/client_data/config/one_tick_config.txt'
#os.environ['OMD_BASE'] = 'C:/CloudMail/Projects/Vanguard/TCA'
#os.environ['OMD_ROOT'] = 'C:/OMD'

context = 'DEFAULT'

def main():

    # 1. Get trade ticks for symbols IBM and CSCO
    # symbols = ['FULL_DEMO_L1::IBM', 'FULL_DEMO_L1::CSCO']
    # start_time, end_time = datetime(2003, 12, 1, 9, 30), datetime(2003, 12, 1, 16)
    # trd_pass = q.passthrough(ticktype='TRD', fields='PRICE,SIZE,EXCHANGE')
    #
    # graph = q.Graph.chainlet([trd_pass])
    # data = q.run_query(graph, symbols, start_time, end_time)
    # for sym in symbols:
    #     print(sym)
    #     df = pd.DataFrame(data[sym])
    #     pd.set_option('display.width', 100)
    #     print(df.head())

    # 2. Retrieve a database snapshot as of given time (i.e. what were the prices as of 9:30 AM)
    # symbols = ['FULL_DEMO_L1::IBM']
    # start_time, end_time = datetime(2006, 6, 1, 9, 30), datetime(2006, 6, 1, 9, 30)
    #
    # where_clause = q.where_clause(where='ASK_PRICE>0 AND BID_PRICE>0 AND COND="R"')
    # qte_pass = q.passthrough(ticktype='QTE', go_back_to_first_tick='86400', max_back_ticks_to_prepend=10)
    # add_field = q.add_field(field='ORIG_TS msectime', value='TIMESTAMP')
    # graph = q.Graph.chainlet([where_clause, add_field, qte_pass])
    #
    # data = q.run_query(graph, symbols, start_time, end_time)
    # df = pd.DataFrame(data[symbols[0]])
    # print(df.head())

    # 3. Filtering ticks (WHERE_CLAUSE and more)
    # symbols = ['IBM']
    # start_time, end_time = datetime(2006, 6, 1, 9, 30), datetime(2006, 6, 1, 16)
    # db = 'FULL_DEMO_L1'
    # conditions_to_exclude = 'N4Q'
    # tz = 'EST5EDT'
    #
    # trd_pass = q.passthrough(ticktype=db+'::TRD')
    # char_present = q.character_present(discard_on_match=True, field='COND', characters=conditions_to_exclude)
    # where_clause = q.where_clause(where='PRICE>0 AND SIZE>0 AND MOD(DAY_OF_WEEK(TIMESTAMP,"{}"),6)!=0'.format(tz))
    # time_filter = q.time_filter(start_time='93000000', end_time='1600000', timezone='EST5EDT')
    #
    # # create a nested query and save it to a file
    # nested_query = q.Graph.chainlet([trd_pass, char_present, where_clause])
    # nested_query.sink(event_processor=time_filter, pin='OUT')
    # otq_file = nested_query.save(symbols, start_time, end_time, otq_file='C:/temp/my_sample_filter.otq', query_name='_FilterTrades')
    #
    # # create the main query
    # trd_pass_main = q.passthrough(db+'::TRD')
    # main_graph = q.Graph.chainlet([trd_pass_main, q.nested_otq(otq_name=otq_file), q.vwap(output_field_name='VWAP')])
    # # Add another output leg with a filter
    # main_graph.head = trd_pass_main
    # main_graph >> q.vwap(output_field_name='VWAP')
    # #main_graph >> q.where_clause(where='PRICE>80') >> q.vwap(output_field_name='VWAP_80')
    # main_graph.save(symbols, start_time, end_time, otq_file='C:/temp/main_filtering.otq', query_name='main')
    #
    # data = q.run_query(main_graph, symbols, start_time, end_time)
    # df_1, df_2 = pd.DataFrame(data(symbols[0])[0]), pd.DataFrame(data(symbols[0])[1])
    # print(df_1.head())
    # print(df_2.head())

    # 4. Tick Aggregation
    symbols = ['FULL_DEMO_L1::A',
               'FULL_DEMO_L1::AA',
               'FULL_DEMO_L1::AAA',
               'FULL_DEMO_L1::C',
               'FULL_DEMO_L1::CSCO']
    start_time, end_time = datetime(2006, 6, 1, 9, 30), datetime(2006, 6, 1, 16)

    trd_pass = q.passthrough('TRD')
    # 4.1. VWAP over all trades from query start to end
    # vwap = q.vwap(output_field_name='VWAP')
    # graph = q.Graph.chainlet([trd_pass, vwap])

    # 4.2. Bucketed volume for N second buckets or N tick buckets
    # bucket_interval_units = 'TICKS' #SECONDS, DAYS, etc.
    # bucket_interval = 600
    # trd_volume = q.sum(bucket_interval=bucket_interval,
    #                    bucket_interval_units=bucket_interval_units,
    #                    is_running_aggr=True,
    #                    output_field_name='VOLUME',
    #                    input_field_name='SIZE')
    # graph = q.Graph.chainlet([trd_pass, trd_volume])

    # 4.3. Append running total and sliding bucketed volumes to each trade tick
    # and calculate a ratio between the two
    # bucket_interval_units = 'TICKS' #SECONDS, DAYS, etc.
    # bucket_interval = 600
    # trd_pass_ltd = q.passthrough(ticktype='TRD', fields='PRICE, SIZE, EXCHANGE')
    # volume = q.sum(bucket_interval=bucket_interval,
    #                    bucket_interval_units=bucket_interval_units,
    #                    is_running_aggr=True,
    #                    all_fields_for_sliding=True,
    #                    output_field_name='VOLUME',
    #                    input_field_name='SIZE')
    # total_running_volume = q.sum(is_running_aggr=True,
    #                               all_fields_for_sliding=True,
    #                               output_field_name='TOTAL_RUNNING_VOLUME',
    #                               input_field_name='SIZE')
    # add_fields = q.add_fields(fields='BUCKET_VOLUME_CHANGE double = VOLUME/VOLUME[-1], '
    #                                  'BUCKET_VS_RUNNING_TOTAL double = VOLUME/TOTAL_RUNNING_VOLUME')
    # graph = q.Graph.chainlet([trd_pass_ltd, volume, total_running_volume, add_fields])

    # 4.4. Sliding aggregation per group
    # trd_pass_ltd = q.passthrough(ticktype='TRD', fields='PRICE, SIZE, EXCHANGE')
    # running_volume_per_exch = q.sum(is_running_aggr=True,
    #                                 all_fields_for_sliding=True,
    #                                 output_field_name='RUNNING_VOLUME_PER_EXCHANGE',
    #                                 group_by='EXCHANGE',
    #                                 input_field_name='SIZE')
    # total_running_volume = q.sum(is_running_aggr=True,
    #                              all_fields_for_sliding=True,
    #                              output_field_name='TOTAL_RUNNING_VOLUME',
    #                              input_field_name='SIZE')
    # add_fields = q.add_fields(fields='EXCHANGE_VOLUME_VS_TOTAL double = RUNNING_VOLUME_PER_EXCHANGE/TOTAL_RUNNING_VOLUME')
    # last_tick = q.last_tick(group_by='EXCHANGE')
    # graph = q.Graph.chainlet([trd_pass_ltd, running_volume_per_exch, total_running_volume, add_fields, last_tick])

    # 4.5. Combine multiple aggregation functions
    # Bucketed OHLC/VWAP/volume bars using COMPUTE
    # bucket_interval = 300
    # bucket_interval_units = 'SECONDS'
    # is_running_aggr = True
    # compute = q.compute(ticktype='TRD',compute='FIRST OPEN, HIGH, LOW, LAST CLOSE, VWAP, AVERAGE, STDDEV, SUM VOLUME, NUM_TICKS',
    #                     bucket_interval=bucket_interval,
    #                     bucket_interval_units=bucket_interval_units,
    #                     is_running_aggr=is_running_aggr,
    #                     append_output_field_name=False)
    # # PASSTHROUGH EP is unnecessary
    # graph = q.Graph.chainlet([compute])

    # 4.6. Aggregate into flexible volume-based buckets
    # volume_bucket_size = 1000
    # trd_pass = q.passthrough(ticktype='TRD', fields='PRICE,SIZE')
    # volume = q.sum(is_running_aggr=True, output_field_name='VOLUME')
    # compute = q.compute(compute='FIRST OPEN,HIGH,LOW,LAST CLOSE,VWAP,HIGH(INPUT_FIELD_NAME=SIZE) HIGH_SIZE, SUM VOLUME, NUM_TICKS',
    #                     bucket_interval_units='FLEXIBLE',
    #                     bucket_end_criteria='DIV(VOLUME,{})>DIV(VOLUME[-1],{}) AND VOLUME[-1]>0'.format(volume_bucket_size, volume_bucket_size),
    #                     append_output_field_name=False)
    # graph = q.Graph.chainlet([trd_pass, volume, compute])

    # 4.7. Append total daily volume to each detail tick to compute % of total
    # #Round - robin - start from leftmost node and construct each node left-to-right.
    # trd_pass = q.passthrough(ticktype='TRD', fields='PRICE,SIZE')
    # compute = q.compute(ticktype='TRD', compute='SUM VOLUME, NUM_TICKS', bucket_time='BUCKET_START', append_output_field_name=False)
    # jbt = q.join_by_time(join_type='INNER', leading_sources='trd')
    #
    # # Create a graph object using TRD PASSTHROUGH
    # graph = q.Graph(trd_pass)
    #
    # # Attach 'join' node. Tag previous node as 'trd' and use it as the leading source
    # graph.sink(jbt, source_tag='trd')
    #
    # # Now remember JBT node as head (will be used later) and add the COMPUTE branch
    # jbt_node = graph.head
    # graph.source(compute, source_tag='day')
    #
    # # Change head back to jbt_node and continue constructing the query
    # rolling_bucket_sec = 60
    # graph.head = jbt_node
    # rename_fields = q.rename_fields(rename_fields='trd.PRICE=PRICE, trd.SIZE=SIZE')
    # compute_2 = q.compute(compute='SUM VOLUME, NUM_TICKS', show_all_fields=True, is_running_aggr=True,append_output_field_name=False)
    # add_fields = q.add_fields(fields='PERCENT_VOLUME double=VOLUME/day.VOLUME,PERCENT_COUNT double = NUM_TICKS/day.NUM_TICKS')
    # compute_3 = q.compute(compute='SUM VOLUME_{}, NUM_TICKS NUM_TICKS_{}'.format(rolling_bucket_sec, rolling_bucket_sec),
    #                       show_all_fields=True,
    #                       bucket_interval=rolling_bucket_sec,
    #                       is_running_aggr=True,
    #                       append_output_field_name=False)
    # add_fields_2 = q.add_fields(fields='PERCENT_VOLUME_{} double=VOLUME_{}/day.VOLUME,'
    #                                    'PERCENT_COUNT_{} double=NUM_TICKS_{}/day.NUM_TICKS'
    #                             .format(rolling_bucket_sec, rolling_bucket_sec, rolling_bucket_sec, rolling_bucket_sec))
    # filter_pt = q.passthrough(fields='PERCENT_VOLUME, PERCENT_COUNT, PERCENT_VOLUME_{}, PERCENT_COUNT_{}'.
    #                           format(rolling_bucket_sec,rolling_bucket_sec))
    # # Add all EPs to the Graph
    # graph >> rename_fields >> compute_2 >> add_fields >> compute_3 >> add_fields_2 >> filter_pt

    # 4.7. Calculate Relative Strength Index (RSI) over past X days for a range of days
    interval = 60
    rsi_ticks = 14
    compute = q.compute(ticktype='TRD', compute='FIRST,HIGH,LAST (TIME_SERIES_TYPE=STATE_TS),SUM',
                        bucket_interval=interval,
                        append_output_field_name=False)
    add_fields = q.add_fields(fields='GAIN double=(LAST-LAST[-1]),LOSS double=(LAST-LAST[-1])')
    update_fields = q.update_fields(set='GAIN=0,LOSS=ABS(LOSS)', else_set='LOSS=0', where='LOSS<0')
    compute_2 = q.compute(compute='SUM (INPUT_FIELD_NAME=GAIN) TOTAL_GAIN,SUM (INPUT_FIELD_NAME=LOSS) TOTAL_LOSS',
                          show_all_fields=True,
                          bucket_interval=rsi_ticks,
                          bucket_interval_units='TICKS',
                          is_running_aggr=True,
                          append_output_field_name=False)
    add_fields_2 = q.add_fields(fields='AVG_GAIN double=TOTAL_GAIN/{}, AVG_LOSS double=TOTAL_LOSS/{}'.format(rsi_ticks, rsi_ticks))
    add_field = q.add_field(field='RSI', value='100 - ( 100/( 1 + AVG_GAIN/AVG_LOSS ) )')
    num_ticks = q.num_ticks(is_running_aggr=True, output_field_name='ROWNUM', bucket_end_per_group=True)
    update_field = q.update_field(field='RSI', value='NAN()', where='ROWNUM<={}'.format(rsi_ticks))
    #drop_fields = q.passthrough(fields='GAIN,LOSS,ROWNUM,AVG_GAIN,AVG_LOSS,TOTAL_GAIN,TOTAL_LOSS', drop_fields=True)
    drop_fields = q.passthrough(fields='\.*GAIN,\.*LOSS, ROWNUM', drop_fields=True, use_regex=True)

    graph = q.Graph(compute)
    graph >> add_fields >> update_fields >> compute_2 >> add_fields_2 >> add_field >> num_ticks >> update_field >> drop_fields

    ################ Process results #################################
    # Save graph
    graph.save(symbols, start_time, end_time, otq_file='C:/temp/all.otq', query_name='main')

    # Print results
    data = q.run_query(graph, symbols, start_time, end_time)
    for sym in symbols:
        print(sym)
        df = pd.DataFrame(data[sym])
        print(df.head())

if __name__ == '__main__': main()