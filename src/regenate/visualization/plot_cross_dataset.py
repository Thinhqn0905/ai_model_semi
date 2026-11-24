import matplotlib.pyplot as plt
from .common import save

def f04(df,out):
    metric = df['metric'].unique()
    if len(metric)!=1 or metric[0] not in ('nmae','skill'): raise ValueError('one NMAE or skill metric required')
    table=df.pivot(index='train_dataset',columns='test_dataset',values='value'); fig,ax=plt.subplots(); im=ax.imshow(table,aspect='auto'); ax.set_xticks(range(len(table.columns)),table.columns); ax.set_yticks(range(len(table.index)),table.index); fig.colorbar(im,ax=ax,label=metric[0]); save(fig,df,out)
