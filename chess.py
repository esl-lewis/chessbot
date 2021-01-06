import numpy as np

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

    def add_square(self, name, coord):
        result = Square(name, coord)
        self.squares.append(result)
        return result

    def add_piece(self, name, square, colour):
        self.pieces.append(Piece(name, square, colour))

    def remove_piece(self, name, square, colour):
        self.pieces.remove(Piece(name, square, colour))

    #def move_piece()
        # somehow involves both adding and removing piece fncs from up there

class Square:
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.occupancy = []

class Piece:
    def __init__(self, name, square, colour, firstMove=True, moveset = []):
        self.name = name
        self.square = square
        self.colour = colour
        self.firstMove = True   
        self.moveset = []
    
    # assume all moves are legal for a second...

    def check_legal(self):
        #self.moveset is a list of array values 
         
        # check for out of bounds (set max and min coord values)
        for coords in self.moveset:
            """
            print(coords)
            print(coords[0])
            print(type(coords[0]))
            print(coords[0].item())
            print(type(coords[0].item()))
            print("<===========>")
            """

            if (coords[0].item() < 0) or (coords[1].item() < 0) or (coords[0].item() > 7) or (coords[0].item() > 7):
                print("?")
                #self.moveset.remove(coords)
                # I think don't change something you are actively iterating on
                print("remove",coords)
                print(self.moveset)
        print("the set of legal squares is: ",self.moveset)


    # show all legal moves 
    # check legality here  
    #  check black or white for taking rules 
    # if pawns, check if taking or moving
    # check for obstructing piece

    def update_position(self, new_position):
        self.square = new_position
        print(self.name, " to ", new_position)
        self.firstMove = False
        self.moveset = []
        # this to wipe available moves to empty set 
    #  need to update this to only use legal moves
 

class Pawn(Piece):
    def __init__(self, name, square, colour):
        super().__init__(name, square, colour, firstMove=True, moveset = []) 
        self.moveset = []

    def two_step_pawn(self):
        if self.colour == 'white':
            new_position = self.square + [2,0]
        elif self.colour == 'black':
            new_position = self.square - [2,0]
        return(new_position)

    def one_step_pawn(self):
        if self.colour == 'white':
            new_position = self.square + [1,0]
        elif self.colour == 'black':
            new_position = self.square - [1,0]
        return(new_position)

    def diag_take_pawn(self):
        if self.colour == 'white':
            new_position_1 = self.square + [1, 1]
            new_position_2 = self.square + [1, -1]
        if self.colour == 'black':
            new_position_1 = self.square + [-1, 1]
            new_position_2 = self.square + [-1, -1]
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
    def __init__(self, name, moveset, square, colour):
        super().__init__(name, square, colour) 
        self.moveset = moveset

class Bishop:
    def __init__(self, name, moveset, square, colour):
        super().__init__(name, square, colour) 
        self.moveset = moveset

class Knight:
    def __init__(self, name, moveset, square, colour):
        super().__init__(name, square, colour) 
        self.moveset = moveset

class King:
    def __init__(self, name, moveset, square, colour):
        super().__init__(name, square, colour) 
        self.moveset = moveset

class Queen:
    def __init__(self, name, moveset, square, colour):
        super().__init__(name, square, colour) 
        self.moveset = moveset


chessboard = ChessBoard('My chessboard')

print(coordinate_grid)
#print(coordinate_grid[:, 0, 2])

# add squares
for i in range(0,8):
    #print('i:',i)
    for j in range(0,8):
        #print(j)
        #print(coordinate_grid[:,i,j])
        chessboard.add_square(str(coordinate_grid[:,i,j]),coordinate_grid[:,i,j])
#print(chessboard.squares[0].name)

# add a pawn, see if it can move
pawn1 = Pawn('pawnpawn', np.array([0,4]), 'black')


# pawn test 

print(pawn1.square)
pawn1.retrieve_moves()
pawn1.check_legal()

#pawn1.update_position(np.array([4,3]))
#print(pawn1.square)
#pawn1.retrieve_moves()



"""
#for pawn_number in range(0,8):
    #print("I am pawn number ",pawn_number)

rook = Piece('rook', [1,1], 'white')
knight = Piece('knight', [1,0], 'black')

# initial setup
for piece in [pawn, rook, knight]:
    #print(piece.name)
    #print(piece.square)
    chessboard.add_piece(piece.name, piece.square, piece.colour)
"""


# where to put taking?

# add pieces

# piece

# functions to move/get taken

# set up empty board, then populate with starting pieces
