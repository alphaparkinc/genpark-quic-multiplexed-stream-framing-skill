class QUICPacketEngine:
    """
    QUIC Multiplexed Stream Framing Engine preventing Head-of-Line blocking
    across parallel byte streams within a single transport connection.
    """
    def __init__(self, connection_id=1024):
        self.connection_id = connection_id
        self.streams = {}
        self.packet_number = 0

    def encode_varint(self, value):
        if value < 64:
            return bytes([value])
        elif value < 16384:
            b0 = (value >> 8) | 0x40
            b1 = value & 0xFF
            return bytes([b0, b1])
        else:
            b0 = (value >> 24) | 0x80
            b1 = (value >> 16) & 0xFF
            b2 = (value >> 8) & 0xFF
            b3 = value & 0xFF
            return bytes([b0, b1, b2, b3])

    def create_stream_frame(self, stream_id, offset, data, fin=False):
        self.packet_number += 1
        frame = {
            "packet_number": self.packet_number,
            "conn_id": self.connection_id,
            "stream_id": stream_id,
            "offset": offset,
            "length": len(data),
            "payload": data,
            "fin": fin
        }
        return frame

    def receive_stream_frame(self, frame):
        sid = frame["stream_id"]
        if sid not in self.streams:
            self.streams[sid] = bytearray()
        offset = frame["offset"]
        data = frame["payload"]
        if len(self.streams[sid]) < offset + len(data):
            self.streams[sid].extend(b"\x00" * (offset + len(data) - len(self.streams[sid])))
        self.streams[sid][offset:offset+len(data)] = data
        return bytes(self.streams[sid])
