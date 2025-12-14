from engine import Variable, SimulationEngine
from miner import DataMiner
from brain import SmartBrain

def main():
    print("=== THE STATISTICAL FRAMEWORK v2.0 ===")
    
    # Initialize Modules
    miner = DataMiner()
    brain = SmartBrain()
    variables = []
    
    # --- STEP 1: BASELINE X' ---
    print("\n[STEP 1] Configuration: Baseline (X')")
    mode = input("Source? (manual/auto): ").strip().lower()
    
    baseline_x = 0.0
    if mode == 'auto':
        url = input("  URL: ")
        sel = input("  CSS Selector: ")
        val = miner.scour(url, sel, "Baseline")
        baseline_x = val if val else float(input("  [Fallback] Manual X': "))
    else:
        baseline_x = float(input("  Manual X': "))

    # --- STEP 2: VARIABLES (y) ---
    print("\n[STEP 2] Configuration: Variables")
    while True:
        name = input("\nAdd Variable Name (or 'done'): ")
        if name.lower() == 'done': break
        
        h_val = float(input(f"  Historical Fact ({name}): "))
        
        # New Fact Input
        src_y = input(f"  Source for New Fact? (manual/auto): ").strip().lower()
        if src_y == 'auto':
            url = input("  URL: ")
            sel = input("  CSS Selector: ")
            val = miner.scour(url, sel, name)
            n_val = val if val else float(input("  [Fallback] Manual Value: "))
        else:
            n_val = float(input(f"  Manual New Fact ({name}): "))

        w = float(input("  Weight (1.0 = Standard): "))
        v = float(input("  Volatility (0.0 - 0.5): "))
        
        variables.append(Variable(name, h_val, n_val, w, v))

    # --- STEP 3: AI OPTIMIZATION ---
    use_ai = input("\n[STEP 3] Activate AI Logic Tweak? (y/n): ").lower()
    if use_ai == 'y':
        # Pass variable names to Brain to learn weights
        var_names = [v.name for v in variables]
        optimized_weights = brain.train(var_names)
        
        # Update variables with new learned weights
        for var in variables:
            if var.name in optimized_weights:
                var.weight = optimized_weights[var.name]

    # --- STEP 4: SIMULATION ---
    iterations = int(input("\n[STEP 4] Simulation Count: "))
    engine = SimulationEngine(baseline_x, variables)
    results = engine.run(iterations)
    stats = engine.get_statistics()

    # --- OUTPUT ---
    print("\n" + "="*40)
    print(f" FINAL PREDICTION (Avg): {stats['avg']:,.2f}")
    print("="*40)

    # Reverse Engineering / Binary Check
    xdn = float(input("\nEnter Desired Outcome (Xdn): "))
    success_count = sum(1 for r in results if r >= xdn)
    prob = (success_count / iterations) * 100
    print(f"Probability of Success: {prob:.1f}%")

    if prob < 100:
        gap = xdn - stats['avg']
        print(f"Gap to Bridge: {gap:+,.2f}")
        print("Reverse Engineering: Adjust your inputs to close this gap.")

if __name__ == "__main__":
    main()