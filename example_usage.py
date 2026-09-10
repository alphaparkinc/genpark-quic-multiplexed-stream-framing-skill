from client import QUICPacketEngine

def main():
    print("=== Testing QUIC Multiplexed Stream Framing ===")
    quic = QUICPacketEngine(connection_id=5555)
    f1 = quic.create_stream_frame(stream_id=1, offset=0, data=b"Hello ", fin=False)
    f2 = quic.create_stream_frame(stream_id=1, offset=6, data=b"World!", fin=True)
    quic.receive_stream_frame(f1)
    full = quic.receive_stream_frame(f2)
    print("Received stream 1 content:", full.decode())
    assert full == b"Hello World!"
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
