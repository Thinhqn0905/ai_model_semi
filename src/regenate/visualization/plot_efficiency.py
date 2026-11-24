import matplotlib.pyplot as plt
from .common import save

def f05(df,out):
    fig,ax=plt.subplots()
    for name,g in df.groupby('device'):
        g=g.sort_values('load_frac'); ax.plot(g['load_frac'],g['eta'],marker='.',label=name)
    ax.set(xlabel='Load fraction',ylabel='Efficiency'); ax.legend(fontsize=6); save(fig,df,out)
