import time
import numpy as np

def run_cache_forensics():
    print("--- DEPLOYING L1/L2 CACHE REVERSE-ENGINEERING AUDIT ---")
    print("Substrate: Measuring Hardware Memory Stride Invalidation\n")
    
    # 20,000 x 20,000 flat matrix array to completely overshoot cache capacity
    size = 20000
    print(f"Allocating high-density matrix footprint: {size}x{size}")
    matrix = np.random.rand(size, size).astype(np.float32)
    
    # --- PHASE 1: THE TURBULENT STRIDE (Column-Major / Jipping Cache Lines) ---
    print("Executing Phase 1: Column-Major Traversal (Choking CPU Cache)...")
    start = time.time()
    # Step every 50th column to force the CPU to constantly clear its cache line
    for col in range(0, size, 50):
        _ = np.sum(matrix[:, col])
    turbulent_duration = time.time() - start
    print(f"Turbulent Traversal Complete: {turbulent_duration:.4f}s")
    
    # --- PHASE 2: THE LAMINAR STRIDE (Row-Major / Riding Cache Lines) ---
    print("\nExecuting Phase 2: Row-Major Traversal (Aligned Laminar Flow)...")
    start = time.time()
    # Step every 50th row—reading data exactly how it sits contiguously in RAM
    for row in range(0, size, 50):
        _ = np.sum(matrix[row, :])
    laminar_duration = time.time() - start
    print(f"Laminar Traversal Complete:   {laminar_duration:.4f}s")
    
    # --- FORENSIC RESULTS ---
    speedup = (turbulent_duration / laminar_duration)
    efficiency_reclaimed = ((turbulent_duration - laminar_duration) / turbulent_duration) * 100
    
    print("\n--- HARDWARE TELEMETRY REPORT ---")
    print(f"Turbulent Execution (Cache Miss Chaos): {turbulent_duration:.4f}s")
    print(f"Laminar Execution (Sequential Perfection): {laminar_duration:.4f}s")
    print(f"Physical Velocity Multiplier:            {speedup:.2f}x Faster")
    print(f"Silicon Efficiency Gap Reclaimed:        {efficiency_reclaimed:.2f}%")

if __name__ == "__main__":
    run_cache_forensics()
