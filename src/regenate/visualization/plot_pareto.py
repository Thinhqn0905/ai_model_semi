import matplotlib.pyplot as plt
from .common import save

def f15(df,out):
    fig,ax=plt.subplots(); ax.scatter(df['latency_ms'],df['mae']);
    for _,r in df.iterrows(): ax.annotate(str(r['model']),(r['latency_ms'],r['mae']))
    ax.set(xlabel='Latency (ms)',ylabel='MAE'); save(fig,df,out)
