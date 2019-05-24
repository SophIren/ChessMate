import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self, groups, size):
        super().__init__(*groups)

        image = pygame.image.load('data/board.png')
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()

    def set_pieces(self):
        tiles_num = 8
        board_size = self.rect.width
        piece_size = round(board_size / tiles_num)
        k = board_size / tiles_num % 1

        for x in range(tiles_num):
            Pawn((all_sprites, pieces), (piece_size, piece_size),
                 ((piece_size + 2) * x - round(k * x * 2), piece_size), 'black')

        for x in range(tiles_num):
            Pawn((all_sprites, pieces), (piece_size, piece_size),
                 ((piece_size + 2) * x - round(k * x * 2), (tiles_num - 2) * piece_size + 5), 'white')


class Pawn(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, color):
        super().__init__(*groups)

        self.color = color
        image = pygame.image.load('data/{}/pawn.png'.format(color))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(pos, size)


pygame.init()

win_size = (651, 651)
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('ChessMate')

all_sprites = pygame.sprite.Group()
pieces = pygame.sprite.Group()

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
