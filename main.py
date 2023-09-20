import pygame
import sys
import random
import config as cfg
import sprites


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption(cfg.TITLE)
        self.clock = pygame.time.Clock()
        self.playing = False
        self.flipping = True
        self.not_enough_letters = False
        self.invalid_word = False
        self.word_list = self.load_game_word_list()
        self.valid_word_list = self.load_valid_word_list()
        
        
    def load_game_word_list(self):
        with open("data/wordle_word_list.txt", "r") as a_file:
            return a_file.read().splitlines()
        
        
    def load_valid_word_list(self):
        with open("data/five_letter_words.txt", "r") as a_file:
            return a_file.read().splitlines()
    
    
    def new(self):
        ''' Reset and prepare things for a new game '''
        self.word = random.choice(self.word_list).upper()
        self.text = ""
        self.current_row = 0
        # List to store Tile objects for user to enter guesses
        self.tiles = []
        # Dictionary to store Tile objects making up the QWERTY keyboard
        self.keyboard_tiles = {}
        self.create_tiles()
        self.flipping = True
        self.not_enough_letters = False
        self.invalid_word = False
        # Initialise and position all text elements
        self.build_text_elements()
        self.centre_text_elements()
        # Timer for animations
        self.timer = 0
        
        
    def build_text_elements(self):
        '''
        Construct all of the text elements that may be required during a game,
        and store them in a list. Their positions are hard-coded and could be
        stored in config.py instead.
        '''
        # Invalid word messages
        self.not_enough_letters_text = sprites.UIElement(100, 70, "Not Enough Letters", cfg.WHITE)
        self.invalid_word_text = sprites.UIElement(20, 70, "Invalid Word", cfg.WHITE)
        # End screen messages
        self.end_screen_fail_text = sprites.UIElement(100, 50, text=f"The Word Was {self.word}", text_colour=cfg.WHITE)
        self.end_screen_win_text = sprites.UIElement(127, 50, text="You Guessed Right!", text_colour=cfg.WHITE)
        # End screen play again message
        self.play_again_text = sprites.UIElement(85, 100, text="Press Enter to Play Again", text_colour=cfg.WHITE, font_size=30)
        
        # Create list of text elements so we can centre them all later
        self.text_elements = [self.not_enough_letters_text,
                              self.invalid_word_text,
                              self.end_screen_fail_text,
                              self.end_screen_win_text,
                              self.play_again_text]
    
    
    def centre_text_elements(self):
        ''' Centre all the text elements the game contains '''
        for el in self.text_elements:
            text_surface_width = el.get_text_width()
            # Calculate the new x position to centre the text
            x = int((cfg.WIDTH - text_surface_width) / 2)
            y = el.y
            el.set_pos(x, y)
    
    
    def create_tiles(self):
        ''' Create tiles for user letters and the QWERTY keyboard representation '''
        # Create rows of tiles for user entry
        for row in range(cfg.NUM_ROWS):
            self.tiles.append([])
            for col in range(cfg.NUM_COLS):
                self.tiles[row].append(sprites.Tile(x=(col * (cfg.TILESIZE + cfg.GAPSIZE)) + cfg.MARGIN_X,
                                                    y=(row * (cfg.TILESIZE + cfg.GAPSIZE)) + cfg.MARGIN_Y,
                                                    size=cfg.TILESIZE))
    
        # Create QWERTY keyboard tiles
        keyboard_letters = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
                            ["z", "x", "c", "v", "b", "n", "m"]]
    
        for i, row in enumerate(keyboard_letters):
            for j, letter in enumerate(row):
                self.keyboard_tiles[letter.upper()] = sprites.Tile(x=(j * (cfg.K_TILESIZE + cfg.K_GAPSIZE)) + cfg.K_MARGIN_X[i],
                                                                    y=(i * (cfg.K_TILESIZE + cfg.K_GAPSIZE)) + cfg.K_Y_OFFSET,
                                                                    size=cfg.K_TILESIZE,
                                                                    letter=letter.upper(),
                                                                    colour=cfg.K_LIGHTGREY)


    def run(self):
        self.playing=True
        while self.playing:
            self.clock.tick(cfg.FPS)
            self.events()
            self.update()
            self.draw()
            
    
    def update(self):
        self.add_letter()


    def add_letter(self):
        # Clear the letters from the tiles in the current row
        for tile in self.tiles[self.current_row]:
            tile.letter = ""
        # Add the letters that have been typed into the current row
        for i, letter in enumerate(self.text):
            self.tiles[self.current_row][i].letter = letter
            self.tiles[self.current_row][i].create_font()


    def draw_input_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)
                        

    def draw_keyboard_tiles(self, surface=None):
        if surface is None:
            surface = self.screen
        for tile in list(self.keyboard_tiles.values()):
            tile.draw(surface)


    def draw(self):
        self.screen.fill(cfg.BGCOLOUR)
        
        # Check for invalid entries and draw error text to screen
        self.check_for_not_enough_letters()
        self.check_for_invalid_word()
            
        self.not_enough_letters_text.draw(self.screen)
        self.invalid_word_text.draw(self.screen)
        
        # Draw tiles and keyboard tiles
        self.draw_input_tiles()
        self.draw_keyboard_tiles()
        pygame.display.flip()
        
        
    def check_for_invalid_word(self):
        '''
        Check for invalid word entry and handle error text fade. This could
        probably be refactored, along with check_for_not_enough_letters, to
        adhere to DRY.
        '''
        if self.invalid_word:
            self.timer += 1
            self.invalid_word_text.fade(fade_dir="in")
            if self.timer > (cfg.FPS * cfg.ERROR_TEXT_FPS_DUR_COEF):
                self.invalid_word = False
                self.timer = 0
        else:
            self.invalid_word_text.fade(fade_dir="out")
    
    
    def check_for_not_enough_letters(self):
        ''' Check length of entered word and handle error text fade '''
        if self.not_enough_letters:
            self.timer += 1
            self.not_enough_letters_text.fade(fade_dir="in")
            if self.timer > (cfg.FPS * cfg.ERROR_TEXT_FPS_DUR_COEF):
                self.not_enough_letters = False
                self.timer = 0
        else:
            self.not_enough_letters_text.fade(fade_dir="out")
    
    
    def box_animation(self):
        ''' Increase then decrease tile size when entering a letter in a tile '''
        for tile in self.tiles[self.current_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()
                # Do the increase, then the decrease
                for start, end, step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2*step):
                        self.screen.blit(screen_copy, (0, 0))
                        # Adjust the position and size of the tile
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        # Create a surface to act as the background for the tile
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(cfg.BGCOLOUR)
                        # Blit this tile background surface to the screen
                        self.screen.blit(surface, (tile.x, tile.y))
                        # Draw the tile to the screen to give the border
                        tile.draw(self.screen)
                        pygame.display.flip()
                        self.clock.tick(cfg.FPS)
                    self.add_letter()
                # We only want to animate one tile, so break after animation complete
                break
                        
        
    def reveal_animation(self, tile, colour):
        '''
        When user checks a valid word, flip tiles and update colours.
        These animation parameters could be stored in config.py instead.
        '''
        screen_copy = self.screen.copy()
        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(cfg.BGCOLOUR)
            screen_copy.blit(surface, (tile.x, tile.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flipping:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.colour = colour
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
                
            if tile.font_height == 0:
                self.flipping = False
                
            tile.draw(self.screen)
            pygame.display.update()
            self.clock.tick(cfg.FPS)
            
            if tile.font_height == tile.font_size:
                self.flipping = True
                break
        
        
    def row_animation(self):
        ''' Animation to shake the row if user's entry is invalid '''
        # Get the x position of a tile to use later as a "rest" position
        start_pos = self.tiles[0][0].x
        # Define maximum displacement and the move step between draw updates
        move_amount = cfg.ROW_MOVE_AMOUNT
        move_step = cfg.ROW_MOVE_STEP
        # Make a copy of self.screen on which to place non-animated elements
        screen_copy = self.screen.copy()
        screen_copy.fill(cfg.BGCOLOUR)
        
        # Draw the tiles onto screen_copy for all rows except the current row
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.current_row]:
                    tile.draw(screen_copy)
        
        # Draw the keyboard tiles onto the screen_copy Surface        
        self.draw_keyboard_tiles(surface=screen_copy)
                    
        while True:
            # Move tiles to the right
            while self.tiles[self.current_row][0].x < (start_pos + move_amount):
                # Blit the screen_copy Surface onto self.screen at position (0, 0)
                self.screen.blit(screen_copy, (0, 0))
                # Move the tiles and blit to screen
                for tile in self.tiles[self.current_row]:
                    tile.x += move_step
                    tile.draw(self.screen)
                self.clock.tick(cfg.FPS)
                # Update the display
                pygame.display.flip()
            
            # Move tiles to the left
            while self.tiles[self.current_row][0].x > (start_pos - move_amount):
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.current_row]:
                    tile.x -= move_step
                    tile.draw(self.screen)
                self.clock.tick(cfg.FPS)
                pygame.display.flip()
                
            # Reduce the tile's maximum displacement from its rest position at each iteration
            move_amount -= 2
            if move_amount < 0:
                break
    
    
    def check_letters(self):
        ''' Check if the input letters are in the secret word '''
        true_letters = [l for l in self.word]
        for i, user_letter in enumerate(self.text):
            # Assume the user's letter is not in the word and apply a default colour
            colour = cfg.LIGHTGREY
            self.keyboard_tiles[user_letter].colour = colour
            for j, true_letter in enumerate(true_letters):
                # User letter is in the word - colour based on position correctness
                if user_letter == true_letter:
                    colour = cfg.YELLOW
                    if i == j:
                        colour = cfg.GREEN
                    # Remove the current letter to prevent duplicate/mixed feedback
                    true_letters[j] = ""
                    self.keyboard_tiles[user_letter].colour = colour
                    break
                
            # Do the card flipping animation. Takes letter and colour
            self.reveal_animation(self.tiles[self.current_row][i], colour)
            
          
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # If the key is an alpha, add it to the word
                if len(self.text) < 5 and event.unicode.isalpha():
                    self.text += event.unicode.upper()
                    self.box_animation()
                    
                # Delete last entered letter from current word/row
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                
                # Check entered word when return key is pressed
                elif event.key == pygame.K_RETURN:
                    if len(self.text) == 5:   
                        # Check for invalid word entries
                        if self.text.lower() not in self.valid_word_list:
                            # Remove the invalid word
                            self.text = ""
                            # Row animation for invalid word
                            self.invalid_word = True
                            self.row_animation()
                            
                        else:
                            # Check if letters are in words and assign colours
                            self.check_letters()
                            # Check for termination conditions (correct guess or player has no more turns)
                            if self.text == self.word or self.current_row + 1 == cfg.NUM_ROWS:
                                # Player loses - show failure message
                                if self.text != self.word:
                                    self.end_screen_text = self.end_screen_fail_text
                                # Player wins - show victory message
                                else:
                                    self.end_screen_text = self.end_screen_win_text
                                
                                # Reset the game
                                self.playing = False
                                self.end_screen()
                                break
                            
                            # Termination conditions are not met. Continue to next row
                            self.current_row += 1
                            self.text = ""
                        
                    # If we don't have enough letters entered, show a message
                    else:
                        # Row animation for not enough letters
                        self.not_enough_letters = True
                        self.row_animation()
                        
       
    def end_screen(self):
        ''' At the end of the game, display a screen and wait for user input '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    
            # Draw the screen to be shown while waiting for user input
            self.screen.fill(cfg.BGCOLOUR)
            # Draw tiles
            self.draw_input_tiles()
            self.draw_keyboard_tiles()
            # Draw text
            self.end_screen_text.fade(fade_dir="in")
            self.end_screen_text.draw(self.screen)
            self.play_again_text.fade(fade_dir="in")
            self.play_again_text.draw(self.screen)
            # Update whole display
            pygame.display.flip()
                


game = Game()
while True:
    game.new()
    game.run()