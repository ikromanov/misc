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
    db = ['DEMO_L1::']
    start_time, end_time = datetime(2003, 12, 1, 9, 30), datetime(2003, 12, 1, 16)

    # first stage: get symbols
    get_symbols = q.Graph(q.find_db_symbols(pattern='%', ticktype='NA'))
    get_symbols >> q.add_field(field='WEIGHT', value='100')
    get_symbols = get_symbols.save(db, start_time, end_time)

    # main query
    graph = q.Graph(q.passthrough(ticktype='TRD', fields='PRICE', go_back_to_first_tick='86400'))
    graph >> q.last(bucket_interval=1800, output_field_name='PRICE') >> q.add_field(field='WEIGHT_IN_PORTFOLIO int', value='ATOF(_SYMBOL_PARAM.WEIGHT)')

    # Process results
    # Save graph
    graph.save(q.staged_query(get_symbols), start_time, end_time, otq_file='C:/temp/multi_stage.otq', query_name='main')
    graph.save('eval("{}")'.format(get_symbols), start_time, end_time, otq_file='C:/temp/multi_stage.otq', query_name='main')

    # Print results
    #data = q.run_query(graph, symbol=q.staged_query('C:/temp/temp.otq::find_db_symbols'), s=start_time, e=end_time)
    data = q.run_query(graph, symbol=q.staged_query(get_symbols), s=start_time, e=end_time)
    print(data)
    #display_results(data)


if __name__ == '__main__': main()
