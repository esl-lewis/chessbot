import numpy as np
# use conda py_game1 env

i_axis = np.array(range(8))
j_axis = np.array(range(8))

i_axis = i_axis.reshape([8,1])
j_axis = j_axis.reshape([1,8])

i_coords, j_coords = np.meshgrid(i_axis, j_axis, sparse=False, indexing='ij')

coordinate_grid = np.array([i_coords, j_coords])

# ^^ redundant but maybe useful for visualising?



"""White pieces start at i matrix 1st row, i.e. initial pieces occupy 0 and 1
 Black at i matrix 7th row, initial pieces at 6 and 7"""

# weird rules to add later
# castling
# en passant
# promoting

class ChessBoard:
    def __init__(self,name):
        self.name = name
        
        # ^^ change this from list to dict
        # squares have a name, coord and maybe a piece
        #self.pieces = {}
        # all pieces have a square? maybe don't need this
        board_coords = []
        squares_list = []
        for i in range(0,8):
            for j in range(0,8):
                board_coords.append((i,j))
                squares_list.append(Square(str([i,j]),[i,j]))

        squares_and_coords = dict(zip(board_coords, squares_list))
        self.squares = squares_and_coords
    """
    def add_square(self, name, square_coord):
        result = Square(name, square_coord)
        self.squares.append(result)
        return result
    """

    # move all pieces to where they want to be
    #def move_piece()
        # somehow involves both adding and removing piece fncs from square

    #def instantiate/create all pieces in correct positions

    # user interface here? pick which move?

class Square:
    def __init__(self, name, square_coord):
        # maybe can squish name and square coord together
        self.name = name
        self.square_coord = square_coord # perhaps should inherit this from ChessBoard class
        self.occupant = {}

    def add_piece(self, piece):
        piece.square_coord = np.asarray(self.square_coord) # piece needs to know where it is, or is it self.square_coord????
        # cast to array so that we can do maths
        piece.square = self
        self.occupant[piece.name] = piece
        self.occupant['colour'] = piece.colour

    def remove_piece(self,piece):
        del self.occupant[piece.name]  
        del self.occupant['colour']  
    
class Piece:
    def __init__(self, name, colour, square=None, square_coord=None, firstMove=True, moveset = []):
        self.name = name
        self.square = square # square is square object, square_coord is its coordinate location
        self.square_coord = square_coord
        self.colour = colour
        self.firstMove = True   
        self.moveset = []
    

    def check_opposite(self, target_piece):
        if self.colour == target_piece.colour:
            return False
        elif self.colour != target_piece.colour:
            return True # maybe swap these T/F values if needed

    # of available piece moves, check which are legal 
    def check_legal(self):
        #self.moveset is a list of array values 
        # test bejesus out of this

        # make list of all illegal moves 
        coords_to_remove = []
        # check for out of bounds (set max and min coord values)
        for coords in self.moveset:
            if np.any((coords[0].item() < 0) or (coords[1].item() < 0) or (coords[0].item() > 7) or (coords[1].item() > 7)):
                #print(np.any((coords[0].item() < 0) or (coords[1].item() < 0) or (coords[0].item() > 7) or (coords[0].item() > 7)))
                coords_to_remove.append(coords)



    
        # remove all invalid coords 
        # have to do by index as have list of numpy arrays (mixed data type, can't use set or list comps)
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


    # this ^^ applies to all pieces, maybe do the rest inside some of the piece classes?
  
    # check black or white for taking rules 
    # if pawns, check if taking or moving   

    # check for obstructing piece, check for pieces colour

    # by taking min value in all directions?

    # this will be ballache with knights

    # maybe redundant as this can be handled by squares class

    # check if leaving king in check/king moving into check

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
        self.moveset = [] # this line redundant?
    # pawns have unusual behaviour in that take and step vectors will be different, distinguish these?
    # and black/white pawns behave differently - move in opposite directions
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

    # need to stop pawns from trying to step diagonally, need to be able to 'see' other pieces on squares. 

class Rook(Piece):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        # do we need both square and square coord above?
        #super().__init__(name, square_coord, colour) 
        self.name = name
        self.colour = colour
        self.moveset = moveset
    
    def retrieve_moves(self):
        for step in range(1,7):
            self.moveset.append(self.square_coord + [step,0])
            self.moveset.append(self.square_coord + [0,step])
            self.moveset.append(self.square_coord + [-step,0])
            self.moveset.append(self.square_coord + [0,-step])
        #print('rook moves generated:',self.moveset)
        return(self.moveset)

class Bishop(Piece):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        #super().__init__(name, square_coord, colour) 
        self.name = name
        self.colour = colour
        self.moveset = moveset

    def retrieve_moves(self):
        for step in range(1,7):
            self.moveset.append(self.square_coord + [step,step])
            self.moveset.append(self.square_coord + [-step,-step])
            self.moveset.append(self.square_coord + [-step,step])
            self.moveset.append(self.square_coord + [step,-step])
        print('bishop moves generated:',self.moveset)
        return(self.moveset)

class Knight(Piece):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        #super().__init__(name, square_coord, colour) 
        self.name = name
        self.colour = colour
        self.moveset = moveset

    def retrieve_moves(self):
        self.moveset.append(self.square_coord + [2,1])
        self.moveset.append(self.square_coord + [1,2])
        self.moveset.append(self.square_coord + [-1,2])
        self.moveset.append(self.square_coord + [-2,1])
        self.moveset.append(self.square_coord + [-2,-1])
        self.moveset.append(self.square_coord + [-1,-2])
        self.moveset.append(self.square_coord + [1,-2])
        self.moveset.append(self.square_coord + [2,-1])
        print('knight moves generated:',self.moveset)
        return(self.moveset)

class King(Piece):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        #super().__init__(name, square_coord, colour) 
        self.name = name
        self.colour = colour
        self.moveset = moveset
    def retrieve_moves(self):
        self.moveset.append(self.square_coord + [1,1])
        self.moveset.append(self.square_coord + [-1,-1])
        self.moveset.append(self.square_coord + [-1,1])
        self.moveset.append(self.square_coord + [1,-1])
        self.moveset.append(self.square_coord + [1,0])
        self.moveset.append(self.square_coord + [0,1])
        self.moveset.append(self.square_coord + [-1,0])
        self.moveset.append(self.square_coord + [0,-1])
        print('king moves generated:',self.moveset)
        return(self.moveset)
    

class Queen(Piece):
    def __init__(self, name, colour, square=None, moveset=[], square_coord=None):
        #super().__init__(name, square_coord, colour) 
        self.name = name
        self.colour = colour
        self.moveset = moveset
    def retrieve_moves(self):
        for step in range(1,7):
            self.moveset.append(self.square_coord + [step,step])
            self.moveset.append(self.square_coord + [-step,-step])
            self.moveset.append(self.square_coord + [-step,step])
            self.moveset.append(self.square_coord + [step,-step])
            self.moveset.append(self.square_coord + [step,0])
            self.moveset.append(self.square_coord + [0,step])
            self.moveset.append(self.square_coord + [-step,0])
            self.moveset.append(self.square_coord + [0,-step])
        print('queen moves generated:',self.moveset)
        return(self.moveset)




#print(coordinate_grid)

#print(coordinate_grid)
#print(coordinate_grid[:, 0, 2])

# add squares

# board_coords = []
# squares_list = []
# for i in range(0,8):
#     for j in range(0,8):
#         board_coords.append((i,j))
#         squares_list.append(Square(str([i,j]),[i,j]))

# squares_and_coords = dict(zip(board_coords, squares_list))

#print(board_coords)
#print(squares_list)

# do this inside chessboard class??


chessboard = ChessBoard('My chessboard')
#print(chessboard.squares[(0,1)])

"""
for i in range(0,8):
    #print('i:',i)
    for j in range(0,8):
        #print(j)
        #print('square names',coordinate_grid[:,i,j])
        chessboard.add_square(str(coordinate_grid[:,i,j]),coordinate_grid[:,i,j])
"""


#for square in range(len(chessboard.squares)):
    #print(square)
    #print(chessboard.squares[square].name)
    # here 
    #print(chessboard.squares[square].square_coord)
    #print(chessboard.squares[square].square_coord + [1,2])
# initialise piece and square separately, see if they talk to each other 



"""
print('square test')
sq1 = Square('top left',np.array([0,0]))
sq2 = Square('top right',np.array([0,1]))
sq3 = Square('bottom left',np.array([1,0]))
sq4 = Square('bottom right',np.array([1,1]))
"""

# take the tests out and put in separate file

"""
# pawn/piece update test
pawn1 = Pawn('pawnpawn', 'white')
print('~~~~~~~~~~~~~~~')

print('pawn start')

(chessboard.squares[(0,4)]).add_piece(pawn1)

print(pawn1.square_coord)
#print(chessboard.squares[(0,4)].occupant)

print('legal moves')
pawn1.retrieve_moves()
pawn1.check_legal()
print(pawn1.moveset)

# here need to cast np move to tuple
chosen_move = pawn1.moveset[0]
print('chosen move ',chosen_move, type(chosen_move))
# cast 
chosen_move = tuple(chosen_move)

print('chosen move ',chosen_move, type(chosen_move))


pawn1.update_position(chessboard.squares[chosen_move])

#pawn1.update_position(chessboard.squares[(0,5)])

print('should be empty',chessboard.squares[(0,4)].occupant)

print('should have a pawn',chessboard.squares[chosen_move].occupant)

print('should be new square',pawn1.square_coord)

print('should have only one object',pawn1.square)

pawn1.retrieve_moves()
pawn1.check_legal()

print(pawn1.firstMove)

pawn1.update_position(chessboard.squares[6])

pawn1.retrieve_moves()
pawn1.check_legal()

print(pawn1.firstMove)
"""


# rook test
"""
rook1 = Rook('rook', 'white')
print('~~~~~~~~~~~~~~~')
print(rook1.name)

(chessboard.squares[(0,5)]).add_piece(rook1)

print(rook1.square_coord)

#rook1.retrieve_moves()
#print('legal rook moves?')
#rook1.check_legal()
"""

"""
# bishop test

bishop1 = Bishop('bish','black')

(chessboard.squares[3]).add_piece(bishop1)
print(bishop1.square_coord)
bishop1.retrieve_moves()
bishop1.check_legal()
"""

"""
# queen test

queen1 = Queen('liz','white')

(chessboard.squares[30]).add_piece(queen1)
print(queen1.square_coord)
queen1.retrieve_moves()
queen1.check_legal()
"""



# knight test
"""
knight1 = Knight('gawain','black')

(chessboard.squares[30]).add_piece(knight1)
print(knight1.square_coord)
knight1.retrieve_moves()
knight1.check_legal()
"""


# knight test
"""
knight1 = Knight('gawain','black')

(chessboard.squares[30]).add_piece(knight1)
print(knight1.square_coord)
knight1.retrieve_moves()
knight1.check_legal()
"""

# king test
"""
king1 = King('freddie','white')

(chessboard.squares[30]).add_piece(king1)
print(king1.square_coord)
king1.retrieve_moves()
king1.check_legal()
king1.update_position(chessboard.squares[6])
"""

#print(chessboard.squares[square].square_coord)

# write some tests, can check if generating the correct number of legal moves
# check if pieces are moving correctly


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