from typing import List
from transmitter import Transmitter


class Connections:
    def __init__(self, quad_root, end_point, max_r):
        self.quad_root = quad_root
        self.end_point = end_point
        self.max_r = max_r

    def find_connected_transmitters(self, transmitters: List[Transmitter], traversed_transmitters: set):
        for transmitter in transmitters:
            if transmitter not in traversed_transmitters:
                traversed_transmitters.add(transmitter)
                adjusted_range = transmitter.r + self.max_r + 1
                transmitters_in_range = self.quad_root.find_in_circle(
                    self.quad_root,
                    transmitter.x,
                    transmitter.y,
                    adjusted_range
                )
                connected_transmitters = []
                for t in transmitters_in_range:
                    # unconnected new transmitter
                    if not t.connected and t != transmitter:
                        in_range = transmitter.is_in_range(t.x, t.y, t.r)
                        if in_range:
                            connected_transmitters.append(t)
                            t.connect()
                            if t.x == self.end_point.x and t.y == self.end_point.y:  # store end_point
                                return True
                # recursively find connections between transmitters
                if self.find_connected_transmitters(connected_transmitters, traversed_transmitters):
                    return True
        return False
