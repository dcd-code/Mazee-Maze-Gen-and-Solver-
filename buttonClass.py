import pygame

# A class to create and manage interactive buttons
class Buttons:
    last_clicked_button = None  # Class-level variable to track the last clicked button

    def __init__(self, screen, colour, x, y, width, height, text=''):
        self.screen = screen
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.clicked = False

    def draw_button(self, outline=None):
        # Draw the button on the screen
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # Draw the button itself
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Arial', 28)
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)
            ))

        # Draw a red outline if this button is clicked
        if self.clicked:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def click(self):
        # Mark the button as clicked and reset the last clicked button if needed
        if Buttons.last_clicked_button and Buttons.last_clicked_button != self:
            Buttons.last_clicked_button.reset()

        self.clicked = True
        Buttons.last_clicked_button = self  # Update the last clicked button

    def reset(self):
        self.clicked = False
