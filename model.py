from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

class MRF_model:
    def __init__(self):
        self.model = MultiOutputRegressor(RandomForestRegressor())

    def fit(self, X, y):
        self.model.fit(X, y)
        return X, y

    def predict(self, X):
        return self.model.predict(X)
