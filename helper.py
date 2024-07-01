def find_connected_transmitters(root, transmitters, traversed_transmitters: set, max_r):
    for transmitter in transmitters:
        if transmitter not in traversed_transmitters:
            traversed_transmitters.add(transmitter)
            adjusted_range = transmitter.r + max_r + 1
            transmitters_in_range = root.find_in_circle(root, transmitter.x, transmitter.y, adjusted_range)
            connected_transmitters = []
            for t in transmitters_in_range:
                if t.connected:
                    # skip already connected transmitters
                    continue
                else:
                    in_range = transmitter.is_in_range(t.x, t.y, t.r)
                    if in_range:
                        connected_transmitters.append(t)
                        t.connect()
                        traversed_transmitters.add(transmitter)

            find_connected_transmitters(root, connected_transmitters, traversed_transmitters, max_r)
    return False
