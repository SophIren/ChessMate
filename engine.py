import pygame


class Board:
    def __init__(self, size, tiles_num, pieces_obj, pieces_group, tiles_group, all_sprites_group, border_size=0):
        self.tiles_num = tiles_num
        self.border_size = border_size
        self.piece_size = (size - border_size * (tiles_num + 1)) / tiles_num
        self.pieces_obj = pieces_obj
        self.pieces = pieces_group
        self.tiles = tiles_group
        self.all_sprites = all_sprites_group
        self.clicked_piece = None
        self.turn = None

        tile_size = round(self.piece_size + 2 * border_size)
        for i in range(tiles_num):
            if i % 2 == 0:
                im_name = 'white_tile.png'
            else:
                im_name = 'black_tile.png'
            for j in range(tiles_num):
                Tile((self.all_sprites, self.tiles), self, (tile_size, tile_size), self.border_size,
                     (round(i * (self.piece_size + self.border_size)), round(j * (self.piece_size + self.border_size))),
                     (i, j), im_name)
                if im_name == 'white_tile.png':
                    im_name = 'black_tile.png'
                else:
                    im_name = 'white_tile.png'

        self.mark = Mark((self.all_sprites,), (round(self.piece_size), round(self.piece_size)))

    def set_pieces(self):
        self.turn = 'white'

        arg_size = (round(self.piece_size), round(self.piece_size))
        groups = (self.all_sprites, self.pieces)

        y_pos_black = round(self.piece_size + self.border_size * 2)
        y_pos_white = round((self.tiles_num - 2) * self.piece_size + self.border_size * (self.tiles_num - 1))
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            self.get_tile_by_coord((x_pos, y_pos_black)).taken_by = self.pieces_obj[0][0](groups, self, arg_size,
                                                                                          (x_pos, y_pos_black),
                                                                                          (x, 1), 'black')
            self.get_tile_by_coord((x_pos, y_pos_white)).taken_by = self.pieces_obj[0][0](groups, self, arg_size,
                                                                                          (x_pos, y_pos_white),
                                                                                          (x, self.tiles_num - 2),
                                                                                          'white')

        y_pos_black = self.border_size
        y_pos_white = round((self.tiles_num - 1) * self.piece_size + self.border_size * self.tiles_num)
        for x in range(self.tiles_num):
            x_pos = round(self.piece_size * x + self.border_size * (x + 1))
            self.get_tile_by_coord((x_pos, y_pos_black)).taken_by = self.pieces_obj[1][x](groups, self, arg_size,
                                                                                          (x_pos, y_pos_black),
                                                                                          (x, 0), 'black')
            self.get_tile_by_coord((x_pos, y_pos_white)).taken_by = self.pieces_obj[1][x](groups, self, arg_size,
                                                                                          (x_pos, y_pos_white),
                                                                                          (x, self.tiles_num - 1),
                                                                                          'white')

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
                        self.change_color()
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
                        self.change_color()
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
        kings = []
        for piece in self.pieces:
            if type(piece) == King and piece.color == color:
                kings.append(piece)

        for king in kings:
            king_tile = self.get_tile_by_pos(king.x_piece, king.y_piece)
            for piece in self.pieces:
                if piece.color != color and piece.can_take(king_tile):
                    return True

        return False

    def change_color(self):
        if self.turn == 'black':
            self.turn = 'white'
        else:
            self.turn = 'black'

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
        for piece in self.board.pieces:
            if piece.color != self.board.turn and piece.can_take(self, skip_tile_ver=True):
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
    def __init__(self, groups, board, size, coord_pos, pawn_pos, color):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, pawn_pos, color, 'pawn.png')

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
            if (self.x_piece - 1 == tile.x_tile or self.x_piece + 1 == tile.x_tile) \
                    and (self.y_piece - 1 == tile.y_tile or self.y_piece + 1 == tile.y_tile):
                self.first_move = False
                return True

        return False


class Rook(Piece):
    def __init__(self, groups, board, size, coord_pos, rook_pos, color):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, rook_pos, color, 'rook.png')

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
    def __init__(self, groups, board, size, coord_pos, knight_pos, color):
        Piece.__init__(self, groups, board, size, coord_pos, knight_pos, color, 'knight.png')

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
    def __init__(self, groups, board, size, coord_pos, bishop_pos, color):
        Piece.__init__(self, groups, board, size, coord_pos, bishop_pos, color, 'bishop.png')

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
    def __init__(self, groups, board, size, coord_pos, queen_pos, color):
        Piece.__init__(self, groups, board, size, coord_pos, queen_pos, color, 'queen.png')

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
    def __init__(self, groups, board, size, coord_pos, king_pos, color):
        self.first_move = True
        Piece.__init__(self, groups, board, size, coord_pos, king_pos, color, 'king.png')

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
    test_board = Board(win_size[0], 8, PIECES_OBJ, pieces_test, tiles_test, all_sprites_test, border_size=2)
    test_board.set_pieces()

    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            test_board.handle_click(event.pos)

        all_sprites_test.draw(screen)

        pygame.display.flip()

    pygame.quit()
