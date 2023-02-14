import pygame
pygame.init()

main_font = pygame.font.SysFont("cambria", 50)

class Button:
    def __init__(self, image, x, y, text, screen):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text
        self.text = main_font.render(self.text_input, True, (0,0,0))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.screen = screen

    def update(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            return True
        
    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, (0,255,0))
        else:
            self.text = main_font.render(self.text_input, True, (255,0,0))
            
