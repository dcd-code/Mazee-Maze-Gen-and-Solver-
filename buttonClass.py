import pygame
class Buttons():
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
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('Arial', 28)
            text = font.render(self.text, 1, (0, 0, 0))
            self.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.clicked:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 3)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def click(self):
        self.clicked = True

    def reset(self):
        self.clicked = False
