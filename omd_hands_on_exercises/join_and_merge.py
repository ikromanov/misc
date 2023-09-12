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

    # 1. Get trades along with prevailing quotes
    # # QTE branch: ticks are filtered; GO_BACK_TO_FIRST_TICK is enabled
    # trd_pass = q.passthrough('TRD', fields='PRICE')
    # where_clause = q.where_clause(where='ASK_PRICE>0 AND BID_PRICE>0 AND COND="R"')
    # add_field = q.add_field(field='TIMESTAMP_ORIG msectime', value='TIMESTAMP')
    # qte_pass = q.passthrough('QTE', fields='ASK_PRICE,BID_PRICE,TIMESTAMP_ORIG', go_back_to_first_tick='expr(3*86400)')
    # num_ticks = q.num_ticks(is_running_aggr=True, output_field_name='TICK_ID')
    #
    # # Construct left/right hand side nodes
    # lhs_epd = [trd_pass, num_ticks]
    # rhs_epd = [where_clause, add_field, qte_pass, num_ticks.copy()]
    # graph = q.Graph.join_chainlets(lhs_epd, rhs_epd, LEADING_SOURCES='L')

    # 2. Compute effective spread average and generate above/below mid flag for each trade
    # #Round - robin - start from leftmost node and construct each node left-to-right.
    # avg_interval_sec = 60
    #
    # trd_pass = q.passthrough(ticktype='TRD', fields='PRICE')
    # trd_where_clause = q.where_clause(where='PRICE>0')
    # jbt = q.join_by_time(join_type='INNER', leading_sources='t')
    # qte_pass = q.passthrough(ticktype='QTE', fields='ASK_PRICE, BID_PRICE', go_back_to_first_tick='expr(3*86400)')
    # qte_where_clause = q.where_clause(where='ASK_PRICE>0 AND BID_PRICE>0 AND COND="R"')
    # add_field = q.add_field(field='MID double', value='(q.ASK_PRICE+q.BID_PRICE)/2')
    # add_fields = q.add_fields(fields='SPREAD double = t.PRICE - MID, '
    #                                  'ABOVE_BELOW_MID_FLAG int = SIGN(t.PRICE - MID)')
    # average = q.average(bucket_interval=avg_interval_sec,
    #                     is_running_aggr=True,
    #                     all_fields_for_sliding=True,
    #                     output_field_name='AVERAGE_SPREAD',
    #                     input_field_name='SPREAD')
    #
    # # Create a graph object
    # graph = q.Graph(trd_pass)
    # graph.sink(trd_where_clause)
    # #graph = q.Graph.chainlet([trd_pass, trd_where_clause])
    #
    # # Attach 'join' node. Tag previous node as 'trd' and use it as the leading source
    # graph.sink(jbt, source_tag='t')
    #
    # # Now remember JBT node as head (will be used later) and add the COMPUTE branch
    # jbt_node = graph.head
    # graph.source(qte_pass, source_tag='q')
    # graph.source(qte_where_clause)
    #
    # # Move the graph head back to JBT node and append Event Processors
    # graph.head = jbt_node
    # graph >> add_field >> add_fields >> average

    # 3. Compute symbol RETURN correlation
    # sym1 = 'FULL_DEMO_L1::MSFT'
    # sym2 = 'FULL_DEMO_L1::CSCO'
    # interval = 60
    # compute_string='FIRST(TIME_SERIES_TYPE=STATE_TS) OPEN, LAST(TIME_SERIES_TYPE=STATE_TS) CLOSE'
    #
    # # create EPs
    # trd_pass = q.passthrough('TRD', fields='PRICE',go_back_to_first_tick=86400)
    # compute = q.compute(compute=compute_string, bucket_interval=0, output_interval=interval, \
    #                     is_running_aggr=False, append_output_field_name=False)
    # add_field = q.add_field(field='RETURN double', value='(CLOSE-CLOSE[-1])/CLOSE[-1]')
    # symbol_pair = q.add_field(field='SYMBOL_PAIR',value='"{}-{}"'.format(sym1,sym2))
    #
    # # Create two lists of the above EPs
    # lhs=[trd_pass, compute, add_field]
    # rhs=[ep.copy() for ep in lhs]
    # graph = q.Graph.join_chainlets(lhs, rhs, lhs_bind_symbol=sym1, rhs_bind_symbol=sym2, \
    #                                source_order='L,R', match_if_identical_times=True)
    #
    # # Can now just add some extra EPs via sinks to the head node,
    # # which is the join (JOIN_BY_TIME) node
    # graph >> q.correlation(is_running_aggr=True, input_field1_name='L.RETURN', \
    #                        input_field2_name='R.RETURN', output_field_name='RETURN_CORRELATION') >> symbol_pair
    #
    # data = q.run_query(graph, symbol=None, s=start_time, e=end_time)
    # display_results(data)

    # 4. Join prices for a list of symbol pairs and compute pairwise correlations
    # db = 'FULL_DEMO_L1'
    # symbols = ['GOOG-MSFT',
    #            'AAPL-ORCL',
    #            'MSFT-ORCL']
    # interval = 60
    #
    # # create EPs
    # # Two branches will use different symbol names, formed from
    # msn_trd = q.modify_symbol_name(symbol_name='TOKEN(_SYMBOL_NAME,0,"-")'.format(db))
    # trd_pass = q.passthrough(ticktype=db + '::TRD', fields='PRICE')
    # last = q.last(bucket_interval=interval, output_field_name='PRICE',
    #               input_field_name='PRICE', time_series_type='STATE')
    #
    # # Create graph
    # lhs = [msn_trd, trd_pass, last]
    # rhs = [ep.copy() for ep in lhs]
    # graph = q.Graph.join_chainlets(lhs, rhs, source_order='L,R', match_if_identical_times=True)
    # graph >> q.correlation(is_running_aggr=True, input_field1_name='L.PRICE',
    #                        input_field2_name='R.PRICE', output_field_name='CORRELATION')
    # data = q.run_query(graph, symbols, s=start_time, e=end_time)
    # display_results(data, symbols)

    # 5. Get top N players, or MERGE times series to compute total across all symbols
    symbols = ['FULL_DEMO_L1::A',
               'FULL_DEMO_L1::AA',
               'FULL_DEMO_L1::AAA',
               'FULL_DEMO_L1::C',
               'FULL_DEMO_L1::CSCO']
    num_of_top_ticks = 10

    # create EPs
    graph = q.Graph(q.passthrough(ticktype='TRD',fields='SIZE'))    \
        >> q.sum(output_field_name='VOLUME',input_field_name='SIZE')    \
        >> q.presort().symbol(symbols)   \
        >> q.merge().label('merge')    \
        >> q.high_tick(num_ticks=num_of_top_ticks,input_field_name='VOLUME').label('H')  \
        >> q.join_by_time(leading_sources='H',match_if_identical_times=True,same_timestamp_join_policy='EACH_FOR_LEADER_WITH_LATEST').label('join') \
        << q.sum(output_field_name='VOLUME',input_field_name='VOLUME').label('T')
    jbt = graph['join']
    graph << graph['merge']
    jbt >> q.add_field(field='PERC_OF_TOTAL',value='H.VOLUME/T.VOLUME')
    result = q.run_query(graph,symbol=None,s=start_time,e=end_time)
    #print(pd.DataFrame(result['FULL_DEMO_L1::GS']).head())

    # Process results
    # Save graph
    graph.save(symbols, start_time, end_time, otq_file='C:/temp/join_and_merge.otq', query_name='main')

    # Print results
    # data = q.run_query(graph, symbols, start_time, end_time)
    # display_results(data, symbols)


if __name__ == '__main__': main()
