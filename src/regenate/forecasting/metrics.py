"""Forecast error and probabilistic calibration metrics."""
import numpy as np


def mae(y, pred):
    return float(np.mean(np.abs(np.asarray(y) - np.asarray(pred))))


def rmse(y, pred):
    return float(np.sqrt(np.mean((np.asarray(y) - np.asarray(pred)) ** 2)))


def nmae(y, pred):
    scale = np.mean(np.abs(y))
    return mae(y, pred) / scale if scale else float('nan')


def pinball(y, pred, q):
    if not 0 < q < 1:
        raise ValueError('q must be between 0 and 1')
    error = np.asarray(y) - np.asarray(pred)
    return float(np.mean(np.maximum(q * error, (q - 1) * error)))


def interval_coverage(y, lo, hi):
    y = np.asarray(y)
    return float(np.mean((np.asarray(lo) <= y) & (y <= np.asarray(hi))))
