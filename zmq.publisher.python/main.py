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
    # directionX:

class DetectionEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        return o.__dict__


url = 'tcp://*:2000'

def main() -> None:
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUB)
    socket.bind(url)

    i = 0
    while True:
        message = Detection(
            id=str(i),
            type=f'dummy {i}',
            description=f'some description {i}',
            position = Detection_Position(
                x=1,
                y=2,
                box_top_x=0,
                box_top_y=1,
                box_bottom_x=55,
                box_bottom_y=56
            ),
            score=5.3,
            velocity=18,
            timestampUtm=time.time()
        )

        message_json =  DetectionEncoder().encode(message)
        print(f"send data {message_json}")
        socket.send_string(message_json)
        time.sleep(0.05)

        i = (i + 1) % 100

if __name__ == '__main__':
    main()