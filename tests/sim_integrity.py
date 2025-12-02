import os
import sys
import time

# Ensure `src` is on sys.path to import the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from mqtt_hmac_local import MqttHmacPacket, encode_packet, decode_packet, HmacSha
from mqtt_hmac_local.exceptions import HmacVerificationError

def run_integrity_simulation():
    print("=== SCENARIO A: INTEGRITY VERIFICATION SIMULATION ===")
    
    # 1. Configuration
    secret_key = b"super-secret-key-2024"
    topic = "industrial/sensor/pressure"
    payload = b"1024.50"
    
    print(f"[Sender] Topic: {topic}")
    print(f"[Sender] Payload: {payload}")
    print(f"[Sender] Key: {secret_key.decode()} (Hidden)")

    # 2. Construct and Sign the Packet
    # We use HmacSha (SHA-256) as the default signer
    packet = MqttHmacPacket(fixed_header=0x30, topic=topic, signature=None, payload=payload)
    encoded_bytes = encode_packet(packet, key=secret_key, signer=HmacSha())
    
    print(f"\n[Network] Transmitting {len(encoded_bytes)} bytes...")
    print(f"[Network] Hex Dump (Valid): {encoded_bytes.hex()[:60]}...")

    # 3. Test 1: Valid Decoding
    print("\n--- Test 1: Legitimate Receiver ---")
    try:
        decoded = decode_packet(encoded_bytes, key=secret_key, signer=HmacSha())
        print(f"[Receiver] Signature Verified! Data: {decoded.payload.decode()}")
        print("[Result] SUCCESS: Valid packet accepted.")
    except HmacVerificationError:
        print("[Result] FAILURE: Valid packet was rejected.")

    # 4. Test 2: Man-in-the-Middle Attack (Tampering)
    print("\n--- Test 2: Tampered Packet (Attack Simulation) ---")
    
    # Simulating a bit-flip or modification in the payload
    # We take the valid bytes but change the last byte (part of the payload)
    tampered_bytes = bytearray(encoded_bytes)
    tampered_bytes[-1] = tampered_bytes[-1] ^ 0xFF  # Invert last byte
    tampered_bytes = bytes(tampered_bytes)

    print(f"[Attacker] Intercepted packet and modified last byte.")
    
    try:
        # Attempt to decode with the correct key, but invalid data
        decode_packet(tampered_bytes, key=secret_key, signer=HmacSha())
        print("[Result] FAILURE: System accepted a fake packet!")
    except HmacVerificationError as e:
        # This is the expected behavior
        print(f"[Receiver] SECURITY ALERT: {e}")
        print("[Result] SUCCESS: Tampered packet rejected.")

if __name__ == "__main__":
    run_integrity_simulation()