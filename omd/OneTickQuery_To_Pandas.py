import NumPy_OneTickQuery
import pandas as pd

argument_string = ""
argument_string += " -context 'DEFAULT'"
argument_string += " -otq_file 'C:/OMD/client_data/otqs/vwap.otq'"
argument_string += " -s '20050103093000'"
argument_string += " -e '20050103160000'"
argument_string += " -otq_params  BucketIntSec=600"

symbol_specs = []
symbol_specs.append( ("FULL_DEMO_L1::IBM", []) )


# Load the result of vwap.otq execution into NumPy array
X = NumPy_OneTickQuery.run_query([argument_string , symbol_specs ])

# Load the X array into pandas df with timestamp as an index
df_CSCO = pd.DataFrame({'vwap':X[0][1][1][1], 'avg_price':X[0][1][3][1], 
				'ann_vol':X[0][1][4][1], 'volume':X[0][1][2][1]}, 
                	index=X[0][1][0][1])