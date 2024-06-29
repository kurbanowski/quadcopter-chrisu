class QuadNode:
    def __init__(self, x0, y0, x1, y1, node_capacity=4):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.children = [None, None, None, None]  # NW, NE, SE, SW
        self.transmitters = []
        self.width = x1
        self.height = y1
        self.node_capacity = node_capacity  # max 4 points per leaf node before division

    def is_leaf(self):
        return all(child is None for child in self.children)

    def insert(self, quad_node, transmitter, x0, y0, x1, y1):
        x, y, r = transmitter.x, transmitter.y, transmitter.r
        if quad_node.is_leaf():
            quad_node.transmitters.append(transmitter)
            if len(quad_node.transmitters) > self.node_capacity:
                self.subdivide(quad_node, x0, y0, x1, y1)
        else:
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            idx = 0 if y < mid_y else 2
            idx += 1 if x > mid_x else 0
            if quad_node.children[idx] is None:
                if idx == 0:  # NW
                    quad_node.children[idx] = QuadNode(x0, y0, mid_x, mid_y)
                elif idx == 1:  # NE
                    quad_node.children[idx] = QuadNode(mid_x, y0, x1, mid_y)
                elif idx == 2:  # SW
                    quad_node.children[idx] = QuadNode(x0, mid_y, mid_x, y1)
                elif idx == 3:  # SE
                    quad_node.children[idx] = QuadNode(mid_x, mid_y, x1, y1)
            self.insert(quad_node.children[idx], transmitter,
                        x0 if idx % 2 == 0 else mid_x,
                        y0 if idx < 2 else mid_y,
                        mid_x if idx % 2 == 0 else x1,
                        mid_y if idx < 2 else y1
                        )

    def subdivide(self, quad_node, x0, y0, x1, y1):
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2

        # Create 4 children for the current node
        quad_node.children = [
            QuadNode(x0, y0, mid_x, mid_y),  # NW
            QuadNode(mid_x, y0, x1, mid_y),  # NE
            QuadNode(x0, mid_y, mid_x, y1),  # SW
            QuadNode(mid_x, mid_y, x1, y1)  # SE
        ]

        # Distribute existing points to the appropriate child
        while quad_node.transmitters:
            transmitter = quad_node.transmitters.pop()
            idx = 0 if transmitter.y < mid_y else 2
            idx += 1 if transmitter.x > mid_x else 0
            self.insert(quad_node.children[idx], transmitter,
                        x0 if idx % 2 == 0 else mid_x,
                        y0 if idx < 2 else mid_y,
                        mid_x if idx % 2 == 0 else x1,
                        mid_y if idx < 2 else y1
                        )

    def find_in_circle(self, quad_node, x, y, radius):
        transmitters_within_radius = []
        radius2 = radius ** 2  # store squared radius to reduce maths operations

        def search(node, x0, y0, x1, y1):
            if node is None:
                return
            if node.is_leaf():
                for transmitter in node.transmitters:
                    distance_x, distance_y = transmitter.x - x, transmitter.y - y
                    if distance_x ** 2 + distance_y ** 2 <= radius2:
                        transmitters_within_radius.append(transmitter)
            else:
                mid_x = (x0 + x1) / 2
                mid_y = (y0 + y1) / 2
                if node.children[0] is not None and x - radius < mid_x and y - radius < mid_y:
                    search(node.children[0], x0, y0, mid_x, mid_y)
                if node.children[1] is not None and x + radius > mid_x and y - radius < mid_y:
                    search(node.children[1], mid_x, y0, x1, mid_y)
                if node.children[2] is not None and x - radius < mid_x and y + radius > mid_y:
                    search(node.children[2], x0, mid_y, mid_x, y1)
                if node.children[3] is not None and x + radius > mid_x and y + radius > mid_y:
                    search(node.children[3], mid_x, mid_y, x1, y1)

        search(quad_node, 0, 0, self.width, self.height)
        return transmitters_within_radius
