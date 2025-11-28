import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import mqtt_hmac_local as mqtt_hmac
print('mqtt_hmac.__file__ =', getattr(mqtt_hmac, '__file__', repr(mqtt_hmac)))
