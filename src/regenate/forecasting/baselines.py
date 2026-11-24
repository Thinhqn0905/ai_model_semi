"""Small, reproducible probabilistic forecasting baselines."""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor


class Baseline:
    def __init__(self, model):
        self.model = model

    def fit(self, X, y):
        if self.model == 'F01':
            point = X['rolling_mean'].to_numpy()
        elif self.model == 'F05':
            self.models = [LGBMRegressor(objective='quantile', alpha=q, n_estimators=40,
                                        n_jobs=2, random_state=0, verbosity=-1)
                           for q in (0.1, 0.5, 0.9)]
            for estimator in self.models:
                estimator.fit(X, y)
            return self
        else:
            self.estimator = {
                'F02': lambda: LinearRegression(),
                'F03': lambda: RandomForestRegressor(n_estimators=20, max_depth=12, n_jobs=2, random_state=0),
                'F04': lambda: LGBMRegressor(n_estimators=40, n_jobs=2, random_state=0, verbosity=-1),
            }[self.model]()
            self.estimator.fit(X, y)
            point = self.estimator.predict(X)
        self.residuals = np.quantile(np.asarray(y) - point, [0.1, 0.5, 0.9])
        return self

    def predict(self, X):
        if self.model == 'F05':
            values = np.column_stack([m.predict(X) for m in self.models])
            values.sort(axis=1)
        else:
            point = X['rolling_mean'].to_numpy() if self.model == 'F01' else self.estimator.predict(X)
            values = point[:, None] + self.residuals
        return dict(zip(('p10', 'p50', 'p90'), values.T))
