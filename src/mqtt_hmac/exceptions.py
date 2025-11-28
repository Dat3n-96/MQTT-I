class MqttHmacError(Exception):
    """Base exception for mqtt_hmac package."""


class InvalidPacketError(MqttHmacError):
    """Raised when a packet cannot be parsed."""


class HmacVerificationError(MqttHmacError):
    """Raised when HMAC verification fails."""
