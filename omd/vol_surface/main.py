import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import os
import numpy as np

os.environ['OMD_ROOT'] = 'C:/CloudMail/Projects/vol_surface'
os.environ['OMD_BASE'] = 'C:/OMD'
os.environ['ONE_TICK_CONFIG'] = 'C:/CloudMail/Projects/vol_surface/client_data/config/one_tick_config.txt'

import quersive as q

def display_results(data, symbols=None, n=5):
    pd.set_option('display.width',250)

    if symbols is not None and symbols != 'all':
        for sym in symbols:
            df = pd.DataFrame(data[sym])
            if len(df) != 0:
                print(sym)
                print(df.head(n),'\n')
    elif symbols == 'all':
        symbols = list(data.keys())
        for sym in symbols[:10]:
            df = pd.DataFrame(data[sym])
            if len(df) != 0:
                print(sym)
                print(df.head(n),'\n')
    else:
        df = pd.DataFrame(data[''])
        if len(df) != 0:
            print(df.head(n),'\n')

def main():
    #symbols = ['P_CBOE::AMZN']
    get_symbols = '{}/client_data/otqs/EquityOptions_v3.otq::getContracts'.format('C:/CloudMail/Projects/vol_surface')
    start_time, end_time = datetime(2017, 10, 2, 9, 30), datetime(2017, 10, 2, 11, 30)
    vol_surface_query = '{}/client_data/otqs/EquityOptions_v3.otq::OptionQuotes'.format('C:/CloudMail/Projects/vol_surface')

    # get last before certain time
    #data = q.run_query(vol_surface_query, symbol='eval({})'.format(get_symbols), s=start_time, e=end_time)
    data = q.run_query(vol_surface_query, symbol=None, s=start_time, e=end_time)

    #display_results(data)

    #plot data
    df = pd.DataFrame(data[''])
    df = df.loc[df['OPTION_TYPE'] == 'CALL']
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y, Z = df['STRIKE'], df['DTE'], df['IMPLIED_VOL']

    #X, Y = np.meshgrid(X, Y)
    #surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    surf = ax.scatter(X,Y,Z)
    ax.set_xlabel('STRIKE')
    ax.set_ylabel('DTE')
    ax.set_zlabel('IMPLIED_VOL')

    ax.set_ylim(0,500)
    #ax.set_zlim(0,2.0)

    plt.show()

if __name__ == '__main__':
    main()