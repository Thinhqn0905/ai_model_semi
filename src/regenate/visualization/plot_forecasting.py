import numpy as np
import matplotlib.pyplot as plt
from .common import save

def f01(df, out):
    fig, ax = plt.subplots(); ax.plot(df['t'], df['actual'], label='Actual'); ax.plot(df['t'], df['pred'], label='Prediction'); ax.fill_between(df['t'].to_numpy(), df['lower'].to_numpy(), df['upper'].to_numpy(), step='mid', alpha=.25, label='Interval'); ax.legend(); save(fig, df, out)

def f02(df, out):
    a, p = df['actual'].to_numpy(), df['pred'].to_numpy(); err = p-a; denom = ((a-a.mean())**2).sum(); r2 = 1-(err**2).sum()/denom if denom else float('nan'); fig, ax = plt.subplots(); ax.scatter(a,p,s=10); lo=min(a.min(),p.min()); hi=max(a.max(),p.max()); ax.plot([lo,hi],[lo,hi], '--'); ax.set(xlabel='Actual', ylabel='Predicted', title=f'MAE {np.mean(abs(err)):.3g} | RMSE {np.sqrt(np.mean(err**2)):.3g} | R2 {r2:.3g}'); save(fig,df,out)

def f03(df,out):
    fig,ax=plt.subplots(); ax.plot(df['horizon'],df['mae'], marker='o'); ax.set(xlabel='Horizon',ylabel='MAE'); save(fig,df,out)

def f11(df,out):
    fig,ax=plt.subplots(); groups=list(df.groupby('model')); ax.boxplot([g['error'].dropna() for _,g in groups], labels=[str(n) for n,_ in groups]); ax.set_ylabel('Forecast error'); save(fig,df,out)

def f12(df,out):
    fig,ax=plt.subplots(); ax.plot(df['nominal'],df['empirical'],marker='o'); ax.plot([0,1],[0,1],'--'); ax.set(xlabel='Nominal coverage',ylabel='Empirical coverage',xlim=(0,1),ylim=(0,1)); save(fig,df,out)

