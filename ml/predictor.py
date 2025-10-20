import pickle
import os
import numpy as np

class ReusePredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "eviction_model.pkl")
        self.load_model()
    
    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.model = None
    
    def predict_reuse_probability(self, time_since_last_access, access_count):
        if self.model is None:
            return 0.5
        
        features = np.array([[time_since_last_access, access_count]])
        probability = self.model.predict_proba(features)[0][1]
        return probability
    
    def should_evict(self, time_since_last_access, access_count, threshold=0.5):
        prob = self.predict_reuse_probability(time_since_last_access, access_count)
        return prob < threshold

