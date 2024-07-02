import pygame
import time
from connections import Connections
from quadnode import QuadNode

RESPONSE_TRUE = "bezpieczny przelot jest możliwy"
RESPONSE_FALSE = "bezpieczny przelot nie jest możliwy"


class Game:
    def __init__(self, root, transmitters, start_point, end_point, width=1000, height=1000, max_r=10, scale=1):
        self.root = root
        self.transmitters = transmitters
        self.start_point = start_point
        self.end_point = end_point
        self.width = width if width < 1000 else 1000  # limit screen size
        self.height = height if height < 1000 else 1000  # limit screen size
        self.max_r = max_r
        self.scale = scale

    def start(self):
        pygame.init()
        # Set up display
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Quadcopter transmitters - Click a node and be patient')

        # Colors
        white = (255, 255, 255)
        black = (0, 0, 0)  # Transmitter ranges
        blue = (0, 0, 255)  # start_point
        red = (255, 0, 0)   # end_point
        green = (0, 255, 0)  # connected nodes

        running = True
        while running:
            screen.fill(white)

            # Draw transmitter ranges
            for transmitter in self.transmitters:
                center = (
                            transmitter.x * self.scale,
                            (self.height - transmitter.y * self.scale)
                        )
                circle_radius = transmitter.r * self.scale
                if transmitter.connected:
                    pygame.draw.circle(screen, green, center, circle_radius, 3)
                else:
                    pygame.draw.circle(screen, black, center, circle_radius, 1)

            if self.start_point:
                center = (
                    self.start_point.x * self.scale,
                    (self.height - self.start_point.y * self.scale)
                )
                pygame.draw.circle(screen, blue, center, self.max_r,)

            if self.end_point:
                center = (
                    self.end_point.x * self.scale,
                    (self.height - self.end_point.y * self.scale)
                )
                pygame.draw.circle(screen, red, center, self.max_r,)

            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # Place a new start_point with mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        pygame.display.set_caption(
                            f"Quadcopter transmitters - Place new Start Point"
                        )

                        # capture coordinates
                        x, y = pygame.mouse.get_pos()
                        x = x // self.scale
                        y = self.height - y  # adjust y for pygame coordinates
                        y = y // self.scale

                        self.end_point.x = x
                        self.end_point.y = y
                    if event.button == 1:
                        pygame.display.set_caption(
                            f"Quadcopter transmitters - Processing..."
                        )

                        # capture coordinates
                        x, y = pygame.mouse.get_pos()
                        x = x // self.scale
                        y = self.height - y  # adjust y for pygame coordinates
                        y = y // self.scale

                        self.start_point.x = x
                        self.start_point.y = y

                        new_root = QuadNode(0, 0, self.root.x1, self.root.y1, self.root.node_capacity)
                        for t in self.transmitters:
                            t.disconnect()
                            new_root.insert(new_root, t, 0, 0, self.root.x1, self.root.y1)

                        # measure find time
                        self.start_point.connect()
                        start_time = time.time()
                        traversed_transmitters = set()
                        connections = Connections(new_root, self.end_point, self.max_r)
                        connected = connections.find_connected_transmitters(
                            [self.start_point],
                            traversed_transmitters
                        )
                        print(RESPONSE_TRUE if connected else RESPONSE_FALSE)
                        print(f"{self.start_point.x} {self.start_point.y}")
                        query_time = time.time() - start_time
                        connections = sum([t.connected for t in self.transmitters])
                        pygame.display.set_caption(
                            f"Quadcopter transmitters - Connections:{int(connections)} in {round(float(query_time), 2)} sec"
                        )
            pygame.display.flip()
    pygame.quit()
