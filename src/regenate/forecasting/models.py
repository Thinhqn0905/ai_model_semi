"""Shared forecasting models; one fixed configuration per model (equal budget)."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

class Model:
    def __init__(self, name): self.name = name
    def fit(self, X, y, X_val=None, y_val=None):
        from lightgbm import LGBMRegressor
        from xgboost import XGBRegressor
        self.est = None
        if self.name == 'M6':
            from .tcn import TCN
            self.est = TCN().fit(X,y,X_val,y_val)
            return self
        if self.name == 'M5':
            self.est = [LGBMRegressor(objective='quantile', alpha=q, n_estimators=40, n_jobs=2, random_state=0, verbosity=-1) for q in (.1,.5,.9)]
            for m in self.est: m.fit(X,y)
            return self
        factories = {'M1': lambda: LinearRegression(), 'M2': lambda: RandomForestRegressor(n_estimators=20,max_depth=12,n_jobs=2,random_state=0), 'M3': lambda: XGBRegressor(n_estimators=40,max_depth=4,n_jobs=2,random_state=0), 'M4': lambda: LGBMRegressor(n_estimators=40,n_jobs=2,random_state=0,verbosity=-1)}
        if self.name != 'M0':
            self.est = factories[self.name]()
            self.est.fit(X,y)
        point = np.asarray(X)[:,-1] if self.est is None else self.est.predict(X)
        self.residual = np.quantile(np.asarray(y)-point,[.1,.5,.9])
        return self
    def predict(self,X):
        if self.name == 'M6': return self.est.predict(X)
        if self.name == 'M5': a=np.column_stack([m.predict(X) for m in self.est])
        else:
            point=np.asarray(X)[:,-1] if self.est is None else self.est.predict(X)
            a=point[:,None]+self.residual
        a.sort(axis=1)
        return dict(zip(('p10','p50','p90'),a.T))

REGISTRY = {f'M{i}': (lambda i=i: Model(f'M{i}')) for i in range(7)}
