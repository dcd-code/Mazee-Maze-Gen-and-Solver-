from buttonClass import *
from undo import *
from coloursss import *

from AsBr import *
from WilsonsAlgo import *
from kruskal import *
from recursiveBacktracker import *

from DFS import *
from BFS import *
from dijkstra import *
from GBFS import *
from BBFS import *

from AfterSave import *

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

from solve_maze_from_image import solve_maze_from_image

class PostLoginPage:

    def __init__(self, screen, font, small_font, db_conn=None, username=None, is_guest=False):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.db_conn = db_conn
        self.username = username
        self.is_guest = is_guest

        if db_conn and username:
            self.db_conn = db_conn
            self.username = username

        else:
            self.db_conn = None
            self.username = None

        self.message = ''
        self.current_screen = 'options'
        self.selected_button = None
        self.mouse_down = False
        self.undo_stack = []
        self.generating_maze = False

        self.create_maze_button = Buttons(self.screen, GREY, 500, 200, 400, 60, text='Create Maze')
        self.solve_from_image_button = Buttons(self.screen, GREY, 500, 400, 400, 60, text='Solve from Image')
        self.size_button = Buttons(self.screen, GREY, 1150, 20, 200, 40, text='Change Maze Size')

        self.slow_button = Buttons(self.screen, GREY, 475, 20, 200, 40, text='Slow')
        self.medium_button = Buttons(self.screen, GREY, 700, 20, 200, 40, text='Medium')
        self.fast_button = Buttons(self.screen, GREY, 925, 20, 200, 40, text='Fast')

        self.animation_speed = FAST_SPEED

        self.init_maze_option_buttons()
        self.grid_size = "Medium"
        self.grid = []
        self.grid_state = []
        self.init_grid()

        self.start_node = None
        self.end_node = None
        self.setting_start_node = True

        self.wilson_gen = None
        self.recursive_backtracker_gen = None
        self.kruskal_gen = None
        self.generating_maze = False

    def init_maze_option_buttons(self):

        button_names = [
            "Aldous-Broder", "Kruskal's", "Recursive Backtracker", "Wilson's",
            "Bidirectional BFS", "DFS", "BFS", "GBFS", "Dijkstra"
        ]
        self.maze_option_buttons = [
            Buttons(self.screen, GREY, 15, (5 + i * 76) + 15, 250, 40, text=name)
            for i, name in enumerate(button_names)
        ]
        self.start_end_node_button = Buttons(self.screen, GREY, 1150, 620, 200, 40, text="Start/End node")
        self.wall_node_button = Buttons(self.screen, GREY, 940, 620, 200, 40, text="Wall node")
        self.empty_node_button = Buttons(self.screen, GREY, 730, 620, 200, 40, text="Empty node")
        self.undo_button = Buttons(self.screen, GREY, 520, 620, 200, 40, text="Undo")
        self.main_menu_button = Buttons(self.screen, GREY, 310, 620, 200, 40, text="Main Menu")
        self.save_button = Buttons(self.screen, GREY, 295, 20, 150, 40, text='Save')

        self.view_mazes_button = Buttons(self.screen, GREY, 1150, 670, 200, 40, text='View Mazes')

        self.maze_option_buttons.append(self.start_end_node_button)
        self.maze_option_buttons.append(self.wall_node_button)
        self.maze_option_buttons.append(self.empty_node_button)
        self.maze_option_buttons.append(self.undo_button)
        self.maze_option_buttons.append(self.main_menu_button)
        self.maze_option_buttons.append(self.save_button)
        self.maze_option_buttons.append(self.view_mazes_button)


    def init_grid(self):

        if self.grid_size == "Small":
            rows, cols, node_size = 15, 25, NODE_SIZE

        elif self.grid_size == "Medium":
            rows, cols, node_size = 21, 35, NODE_SIZE
        else:
            rows, cols, node_size = 25, 51, LARGE_NODE_SIZE

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.grid_state = [[1 for _ in range(cols)] for _ in range(rows)]

        for y in range(rows):
            for x in range(cols):
                self.grid[y][x] = pygame.Rect(
                    GRID_POS_X + x * node_size,
                    GRID_POS_Y + y * node_size,
                    node_size, node_size
                )

        self.start_node = None
        self.end_node = None
        self.undo_stack.clear()

    def draw(self):

        self.screen.fill(WHITE)

        if self.current_screen == 'options':
            self.draw_options_screen()
        elif self.current_screen == 'create_maze_options':
            self.draw_create_maze_options_screen()
            self.draw_grid()

        if self.message:
            message_surface = self.small_font.render(self.message, True, BLACK)
            self.screen.blit(message_surface, (GRID_POS_X, GRID_POS_Y - 30))

        pygame.display.flip()

    def draw_options_screen(self):

        self.create_maze_button.draw_button()

        self.solve_from_image_button.draw_button()

    def draw_create_maze_options_screen(self):

        for button in self.maze_option_buttons:
            button.draw_button()
        self.size_button.draw_button()
        self.slow_button.draw_button()
        self.medium_button.draw_button()
        self.fast_button.draw_button()
        self.save_button.draw_button()
        self.view_mazes_button.draw_button()

    def draw_grid(self):

        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                node_value = self.grid_state[y][x]
                if node_value == 0: #Wall node
                    color = BLACK
                elif node_value == 1: #Empty node
                    color = WHITE
                elif node_value == 2:
                    color = GREEN  #Start node
                elif node_value == 3:
                    color = RED  #End node
                elif node_value == 4:
                    color = YELLOW #Path node
                else:
                    color = WHITE

                pygame.draw.rect(self.screen, color, node)
                pygame.draw.rect(self.screen, GREY, node, 1)

        pygame.display.flip()

    def handle_event(self, event):

        if self.generating_maze:
            return

        if self.current_screen == 'options':
            self.handle_options_event(event)
        elif self.current_screen == 'create_maze_options':
            self.handle_create_maze_options_event(event)

    def handle_options_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.create_maze_button.isOver(pygame.mouse.get_pos()):
                self.current_screen = 'create_maze_options'
                self.message = ''
            elif self.solve_from_image_button.isOver(pygame.mouse.get_pos()):
                self.solve_from_image()
                self.message = ''

    def handle_create_maze_options_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            if self.size_button.isOver(pygame.mouse.get_pos()):
                self.change_maze_size()
                self.message = ''
            elif self.view_mazes_button.isOver(pygame.mouse.get_pos()):
                self.view_mazes()
                self.message = ''

            elif self.slow_button.isOver(pygame.mouse.get_pos()):
                self.animation_speed = SLOW_SPEED
                self.message = "Animation speed set to Slow."
            elif self.medium_button.isOver(pygame.mouse.get_pos()):
                self.animation_speed = MEDIUM_SPEED
                self.message = "Animation speed set to Medium."
            elif self.fast_button.isOver(pygame.mouse.get_pos()):
                self.animation_speed = FAST_SPEED
                self.message = "Animation speed set to Fast."

            for button in self.maze_option_buttons:
                if button.isOver(pygame.mouse.get_pos()):
                    self.selected_button = button.text
                    self.execute_button_functionality(button.text)
                    self.message = ''

            if self.selected_button == "Start/End node":
                self.set_start_end_node(event)
            elif self.selected_button == "Wall node":
                self.set_wall_node(event)
            elif self.selected_button == "Empty node":
                self.set_empty_node(event)
            elif self.selected_button == "Undo":
                self.message, self.grid_state, self.start_node, self.end_node, self.setting_start_node = undo_action(
                    self.undo_stack, self.grid_state, self.start_node, self.end_node, self.setting_start_node
                )
                self.message = ''
            elif self.selected_button == "Main Menu":
                self.current_screen = 'options'
                self.message = ''

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False

        elif event.type == pygame.MOUSEMOTION and self.mouse_down:
            if self.selected_button == "Wall node":
                self.set_wall_node(event)
            elif self.selected_button == "Empty node":
                self.set_empty_node(event)




    def change_maze_size(self):
        size_options = ["Small", "Medium", "Large"]
        current_index = size_options.index(self.grid_size)
        new_index = (current_index + 1) % len(size_options)
        self.grid_size = size_options[new_index]
        print(f"Maze size set to {self.grid_size}.")
        self.init_grid()

    def execute_button_functionality(self, button_text):
        if button_text == "Start/End node":
            self.start_end_node()
        elif button_text == "Wall node":
            self.wall_node()
        elif button_text == "Empty node":
            self.empty_node()
        elif button_text == "Clear maze":
            self.clear_maze_action()
        elif button_text == "Undo":
            self.message, self.grid_state, self.start_node, self.end_node, self.setting_start_node = undo_action(
                self.undo_stack, self.grid_state, self.start_node, self.end_node, self.setting_start_node
            )
        elif button_text == "Main Menu":
            self.current_screen = 'options'
        elif button_text == "Dijkstra":
            self.solve_with_dijkstra()
        elif button_text == "Wilson's":
            self.generate_wilson_maze()
        elif button_text == "Recursive Backtracker":
            self.generate_recursive_backtracker_maze()
        elif button_text == "Bidirectional BFS":
            self.solve_with_bbfs()
        elif button_text == "Kruskal's":
            self.generate_kruskal_maze()
        elif button_text == "Aldous-Broder":
            self.generate_aldous_broder_maze()
        elif button_text == "DFS":
            self.solve_with_dfs()
        elif button_text == "BFS":
            self.solve_with_bfs()
        elif button_text == "GBFS":
            self.solve_with_gbfs()
        elif button_text == "Save":
            self.transition_to_after_save_page()

    def set_start_end_node(self, event):
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                if node.collidepoint(event.pos):
                    if self.setting_start_node:
                        if self.start_node:
                            prev_y, prev_x = self.get_node_position(self.start_node)
                            self.grid_state[prev_y][prev_x] = 1
                        self.start_node = node
                        self.grid_state[y][x] = 2
                        self.undo_stack.append(("start", (y, x)))
                        self.setting_start_node = False
                    else:
                        if self.end_node:
                            prev_y, prev_x = self.get_node_position(self.end_node)
                            self.grid_state[prev_y][prev_x] = 1
                        self.end_node = node
                        self.grid_state[y][x] = 3
                        self.undo_stack.append(("end", (y, x)))
                        self.setting_start_node = True
                    break

    def get_node_position(self, node):
        if node is None:
            return None
        for y, row in enumerate(self.grid):
            for x, grid_node in enumerate(row):
                if grid_node == node:
                    return y, x
        return None

    def validate_start_end_nodes(self):
        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        if start_pos is None or end_pos is None:
            print("Start and/or end node is not set. Please set both nodes before solving.")
            return False
        return True

    def set_wall_node(self, event):
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                if node.collidepoint(event.pos):
                    if self.grid_state[y][x] != 0 and self.grid_state[y][x] != 2 and self.grid_state[y][x] != 3:
                        self.grid_state[y][x] = 0
                        self.undo_stack.append(("wall", (y, x)))
                    break

    def set_empty_node(self, event):
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                if node.collidepoint(event.pos):
                    if self.grid_state[y][x] == 0:
                        self.grid_state[y][x] = 1
                        self.undo_stack.append(("empty", (y, x)))
                    break

    def start_end_node(self):
        print("Click on the grid to set start/end nodes.")

    def wall_node(self):
        self.selected_button = "Wall node"
        print("Click and drag on the grid to set wall nodes.")

    def empty_node(self):
        self.selected_button = "Empty node"
        print("Click and drag on the grid to set empty nodes.")

    def clear_maze_action(self):
        for y in range(len(self.grid_state)):
            for x in range(len(self.grid_state[0])):
                self.grid_state[y][x] = 1

        self.start_node = None
        self.end_node = None
        self.undo_stack.clear()
        self.draw_grid()

    def generate_recursive_backtracker_maze(self):
        self.generating_maze = True
        self.recursive_backtracker_gen = generate_maze(self.grid_state)

    def generate_wilson_maze(self):
        rows = len(self.grid_state)
        cols = len(self.grid_state[0])

        for y in range(rows):
            for x in range(cols):
                self.grid_state[y][x] = 1
        self.start_node = None
        self.end_node = None

        self.wilson_gen = MazeGenerator(cols, rows).generateMaze()
        self.generating_maze = True

    def generate_kruskal_maze(self):
        self.clear_maze_action()

        rows = len(self.grid_state)
        cols = len(self.grid_state[0])

        if rows % 2 == 0:
            rows -= 1
        if cols % 2 == 0:
            cols -= 1

        self.kruskal_gen = KruskalMazeGenerator(cols, rows).generate_maze()
        self.generating_maze = True

    def animate_maze_generation(self):
        if self.generating_maze and self.kruskal_gen:
            try:
                current_maze_state = next(self.kruskal_gen)

                for y in range(len(current_maze_state)):
                    for x in range(len(current_maze_state[0])):
                        self.grid_state[y][x] = current_maze_state[y][x]

                self.draw_grid()
                pygame.display.update()
                pygame.time.delay(self.animation_speed)

            except StopIteration:
                self.generating_maze = False

    def generate_aldous_broder_maze(self):
        self.generating_maze = True
        rows = len(self.grid_state)
        cols = len(self.grid_state[0])

        for y in range(rows):
            for x in range(cols):
                self.grid_state[y][x] = 1

        aldous_broder_gen = AldousBroderMazeGenerator(cols, rows).generate_maze()

        while self.generating_maze:
            try:
                self.grid_state = next(aldous_broder_gen)
                self.draw_grid()
                pygame.display.update()
                pygame.time.delay(self.animation_speed)
            except StopIteration:
                self.generating_maze = False
                print("Maze generated using Aldous-Broder algorithm.")

    def solve_with_dfs(self):
        self.clear_previous_path()
        if not self.validate_start_end_nodes():
            return

        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        dfs_gen = dfs(self.grid_state, start_pos, end_pos)

        path_found = False
        for (y, x), path, is_final in dfs_gen:
            path_found = True

            if is_final:
                color = YELLOW
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 4
            else:
                color = CYAN

            rect = self.grid[y][x]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GREY, rect, 1)

            pygame.display.update()
            pygame.time.delay(self.animation_speed)

        if not path_found:
            print("No path found using DFS.")

        else:
            print("Path found using DFS.")

    def clear_previous_path(self):
        for y in range(len(self.grid_state)):
            for x in range(len(self.grid_state[0])):
                if self.grid_state[y][x] == 4:
                    self.grid_state[y][x] = 1

    def solve_with_bfs(self):
        self.clear_previous_path()
        if not self.validate_start_end_nodes():
            return

        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        bfs_gen = bfs(self.grid_state, start_pos, end_pos)

        path_found = False
        for (y, x), is_final in bfs_gen:
            path_found = True

            if is_final:
                color = YELLOW
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 4
            else:
                color = CYAN

            rect = self.grid[y][x]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GREY, rect, 1)

            pygame.display.update()
            pygame.time.delay(self.animation_speed)

        if not path_found:
            print("No path found using BFS.")

        else:
            print("Path found using BFS.")

    def solve_with_dijkstra(self):
        self.clear_previous_path()
        if not self.validate_start_end_nodes():
            return

        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        dijkstra_gen = dijkstra(self.grid_state, start_pos, end_pos)

        for (y, x), is_final in dijkstra_gen:
            if is_final:
                color = YELLOW
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 4
            else:
                color = CYAN
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 5

            rect = self.grid[y][x]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GREY, rect, 1)

            pygame.display.update()
            pygame.time.delay(self.animation_speed)

        print("Path search with Dijkstra completed.")

    def solve_with_gbfs(self):
        self.clear_previous_path()
        if not self.validate_start_end_nodes():
            return

        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        gbfs_gen = gbfs(self.grid_state, start_pos, end_pos)

        path_found = False
        for (y, x), is_final in gbfs_gen:
            path_found = True

            if is_final:
                color = YELLOW
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 4
            else:
                color = CYAN

            rect = self.grid[y][x]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GREY, rect, 1)

            pygame.display.update()
            pygame.time.delay(self.animation_speed)

        if not path_found:
            print("No path found using GBFS.")

        else:
            print("Path found using GBFS.")

    def solve_with_bbfs(self):
        self.clear_previous_path()
        if not self.validate_start_end_nodes():
            return

        start_pos = self.get_node_position(self.start_node)
        end_pos = self.get_node_position(self.end_node)

        bbfs_gen = bbfs(self.grid_state, start_pos, end_pos)

        path_found = False
        for (y, x), is_final in bbfs_gen:
            path_found = True

            if is_final:
                color = YELLOW
                if self.grid_state[y][x] not in (2, 3):
                    self.grid_state[y][x] = 4
            else:
                color = CYAN

            rect = self.grid[y][x]
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GREY, rect, 1)

            pygame.display.update()
            pygame.time.delay(self.animation_speed)

        if not path_found:
            print("No path found using Bidirectional BFS.")

        else:
            print("Path found using Bidirectional BFS.")

    def transition_to_after_save_page(self):
        after_save_page = AfterSavePage(self.screen, self.font, self.small_font, self, self.db_conn, self.username,self.is_guest)
        after_save_page.start()

    def solve_from_image(self):
        print("solve maze from image")
        solve_maze_from_image()

    def read_maze_from_file(self, filename):
        grid = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    row = list(map(int, line.split()))
                    grid.append(row)
        except FileNotFoundError:
            print(f"{filename} not found")
        except IOError as e:
            print("Error!!!")
        return grid

    def reinitialize_grid(self):
        rows = len(self.grid_state)
        cols = len(self.grid_state[0])
        node_size = NODE_SIZE if rows <= 21 else LARGE_NODE_SIZE

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        for y in range(rows):
            for x in range(cols):
                self.grid[y][x] = pygame.Rect(
                    GRID_POS_X + x * node_size,
                    GRID_POS_Y + y * node_size,
                    node_size, node_size
                )
        self.start_node = None
        self.end_node = None
        self.undo_stack.clear()

    def view_mazes_from_device(self):
        root = tk.Tk()
        root.withdraw()  
        file_path = filedialog.askopenfilename(
            title="Select Maze File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            grid = self.read_maze_from_file(file_path)
            if grid:
                self.grid_state = grid
                self.reinitialize_grid()
                self.draw_grid()
                self.current_screen = 'create_maze_options'

        root.quit()

    def view_mazes(self):
        root = tk.Tk()
        root.withdraw()

        choice = messagebox.askquestion(
            "View Mazes",
            "Do you want to view mazes stored on your device (Yes) or in the database (No)?",
            icon="question"
        )

        if choice == 'yes':
            self.view_mazes_from_device()
        else:
            if self.db_conn == None and self.username == None:
                print("You need to be logged in to use this feature.")
            else:
                self.view_mazes_from_database()

        root.quit()

    def view_mazes_from_database(self):
        if self.is_guest:
            print("Guest users have no mazes saved online.")
            return None
        else:
            try:
                cursor = self.db_conn.cursor()
                query = "SELECT maze_name, maze_text FROM maze_table WHERE username = %s"
                cursor.execute(query, (self.username,))
                mazes = cursor.fetchall()

                if mazes:
                    maze_names = [maze[0] for maze in mazes]
                    root = tk.Tk()
                    root.withdraw()

                    selected_maze_name = simpledialog.askstring(
                        "Select Maze",
                        f"Choose a maze to view:\n{', '.join(maze_names)}",
                    )

                    if selected_maze_name:
                        selected_maze = next((maze for maze in mazes if maze[0] == selected_maze_name), None)
                        if selected_maze:
                            maze_text = selected_maze[1]
                            grid = [list(map(int, row.split())) for row in maze_text.splitlines()]


                            self.generating_maze = False
                            self.kruskal_gen = None
                            self.recursive_backtracker_gen = None

                            self.grid_state = grid
                            self.reinitialize_grid()
                            self.draw_grid()
                            self.current_screen = 'create_maze_options'

                    root.quit()
                else:
                    print("No mazes found in the database.")

            except mysql.connector.Error as err:
                print(f"Error fetching mazes: {err}")


    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.draw()
            if self.generating_maze:
                self.animate_maze_generation()

            if self.wilson_gen:
                try:
                    maze_step = next(self.wilson_gen)

                    if len(maze_step) != len(self.grid_state) or len(maze_step[0]) != len(self.grid_state[0]):
                        print("Generated maze size ≠ grid state dimensions.")
                        print(f"Generated maze dimensions: {len(maze_step)}x{len(maze_step[0])}")
                        print(f"Grid state dimensions: {len(self.grid_state)}x{len(self.grid_state[0])}")
                        raise ValueError("Generated maze size ≠ grid state dimensions.")

                    for y, row in enumerate(maze_step):
                        for x, cell in enumerate(row):
                            self.grid_state[y][x] = cell
                    self.draw_grid()
                    pygame.display.update()
                    pygame.time.delay(self.animation_speed)
                except StopIteration:
                    self.wilson_gen = None
                    self.generating_maze = False
                    print("Maze generated using Wilson's algorithm.")

            if self.recursive_backtracker_gen:
                try:
                    self.grid_state = next(self.recursive_backtracker_gen)
                    self.draw_grid()
                    pygame.display.update()
                    pygame.time.delay(self.animation_speed)
                except StopIteration:
                    self.recursive_backtracker_gen = None
                    self.generating_maze = False
                    print("Maze generated using Recursive Backtracker algorithm.")

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1400, 720))
    pygame.display.set_caption("Post Login Page")
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    post_login_page = PostLoginPage(screen, font, small_font)
    post_login_page.start()
