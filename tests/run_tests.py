import os
import sys

# ensure package import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from test_codec import test_encode_decode_roundtrip, test_signature_mismatch


def run():
    tests = [test_encode_decode_roundtrip, test_signature_mismatch]
    ok = 0
    total = len(tests)
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            ok += 1
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")

    print(f"{ok}/{total} tests passed")
    sys.exit(0 if ok == total else 2)


if __name__ == "__main__":
    run()
