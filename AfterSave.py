import pygame
import mysql.connector
from buttonClass import Buttons
from coloursss import *
import os


class AfterSavePage:
    def __init__(self, screen, font, small_font, post_login_page, db_conn, username, is_guest=False):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.post_login_page = post_login_page
        self.message = ''
        self.db_conn = db_conn
        self.username = username
        self.is_guest = is_guest

        self.back_button = Buttons(self.screen, GREY, 500, 400, 200, 60, text='Back')
        self.save_device_button = Buttons(self.screen, GREY, 500, 200, 200, 60, text='Save on device')
        self.save_online_button = Buttons(self.screen, GREY, 500, 300, 200, 60, text='Save online')

    def draw(self):
        self.screen.fill(WHITE)

        self.save_device_button.draw_button()
        self.save_online_button.draw_button()
        self.back_button.draw_button()

        if self.message:
            message_surface = self.small_font.render(self.message, True, BLACK)
            self.screen.blit(message_surface, (500, 500))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.isOver(pygame.mouse.get_pos()):
                return 'back'
            elif self.save_device_button.isOver(pygame.mouse.get_pos()):
                return 'save_on_device'
            elif self.save_online_button.isOver(pygame.mouse.get_pos()):
                if self.is_guest:  # Corrected guest check
                    print("Guest users cannot save maze online.")
                    self.message = "Guest users cannot save online."
                    return None
                return 'save_online'
        return None

    def save_maze_to_db(self):
        maze_name = input("Enter a name for your maze: ")
        grid_state = self.post_login_page.grid_state
        maze_text = '\n'.join([' '.join(map(str, row)) for row in grid_state])

        try:
            cursor = self.db_conn.cursor()
            query = "INSERT INTO maze_table (username, maze_name, maze_text) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.username, maze_name, maze_text))
            self.db_conn.commit()
            cursor.close()
            self.message = f"Maze '{maze_name}' saved to database."
            print(f"Maze '{maze_name}' saved to database.")
        except mysql.connector.Error as err:
            print(f"Error saving maze to database: {err}")
            self.message = f"Error saving maze to database: {err}"


    def save_maze_to_file(self):
        filename = input("Enter a filename to save the maze: ") + ".txt"
        if os.path.exists(filename):
            print("Name taken. Choose another name for your maze file.")
        else:
            try:
                with open(filename, 'w') as f:
                    for row in self.post_login_page.grid_state:
                        f.write(' '.join(str(cell) for cell in row) + '\n')
                print(f"{filename} saved")

            except IOError as e:
                print(f"Error saving to file: {e}")

    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                action = self.handle_event(event)
                if action == 'back':
                    self.post_login_page.start()
                    return
                elif action == 'save_on_device':
                    self.save_maze_to_file()
                elif action == 'save_online':
                    if self.db_conn ==None and self.username == None:
                        print("You need to be logged in to use this feature.")#
                    else:
                        self.save_maze_to_db()

            self.draw()
            clock.tick(30)

        pygame.quit()
