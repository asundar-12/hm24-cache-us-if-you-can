
def print_employee_salaries(employee_list):
    for employee in employee_list:
        if employee.get('salary') is not None:
            print(f"Employee {employee.get('name')} has a salary of {employee.get('salary')}")
        else:
            print(f"Employee {employee.get('name')} does not have a salary specified.")


# Define constants
CLOSED_E4, CLOSED_D4, CLOSED_E3, CLOSED_E5, CLOSED_D3, CLOSED_D5, LATE_PART, FIRST_W = False, False, False, False, False, False, False, False
ROKERET_BONUS, PD1080, PD2070, PD3060, PD4050, PD1080QB, PD3060QB, PD3060QE, PD1080K, PD2070K, PD3060K, PD7R, PD8R, PD6Q, PD7Q, PDKC12, PDPKCF, PDPKDE, PDPK, PDPEND, PENAL_UNDEVEL, BISHOP_PENALTY, OPEN_GAME_VALUE, END_GAME_VALUE, PDB5, KING_AREA30, KING_AREA20, KING_AREA16, KING_AREA12, KING_AREA8, AROUND_KING_BONUS, PAWN_STRATEG20, PAWN_STRATEG10, BISHOP_CLOSED, BISHOP_OPEN, KNIGHT_CLOSED, ROOKER_FULL_OPEN_LINE, ROOKER_HALF_OPEN_LINE, EARLY_KNIGHT, LATE_BISHOP, PAWNH3A3ATTACK, AVOID_CASTLING, CASTLE_BONUS, IN_MOVE_BONUS, ACTIVITY_WEIGHT, TWO_ON_ROW7, TWO_ON_ROW6, TWO_ON_ROW5, ROOKER_FIRST_ROW_BEHIND_PAWN, ROOKER_CORNER_NEXT_TO_KING, ROOKER_CORNER_NEXT_TO_PIECE, KING_CLOSE_ROOK, KING_BEHIND_PAWNS, QUEEN_DEVELOPED, QUEEN_BEFORE_PAWN, QUEEN_BEFORE_PAWN_BLOCKED_BISHOP, QUEEN_BEFORE_BISHOP, BISHOP_BEFORE_PAWN, BISHOP_BEHIND_PAWN, BISHOP_PROTECTED_BY_PAWN, KNIGHT_BEFORE_PAWN, KNIGHT_PROTECTED_BY_PAWN, KNIGHT_PAWN_IN_FRONT, PAWN_NEXT_TO_PAWN, PAWN_GUARDS_PAWN, PAWN_F3, PAWN_DOUBBLED_PAWN, KN_END_GAME_PRIO, KN_END_GAME_BPrio, SUPPORTED_PAWN_PENALTY, SUPPORTED_PAWN_0911, SUPPORTED_PAWN_1020, SUPPORTED_PAWN_1921, BAD_DEVEL_PENALTY, BAD_DEVEL_BISHOP, BISHOP_PAIR_BONUS = 20, -9, -2, 3, 8, -5, 20, 5, 12, -20, 5, 12, 5, 17, 3, 12, 8, 30, 20, 16, 12, 8, 5, 15, 10, 15, 7, 17, 10, 12, 3, 6, 3, 8, 8, 13, 8, 30, 28, 10, 0, 350, 150, 50, 8, 30, 4, 22, 12, 13, 8, 10, 8, 12, 50, 50, 20, 80, 6, 6, 50, 80, 17, 6, 30

# Define boolean constants
K_OUT, K_OUT = False, False

# Define offset for arrays
ST_OFF = 11

# Define constants for numeric representation of pieces
W_N, B_N, W_B, B_B, W_R, B_R, W_C, B_C, W_Q, B_Q, W_P, B_P, W_E, B_E, W_K, B_K, W_M, B_M, W_T, B_T, SPC, EDGE = 115, 83, 108, 76, 116, 84, 114, 82, 100, 68, 98, 66, 107, 75, 101, 69, 109, 77, 107, 75, 32, 46

# Define function for uppercase conversion
def upper_n(n):
    if n < W_A:
        return n
    else:
        return n - 32

# Define function for positional evaluation
def positional_evaluation(brik, felt):
    return (brik - 66) * 78 + felt - 10

# Define variables
p = 0


def pdN(brik_n, felt):
    return brik_n * 78 - 5158 + felt

def pdX(brik, felt):
    return (ord(brik) - 66) * 78 + felt - 10

def print_message(message):
    print(message)

def preprocess_position(position):
    # Initialize variables
    open_game, late_part, end_game, piece_clear, piece_adjust = False, False, False, False, False
    pawn_center_value, king_area_value, rook_open_line_value, bishop_open_line_value, knight_closed_value = 0, 0, 0, 0, 0
    pawn_strategy_value, bishop_open_line_value, knight_closed_value, bishop_early_value, bishop_late_value = 0, 0, 0, 0, 0
    pawn_h3_a3_attack_value, bishop_penalty_value = 0, 0

    # Count pieces
    white_queens, white_rooks, white_bishops, white_knights, white_pawns, black_queens, black_rooks, black_bishops, black_knights, black_pawns = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in range(11, 89):
        piece = position[i]
        if piece == 'wQ':
            white_queens += 1
        elif piece == 'wR':
            white_rooks += 1
        elif piece == 'wB':
            white_bishops += 1
        elif piece == 'wN':
            white_knights += 1
        elif piece == 'wP':
            white_pawns += 1
        elif piece == 'bQ':
            black_queens += 1
        elif piece == 'bR':
            black_rooks += 1
        elif piece == 'bB':
            black_bishops += 1
        elif piece == 'bN':
            black_knights += 1
        elif piece == 'bP':
            black_pawns += 1

    # Set global flags
    open_game = (white_pawns + black_pawns) > 16
    if open_game:
        late_part = (white_pawns + black_pawns) < 19
        end_game = (white_queens + white_rooks + white_bishops + white_knights + white_pawns + black_queens + black_rooks + black_bishops + black_knights + black_pawns) < 32
        if end_game:
            late_part = (white_queens + white_rooks + white_bishops + white_knights + white_pawns + black_queens + black_rooks + black_bishops + black_knights + black_pawns) < 26

    # Calculate pawn center type
    if (position[44] == 'wP') and (position[54] == 'bP'):
        closed_d4 = True
        if (position[35] == 'wP') and (position[45] == 'bP'):
            closed_e3 = True
        if (position[55] == 'wP') and (position[65] == 'bP'):
            closed_e5 = True
    elif (position[45] == 'wP') and (position[55] == 'bP'):
        closed_e4 = True
        if (position[34] == 'wP') and (position[44] == 'bP'):
            closed_d3 = True
        if (position[54] == 'wP') and (position[64] == 'bP'):
            closed_d5 = True

    # Calculate pawn center value
    if not end_game and not (open_game and not late_part) and king_air:
        if (position[44] == 'wP') and (position[54] == 'bP'):
            pawn_center_value = 2
        elif (position[45] == 'wP') and (position[55] == 'bP'):
            pawn_center_value = 2

    # Calculate king positions
    if position[15] == 'wM':
        white_king_position = 15
    else:
        white_king_position = 11
        while position[white_king_position] != 'wK':
            white_king_position += 1

    if position[85] == 'bM':
        black_king_position = 85
    else:
        black_king_position = 88
        while position[black_king_position] != 'bK':
            black_king_position -= 1

    # Calculate king air
    if not end_game and not (open_game and not late_part) and king_air:
        if white_king_position == 17 and (position[26] == 'wP') and (position[27] == 'wP') and (position[28] == 'wP'):
            defenders = 0
            for sc in range(11, 17):
                if position[sc] in ('wR', 'wQ'):
                    defenders += 1
            if position[16] in ('wB', 'wN'):
                defenders += 1
            if defenders < 2:
                ix = pdn('wP', 27)
                pawn_center_value = pawn_center_value + defenders_weight * 4 - defenders * defenders_weight * 2
                pawn_center_value = pawn_center_value + defenders_weight * 6 - defenders * defenders_weight * 3
                pdw[ix] = pdw[ix] + pawn_center_value

        elif white_king_position == 12 and (position[21] == 'wP') and (position[22] == 'wP') and (position[23] == 'wP'):
            defenders = 0
            for sc in range(13, 18):
                if position[sc] in ('wR', 'wQ'):
                    defenders += 1
            if position[13] in ('wB', 'wN'):
                defenders += 1
            if defenders < 2:
                ix = pdn('wP', 22)
                pawn_center_value = pawn_center_value + defenders_weight * 4 - defenders * defenders_weight * 2
                pawn_center_value = pawn_center_value + defenders_weight * 6 - defenders * defenders_weight * 3
                pdw[ix] = pdw[ix] + pawn_center_value

        elif black_king_position == 87 and (position[76] == 'bP') and (position[77] == 'bP') and (position[78] == 'bP'):
            defenders = 0
            for sc in range(81, 87):
                if position[sc] in ('bR', 'bQ'):
                    defenders += 1
            if position[86] in ('bB', 'bN'):
                defenders += 1
            if defenders < 2:
                ix = pdn('bP', 77)
                pawn_center_value = pawn_center_value + defenders_weight * 4 - defenders * defenders_weight * 2
                pawn_center_value = pawn_center_value + defenders_weight * 6 - defenders * defenders_weight * 3
                pdw[ix] = pdw[ix] + pawn_center_value

        elif black_king_position == 82 and (position[71] == 'bP') and (position[72] == 'bP') and (position[73] == 'bP'):
            defenders = 0
            for sc in range(83, 88):
                if position[sc] in ('bR', 'bQ'):
                    defenders += 1
            if position[83] in ('bB', 'bN'):
                defenders += 1
            if defenders < 2:
                ix = pdn('bP', 72)
                pawn_center_value = pawn_center_value + defenders_weight * 4 - defenders * defenders_weight * 2
                pawn_center_value = pawn_center_value + defenders_weight * 6 - defenders * defenders_weight * 3
                pdw[ix] = pdw[ix] + pawn_center_value

    # Calculate king castling bonus
    if not end_game and not (open_game and not late_part) and king_air:
        if white_king_position == 17 and (position[21] != 'wP') and (position[22] != 'wP') and (position[23] != 'wP'):
            f = 0
            if (position[21] != 'wP') and (position[61] != 'wP'):
                f += 1
            if (position[22] != 'wP') and (position[63] != 'wP'):
                f += 1
            if position[23] != 'wP':
                f += 1
            for x in range(1, 4):
                if r[x]:
                    f += 1
            if f > 0:
                ix = pdn('wK', 13)
                pdw[ix] = pdw[ix] - f * f * avoid_castling

        elif white_king_position == 12 and (position[21] != 'wP') and (position[22] != 'wP') and (position[23] != 'wP'):
            f = 0
            if (position[21] != 'wP') and (position[22] != 'wP') and (position[23] != 'wP'):
                f += 1
            if (position[21] != 'wP') and (position[61] != 'wP'):
                f += 1
            if (position[22] != 'wP') and (position[63] != 'wP'):
                f += 1
            if position[23] != 'wP':
                f += 1
            for x in range(6, 9):
                if r[x]:
                    f += 1
            if f > 0:
                ix = pdn('wK', 17)
                pdw[ix] = pdw[ix] - f * f * avoid_castling

        elif black_king_position == 87 and (position[76] != 'bP') and (position[77] != 'bP') and (position[78] != 'bP'):
            f = 0
            if (position[76] != 'bP') and (position[36] != 'bP'):
                f += 1
            if (position[77] != 'bP') and (position[33] != 'bP'):
                f += 1
            if position[78] != 'bP':
                f += 1
            for x in range(6, 9):
                if r[x]:
                    f += 1
            if f > 0:
                ix = pdn('bK', 87)
                pdw[ix] = pdw[ix] - f * f * avoid_castling

        elif black_king_position == 82 and (position[71] != 'bP') and (position[72] != 'bP') and (position[73] != 'bP'):
            if (position[71] != 'bP') and (position[31] != 'bP'):
                f += 1
            if (position[72] != 'bP') and (position[33] != 'bP'):
                f += 1
            if position[73] != 'b':
                f = 0

def eval_position(position, activity, black, alpha, beta):
    inmv = 1 if position.turn else -1
    open_center_degree = 2

    matr = 0
    wbonus = 0
    bbonus = 0
    pawns_init = False

    king_endgame_w = True
    king_endgame_b = True
    kn_endgame_w = False
    kn_endgame_b = False
    pri_w = 0
    pri_b = 0

    white_pawns = [False] * 89
    black_pawns = [False] * 89
    white_pawn_lines = [0] * 8
    black_pawn_lines = [0] * 8
    white_pawn_count = 0
    black_pawn_count = 0

    for n in range(11, 89):
        piece = position.board[n]
        if piece > 'a':
            matr += piece_value(piece)
            if piece == 'w':
                if piece in ('wR', 'wC'):
                    matr += rook_value
                    if n < 50:
                        if position.board[n + 10] == 'wP' or position.board[n + 20] == 'wP':
                            wbonus -= rook_behind_pawn
                if piece == 'wM':
                    matr += knight_value
                    kposs = n
                if piece == 'wK':
                    matr += king_value
                    if not position.endgame:
                        if (n == 16 and (position.board[n + 10] == 'wR' or position.board[n + 17] == 'wR')) or (
                                n == 13 and (position.board[n + 11] == 'wR' or position.board[n + 22] == 'wR')):
                            if (n == 16 and position.board[n + 26] == 'wP' and position.board[n + 27] == 'wP') or (
                                    n == 13 and position.board[n + 23] == 'wP' and position.board[n + 22] == 'wP'):
                                wbonus -= king_close_rook
                            else:
                                for m in range(n + 9, n + 11):
                                    if position.board[m] == 'wP':
                                        wbonus += 12
                                wbonus -= king_behind_pawns
                if piece == 'wQ':
                    matr += queen_value
                    if position.open_game:
                        if n > 28:
                            wbonus -= queen_developed
                            if n > 41:
                                wbonus -= 12
                        elif (n == 24 and position.board[n + 13] == 'wB' and position.board[n + 22] == 'wP') or (
                                n == 25 and position.board[n + 16] == 'wB' and position.board[n + 27] == 'wP'):
                            wbonus -= queen_before_bishop
                if piece == 'wB':
                    matr += bishop_value
                    if 30 < n < 39:
                        if position.board[n - 10] == 'wP':
                            wbonus -= bishop_before_pawn
                    if (n == 13 and position.board[n + 22] == 'wP') or (n == 16 and position.board[n + 27] == 'wP'):
                        wbonus -= bishop_behind_pawn
                    if (position.board[n - 11] == 'wP') or (position.board[n - 9] == 'wP'):
                        wbonus += bishop_protected_by_pawn
                if piece == 'wN':
                    matr += knight_value
                    if 30 < n < 39:
                        if position.board[n - 10] == 'wP':
                            wbonus -= knight_before_pawn
                    if (position.board[n - 11] == 'wP') or (position.board[n - 9] == 'wP'):
                        wbonus += knight_protected_by_pawn
                    if (position.board[n + 10] == 'bP') and (position.board[n + 11] != 'bP') and (
                            position.board[n + 9] != 'bP'):
                        wbonus += knight_pawn_in_front
                        if (n > 50) or (position.board[n + 19] != 'bP') and (position.board[n + 21] != 'bP'):
                            wbonus += knight_pawn_in_front
                            if (n > 60) or (position.board[n + 29] != 'bP') and (position.board[n + 31] != 'bP'):
                                wbonus += knight_pawn_in_front
        else:
            matr -= piece_value(piece)
            if piece == 'bR':
                if n > 40:
                    if position.board[n - 10] == 'bP' or position.board[n - 20] == 'bP':
                        bbonus -= rook_behind_pawn
                if n == 81:
                    if piece == 'bC':
                        matr += rook_value - bishop_value
                    if position.board[n + 1] != ' ':
                        if position.board[n + 1] == 'bK':
                            bbonus -= rook_corner_next_to_king
                        else:
                            bbonus -= rook_corner_next_to_piece
                elif n == 88:
                    if piece == 'bC':
                        matr += rook_value - bishop_value
                    if position.board[n - 1] != ' ':
                        if position.board[n - 1] == 'bK':
                            bbonus -= rook_corner_next_to_king
                        else:
                            bbonus -= rook_corner_next_to_piece
            if piece == 'bM':
                matr -= knight_value
                kpos = n
            if piece == 'bK':
                matr -= king_value
                if not position.endgame:
                    if (n == 86 and (position.board[n + 10] == 'bR' or position.board[n + 17] == 'bR')) or (
                            n == 83 and (position.board[n - 10] == 'bR' or position.board[n - 22] == 'bR')):
                        if (n == 86 and position.board[n - 6] == 'bP' and position.board[n - 7] == 'bP') or (
                                n == 83 and position.board[n - 3] == 'bP' and position.board[n - 4] == 'bP'):
                            bbonus -= king_close_rook
                        else:
                            for m in range(n - 11, n - 9):
                                if position.board[m] == 'bP':
                                    bbonus += king_behind_pawns
                            bbonus -= king_behind_pawns
                if piece == 'bQ':
                    matr -= queen_value
                    if position.open_game:
                        if n < 71:
                            bbonus -= 12
                        elif (n == 74 and position.board[n + 13] == 'bB' and position.board[n + 72] == 'bP') or (
                                n == 75 and position.board[n + 16] == 'bB' and position.board[n + 77] == 'bP'):
                            bbonus -= queen_before_bishop
                if piece == 'bB':
                    matr -= bishop_value
                    if 60 < n < 69:
                        if position.board[n + 10] == 'bP':
                            bbonus -= bishop_before_pawn
                    if (n == 83 and position.board[n + 72] == 'bP') or (n == 86 and position.board[n + 77] == 'bP'):
                        bbonus -= bishop_behind_pawn
                    if (position.board[n + 11] == 'bP') or (position.board[n + 9] == 'bP'):
                        bbonus += bishop_protected_by_pawn
                if piece == 'bN':
                    matr -= knight_value
                    if 60 < n < 69:
                        if position.board[n + 10] == 'bP':
                            bbonus -= knight_before_pawn
                    if (position.board[n + 11] == 'bP') or (position.board[n + 9] == 'bP'):
                        bbonus += knight_protected_by_pawn
                    if (position.board[n - 10] == 'wP') and (position.board[n - 11] != 'wP') and (
                            position.board[n - 9] != 'wP'):
                        bbonus += knight_pawn_in_front
                        if (n < 31) or (position.board[n - 19] != 'wP') and (position.board[n - 21] != 'wP'):
                            bbonus += knight_pawn_in_front
                        if (n < 41) or (position.board[n - 29] != 'wP') and (position.board[n - 31] != 'wP'):
                            bbonus += knight_pawn_in_front
        if piece == piece.upper():
            posi += piece_value(piece) * piece_position_adjustment(piece, n)

    if white_pawns.count('wP') == 2:
        wbonus += bishop_pair_bonus * open_center_degree
    if black_pawns.count('bP') == 2:
        bbonus += bishop_pair_bonus * open_center_degree

    if king_endgame_w and abs(matr + posi + wbonus - bbonus) < 800:
        if kn_endgame_w:
            pri_w = kn_endgame_prio
        else:
            pri_w = kn_endgame_prio * 2

        if position.black:
            for y in range(2, 8):
                for x in range(1, 9):
                    if position.board[n] == 'wP' or (y == 2 and position.board[n - 10] == 'wP'):
                        if not black_pawns[n]:
                            if (position.king_pos // 10) < y or (abs(position.king_pos % 10 - x))
                                n = 10 * y + x
def initialize():
    n = 0
    first_w = True
    if not first_w:
        to_file = True
        first_w = True
        # Uncomment these lines if you want to include logging
        # log_version("SkakBrainEval.def", skak_brain_eval_def_compilation)
        # log_version("SkakBrainEval.mod", skak_brain_eval_mod_compilation)
        # print('Initialize A')
        pdw.extend(pd_sz)
        # print('Initialize B')
        for n in range(1, pd_sz + 1):
            pdw[n] = 0
        # print('Initialize C')
        pd = pdw
        pdb = pdw
        # print('Initialize EVAL')
    else:
        # print('Initialize EVAL SKIP')
        pass

# Call the function
initialize()