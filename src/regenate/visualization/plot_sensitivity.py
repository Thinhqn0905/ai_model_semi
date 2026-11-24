import matplotlib.pyplot as plt
from .common import save

def f10(df,out):
    table=df.pivot(index='flexibility',columns='efficiency',values='value'); fig,ax=plt.subplots(); im=ax.imshow(table,aspect='auto',origin='lower'); ax.set_xticks(range(len(table.columns)),table.columns); ax.set_yticks(range(len(table.index)),table.index); ax.set(xlabel='Efficiency',ylabel='Flexibility'); fig.colorbar(im,ax=ax); save(fig,df,out)
