import matplotlib.pyplot as plt
from .common import save

def f04(df,out):
    metric = df['metric'].unique()
    if len(metric)!=1 or metric[0] not in ('nmae','skill'): raise ValueError('one NMAE or skill metric required')
    table=df.pivot(index='train_dataset',columns='test_dataset',values='value'); fig,ax=plt.subplots(); im=ax.imshow(table,aspect='auto'); ax.set_xticks(range(len(table.columns)),table.columns); ax.set_yticks(range(len(table.index)),table.index); fig.colorbar(im,ax=ax,label=metric[0]); save(fig,df,out)

def f04_v3(df, out):
    """Plot matched-split skills; missing combinations are hatched."""
    import numpy as np
    from matplotlib.patches import Rectangle
    from regenate.forecasting.xbench import IDS
    data=df.copy()
    data['row']=data.apply(lambda r: f"{r['dataset']} / {r['target']} / " + ('duration' if np.isnan(r['horizon_min']) else f"{r['horizon_min']:g} min"),axis=1)
    fig, axes=plt.subplots(1,2,figsize=(16,max(8,len(data['row'].unique())*.34)),layout='constrained')
    for ax,metric,title in zip(axes,['skill_vs_persistence','skill_vs_domain_baseline'],['vs persistence','vs domain baseline']):
        table=data.pivot(index='row',columns='model_id',values=metric).reindex(columns=IDS)
        values=table.to_numpy(dtype=float); im=ax.imshow(np.ma.masked_invalid(values),aspect='auto',cmap='RdBu',vmin=-1,vmax=1)
        for (i,j),v in np.ndenumerate(values):
            if np.isnan(v): ax.add_patch(Rectangle((j-.5,i-.5),1,1,facecolor='white',edgecolor='gray',hatch='///',linewidth=.2))
            else: ax.text(j,i,f'{v:.2f}',ha='center',va='center',fontsize=6)
        ax.set_xticks(range(len(IDS)),IDS,rotation=45,ha='right'); ax.set_yticks(range(len(table)),table.index,fontsize=6); ax.set_title(title)
    fig.colorbar(im,ax=axes,label='1 − MAE / baseline MAE',shrink=.6,extend='both')
    for ext in ('png','pdf','svg'): fig.savefig(str(out)+'.'+ext,dpi=300)
    plt.close(fig)
