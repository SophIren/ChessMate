import pygame


class Board:
    def __init__(self, size, tiles_num,
                 white_tile_im_name='white_tile.png', black_tile_im_name='black_tile.png', border_size=0):
        self.tiles_num = tiles_num
        self.border_size = border_size
        self.piece_size = (size - self.border_size * (self.tiles_num + 1)) / self.tiles_num
        self.clicked_piece = None
        self.turn = None

        group_names = ['all_sprites', 'pieces', 'white_pieces', 'black_pieces', 'kings', 'tiles',
                       'pawns', 'rooks', 'knights', 'bishops', 'queens', 'kings']
        for group_name in group_names:
            exec("self.{} = pygame.sprite.Group()".format(group_name))

        self.piece_color_rel = {
            'white': self.white_pieces,
            'black': self.black_pieces
        }
        self.piece_class_rel = {
            Pawn: self.pawns,
            Rook: self.rooks,
            Knight: self.knights,
            Bishop: self.bishops,
            Queen: self.queens,
            King: self.kings
        }

        tile_size = round(self.piece_size + 2 * self.border_size)
        for i in range(self.tiles_num):
            if i % 2 == 0:
                im_name = white_tile_im_name
            else:
                im_name = black_tile_im_name

            for j in range(self.tiles_num):
                x_coord = round(i * (self.piece_size + self.border_size))
                y_coord = round(j * (self.piece_size + self.border_size))
                Tile((self.all_sprites, self.tiles), self, (tile_size, tile_size),
                     self.border_size, (x_coord, y_coord), (i, j), im_name)

                if im_name == black_tile_im_name:
                    im_name = white_tile_im_name
                else:
                    im_name = black_tile_im_name

        self.mark = Mark((self.all_sprites,), (round(self.piece_size), round(self.piece_size)))

    def set_pieces(self, pieces_obj):
        self.turn = 'white'

        arg_size = (round(self.piece_size), round(self.piece_size))

        white_groups = [self.all_sprites, self.pieces, self.white_pieces]
        black_groups = [self.all_sprites, self.pieces, self.black_pieces]
        pawn_group = [self.piece_class_rel[pieces_obj[0][0]]]

        y_coord_white_pawn = round((self.tiles_num - 2) * self.piece_size + self.border_size * (self.tiles_num - 1))
        y_coord_white_piece = round((self.tiles_num - 1) * self.piece_size + self.border_size * self.tiles_num)
        y_coord_black_pawn = round(self.piece_size + self.border_size * 2)
        y_coord_black_piece = self.border_size

        for x in range(self.tiles_num):
            x_coord = round(self.piece_size * x + self.border_size * (x + 1))

            piece_group = [self.piece_class_rel[pieces_obj[1][x]]]

            white_tile_pawn = self.get_tile_by_coord((x_coord, y_coord_white_pawn))
            white_tile_pawn.taken_by = pieces_obj[0][0](white_groups + pawn_group, self, arg_size,
                                                        (x_coord, y_coord_white_pawn),
                                                        (x, self.tiles_num - 2), 'white')

            white_tile_piece = self.get_tile_by_coord((x_coord, y_coord_white_piece))
            white_tile_piece.taken_by = pieces_obj[1][x](white_groups + piece_group, self, arg_size,
                                                         (x_coord, y_coord_white_piece),
                                                         (x, self.tiles_num - 1), 'white')

            black_tile_pawn = self.get_tile_by_coord((x_coord, y_coord_black_pawn))
            black_tile_pawn.taken_by = pieces_obj[0][0](black_groups + pawn_group, self, arg_size,
                                                        (x_coord, y_coord_black_pawn),
                                                        (x, 1), 'black')

            black_tile_piece = self.get_tile_by_coord((x_coord, y_coord_black_piece))
            black_tile_piece.taken_by = pieces_obj[1][x](black_groups + piece_group, self, arg_size,
                                                         (x_coord, y_coord_black_piece),
                                                         (x, 0), 'black')

    def reverse(self):
        for piece in self.pieces:
            y_piece = self.tiles_num - piece.y_piece - 1

            piece.y_piece = y_piece
            piece.rect.y = round(y_piece * self.piece_size + self.border_size * (y_piece + 1))

        for tile in self.tiles:
            y_tile = self.tiles_num - tile.y_tile - 1

            tile.y_tile = y_tile
            tile.rect.y = round(y_tile * (self.piece_size + self.border_size))

    def handle_click(self, coord):
        if self.clicked_piece is not None:

            if self.clicked_piece.color == self.turn:
                tile = self.get_tile_by_coord(coord)
                prev_tile = self.get_tile_by_pos(self.clicked_piece.x_piece, self.clicked_piece.y_piece)

                if self.clicked_piece.can_move(tile):
                    self.clicked_piece.move_on(tile)

                    if not self.have_check_on(self.clicked_piece.color):
                        self.turn = self.get_opposite_color(self.turn)
                        self.reverse()  # Is required now (need fix)
                        return
                    else:
                        self.clicked_piece.move_on(prev_tile)

                elif self.clicked_piece.can_take(tile):
                    prev_piece = self.get_piece_by_pos(tile.x_tile, tile.y_tile)
                    prev_piece_groups = prev_piece.groups()
                    prev_piece.delete_from_groups()

                    self.clicked_piece.move_on(tile)

                    if not self.have_check_on(self.clicked_piece.color):
                        self.turn = self.get_opposite_color(self.turn)
                        self.reverse()  # Is required now (need fix)
                        return
                    else:
                        self.clicked_piece.move_on(prev_tile)
                        prev_piece.add(*prev_piece_groups)

        self.set_mark_on_piece_by_coord(coord)

    def set_mark_on_piece_by_coord(self, coord):
        piece = self.get_piece_by_coord(coord)
        if piece is not None:
            self.clicked_piece = self.get_piece_by_coord(coord)
            self.mark.rect = self.clicked_piece.rect

    def have_check_on(self, color):
        for king in set(self.kings).intersection(self.piece_color_rel[color]):
            king_tile = self.get_tile_by_pos(king.x_piece, king.y_piece)
            for piece in self.piece_color_rel[self.get_opposite_color(color)]:
                if piece.can_take(king_tile):
                    return True

        return False

    def check_pieces_on_line_between(self, piece, tile):
        min_x, min_y, max_x, max_y = self.get_range_between(piece, tile)

        for i in range(max_x - min_x):
            if self.get_tile_by_pos(min_x + i, piece.y_piece).taken_by is not None:
                return True

        for i in range(max_y - min_y):
            if self.get_tile_by_pos(piece.x_piece, min_y + i).taken_by is not None:
                return True

        return False

    def check_pieces_on_diagonal_between(self, piece, tile):
        min_x, min_y, max_x, max_y = self.get_range_between(piece, tile)

        for i in range(max_x - min_x):
            if (piece.x_piece > tile.x_tile and piece.y_piece > tile.y_tile) or \
                    (piece.x_piece < tile.x_tile and piece.y_piece < tile.y_tile):
                if self.get_tile_by_pos(min_x + i, min_y + i).taken_by is not None:
                    return True

            else:
                if self.get_tile_by_pos(min_x + i, max_y - i - 1).taken_by is not None:
                    return True

        return False

    def get_piece_by_pos(self, x_pos, y_pos):
        for piece in self.pieces:
            if piece.x_piece == x_pos and piece.y_piece == y_pos:
                return piece

    def get_tile_by_pos(self, x_pos, y_pos):
        for tile in self.tiles:
            if tile.x_tile == x_pos and tile.y_tile == y_pos:
                return tile

    def get_piece_by_coord(self, coord):
        for piece in self.pieces:
            if piece.rect.collidepoint(coord):
                return piece

    def get_tile_by_coord(self, coord):
        for tile in self.tiles:
            if tile.rect.collidepoint(coord):
                return tile

    def run_game(self):
        running = True

        while running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

            self.all_sprites.draw(screen)

            pygame.display.flip()

    @staticmethod
    def get_range_between(piece, tile):
        if piece.y_piece < tile.y_tile:
            min_y = piece.y_piece + 1
            max_y = tile.y_tile
        else:
            min_y = tile.y_tile + 1
            max_y = piece.y_piece

        if piece.x_piece < tile.x_tile:
            min_x = piece.x_piece + 1
            max_x = tile.x_tile
        else:
            min_x = tile.x_tile + 1
            max_x = piece.x_piece

        return min_x, min_y, max_x, max_y

    @staticmethod
    def get_opposite_color(color):
        if color == 'black':
            return 'white'
        else:
            return 'black'


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, board, tile_size, border_size, coord_pos, tile_pos, im_name, taken_by=None):
        super().__init__(*groups)

        self.board = board
        self.x_tile, self.y_tile = tile_pos
        self.border_size = border_size
        self.taken_by = taken_by

        image = pygame.image.load('data/{}'.format(im_name))
        self.image = pygame.transform.scale(image, tile_size)
        self.rect = pygame.Rect(coord_pos, tile_size)

    def is_under_attack(self):
        opposite_color = self.board.get_opposite_color(self.board.turn)
        for piece in self.board.piece_color_rel[opposite_color]:
            if piece.can_take(self, skip_tile_ver=True):
                return True
        return False


class Mark(pygame.sprite.Sprite):
    def __init__(self, groups, size):
        super().__init__(*groups)

        image = pygame.image.load('data/mark.png')
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect((-size[0], -size[1]), size)


class Piece(pygame.sprite.Sprite):
    def __init__(self, groups, board, size, coord_pos, piece_pos, color, im_name):
        super().__init__(*groups)

        self.board = board
        self.color = color
        self.x_piece, self.y_piece = piece_pos

        image = pygame.image.load('data/{}/{}'.format(color, im_name))
        self.image = pygame.transform.scale(image, size)
        self.rect = pygame.Rect(coord_pos, size)

    def move_on(self, tile):
        self.board.get_tile_by_pos(self.x_piece, self.y_piece).taken_by = None
        tile.taken_by = self

        self.rect.x = tile.rect.x + tile.border_size
        self.rect.y = tile.rect.y + tile.border_size

        self.x_piece = tile.x_tile
        self.y_piece = tile.y_tile

    def delete_from_groups(self):
        for group in self.groups():
            group.remove(self)


class Pawn(Piece):
    def __init__(self, groups, board, size, coord_pos, pawn_pos, color, im_name='pawn.png'):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, pawn_pos, color, im_name)

    def can_move(self, tile):
        if tile.taken_by is None:
            if tile.x_tile == self.x_piece and self.y_piece - tile.y_tile == 1:
                self.first_move = False
                return True

            elif tile.x_tile == self.x_piece and self.y_piece - tile.y_tile == 2 and \
                    self.first_move and not self.board.check_pieces_on_line_between(self, tile):
                self.first_move = False
                return True

        return False

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            if (self.x_piece - 1 == tile.x_tile or self.x_piece + 1 == tile.x_tile) and \
                    (self.y_piece - 1 == tile.y_tile or self.y_piece + 1 == tile.y_tile):
                self.first_move = False
                return True

        return False


class Rook(Piece):
    def __init__(self, groups, board, size, coord_pos, rook_pos, color, im_name='rook.png'):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, rook_pos, color, im_name)

    def can_move(self, tile, skip_tile_ver=False):
        if tile.taken_by is None or skip_tile_ver:
            if (self.x_piece == tile.x_tile and not self.board.check_pieces_on_line_between(self, tile)) or \
                    (self.y_piece == tile.y_tile and not self.board.check_pieces_on_line_between(self, tile)):
                self.first_move = False
                return True

            return False

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            return self.can_move(tile, skip_tile_ver=True)

        return False


class Knight(Piece):
    def __init__(self, groups, board, size, coord_pos, knight_pos, color, im_name='knight.png'):
        Piece.__init__(self, groups, board, size, coord_pos, knight_pos, color, im_name)

    def can_move(self, tile, skip_tile_ver=False):
        if tile.taken_by is None or skip_tile_ver:
            x_dif = abs(self.x_piece - tile.x_tile)
            y_dif = abs(self.y_piece - tile.y_tile)

            if (x_dif == 2 and y_dif == 1) or (x_dif == 1 and y_dif == 2):
                return True

        return False

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            return self.can_move(tile, skip_tile_ver=True)

        return False


class Bishop(Piece):
    def __init__(self, groups, board, size, coord_pos, bishop_pos, color, im_name='bishop.png'):
        Piece.__init__(self, groups, board, size, coord_pos, bishop_pos, color, im_name)

    def can_move(self, tile, skip_tile_ver=False):
        if tile.taken_by is None or skip_tile_ver:
            x_dif = abs(self.x_piece - tile.x_tile)
            y_dif = abs(self.y_piece - tile.y_tile)

            if x_dif == y_dif and not self.board.check_pieces_on_diagonal_between(self, tile):
                return True

            return False

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            return self.can_move(tile, skip_tile_ver=True)

        return False


class Queen(Piece):
    def __init__(self, groups, board, size, coord_pos, queen_pos, color, im_name='queen.png'):
        Piece.__init__(self, groups, board, size, coord_pos, queen_pos, color, im_name)

    def can_move(self, tile, skip_tile_ver=False):
        if tile.taken_by is None or skip_tile_ver:
            x_dif = abs(self.x_piece - tile.x_tile)
            y_dif = abs(self.y_piece - tile.y_tile)

            if x_dif == y_dif and not self.board.check_pieces_on_diagonal_between(self, tile):
                return True

            elif (self.x_piece == tile.x_tile and not self.board.check_pieces_on_line_between(self, tile)) or \
                    (self.y_piece == tile.y_tile and not self.board.check_pieces_on_line_between(self, tile)):
                return True

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            return self.can_move(tile, skip_tile_ver=True)

        return False


class King(Piece):
    def __init__(self, groups, board, size, coord_pos, king_pos, color, im_name='king.png'):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, king_pos, color, im_name)

    def can_move(self, tile, skip_tile_ver=False):
        if tile.taken_by is None or skip_tile_ver:
            x_dif = abs(self.x_piece - tile.x_tile)
            y_dif = abs(self.y_piece - tile.y_tile)

            if (x_dif == 1 and y_dif == 0) or (x_dif == 0 and y_dif == 1) or (x_dif == 1 and y_dif == 1):
                self.first_move = False
                return True

            elif x_dif == 2 and not self.board.check_pieces_on_line_between(self, tile) and self.first_move:
                # This verification (castling check) works only for default board size
                # Places with +-1 and +-2 breaking it (need a formula for future)

                rook_tile = self.board.get_tile_by_pos(tile.x_tile + 1, tile.y_tile)
                if type(rook_tile.taken_by) == Rook:
                    if rook_tile.taken_by.first_move and \
                            not self.board.get_tile_by_pos(self.x_piece + 1, self.y_piece).is_under_attack() and \
                            not self.board.get_tile_by_pos(self.x_piece + 2, self.y_piece).is_under_attack():
                        rook_tile.taken_by.move_on(self.board.get_tile_by_pos(tile.x_tile - 1, tile.y_tile))
                        self.first_move = False
                        return True

                rook_tile = self.board.get_tile_by_pos(tile.x_tile - 2, tile.y_tile)
                if type(rook_tile.taken_by) == Rook:
                    if rook_tile.taken_by.first_move and \
                            not self.board.get_tile_by_pos(self.x_piece - 1, self.y_piece).is_under_attack() and \
                            not self.board.get_tile_by_pos(self.x_piece - 2, self.y_piece).is_under_attack():
                        rook_tile.taken_by.move_on(self.board.get_tile_by_pos(tile.x_tile + 1, tile.y_tile))
                        self.first_move = False
                        return True

        return False

    def can_take(self, tile, skip_tile_ver=False):
        if (tile.taken_by is not None and tile.taken_by.color != self.color) or skip_tile_ver:
            return self.can_move(tile, skip_tile_ver=True)

        return False


if __name__ == '__main__':
    pygame.init()

    win_size = (658, 658)
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption('ChessMate')

    all_sprites_test = pygame.sprite.Group()
    pieces_test = pygame.sprite.Group()
    tiles_test = pygame.sprite.Group()

    PIECES_OBJ = [[Pawn],
                  [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]]
    test_board = Board(win_size[0], 8, border_size=2)
    test_board.set_pieces(PIECES_OBJ)

    test_board.run_game()

    pygame.quit()
