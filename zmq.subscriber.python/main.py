import zmq
import time
import json
from json import JSONEncoder
from dataclasses import dataclass
from typing import Any

@dataclass
class Detection_Position:
    x: int
    y: int
    box_top_x: int
    box_top_y: int
    box_bottom_x: int
    box_bottom_y: int

@dataclass
class Detection:
    id: str
    type: str
    description: str
    position: Detection_Position
    score: float
    velocity: float
    timestampUtm: float

    def __init__(self, dict):
        vars(self).update(dict)

class DetectionEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        return o.__dict__

publisher_url = 'tcp://127.0.0.1:2000'

def main() -> None:
    ctx = zmq.Context()
    socket = ctx.socket(zmq.SUB)
    socket.connect(publisher_url)

    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        json_res = socket.recv_string()
        detection = json.loads(json_res, object_hook=Detection)
        delay = time.time() - detection.timestampUtm
        print(f"delay {delay} " + DetectionEncoder().encode(detection))


if __name__ == '__main__':
    main()