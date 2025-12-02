import os
import sys

# Ensure `src` is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mqtt_hmac_local import MqttHmacPacket, encode_packet, HmacSha

def run_overhead_simulation():
    print("=== SCENARIO B: PROTOCOL OVERHEAD ANALYSIS ===")
    print("Measuring packet size increase introduced by HMAC-SHA256 framing.\n")

    secret_key = b"test-key"
    topic = "sensors/data"  # Fixed topic length for consistency
    
    # Define different payload sizes to simulate (10B, 50B, 100B, 1KB)
    test_sizes = [10, 50, 100, 500, 1024]

    # Header for the results table
    print(f"{'Payload (Bytes)':<15} | {'Total Packet (Bytes)':<20} | {'Overhead (Bytes)':<18} | {'Efficiency (%)':<15}")
    print("-" * 75)

    for size in test_sizes:
        # Generate dummy payload of 'size' bytes
        payload_data = b'x' * size
        
        # Create packet
        pkt = MqttHmacPacket(fixed_header=0x30, topic=topic, signature=None, payload=payload_data)
        
        # Encode (this adds the signature and headers)
        encoded_data = encode_packet(pkt, key=secret_key, signer=HmacSha())
        
        total_size = len(encoded_data)
        overhead = total_size - size
        
        # Calculate efficiency: (Payload / Total) * 100
        efficiency = (size / total_size) * 100
        
        print(f"{size:<15} | {total_size:<20} | {overhead:<18} | {efficiency:.2f}%")

    print("\n[Analysis] Overhead includes:")
    print(" - Fixed Header (1B)")
    print(" - Topic Length (2B) + Topic Name")
    print(" - HMAC Length (2B) + HMAC Signature (32B for SHA256)")

if __name__ == "__main__":
    run_overhead_simulation()