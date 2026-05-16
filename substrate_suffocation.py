import time
import threading
import numpy as np

def brute_force_payload(size, use_laminar, thread_id, iterations=3):
    durations = []
    
    # Introduce a micro-temporal offset for Laminar threads to prevent lockstep bus collision
    if use_laminar:
        time.sleep(thread_id * 0.015)  # 15ms staggered entry window
        
    for amg in range(iterations):
        start = time.time()
        if not use_laminar:
            a = np.random.rand(size, size).astype(np.float32)
            b = np.random.rand(size, size).astype(np.float32)
            c = np.dot(a, b)
        else:
            # Staggered Laminar execution
            a = np.ascontiguousarray(np.random.rand(size, size).astype(np.float32))
            b = np.ascontiguousarray(np.random.rand(size, size).astype(np.float32))
            c = np.empty((size, size), dtype=np.float32)
            np.dot(a, b, out=c)
            
        durations.append(time.time() - start)
    
    return sum(durations) / iterations

def execute_suffocation_rally():
    print("--- DEPLOYING AMENDED SUBSTRATE SUFFOCATION ---")
    
    size = 6500
    thread_count = 8
    
    # --- PHASE 1: UNCONTROLLED TURBULENT COLLISION ---
    print(f"\n[PHASE 1] Igniting {thread_count} Turbulent Threads...")
    turbulent_threads = []
    turbulent_scores = [0] * thread_count
    
    start_wall = time.time()
    for i in range(thread_count):
        t = threading.Thread(target=lambda idx=i: turbulent_scores.__setitem__(idx, brute_force_payload(size, False, idx)))
        turbulent_threads.append(t)
        t.start()
        
    for t in turbulent_threads:
        t.join()
    turbulent_wall_time = time.time() - start_wall
    print(f"Turbulent Wall-Clock Execution Time: {turbulent_wall_time:.2f}s")

    # --- PHASE 2: STAGGERED LAMINAR ALIGNMENT ---
    print(f"\n[PHASE 2] Igniting {thread_count} Staggered Laminar Threads...")
    laminar_threads = []
    laminar_scores = [0] * thread_count
    
    start_wall = time.time()
    for i in range(thread_count):
        t = threading.Thread(target=lambda idx=i: laminar_scores.__setitem__(idx, brute_force_payload(size, True, idx)))
        laminar_threads.append(t)
        t.start()
        
    for t in laminar_threads:
        t.join()
    laminar_wall_time = time.time() - start_wall
    print(f"Laminar Wall-Clock Execution Time: {laminar_wall_time:.2f}s")

    # --- FORENSIC SUMMARY ---
    total_delta = turbulent_wall_time - laminar_wall_time
    efficiency_reclaimed = (total_delta / turbulent_wall_time) * 100
    
    print("\n--- RECALIBRATED METRICS ---")
    print(f"Turbulent Total Lock: {turbulent_wall_time:.2f}s")
    print(f"Laminar Total Lock:   {laminar_wall_time:.2f}s")
    print(f"Net Recovery:         {total_delta:.2f}s")
    print(f"Efficiency Delta:     {efficiency_reclaimed:.2f}%")

if __name__ == "__main__":
    execute_suffocation_rally()
