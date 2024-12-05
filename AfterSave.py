import pygame
import mysql.connector
from buttonClass import Buttons
from coloursss import *
import os


# all necessary libraries imported

class AfterSavePage:
    def __init__(self, screen, font, small_font, post_login_page, db_conn, username, is_guest=False):
        # Initialize the AfterSavePage with necessary attributes and dependencies
        self.screen = screen  # Pygame screen for rendering
        self.font = font  # Font for large text
        self.small_font = small_font  # Font for smaller messages
        self.post_login_page = post_login_page  # Reference to the parent page
        self.message = ''  # Status message to display to the user
        self.db_conn = db_conn  # Database connection for online saves
        self.username = username  # Current user's username
        self.is_guest = is_guest  # Flag to check if the user is a guest

        # Initialize buttons for the page
        self.back_button = Buttons(self.screen, GREY, 500, 400, 200, 60, text='Back')
        self.save_device_button = Buttons(self.screen, GREY, 500, 200, 200, 60, text='Save on device')
        self.save_online_button = Buttons(self.screen, GREY, 500, 300, 200, 60, text='Save online')

    # Draws the page elements on the screen
    def draw(self):
        self.screen.fill(WHITE)  # Clear the screen with a white background

        # Draw buttons
        self.save_device_button.draw_button()
        self.save_online_button.draw_button()
        self.back_button.draw_button()

        # Display the status message if it exists
        if self.message:
            message_surface = self.small_font.render(self.message, True, BLACK)
            self.screen.blit(message_surface, (500, 500))

        pygame.display.flip()  # Update the display

    # Handles user interactions with buttons
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # Check if a button was clicked
            if self.back_button.isOver(pygame.mouse.get_pos()):
                return 'back'  # User clicked "Back"
            elif self.save_device_button.isOver(pygame.mouse.get_pos()):
                return 'save_on_device'  # User clicked "Save on Device"
            elif self.save_online_button.isOver(pygame.mouse.get_pos()):
                if self.is_guest:  # Check if the user is a guest
                    print("Guest users cannot save maze online.")
                    self.message = "Guest users cannot save online."
                    return None
                return 'save_online'  # User clicked "Save Online"
        return None  # No action taken

    # Saves the maze to the database
    def save_maze_to_db(self):
        maze_name = input("Enter a name for your maze: ")  # Prompt the user for a maze name
        grid_state = self.post_login_page.grid_state  # Get the current grid state from the parent page
        # Convert the grid to a string format for storage
        maze_text = '\n'.join([' '.join(map(str, row)) for row in grid_state])

        try:
            # Insert the maze into the database
            cursor = self.db_conn.cursor()
            query = "INSERT INTO maze_table (username, maze_name, maze_text) VALUES (%s, %s, %s)"
            cursor.execute(query, (self.username, maze_name, maze_text))
            self.db_conn.commit()
            cursor.close()
            self.message = f"Maze '{maze_name}' saved to database."
            print(f"Maze '{maze_name}' saved to database.")
        except mysql.connector.Error as err:
            # Handle database errors
            print(f"Error saving maze to database: {err}")
            self.message = f"Error saving maze to database: {err}"

    # Saves the maze to a text file on the user's device
    def save_maze_to_file(self):
        filename = input("Enter a filename to save the maze: ") + ".txt"  # Prompt for a filename
        if os.path.exists(filename):  # Check if the file already exists
            print("Name taken. Choose another name for your maze file.")
        else:
            try:
                # Write the maze grid to the file
                with open(filename, 'w') as f:
                    for row in self.post_login_page.grid_state:
                        f.write(' '.join(str(cell) for cell in row) + '\n')
                print(f"{filename} saved")
            except IOError as e:
                # Handle file write errors
                print(f"Error saving to file: {e}")

    # Starts the AfterSavePage and handles its main loop
    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle the quit event
                    running = False

                # Handle button clicks
                action = self.handle_event(event)
                if action == 'back':
                    self.post_login_page.start()  # Go back to the parent page
                    return
                elif action == 'save_on_device':
                    self.save_maze_to_file()  # Save the maze to the device
                elif action == 'save_online':
                    if self.db_conn ==None or self.username == None:  # Ensure user is logged in
                        print("You need to be logged in to use this feature.")
                    else:
                        self.save_maze_to_db()  # Save the maze online

            self.draw()  # Redraw the page elements
            clock.tick(30)  # Limit the frame rate to 30 FPS

        pygame.quit()  # Quit Pygame when exiting the loop
