'''
Created on Aug 15, 2017

@author: daniel
'''
import quersive as q
from datetime import datetime
import pandas as pd

symbol = 'FULL_DEMO_L1::GS'
start = datetime(2005,1,3,9,30)
end = datetime(2005,1,3,16)

def main():
    g = q.Graph(q.passthrough(ticktype='TRD',fields='SIZE'))    \
        >> q.sum(output_field_name='VOLUME',input_field_name='SIZE')    \
        >> q.presort().symbol(symbol)   \
        >> q.merge().label('merge')    \
        >> q.high_tick(num_ticks=10,input_field_name='VOLUME').label('H')  \
        >> q.join_by_time(leading_sources='H',match_if_identical_times=True,same_timestamp_join_policy='EACH_FOR_LEADER_WITH_LATEST').label('join') \
        << q.sum(output_field_name='VOLUME',input_field_name='VOLUME').label('T')
    jbt = g['join']
    g << g['merge']
    jbt >> q.add_field(field='PERC_OF_TOTAL',value='H.VOLUME/T.VOLUME')
    print(g.head.name)
    result = q.run_query(g,symbol=None,s=start,e=end)
    print(pd.DataFrame(result['FULL_DEMO_L1::GS']).head())
    #print(result)
        
        
    
    
    
if __name__ == "__main__": main()