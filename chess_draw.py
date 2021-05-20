import pygame
import sys

import chess_logic
from chess_logic import Piece, Rook, ChessBoard, Square


chessboard = ChessBoard('My chessboard')
rook1 = Rook('rook', 'white')
print('~~~~~~~~~~~~~~~')
print(rook1.name)
(chessboard.squares[(0,5)]).add_piece(rook1)
print(rook1.square_coord)

# setup the game objects here? ^^ outside loop?
black = (0,0,0)
white = (255,255,255)

# create the display surface object 
# of specific dimension..e(X, Y). 
display_surface = pygame.display.set_mode((10, 10 )) 
  
# set the pygame window name 
pygame.display.set_caption('Image') 
  
# create a surface object, image is drawn on it. 
image = pygame.image.load(r'C:\Users\user\Pictures\geek.jpg') 

# new logic here to allow us to draw pieces, maybe combine with actual piece class. not sure
class renderRook(Rook):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        super().__init__(name, colour, square=None, square_coord=None, firstMove=True, moveset = []) 




def main():
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surface_sz = 480   # Desired physical surface size, in pixels.

    # Create surface of (width, height), and its window.
    main_surface = pygame.display.set_mode((surface_sz, surface_sz))
    pygame.display.set_caption("Chess")
 
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop

        # Update your game objects and data structures here...

        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        main_surface.fill((0, 200, 255))

        # draw the chessboard
        
        
        # loop over all the squares and draw them in?


        # loop over all the pieces and draw them in ?
        
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

    pygame.quit()     # Once we leave the loop, close the window.

main()