import pygame


class Board:
    def __init__(self, size, tiles_num, border_size=0):
        self.tiles_num = tiles_num
        self.border_size = border_size
        self.piece_size = (size - border_size * (tiles_num + 1)) / tiles_num
        self.clicked_piece = None

        tile_size = round(self.piece_size + 2 * border_size)
        for i in range(tiles_num):
            if i % 2 == 0:
                im_name = 'white_tile.png'
            else:
                im_name = 'black_tile.png'
            for j in range(tiles_num):
                Tile((all_sprites, tiles),
                     (tile_size, tile_size),
                     (round(i * (self.piece_size + self.border_size)), round(j * (self.piece_size + self.border_size))),
                     im_name)
                if im_name == 'white_tile.png':
                    im_name = 'black_tile.png'
                else:
                    im_name = 'white_tile.png'

    def set_pieces(self):
        arg_size = (round(self.piece_size), round(self.piece_size))

        y_pos_black = round(self.piece_size + self.border_size)
        y_pos_white = round((self.tiles_num - 2) * self.piece_size + self.border_size * (self.tiles_num - 1))
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            Pawn((all_sprites, pieces), arg_size,
                 (x_pos, y_pos_black),
                 'black')
            Pawn((all_sprites, pieces), arg_size,
                 (x_pos, y_pos_white),
                 'white')

        y_pos_black = self.border_size
        y_pos_white = round((self.tiles_num - 1) * self.piece_size + self.border_size * self.tiles_num)
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            PIECES_OBJ[x]((all_sprites, pieces), arg_size,
                          (x_pos, y_pos_black),
                          'black')
            PIECES_OBJ[x]((all_sprites, pieces), arg_size,
                          (x_pos, y_pos_white),
                          'white')

    def handle_click(self, pos):
        if self.clicked_piece is None:
            for piece in pieces:
                if piece.rect.collidepoint(pos):
                    self.clicked_piece = piece
                    break
        elif self.clicked_piece.can_move(pos):
            self.clicked_piece.move_on(pos)


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, im_name):
        super().__init__(*groups)

        image = pygame.image.load('data/{}'.format(im_name))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(pos, size)


class Piece(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, color, im_name):
        super().__init__(*groups)

        self.color = color
        image = pygame.image.load('data/{}/{}'.format(color, im_name))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(pos, size)


class Pawn(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'pawn.png')

    def can_move(self, pos):
        pass

    def move_on(self, pos):
        pass


class Rook(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'rook.png')


class Knight(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'knight.png')


class Bishop(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'bishop.png')


class Queen(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'queen.png')


class King(Piece):
    def __init__(self, groups, size, pos, color):
        super().__init__(groups, size, pos, color, 'king.png')


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
