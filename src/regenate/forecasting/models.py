"""Shared forecasting models; one fixed configuration per model (equal budget)."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

class Model:
    def __init__(self, name, variant=0): self.name, self.variant = name, variant
    def fit(self, X, y, X_val=None, y_val=None):
        from lightgbm import LGBMRegressor
        from xgboost import XGBRegressor
        self.est = None
        if self.name == 'M6':
            from .tcn import TCN
            self.est = TCN(epochs=20 + 10*self.variant).fit(X,y,X_val,y_val)
            return self
        if self.name == 'M5':
            self.est = [LGBMRegressor(objective='quantile', alpha=q, n_estimators=30 + 20*self.variant, n_jobs=2, random_state=0, verbosity=-1) for q in np.arange(1,10)/10]
            for m in self.est: m.fit(X,y)
            return self
        factories = {'M1': lambda: LinearRegression(), 'M2': lambda: RandomForestRegressor(n_estimators=20,max_depth=8 + 4*self.variant,n_jobs=2,random_state=0), 'M3': lambda: XGBRegressor(n_estimators=30 + 20*self.variant,max_depth=4,n_jobs=2,random_state=0), 'M4': lambda: LGBMRegressor(n_estimators=30 + 20*self.variant,n_jobs=2,random_state=0,verbosity=-1)}
        if self.name != 'M0':
            self.est = factories[self.name]()
            self.est.fit(X,y)
        point = np.asarray(X)[:,-1] if self.est is None else self.est.predict(X)
        self.residual = np.quantile(np.asarray(y)-point,np.arange(1,10)/10)
        return self
    def predict(self,X):
        if self.name == 'M6':
            p=self.est.predict(X); a=np.column_stack([np.interp(q,[.1,.5,.9],[p['p10'][i],p['p50'][i],p['p90'][i]]) for i in range(len(X)) for q in []]) if False else np.column_stack([p['p10']+(p['p50']-p['p10'])*((q-.1)/.4) if q<=.5 else p['p50']+(p['p90']-p['p50'])*((q-.5)/.4) for q in np.arange(1,10)/10]); return {f'p{i*10}':a[:,i-1] for i in range(1,10)}
        if self.name == 'M5': a=np.column_stack([m.predict(X) for m in self.est])
        else:
            point=np.asarray(X)[:,-1] if self.est is None else self.est.predict(X)
            a=point[:,None]+self.residual
        a.sort(axis=1)
        return {f'p{i*10}':a[:,i-1] for i in range(1,10)}

REGISTRY = {f'M{i}': (lambda variant=0, i=i: Model(f'M{i}', variant)) for i in range(7)}
