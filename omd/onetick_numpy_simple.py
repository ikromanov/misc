import NumPy_OneTickQuery as otq
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline

# Call the query
result = otq.run_query(["-otq_file C:/OMD/client_data/otqs/vwap.otq -otq_params BucketIntSec=600"])

# Extract values from numpy array
vwap = result[0][1][1][1]
volume = result[0][1][2][1]
ts = result[0][1][0][1]

# Plot line on one graph
plt.plot(ts,vwap)

# Use pandas Series
ser1 = pd.Series(result[0][1][1][1], index=result[0][1][0][1])
ser1.plot()

# Put output of the query into the pandas Data Frame
df = pd.DataFrame({'vwap':result[0][1][1][1], 'avg_price':result[0][1][3][1], 
				'ann_vol':result[0][1][4][1], 'volume':result[0][1][2][1]}, 
                	index=result[0][1][0][1])

# Simple plots
df.plot(subplots=True, figsize=(12,10))
df.vwap.plot()