import random
import statistics

class Variable:
    def __init__(self, name, h_val, n_val, weight, vol):
        self.name = name
        self.h_val = float(h_val)
        self.n_val = float(n_val)
        self.weight = float(weight)
        self.vol = float(vol)

    def calculate_impact(self, baseline_x, is_sim=False):
        """
        Formula: y = X' * ((Hist - New) / Hist) * w
        """
        if self.h_val == 0: return 0
        
        current = self.n_val
        # Apply Monte Carlo Noise
        if is_sim and self.vol > 0:
            current = current * (1 + random.uniform(-self.vol, self.vol))
            
        variance_ratio = (self.h_val - current) / self.h_val
        return baseline_x * variance_ratio * self.weight

class SimulationEngine:
    def __init__(self, baseline, variables):
        self.baseline = baseline
        self.variables = variables # List of Variable objects
        self.results = []

    def run(self, iterations=10000):
        print(f"\n[ENGINE] Simulating {iterations} iterations...")
        self.results = []
        
        for _ in range(iterations):
            sum_y = 0
            for var in self.variables:
                # If weight is 0 (Omitted by AI), skip calculation
                if var.weight != 0:
                    sum_y += var.calculate_impact(self.baseline, is_sim=True)
            
            final_x = self.baseline + sum_y
            self.results.append(final_x)
            
        return self.results

    def get_statistics(self):
        if not self.results: return None
        return {
            "avg": statistics.mean(self.results),
            "min": min(self.results),
            "max": max(self.results),
            "median": statistics.median(self.results)
        }