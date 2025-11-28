class MqttHmacError(Exception):
    pass


class InvalidPacketError(MqttHmacError):
    pass


class HmacVerificationError(MqttHmacError):
    pass
