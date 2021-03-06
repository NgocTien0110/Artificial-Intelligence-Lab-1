# ---------------------------------------
#   Trường Đại học Khoa Học Tự Nhiên    #
#   Đặng Ngọc Tiến - 20127641           #
# ---------------------------------------
from queue import PriorityQueue

import pygame
import time
import Gui
pygame.init()

# read file
with open('input.txt', 'r') as f:
    rows, cols = [int(x) for x in next(f).split()]  # read first line
    start_goal = [int(x) for x in next(f).split()]
    n = int(f.readline())
    array = []
    for line in f:  # read rest of lines
        array.append([int(x) for x in line.split()])


# grid
class Grid:
    WHITE = (255, 255, 255)

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.start = None
        self.end = None
        self.nodes = self.make_grid()

    def make_grid(self):
        grid = []
        gap = (self.height) / (self.cols)
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                node = Node(i, j, gap, self.rows, self.cols, self.win)
                grid[i].append(node)
        return grid

    def draw_grid(self):
        gap = (self.height) / (self.cols)
        for row in self.nodes:
            for node in row:
                node.draw()

        for i in range(self.cols+1):
            pygame.draw.line(self.win, (0, 255, 0), (0, i * gap),
                             (self.rows*gap, i * gap))
            for j in range(self.rows+1):
                pygame.draw.line(self.win, (0, 255, 0), (j * gap, 0),
                                 (j * gap, self.cols*gap))

        pygame.display.update()

    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.nodes[i][j].reset()
        self.start = None
        self.end = None

    def clear_algorithm(self):
        for row in self.nodes:
            for node in row:
                if node.is_empty():
                    node.reset()

    def init_maze(self):
        sNode = self.nodes[start_goal[0]][rows - start_goal[1]]
        gNode = self.nodes[start_goal[2]][rows - start_goal[3]]
        if not self.start:
            # If start node is not set, set start node
            sNode.make_start()
            self.start = sNode
        elif not self.end:
            # If end node is not set, set end node
            gNode.make_end()
            self.end = gNode
        else:
            # if both start and end are set, make wall
            for i in range(rows+1):
                wallNode = self.nodes[0][i]
                wallNode.make_wall()
                wallNode = self.nodes[cols][i]
                wallNode.make_wall()
            for i in range(cols+1):
                wallNode = self.nodes[i][0]
                wallNode.make_wall()
                wallNode = self.nodes[i][rows]
                wallNode.make_wall()

            for i in range(0, n):
                tx = []
                ty = []
                for j in range(len(array[i])):
                    if j % 2 == 0:
                        tx.append(array[i][j])
                    else:
                        ty.append(array[i][j])
                j = 0
                # draw p1 -> p(n-1)
                while j < len(tx)-1:
                    if tx[j+1] == tx[j]:  # draw vertical lines
                        for l in range(timmin(ty[j], ty[j+1]), timmax(ty[j], ty[j+1])+1):
                            a = tx[j]
                            b = l
                            barrierNode = self.nodes[tx[j]][rows - l]
                            barrierNode.make_wall()
                    elif ty[j] == ty[j+1]:   # draw horizontal lines
                        for l in range(timmin(tx[j], tx[j+1]), timmax(tx[j], tx[j+1])+1):
                            barrierNode = self.nodes[l][rows - ty[j]]
                            barrierNode.make_wall()
                    else:  # draw diagonal lines
                        b = (tx[j]*ty[j+1] - tx[j+1]*ty[j])/(tx[j]-tx[j+1])
                        a = (ty[j]-b)/tx[j]

                        for l in range(timmin(tx[j], tx[j+1]), timmax(tx[j], tx[j+1])):
                            p = int(a*l+b)
                            barrierNode = self.nodes[l][rows - p]
                            barrierNode.make_wall()
                        for l in range(timmin(ty[j], ty[j+1]), timmax(ty[j], ty[j+1])):
                            p = int((l-b)/a)
                            barrierNode = self.nodes[p][rows - l]
                            barrierNode.make_wall()

                    j = j+1

                # draw p(n-1) -> p0
                if tx[0] == tx[j]:  # draw vertical lines
                    for l in range(timmin(ty[j], ty[0]), timmax(ty[j], ty[0])+1):
                        a = tx[j]
                        b = l
                        barrierNode = self.nodes[tx[j]][rows - l]
                        barrierNode.make_wall()
                elif ty[j] == ty[0]:   # draw horizontal lines
                    for l in range(timmin(tx[j], tx[0]), timmax(tx[j], tx[0])+1):
                        barrierNode = self.nodes[l][rows - ty[j]]
                        barrierNode.make_wall()
                else:  # draw diagonal lines
                    b = (tx[j]*ty[0] - tx[0]*ty[j])/(tx[j]-tx[0])
                    a = (ty[j]-b)/tx[j]
                    for l in range(timmin(tx[j], tx[0]), timmax(tx[j], tx[0])):
                        p = int(a*l+b)
                        barrierNode = self.nodes[l][rows - p]
                        barrierNode.make_wall()
                    

    # BFS Search Algorithm 

    def bfs(self, start_node):
        parent = {}  # explored
        queue = []  # frontier
        queue.append(start_node)

        # Loop through while queue is not empty
        while len(queue) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_algorithm()
                        return -1

            # Set current node to first time inserted into the queue - FIFO
            current = queue.pop(0)

            for neighbor in current.neighbors:
                if not neighbor.is_visited():
                    parent[neighbor] = current
                   
                    if neighbor.is_end():
                        # Found the end - Reconstruct the Path
                        return self.reconstruct_path(parent, neighbor)
                   
                    if not neighbor.is_end() and not neighbor.is_start():
                        # Mark neighbor node open and visited
                        neighbor.make_open()
                        neighbor.make_visited()
                    queue.append(neighbor)

                # Update the grid with open & closed nodes
                self.draw_grid()

                # Close current node
                if current != start_node:
                    current.make_closed()

        return -1

    # UCS Search Algorithm 
    def ucs(self, start_node):
        parent = {} 
        queue = [] # frontier
        queue.append(start_node)

        # Loop through while queue is not empty
        while len(queue) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_algorithm()
                        return -1

            # chooses the lowest-cost node in frontier
            sorted(queue)
            current = queue.pop(0)
    
            for neighbor in current.neighbors:
                if not neighbor.is_visited():
                    parent[neighbor] = current
                    if neighbor.is_end():
                        # Found the end - Reconstruct the Path
                        return self.reconstruct_path(parent, neighbor)
                    
                    if not neighbor.is_end() and not neighbor.is_start():
                        # Mark neighbor node open and visited
                        neighbor.make_open()
                        neighbor.make_visited()
                    queue.append(neighbor)

                # Update the grid with open & closed nodes              
                self.draw_grid()

                # Close current node
                if current != start_node:
                    current.make_closed()

        return -1

    # Depth limit Search Algorithm
    def dls(self,start_node, limit):
        stack = []
        parent = {}
        stack.append(start_node)
        while limit <= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_algorithm()

                        return -1
            # Set current node to the last added to the stack - LIFO
            current = stack.pop()
            if current.is_end():
                # Found the end - Reconstruct the Path
                return parent, current, True #self.reconstruct_path(parent, current)

            if not current.is_start():
                # Close and mark node as visited
                current.make_closed()

                current.make_visited()

            # Loop through all neighbors of current node (up,down,left,right)
            for neighbor in current.neighbors:
                if not neighbor.is_visited():
                    parent[neighbor] = current
                    stack.append(neighbor)

                    if not neighbor.is_start() and not neighbor.is_end():
                        neighbor.make_open()

                self.draw_grid()
            limit = limit-1
        return -1

    # Iterative Deepening Search Algorithm
    def ids(self, start_node, limit):
        notcutoff = False
        for depth in range(limit):
            parent, current, notcutoff = self.dls(start_node, depth)
            if (notcutoff == True):
                return self.reconstruct_path(parent, current)
        return -1


    # A* Search Algorithm - Weigthed and gaurentee's the shortest path
    def astar(self, start_node, end_node):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start_node))
        parent = {}
        g_score = {node: float("inf") for row in self.nodes for node in row}
        g_score[start_node] = 0
        f_score = {node: float("inf") for row in self.nodes for node in row}
        f_score[start_node] = self.manhattan_distance(
            start_node.get_pos(), end_node.get_pos())

        open_set_hash = {start_node}

        # While open set is not empty, loop through
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_algorithm()
                        return -1

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current.is_end():
                return self.reconstruct_path(parent, end_node)

            if current != start_node:
                current.make_closed()

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    parent[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + \
                        self.manhattan_distance(neighbor.get_pos(),
                                                end_node.get_pos())

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        if not neighbor.is_end():
                            neighbor.make_open()

            # Update the grid with open & closed nodes           
            self.draw_grid()

        return -1

    # Greedy - Best First Search Algorithm 
    def greedy(self, start_node, end_node):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start_node))
        parent = {}
        f_score = {node: float("inf") for row in self.nodes for node in row}
        f_score[start_node] = self.manhattan_distance(
            start_node.get_pos(), end_node.get_pos())

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_algorithm()
                        return -1

            current = open_set.get()[2]

            if current.is_end():
                return self.reconstruct_path(parent, end_node)

            if current != start_node:
                current.make_closed()

            for neighbor in current.neighbors:
                if not neighbor.is_closed() and not neighbor.is_open():
                    f_score[neighbor] = self.manhattan_distance(
                        neighbor.get_pos(), end_node.get_pos())
                    parent[neighbor] = current
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    if not neighbor.is_end() and not neighbor.is_start():
                        neighbor.make_open()

            # Update the grid with open & closed nodes
            self.draw_grid()

        return -1

    def manhattan_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, parent, current):
        count = 0
        while current in parent:
            current = parent[current]
            if current == self.start:
                return count
            current.make_path()
            count += 1
            # Draw the Path by steps
            self.draw_grid()

    def run_algorithm(self, value):
        # Check if Algorithm is selected
        if value < 0:
            return -1

        start_node = self.start
        end_node = self.end

        # Check if Start and End nodes are added
        if start_node == None or end_node == None:
            return -1

        # Update Neighbors for all nodes
        for row in self.nodes:
            for node in row:
                node.update_neighbors(self.nodes)

        # clear board
        self.clear_algorithm()

        if value == 0:
            return self.bfs(start_node)
        elif value == 1:
            return self.ucs(start_node)
        elif value == 2:
            return self.ids(start_node,4)
        elif value == 3:
            return self.astar(start_node, end_node)
        else:
            # Greedy Best First Search
            return self.greedy(start_node, end_node)


class Node:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)

    def __init__(self, row, col, width, total_rows, total_cols, win):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = self.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.win = win
        self.start = False
        self.end = False
        self.visited = False

    def get_pos(self):
        return self.row, self.col

    def is_visited(self):
        return self.visited

    def is_closed(self):
        return self.color == self.RED

    def is_open(self):
        return self.color == self.GREEN

    def is_wall(self):
        return self.color == self.BLACK

    def is_start(self):
        return self.color == self.BLUE

    def is_end(self):
        return self.color == self.ORANGE

    def is_empty(self):
        if self.color == self.WHITE or self.color == self.GREEN or self.color == self.RED or self.color == self.PURPLE:
            return True

    def reset(self):
        self.start = False
        self.end = False
        self.wall = False
        self.visited = False
        self.color = self.WHITE

    def make_visited(self):
        self.visited = True

    def make_closed(self):
        self.color = self.RED

    def make_open(self):
        self.color = self.GREEN

    def make_wall(self):
        self.color = self.BLACK

    def make_start(self):
        self.start = True
        self.visited = False
        self.color = self.BLUE

    def make_end(self):
        self.end = True
        self.visited = False
        self.color = self.ORANGE

    def make_path(self):
        self.color = self.PURPLE

    def draw(self):
        pygame.draw.rect(self.win, self.color,
                         (self.x, self.y, self.width, self.width))

    def update_neighbors(self, nodes):
        self.neighbors = []
        if self.row > 0 and not nodes[self.row - 1][self.col].is_wall():  # Up
            self.neighbors.append(nodes[self.row - 1][self.col])

        # Down
        if self.row < self.total_rows - 1 and not nodes[self.row + 1][self.col].is_wall():
            self.neighbors.append(nodes[self.row + 1][self.col])

        # Right
        if self.col < self.total_cols - 1 and not nodes[self.row][self.col + 1].is_wall():
            self.neighbors.append(nodes[self.row][self.col + 1])

        if self.col > 0 and not nodes[self.row][self.col - 1].is_wall():  # Left
            self.neighbors.append(nodes[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def redraw_window(win, board, event_list, time, display_count, run_button,  clear_button):
    # Draw time
    if time != None:
        fnt = pygame.font.SysFont("cambria", 35)
        win.fill(("#E0FFFF"), (600, 470, 600, 470))  # clear the text
        time_text = fnt.render("Time: " + str(time), 1, (71, 95, 119))
        win.blit(time_text, (600, 470))

    if display_count >= 0:
        fnt = pygame.font.SysFont("cambria", 20)
        time_text = fnt.render(
            "Path to Goal: " + str(display_count), 1, (71, 95, 119))
        win.blit(time_text, (610, 520))

    # Draw grid and board
    board.draw_grid()

    # Draw Buttons
    run_button.draw(event_list)
    clear_button.draw(event_list)


def timmin(a, b):
    if a < b:
        return a
    else:
        return b


def timmax(a, b):
    if a > b:
        return a
    else:
        return b


if __name__ == "__main__":
    # of win
    width = 800
    height = 600

    # gap
    gap = (height - 150) // (rows+1)
    clock = pygame.time.Clock()  # time
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lab 1: Search ")
    board = Grid(cols+1, rows+1, (cols+1)*gap, (rows+1)*gap, win)

    run = True
    start = None
    play_time = None

    # font of button
    font = pygame.font.SysFont("cambria", 55)
    small_font = pygame.font.SysFont("cambria", 35)
    tiny_font = pygame.font.SysFont("cambria", 17)

    run_button = Gui.Button("Run Algorithm", 360, 65,
                            (200, 470), win, font)
    clear_button = Gui.Button("Reset", 360, 45,
                              (200, 540), win, small_font)

    WHITE = (255, 255, 255)
    list1 = Gui.DropDown(
        [("#CCCCCC"), ("#CCCCCC")],
        [(WHITE), ("#CCCCCC")],
        50, 470, 130, 17,
        tiny_font,
        "Select Algorithm", ["Breadth First", "Uniform Cost", "IDDFS", "A* Search", "Greedy-BFS"])

    # bg win
    win.fill(("#E0FFFF"))
    algorithm = -1
    display_count = -1

    while run:

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.QUIT

                if event.key == pygame.K_DELETE:
                    board.clear()

                if event.key == pygame.K_SPACE:
                    start = time.perf_counter()
                    display_count = board.run_algorithm(algorithm)
                    play_time = round(time.perf_counter() - start, 2)

                # if event.key == pygame.K_RETURN:
                #     board.clear_algorithm()
        # init maze
        board.init_maze()

        # Get algorithm from drop down menu
        selected_option = list1.update(event_list)
        if selected_option >= 0:
            list1.main = list1.options[selected_option]
            algorithm = selected_option

        # Check in Run Button is Pressed, if so run algorithm
        if run_button.check_pressed():
            start = time.perf_counter()
            display_count = board.run_algorithm(algorithm)
            play_time = round(time.perf_counter() - start, 2)

        # Clear Board
        if clear_button.check_pressed():
            board.clear()

        win.fill("#E0FFFF", ((50, 480), (130, 300)))
        list1.draw(win)

        # Draw Board + Time
        redraw_window(win, board, event_list, play_time, display_count, run_button,
                      clear_button)
        pygame.display.update()
        clock.tick(60)

pygame.quit()
