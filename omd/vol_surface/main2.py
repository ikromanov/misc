import NumPy_OneTickQuery
import datetime
import matplotlib.pyplot as plt
import pandas as pd

argument_string = ""
#argument_string += " -context 'DEFAULT'"
argument_string += " -otq_file 'C:/CloudMail/Projects/vol_surface/vol_surface.otq::main'"
#argument_string += " -s '20050103093000'"
#argument_string += " -e '20050103160000'"
#argument_string += " -otq_params  BucketIntSec=600"

symbol_specs = []
symbol_specs.append(("FULL_DEMO_L1::IBM", []))
#symbol_specs.append(("FULL_DEMO_L1::MSFT", []))
#symbol_specs.append(("FULL_DEMO_L1::CSCO", []))

#print(datetime.datetime.now())
X = NumPy_OneTickQuery.run_query([argument_string, symbol_specs])
#print(datetime.datetime.now())

data = {}

n_symbols = len(X)
for s in range(n_symbols):
    symbol = X[s][0]
    symbol_data = X[s][1]
    symbol_error_warning = X[s][2]
    symbol_query_label_name = X[s][3]

    if len(symbol_error_warning) > 0:
        print('Skipping bad symbol ' + symbol)
        print(symbol_error_warning)
    else:
        if len(symbol_data) == 0:
            print('Skipping no-data symbol ' + symbol)
            continue
        data[symbol] = {}
        n_fields = len(symbol_data)
        for k in range(n_fields):
            field_name = X[s][1][k][0]
            data[symbol][field_name] = X[s][1][k][1]
        print('N ticks for ', symbol, ': ', len(data[symbol][field_name]))

vol_surf = data['FULL_DEMO_L1::IBM']['VOL_SURF']
print(vol_surf[0])
print(type(vol_surf[0]))

# Use numpy + matplotlib
# vwap_CSCO = X[0][1][1][1]
# ts = X[0][1][0][1]
# plt.plot(ts, vwap_CSCO)
# plt.title('NumPy + Matplotlib')

# Put data in pandas DataFrame and make simple plots
# df_CSCO = pd.DataFrame({'vwap': X[0][1][1][1], 'avg_price': X[0][1][3][1],
#                         'ann_vol': X[0][1][4][1], 'volume': X[0][1][2][1]},
#                        index=X[0][1][0][1])
#
# print(df_CSCO.index)
# df_CSCO.plot(subplots=True, figsize=(12, 10), title='Pandas plot')