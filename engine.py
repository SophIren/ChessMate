import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self, groups, size):
        super().__init__(*groups)

        image = pygame.image.load('data/board.png')
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()

    def set_pieces(self):
        tiles_num = 8
        border_size = 2
        piece_size = (self.rect.width - border_size * tiles_num) / tiles_num
        arg_size = (round(piece_size), round(piece_size))

        for x in range(tiles_num):
            x_pos = round(piece_size * x + border_size * (x + 1))
            Pawn((all_sprites, pieces), arg_size,
                 (x_pos, round(piece_size + border_size)),
                 'black', 'pawn.png')
            Pawn((all_sprites, pieces), arg_size,
                 (x_pos, round((tiles_num - 2) * piece_size + border_size * (tiles_num - 1))),
                 'white', 'pawn.png')

        for x in range(tiles_num):
            x_pos = round(piece_size * x + border_size * (x + 1))
            PIECES[x]['obj']((all_sprites, pieces), arg_size,
                             (x_pos, border_size),
                             'black', PIECES[x]['pic'])
            PIECES[x]['obj']((all_sprites, pieces), arg_size,
                             (x_pos, round((tiles_num - 1) * piece_size + border_size * tiles_num)),
                             'white', PIECES[x]['pic'])


class Piece(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, color, im_name):
        super().__init__(*groups)

        self.color = color
        image = pygame.image.load('data/{}/{}'.format(color, im_name))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(pos, (self.image.get_width(), self.image.get_height()))


class Pawn(Piece):
    pass


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):
    pass


pygame.init()

win_size = (658, 658)
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('ChessMate')

all_sprites = pygame.sprite.Group()
pieces = pygame.sprite.Group()

PIECES = [{'obj': Rook, 'pic': 'rook.png'}, {'obj': Knight, 'pic': 'knight.png'}, {'obj': Bishop, 'pic': 'bishop.png'},
          {'obj': Queen, 'pic': 'queen.png'}, {'obj': King, 'pic': 'king.png'},
          {'obj': Bishop, 'pic': 'bishop.png'}, {'obj': Knight, 'pic': 'knight.png'}, {'obj': Rook, 'pic': 'rook.png'}]

board = Board((all_sprites,), win_size)
board.set_pieces()

running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        print(event.pos)

    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
