# packages
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

# set seed
seed = 314

def train_model(X, y, seed=seed):
    """
    Build a GBM on given data
    """
    model = GradientBoostingClassifier(
        learning_rate=0.03,
        n_estimators=120,
        max_depth=2,
        subsample=0.7,
        min_samples_leaf=15,
        random_state=seed
    )
    model.fit(X, y)
    return model