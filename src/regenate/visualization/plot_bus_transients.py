import matplotlib.pyplot as plt
from .common import save

def f07(df,out):
    fig,ax=plt.subplots(); ax.plot(df['t_s'],df['v_bus']); ax.axhline(df['v_min'].iloc[0],ls='--',color='red'); ax.axhline(df['v_max'].iloc[0],ls='--',color='red'); ax.set(xlabel='Time (s)',ylabel='Bus voltage (V)'); save(fig,df,out)
