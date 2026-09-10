import sys
import json
import base64
from client import QUICPacketEngine

def main():
    quic = QUICPacketEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "create_frame":
            raw_b64 = params.get("data_b64", "")
            data = base64.b64decode(raw_b64.encode())
            frame = quic.create_stream_frame(params.get("stream_id", 0), params.get("offset", 0), data, params.get("fin", False))
            res = {
                "packet_number": frame["packet_number"],
                "length": frame["length"],
                "fin": frame["fin"]
            }
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
