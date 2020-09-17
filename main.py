import pygame
import random
""" MAZE FUNCTION() IS CALLED AT THE END OF THE CODE"""


class Cell:
    def __init__(self, x, y, cell_size):
        self.x = x * cell_size
        self.y = y * cell_size
        self.walls = [True, True, True, True]


class Maze:
    # THE CELL SIZE IS THE SIZE OF THE BLOCKS INSIDE THE MAZE IN PIXELS
    def __init__(self, cell_size):
        self.clock = pygame.time.Clock()
        self.FPS = 14
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PURPLE = (108, 0, 108)
        self.PURPLE_2 = (198, 0, 198)
        self.screen = pygame.display.set_mode((600, 600))
        self.size = cell_size
        (self.width, height) = (600, 600)
        pygame.display.set_caption('Maze generator')
        self.running = True
        self.grid_list = []
        self.current = 0
        self.next_curr = (0, 0)
        self.last_curr = (0, 0)
        self.visited_points = [(0, 0)]
        self.stack = [(0, 0)]
        limit = int(self.width / self.size)
        lines = [x * self.size for x in range(limit + 1)]
        for y in range(len(lines) - 1):
            for x in range(len(lines) - 1):
                c = Cell(x, y, self.size)
                self.grid_list.append(c)

    def show_lines(self):
        size = self.size
        for obj in self.grid_list:
            if obj.walls[0]:
                # UP
                pygame.draw.line(self.screen, self.WHITE, (obj.y, obj.x), (obj.y + size, obj.x), 1)
            if obj.walls[1]:
                # DOWN
                pygame.draw.line(self.screen, self.WHITE, (obj.y, obj.x + size), (obj.y + size, obj.x + size), 1)
            if obj.walls[2]:
                # LEFT
                pygame.draw.line(self.screen, self.WHITE, (obj.y, obj.x), (obj.y, obj.x + size), 1)
            if obj.walls[3]:
                # RIGHT
                pygame.draw.line(self.screen, self.WHITE, (obj.y + size, obj.x), (obj.y + size, obj.x + size), 1)

    def show_rect(self):
        for p in self.visited_points:
            pygame.draw.rect(self.screen, self.PURPLE_2, (p[0], p[1], self.size, self.size))
        pygame.draw.rect(self.screen, self.PURPLE, (self.next_curr[0], self.next_curr[1], self.size, self.size), 0)

    def check_neighbors(self, x, y):
        neighbors = []
        if x > 0 and (x-self.size, y) not in self.visited_points:
            neighbors.append((x-self.size, y))
        if x < self.width-self.size and (x + self.size, y) not in self.visited_points:
            neighbors.append((x + self.size, y))
        if y > 0 and (x,y-self.size) not in self.visited_points:
            neighbors.append((x,y-self.size))
        if y < self.width-self.size and (x, y+self.size) not in self.visited_points:
            neighbors.append((x, y+self.size))

        if neighbors:
            neighbor = random.choice(neighbors)
            self.visited_points.append(neighbor)
            self.stack.append(neighbor)
            self.last_curr = self.next_curr
            self.next_curr = (neighbor[0], neighbor[1])
        else:
            if self.stack:
                self.next_curr = [self.stack[-1][0], self.stack[-1][1]]
                self.stack.pop()

    def remove_walls(self, x, y, x2, y2, wall1, wall2):
        for obj in self.grid_list:
            if (obj.x, obj.y) == (x, y):
                obj.walls[wall1] = False
            if (obj.x, obj.y) == (x2, y2):
                obj.walls[wall2] = False

    def check_walls(self):
        walls = [self.last_curr, self.next_curr]
        y = walls[0][0]
        x = walls[0][1]
        y2 = walls[1][0]
        x2 = walls[1][1]
        if x > x2:
            self.remove_walls(x, y, x2, y2, 0, 1)
        elif x < x2:
            self.remove_walls(x, y, x2, y2, 1, 0)
        elif y < y2:
            self.remove_walls(x, y, x2, y2, 3, 2)
        elif y > y2:
            self.remove_walls(x, y, x2, y2, 2, 3)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(self.BLACK)
            self.show_rect()
            if self.next_curr != self.last_curr:
                self.check_walls()
            self.show_lines()
            self.check_neighbors(self.next_curr[0], self.next_curr[1])
            self.clock.tick(self.FPS)
            pygame.display.flip()


m = Maze(20)
m.run()