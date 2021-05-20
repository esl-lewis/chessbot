import numpy as np
# use conda py_game1 env

i_axis = np.array(range(8))
j_axis = np.array(range(8))

i_axis = i_axis.reshape([8,1])
j_axis = j_axis.reshape([1,8])

i_coords, j_coords = np.meshgrid(i_axis, j_axis, sparse=False, indexing='ij')

coordinate_grid = np.array([i_coords, j_coords])

"""White pieces start at i matrix 1st row, i.e. initial pieces occupy 0 and 1
 Black at i matrix 7th row, initial pieces at 6 and 7"""

# weird rules to add later
# castling
# en passant
# promoting

class ChessBoard:
    def __init__(self,name):
        self.name = name
        self.squares = []
        self.pieces = []

    def add_square(self, name, square_coord):
        result = Square(name, square_coord)
        self.squares.append(result)
        return result

    # move all pieces to where they want to be
    #def move_piece()
        # somehow involves both adding and removing piece fncs from square

    #def instantiate/create all pieces in correct positions

    # user interface here? pick which move?

class Square:
    def __init__(self, name, square_coord):
        self.name = name
        self.square_coord = square_coord
        self.occupant = {}

    def add_piece(self, piece):
        piece.square_coord = self.square_coord # piece needs to know where it is, or is it self.square_coord????
        piece.square = self
        self.occupant[piece.name] = piece
        self.occupant['colour'] = piece.colour

    def remove_piece(self,piece):
        del self.occupant[piece.name]  
        del self.occupant['colour']  
    
class Piece:
    def __init__(self, name, colour, square=None, square_coord=None, firstMove=True, moveset = []):
        self.name = name
        self.square = square
        self.square_coord = square_coord
        self.colour = colour
        self.firstMove = True   
        self.moveset = []
    
    # of available piece moves, check which are legal 
    def check_legal(self):
        #self.moveset is a list of array values 
        # test this

        coords_to_remove = []
        # check for out of bounds (set max and min coord values)
        for coords in self.moveset:
            if np.any((coords[0].item() < 0) or (coords[1].item() < 0) or (coords[0].item() > 7) or (coords[0].item() > 7)):
                #print(np.any((coords[0].item() < 0) or (coords[1].item() < 0) or (coords[0].item() > 7) or (coords[0].item() > 7)))
                coords_to_remove.append(coords)
  
        # remove all invalid coords, have to do by index as have list of numpy arrays (mixed data type, can't use set or list comps)
        coord_index_to_remove = []
        for x in range(len(self.moveset)):
            for y in range(len(coords_to_remove)):
                if (self.moveset[x]==coords_to_remove[y]).all():
                    #print('remove index',x)
                    coord_index_to_remove.append(x)
        for i in sorted(coord_index_to_remove, reverse=True):
            del self.moveset[i]
        print("the set of legal squares is: ",self.moveset)
        return(self.moveset)

    # check black or white for taking rules 
    # if pawns, check if taking or moving

    # check for obstructing piece
    # by taking min value in all directions?
    # this will be different with knights

    # maybe redundant as this can be handled by squares class

    def update_position(self, new_position):
        # remove from old square
        self.square.remove_piece(self)
        # add to new square 
        new_position.add_piece(self)

        print(self.name, " to ", new_position.square_coord)
        self.firstMove = False
        self.moveset = []
        # this line to wipe available moves to empty set 

    #  need to update this to only use legal moves
 

class Pawn(Piece):
    def __init__(self, name, colour, square=None, square_coord=None):
        super().__init__(name, colour, square=None, square_coord=None, firstMove=True, moveset = []) 
        self.moveset = []

    def two_step_pawn(self):
        if self.colour == 'white':
            new_position = self.square_coord + [2,0]
        elif self.colour == 'black':
            new_position = self.square_coord - [2,0]
        return(new_position)

    def one_step_pawn(self):
        if self.colour == 'white':
            new_position = self.square_coord + [1,0]
        elif self.colour == 'black':
            new_position = self.square_coord - [1,0]
        return(new_position)

    def diag_take_pawn(self):
        if self.colour == 'white':
            new_position_1 = self.square_coord + [1, 1]
            new_position_2 = self.square_coord + [1, -1]
        if self.colour == 'black':
            new_position_1 = self.square_coord + [-1, 1]
            new_position_2 = self.square_coord + [-1, -1]
        return(new_position_1,new_position_2)

    def retrieve_moves(self):
        if self.firstMove == True:
            new_position_1 = self.two_step_pawn()
            self.moveset.append(new_position_1)
        new_position_2 = self.one_step_pawn()
        self.moveset.append(new_position_2)
        new_position_3, new_position_4 = self.diag_take_pawn()
        self.moveset.append(new_position_3)
        self.moveset.append(new_position_4)
        print("the set of possible new squares is: ",self.moveset)
        return(self.moveset)

class Rook:
    def __init__(self, name, moveset, square_coord, colour):
        super().__init__(name, square_coord, colour) 
        self.moveset = moveset

class Bishop:
    def __init__(self, name, moveset, square_coord, colour):
        super().__init__(name, square_coord, colour) 
        self.moveset = moveset

class Knight:
    def __init__(self, name, moveset, square_coord, colour):
        super().__init__(name, square_coord, colour) 
        self.moveset = moveset

class King:
    def __init__(self, name, moveset, square_coord, colour):
        super().__init__(name, square_coord, colour) 
        self.moveset = moveset

class Queen:
    def __init__(self, name, moveset, square_coord, colour):
        super().__init__(name, square_coord, colour) 
        self.moveset = moveset


chessboard = ChessBoard('My chessboard')

#print(coordinate_grid)
#print(coordinate_grid[:, 0, 2])

# add squares
for i in range(0,8):
    #print('i:',i)
    for j in range(0,8):
        #print(j)
        #print('square names',coordinate_grid[:,i,j])
        chessboard.add_square(str(coordinate_grid[:,i,j]),coordinate_grid[:,i,j])


# initialise piece and square separately, see if they recognise each other 



"""
print('square test')
sq1 = Square('top left',np.array([0,0]))
sq2 = Square('top right',np.array([0,1]))
sq3 = Square('bottom left',np.array([1,0]))
sq4 = Square('bottom right',np.array([1,1]))
"""

pawn1 = Pawn('pawnpawn', 'white')



print('~~~~~~~~~~~~~~~')

print('pawn start')

(chessboard.squares[0]).add_piece(pawn1)

print(pawn1.square_coord)

pawn1.retrieve_moves()
pawn1.check_legal()

pawn1.update_position(chessboard.squares[3])

pawn1.retrieve_moves()
pawn1.check_legal()

#sq2.add_piece(pawn1)
#print(pawn1.square_coord)
#pawn1.update_position(sq3)
#print(pawn1.square_coord)




#sq1.remove_piece()
#print(sq1.piece_colour())




"""
pawn1.update_position(np.array([4,3]))
print(pawn1.square_coord)
pawn1.retrieve_moves()
pawn1.check_legal()
"""


"""
#for pawn_number in range(0,8):
    #print("I am pawn number ",pawn_number)

rook = Piece('rook', [1,1], 'white')
knight = Piece('knight', [1,0], 'black')

# initial setup
for piece in [pawn, rook, knight]:
    #print(piece.name)
    #print(piece.square_coord)
    chessboard.add_piece(piece.name, piece.square_coord, piece.colour)
"""



# where to put taking?

# add pieces

# piece

# functions to move/get taken

# set up empty board, then populate with starting pieces
