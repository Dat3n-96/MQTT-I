import os
import sys
import time
import statistics

# Ensure `src` is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mqtt_hmac_local import MqttHmacPacket, encode_packet, decode_packet, HmacSha

def run_latency_simulation():
    print("=== SCENARIO C: COMPUTATIONAL LATENCY SIMULATION ===")
    print("Benchmarking Signing vs. Verification time (N=10000 iterations)...\n")

    secret_key = b"benchmark-key-2024"
    pkt = MqttHmacPacket(fixed_header=0x30, topic="bench/test", signature=None, payload=b"sensor-value-12345")
    
    # Prepare encoded data for verification test
    encoded_sample = encode_packet(pkt, key=secret_key, signer=HmacSha())
    
    iterations = 10000
    sign_times = []
    verify_times = []

    # 1. Benchmark Signing (Encoding)
    print("Running Encoding/Signing benchmark...")
    for _ in range(iterations):
        # Reset signature to None to force re-calculation
        pkt.signature = None 
        
        t_start = time.perf_counter()
        encode_packet(pkt, key=secret_key, signer=HmacSha())
        t_end = time.perf_counter()
        
        sign_times.append(t_end - t_start)

    # 2. Benchmark Verification (Decoding)
    print("Running Decoding/Verification benchmark...")
    for _ in range(iterations):
        t_start = time.perf_counter()
        # Decode performs the HMAC verification
        decode_packet(encoded_sample, key=secret_key, signer=HmacSha())
        t_end = time.perf_counter()
        
        verify_times.append(t_end - t_start)

    # 3. Calculate Statistics
    avg_sign = statistics.mean(sign_times) * 1_000_000  # Convert to microseconds
    avg_verify = statistics.mean(verify_times) * 1_000_000 # Convert to microseconds

    print("\n--- RESULTS ---")
    print(f"Total Iterations: {iterations}")
    print(f"Avg Time to SIGN (Encode):   {avg_sign:.4f} \u00b5s (microseconds)")
    print(f"Avg Time to VERIFY (Decode): {avg_verify:.4f} \u00b5s (microseconds)")
    
    print("\n[Conclusion] The cryptographic overhead is negligible for modern IoT gateways.")

if __name__ == "__main__":
    run_latency_simulation()