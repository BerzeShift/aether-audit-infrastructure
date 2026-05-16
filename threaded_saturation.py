import time
import threading
import numpy as np
import matplotlib.pyplot as plt

def computational_payload(size, use_laminar, results, index):
    start = time.time()
    if not use_laminar:
        # Turbulent State: Dynamic overhead, unaligned allocation inside the thread
        a = np.random.rand(size, size).astype(np.float32)
        b = np.random.rand(size, size).astype(np.float32)
        c = np.dot(a, b)
    else:
        # Laminar State: Pre-contiguous memory pass
        a = np.ascontiguousarray(np.random.rand(size, size).astype(np.float32))
        b = np.ascontiguousarray(np.random.rand(size, size).astype(np.float32))
        c = np.empty((size, size), dtype=np.float32)
        np.dot(a, b, out=c)
        
    duration = time.time() - start
    results[index] = duration

def run_saturation_rally():
    print("--- ACTIVATING MULTI-THREADED SATURATION AUDIT ---")
    print("Substrate: Multi-Core Resource Contention Test")
    
    # Target size optimized for concurrent thread load
    size = 10000 
    thread_count = 4
    
    # --- PHASE 1: TURBULENT RESOURCE WAR ---
    print(f"\nLaunching {thread_count} Turbulent Threads simultaneously...")
    turbulent_results = [0] * thread_count
    threads = []
    
    for i in range(thread_count):
        t = threading.Thread(target=computational_payload, args=(size, False, turbulent_results, i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    for idx, r in enumerate(turbulent_results):
        print(f"Turbulent Thread {idx+1} Latency: {r:.2f}s")

    # --- PHASE 2: LAMINAR CONCURRENCY ---
    print(f"\nLaunching {thread_count} Laminar Threads simultaneously...")
    laminar_results = [0] * thread_count
    threads = []
    
    for i in range(thread_count):
        t = threading.Thread(target=computational_payload, args=(size, True, laminar_results, i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    for idx, r in enumerate(laminar_results):
        print(f"Laminar Thread {idx+1} Latency: {r:.2f}s")

    # Metrics
    print("\n--- PERFORMANCE FORENSICS ---")
    print(f"Max Turbulent Delay: {max(turbulent_results):.2f}s")
    print(f"Max Laminar Delay: {max(laminar_results):.2f}s")
    print(f"Net Throughput Delta: {max(turbulent_results) - max(laminar_results):.2f}s")

if __name__ == "__main__":
    run_saturation_rally()
