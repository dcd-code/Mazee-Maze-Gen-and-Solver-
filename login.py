import pygame
import mysql.connector
import hashlib
import re

from afterLogin import PostLoginPage
from buttonClass import Buttons
from coloursss import *

pygame.init()

WIDTH, HEIGHT = 1400, 730
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mazee')

FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

class LoginPage:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.active_input = None
        self.message = ''
        self.current_screen = 'login'
        self.is_guest = False


        self.username_box = pygame.Rect(550, 200, 300, 50)
        self.password_box = pygame.Rect(550, 300, 300, 50)
        self.login_button = Buttons(screen, GREEN, 450, 400, 200, 60, text='Login')
        self.signup_button = Buttons(screen, RED, 700, 400, 200, 60, text='Sign Up')
        self.guest_button = Buttons(screen, GREY, 575, 500, 200, 60, text="Guest")


        try:
            self.conn = mysql.connector.connect(
                host= address,
                port="3306",
                user="remoteUser",
                password="yourPassword",
                database="mazeandusertables"
            )
            print("DB connected")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None

    def draw(self):
        screen.fill(WHITE)
        if self.current_screen == 'login':
            self.draw_login_screen()
        if self.message:
            message_surface = SMALL_FONT.render(self.message, True, BLACK)
            screen.blit(message_surface, (550, 600))

    def draw_login_screen(self):
        # Draw input boxes and labels
        username_label = FONT.render("Username:", True, BLACK)
        password_label = FONT.render("Password:", True, BLACK)
        pygame.draw.rect(screen, GREY, self.username_box, 2)
        pygame.draw.rect(screen, GREY, self.password_box, 2)
        username_text = FONT.render(self.username, True, BLACK)
        password_text = FONT.render('*' * len(self.password), True, BLACK)

        screen.blit(username_label, (400, 210))
        screen.blit(password_label, (400, 310))
        screen.blit(username_text, (560, 210))
        screen.blit(password_text, (560, 310))


        self.login_button.draw_button()
        self.signup_button.draw_button()
        self.guest_button.draw_button()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_box.collidepoint(event.pos):
                self.active_input = 'username'
            elif self.password_box.collidepoint(event.pos):
                self.active_input = 'password'
            elif self.login_button.isOver(pygame.mouse.get_pos()):
                self.login()
            elif self.signup_button.isOver(pygame.mouse.get_pos()):
                self.signUp()
            elif self.guest_button.isOver(pygame.mouse.get_pos()):
                self.guest_login()  # Handle guest login
            else:
                self.active_input = None

        if event.type == pygame.KEYDOWN:
            if self.active_input == 'username':
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_input == 'password':
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode

    def login(self):
        if not self.conn:
            self.message = "No database connection."
            return

        if self.is_guest:
            self.message = "Guest users cannot access database features."
            return

        username = self.username
        password = self.password

        try:
            cursor = self.conn.cursor()
            query = "SELECT password FROM user_table WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]
                if self.verify_pwd(password, stored_password):
                    print(f"Welcome, {username}!")
                    self.username = username
                    self.transition_to_post_login()
                else:
                    self.message = "Invalid username or password."
            else:
                self.message = "User does not exist."

            cursor.close()

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            self.message = "Database error occurred."

    def guest_login(self):
        self.username = "Guest"
        self.password = "GuestPwd"
        self.is_guest = True
        print("Logged in as guest.")
        print("Since you have logged in as guest, you wont be able to access features like save maze online and view mazes stored online.")
        self.transition_to_post_login()

    def signUp(self):
        if not self.conn:
            self.message = "No database connection."
            return

        if self.is_guest:
            self.message = "Guest users cannot sign up."
            return

        username = self.username
        password = self.password

        if len(username) < 3:
            self.message = "Username must be at least 3 characters long."
            return

        if not re.match(r"^(?=.*[A-Z]).{7,}$", password):
            self.message = "Password must be 7+ characters and 1 uppercase."
            return

        hashed_password = self.hashPwd(password)

        try:
            cursor = self.conn.cursor()
            insert_query = "INSERT INTO user_table (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, hashed_password))
            self.conn.commit()
            self.message = f"User {username} created."
            cursor.close()

        except mysql.connector.Error as err:
            if err.errno == 1062:
                self.message = "Username already taken."
            else:
                print(f"Database error: {err}")
                self.message = "Database error occurred."

    def hashPwd(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verify_pwd(self, plain_password, hashed_password):
        return self.hashPwd(plain_password) == hashed_password

    def transition_to_post_login(self):
        post_login = PostLoginPage(screen, FONT, SMALL_FONT, self.conn, self.username, self.is_guest)
        post_login.start()

    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)

            self.draw()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    address = str(input("Enter the IP address of the host (Leave blank if you don't know): "))
    if address == "":
        address = "123456"
    app = LoginPage()
    app.start()

