import pygame
import config as cfg
          
            
class Tile:
    def __init__(self, x, y, size=None, letter="", colour=None):
        # x and y are coordinates of the top-left point of the pygame Rect
        self.x = x
        self.y = y
        self.letter = letter
        self.colour = colour
        
        if size is None:
            size = cfg.TILESIZE
        self.width = size
        self.height = size
        
        self.font_size = int(60 * (size / 100))
        self.create_font()
        
        
    def create_font(self):
        font = pygame.font.SysFont("Consolas", self.font_size)
        self.rendered_letter = font.render(self.letter, True, cfg.WHITE)
        # Get the size of the rendered letter in px
        self.font_width, self.font_height = font.size(self.letter)
        
        
    def draw(self, screen):
        if self.colour is None:
            # The tile entry hasn't been checked yet so we don't need a fill colour
            pygame.draw.rect(screen, cfg.WHITE, (self.x, self.y, self.width, self.height), 2)
        else:
            # We need to fill the rectangle with the appropriate colour
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
            
            
        if self.letter != "":
            # We want to draw the letter on the tile, if it exists
            # Get the coordinates for the centre of the letter
            self.font_x = self.x + (self.width / 2) - (self.font_width / 2)
            self.font_y = self.y + (self.height / 2) - (self.font_height / 2)
            # To handle the animation with the font height changing, we scale the letter
            letter = pygame.transform.scale(self.rendered_letter, (self.font_width, self.font_height))
            screen.blit(letter, (self.font_x, self.font_y))
            

class UIElement:
    ''' Fading text for messages shown on game board '''
    def __init__(self, x, y, text, text_colour, font_size=40):
        self.x = x
        self.y = y
        self.text = text
        self.text_colour = text_colour
        self.font_size = font_size
        self.alpha = 0.0
        self.create_font()
        
        
    def create_font(self):
        font = pygame.font.SysFont("Consolas", self.font_size)
        self.original_surface = font.render(self.text, True, self.text_colour)
        self.text_surface = self.original_surface.copy()
        # This surface is used to adjust the alpha of self.text_surface
        self.alpha_surface = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)
    
    
    def draw(self, screen):
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.alpha))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.text_surface, (self.x, self.y))
        
    
    def fade(self, fade_dir):
        ''' Adjust the self.alpha value to fade the text out '''
        if fade_dir == "out":
            self.alpha = max(self.alpha - 10, 0)
        elif fade_dir == "in":
            self.alpha = min(self.alpha + 10, 255)
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.alpha))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        
    def get_text_width(self):
        return self.text_surface.get_width()
    
    
    def set_pos(self, new_x_pos, new_y_pos):
        self.x = new_x_pos
        self.y = new_y_pos