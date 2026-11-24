import matplotlib.pyplot as plt
from .common import save

def f13(df,out):
    methods=list(df['method'].unique()); fig,axes=plt.subplots(len(methods),1,squeeze=False,figsize=(8,2.5*len(methods)))
    for ax,method in zip(axes[:,0],methods):
        for _,r in df[df['method']==method].iterrows(): ax.broken_barh([(r.start_h,r.end_h-r.start_h)],(r.station-.4,.8))
        ax.set(title=str(method),ylabel='Station',xlabel='Time (h)')
    save(fig,df,out)
