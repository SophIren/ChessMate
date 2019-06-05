import pygame


class Board:
    def __init__(self, size, tiles_num, border_size=0):
        self.tiles_num = tiles_num
        self.border_size = border_size
        self.piece_size = (size - border_size * (tiles_num + 1)) / tiles_num
        self.clicked_piece = None
        self.turn = None

        tile_size = round(self.piece_size + 2 * border_size)
        for i in range(tiles_num):
            if i % 2 == 0:
                im_name = 'white_tile.png'
            else:
                im_name = 'black_tile.png'
            for j in range(tiles_num):
                Tile((all_sprites, tiles), (tile_size, tile_size), (self.border_size, self.border_size),
                     (round(i * (self.piece_size + self.border_size)), round(j * (self.piece_size + self.border_size))),
                     (i, j), im_name)
                if im_name == 'white_tile.png':
                    im_name = 'black_tile.png'
                else:
                    im_name = 'white_tile.png'

        self.mark = Mark((all_sprites,), (round(self.piece_size), round(self.piece_size)))

    def set_pieces(self):
        self.turn = 'white'

        arg_size = (round(self.piece_size), round(self.piece_size))
        groups = (all_sprites, pieces)

        y_pos_black = round(self.piece_size + self.border_size * 2)
        y_pos_white = round((self.tiles_num - 2) * self.piece_size + self.border_size * (self.tiles_num - 1))
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            get_tile_by_coord((x_pos, y_pos_black)).taken_by = Pawn(groups, arg_size,
                                                                    (x_pos, y_pos_black),
                                                                    (x, 1), 'black')
            get_tile_by_coord((x_pos, y_pos_white)).taken_by = Pawn(groups, arg_size,
                                                                    (x_pos, y_pos_white),
                                                                    (x, self.tiles_num - 2), 'white')

        y_pos_black = self.border_size
        y_pos_white = round((self.tiles_num - 1) * self.piece_size + self.border_size * self.tiles_num)
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            get_tile_by_coord((x_pos, y_pos_black)).taken_by = PIECES_OBJ[x](groups, arg_size,
                                                                             (x_pos, y_pos_black),
                                                                             (x, 0), 'black')
            get_tile_by_coord((x_pos, y_pos_white)).taken_by = PIECES_OBJ[x](groups, arg_size,
                                                                             (x_pos, y_pos_white),
                                                                             (x, self.tiles_num - 1), 'white')

    def reverse(self):
        for piece in pieces:
            piece_x, piece_y = piece.piece_pos
            piece_y = abs(piece_y - self.tiles_num) - 1

            piece.piece_pos = (piece_x, piece_y)
            piece.rect.y = round(piece_y * self.piece_size + self.border_size * (piece_y + 1))

        for tile in tiles:
            tile_x, tile_y = tile.tile_pos
            tile_y = abs(tile_y - self.tiles_num) - 1

            tile.tile_pos = (tile_x, tile_y)
            tile.rect.y = round(tile_y * (self.piece_size + self.border_size))

    def handle_click(self, coord):
        if self.clicked_piece is not None:

            if self.clicked_piece.color == self.turn:
                tile = get_tile_by_coord(coord)

                if self.clicked_piece.can_move(tile):
                    self.clicked_piece.move_on(tile)
                    self.change_color()
                    self.reverse()
                    return

                elif self.clicked_piece.can_take(tile):
                    self.clicked_piece.take_on(tile)
                    self.change_color()
                    self.reverse()
                    return

            piece = get_piece_by_coord(coord)
            if piece is not None:
                self.clicked_piece = piece
                self.mark.rect = self.clicked_piece.rect

        else:
            piece = get_piece_by_coord(coord)
            if piece is not None:
                self.clicked_piece = get_piece_by_coord(coord)
                self.mark.rect = self.clicked_piece.rect

    def change_color(self):
        if self.turn == 'black':
            self.turn = 'white'
        else:
            self.turn = 'black'


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, tile_size, border_size, coord_pos, tile_pos, im_name, taken_by=None):
        super().__init__(*groups)

        self.tile_pos = tile_pos
        self.border_size = border_size
        self.taken_by = taken_by

        image = pygame.image.load('data/{}'.format(im_name))
        self.image = pygame.transform.scale(image, tile_size)
        self.rect = pygame.Rect(coord_pos, tile_size)


class Mark(pygame.sprite.Sprite):
    def __init__(self, groups, size):
        super().__init__(*groups)

        image = pygame.image.load('data/mark.png')
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect((-size[0], -size[1]), size)


class Piece(pygame.sprite.Sprite):
    def __init__(self, groups, size, coord_pos, piece_pos, color, im_name):
        super().__init__(*groups)

        self.color = color
        self.piece_pos = piece_pos

        image = pygame.image.load('data/{}/{}'.format(color, im_name))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(coord_pos, size)

    def move_on(self, tile):
        get_tile_by_pos(self.piece_pos).taken = None
        tile.taken_by = self

        border_x, border_y = tile.border_size
        self.rect.x = tile.rect.x + border_x
        self.rect.y = tile.rect.y + border_y

        self.piece_pos = tile.tile_pos

    def take_on(self, tile):
        taken_piece = get_piece_by_pos(tile.tile_pos)
        for group in taken_piece.groups():
            group.remove(taken_piece)

        self.move_on(tile)


class Pawn(Piece):
    def __init__(self, groups, size, coord_pos, pawn_pos, color):
        self.first_move = True
        super().__init__(groups, size, coord_pos, pawn_pos, color, 'pawn.png')

    def can_move(self, tile):
        x_tile, y_tile = tile.tile_pos
        x_piece, y_piece = self.piece_pos
        if tile.taken_by is None:
            if x_tile == x_piece and y_piece - y_tile == 1:
                return True
            elif x_tile == x_piece and y_piece - y_tile == 2 and \
                    self.first_move and get_piece_by_pos((x_piece, y_piece - 1)) is None:
                self.first_move = False
                return True

        return False

    def can_take(self, tile):
        x_piece, y_piece = self.piece_pos
        x_tile, y_tile = tile.tile_pos

        if ((x_piece - 1) == x_tile or (x_piece + 1) == x_tile) \
                and (y_piece - 1 == y_tile or y_piece + 1 == y_tile) \
                and tile.taken_by is not None:
            return True

        return False


class Rook(Piece):
    def __init__(self, groups, size, coord_pos, rook_pos, color):
        super().__init__(groups, size, coord_pos, rook_pos, color, 'rook.png')

    def can_move(self, tile):
        pass

    def can_take(self, tile):
        pass


class Knight(Piece):
    def __init__(self, groups, size, coord_pos, knight_pos, color):
        super().__init__(groups, size, coord_pos, knight_pos, color, 'knight.png')

    def can_move(self, tile):
        pass

    def can_take(self, tile):
        pass


class Bishop(Piece):
    def __init__(self, groups, size, coord_pos, bishop_pos, color):
        super().__init__(groups, size, coord_pos, bishop_pos, color, 'bishop.png')

    def can_move(self, tile):
        pass

    def can_take(self, tile):
        pass


class Queen(Piece):
    def __init__(self, groups, size, coord_pos, queen_pos, color):
        super().__init__(groups, size, coord_pos, queen_pos, color, 'queen.png')

    def can_move(self, tile):
        pass

    def can_take(self, tile):
        pass


class King(Piece):
    def __init__(self, groups, size, coord_pos, king_pos, color):
        super().__init__(groups, size, coord_pos, king_pos, color, 'king.png')

    def can_move(self, tile):
        pass

    def can_take(self, tile):
        pass


def get_piece_by_pos(pos):
    for piece in pieces:
        if piece.piece_pos == pos:
            return piece


def get_piece_by_coord(coord):
    for piece in pieces:
        if piece.rect.collidepoint(coord):
            return piece


def get_tile_by_coord(coord):
    for tile in tiles:
        if tile.rect.collidepoint(coord):
            return tile


def get_tile_by_pos(pos):
    for tile in tiles:
        if tile.tile_pos == pos:
            return tile


pygame.init()

win_size = (658, 658)
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('ChessMate')

all_sprites = pygame.sprite.Group()
pieces = pygame.sprite.Group()
tiles = pygame.sprite.Group()

PIECES_OBJ = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

board = Board(win_size[0], 8, 2)
board.set_pieces()

running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        board.handle_click(event.pos)

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
