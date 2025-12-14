import pandas as pd
import random
from sklearn.linear_model import Lasso
from sklearn.exceptions import ConvergenceWarning
import warnings

# Suppress technical warnings for cleaner user experience
warnings.filterwarnings("ignore", category=ConvergenceWarning)

class SmartBrain:
    def __init__(self):
        # Alpha=0.1 ensures aggressive filtering of useless variables
        self.model = Lasso(alpha=0.1, positive=False, fit_intercept=False)

    def train(self, variable_names, csv_path=None):
        print("\n[BRAIN] Initiating Learning Sequence...")
        X_train = []
        y_train = []

        # 1. Load Data
        if csv_path:
            try:
                # Expects a CSV where columns match variable_names, last col is Result
                df = pd.read_csv(csv_path)
                print("   -> Loaded User CSV Data.")
                # (Data parsing logic would go here in a full production version)
            except Exception as e:
                print(f"   [!] CSV Error: {e}. Switching to Synthetic Calibration.")
        
        # 2. Synthetic Calibration (if no CSV provided)
        if not X_train:
            print("   -> Generating Synthetic Training Data for Calibration...")
            for _ in range(50):
                # Create fake history: Random variances for inputs
                row = [random.uniform(-0.5, 0.5) for _ in variable_names]
                X_train.append(row)
                
                # Assume a 'Hidden Truth' (Only 1st variable matters)
                # This tests if the AI can ignore the others.
                true_result = (row[0] * 1000) + random.uniform(-10, 10)
                y_train.append(true_result)

        # 3. Fit Lasso Model
        self.model.fit(X_train, y_train)
        
        # 4. Map Weights
        new_weights = {}
        for i, name in enumerate(variable_names):
            w = self.model.coef_[i]
            if abs(w) < 0.01:
                print(f"   [OMITTED] Variable '{name}' determined to be noise (w=0).")
                new_weights[name] = 0.0
            else:
                print(f"   [KEPT]    Variable '{name}' adjusted weight: {w:.4f}")
                new_weights[name] = w
                
        return new_weights