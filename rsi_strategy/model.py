import pickle
from sklearn.ensemble import RandomForestClassifier

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*InconsistentVersionWarning.*")

# The current model is already imported, but might need to update
class RSIDynamicModel:
    def __init__(self, model_path="/Users/sophiochikhladze/Desktop/Dynamic_RSI/rsi_strategy/model.pkl"):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict_proba(self, X_scaled):
        return self.model.predict_proba(X_scaled)[:, 1]