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
            Pawn(groups, arg_size,
                 (x_pos, y_pos_black),
                 (x, 1), 'black')
            get_tile((x_pos, y_pos_black)).taken = True
            Pawn(groups, arg_size,
                 (x_pos, y_pos_white),
                 (x, self.tiles_num - 2), 'white')
            get_tile((x_pos, y_pos_white)).taken = True

        y_pos_black = self.border_size
        y_pos_white = round((self.tiles_num - 1) * self.piece_size + self.border_size * self.tiles_num)
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            PIECES_OBJ[x](groups, arg_size,
                          (x_pos, y_pos_black),
                          (x, 0), 'black')
            get_tile((x_pos, y_pos_black)).taken = True
            PIECES_OBJ[x](groups, arg_size,
                          (x_pos, y_pos_white),
                          (x, self.tiles_num - 1), 'white')
            get_tile((x_pos, y_pos_white)).taken = True

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

    def handle_click(self, pos):
        if self.clicked_piece is not None:

            if self.clicked_piece.color == self.turn:
                tile = get_tile(pos)

                if self.clicked_piece.can_move(tile):
                    self.clicked_piece.move_on(tile)
                    self.change_color()
                    self.reverse()
                    return

                elif self.clicked_piece.can_take(tile):
                    return

            piece = get_piece(pos)
            if piece is not None:
                self.clicked_piece = piece
                self.mark.rect = self.clicked_piece.rect

        else:
            piece = get_piece(pos)
            if piece is not None:
                self.clicked_piece = get_piece(pos)
                self.mark.rect = self.clicked_piece.rect

    def change_color(self):
        if self.turn == 'black':
            self.turn = 'white'
        else:
            self.turn = 'black'


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, tile_size, border_size, coord_pos, tile_pos, im_name, taken=False):
        super().__init__(*groups)

        self.tile_pos = tile_pos
        self.border_size = border_size
        self.taken = taken

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
        tile.taken = True

        border_x, border_y = tile.border_size
        self.rect.x = tile.rect.x + border_x
        self.rect.y = tile.rect.y + border_y

        self.piece_pos = tile.tile_pos

    def take_on(self, tile):
        pass


class Pawn(Piece):
    def __init__(self, groups, size, coord_pos, pawn_pos, color):
        self.first_move = True
        super().__init__(groups, size, coord_pos, pawn_pos, color, 'pawn.png')

    def can_move(self, tile):
        x_tile, y_tile = tile.tile_pos
        x_piece, y_piece = self.piece_pos

        if not tile.taken:
            if x_tile == x_piece and y_piece - y_tile == 1:
                return True
            elif x_tile == x_piece and y_piece - y_tile == 2 and self.first_move:
                self.first_move = False
                return True

        return False

    def can_take(self, tile):
        pass


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


def get_piece(pos):
    for piece in pieces:
        if piece.rect.collidepoint(pos):
            return piece


def get_tile(pos):
    for tile in tiles:
        if tile.rect.collidepoint(pos):
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
