import numpy as np
import matplotlib.pyplot as plt
from .common import save

def f06(df,out):
    matched=np.minimum(np.minimum(df['source_kw'],df['sink_kw']),df['link_cap_kw']); fig,ax=plt.subplots(); ax.plot(df['t_h'],df['source_kw'],label='Source'); ax.plot(df['t_h'],df['sink_kw'],label='Sink'); ax.plot(df['t_h'],matched,label='Matched'); ax.set(xlabel='Time (h)',ylabel='Power (kW)'); ax.legend(); save(fig,df,out)
