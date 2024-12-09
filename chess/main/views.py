from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ChessGame
from .serializer import ChessGameSerializer, ChessGameSerializerPost

def traverse_directions(start_row, start_col, fields_chess, player_code, directions):
    moves = []
    for dr, dc in directions:
        current_row = start_row
        current_col = start_col

        while True:
            current_row += dr
            current_col += dc
            if not (1 <= current_row <= 8 and ord('a') <= current_col <= ord('h')):
                break

            current_row_str = str(current_row)
            current_col_letter = chr(current_col)

            if fields_chess[current_row_str][current_col_letter]["figure"]:
                if fields_chess[current_row_str][current_col_letter]["owner"] != player_code:
                    moves.append((current_row_str, current_col_letter))
                break
            moves.append((current_row_str, current_col_letter))
    return moves

def update_board(fields_chess, start, end):
    start_row, start_col = str(start[1]), start[0]
    end_row, end_col = str(end[1]), end[0]

    fields_chess[end_row][end_col] = fields_chess[start_row][start_col]
    fields_chess[start_row][start_col] = {"figure": False, "owner": None, "type": None}
    return fields_chess

def get_available_moves(figure_type, start_row, start_col, player_code, fields_chess, pl1codewhite, pl2codeblack):
    moves = []
    start_row_int = int(start_row)
    start_col_int = ord(start_col)

    if figure_type == "pawn":
        direction = 1 if player_code == pl1codewhite else -1

        next_row = start_row_int + direction
        if 1 <= next_row <= 8:
            next_row_str = str(next_row)

            if not fields_chess[next_row_str][start_col]["figure"]:
                moves.append((next_row_str, start_col))

            if (player_code == pl1codewhite and start_row_int == 2) or (player_code == pl2codeblack and start_row_int == 7):
                next_row_two = start_row_int + 2 * direction
                if not fields_chess[str(next_row_two)][start_col]["figure"] and not fields_chess[str(next_row_str)][start_col]["figure"]:
                    moves.append((str(next_row_two), start_col))

        for col_offset in [-1, 1]:
            next_col_int = start_col_int + col_offset
            if ord('a') <= next_col_int <= ord('h'):
                next_col = chr(next_col_int)
                if fields_chess[next_row_str][next_col]["figure"] and fields_chess[next_row_str][next_col]["owner"] != player_code:
                    moves.append((next_row_str, next_col))

    elif figure_type == "rook":
        moves += traverse_directions(start_row_int, start_col_int, fields_chess, player_code, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    elif figure_type == "bishop":
        moves += traverse_directions(start_row_int, start_col_int, fields_chess, player_code, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    elif figure_type == "queen":
        moves += traverse_directions(start_row_int, start_col_int, fields_chess, player_code, [
            (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ])

    elif figure_type == "knight":
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in knight_moves:
            next_row = start_row_int + dr
            next_col = start_col_int + dc
            if 1 <= next_row <= 8 and ord('a') <= next_col <= ord('h'):
                next_col_letter = chr(next_col)
                next_row_str = str(next_row)
                if not fields_chess[next_row_str][next_col_letter]["figure"] or fields_chess[next_row_str][next_col_letter]["owner"] != player_code:
                    moves.append((next_row_str, next_col_letter))

    elif figure_type == "king":
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in king_moves:
            next_row = start_row_int + dr
            next_col = start_col_int + dc
            if 1 <= next_row <= 8 and ord('a') <= next_col <= ord('h'):
                next_col_letter = chr(next_col)
                next_row_str = str(next_row)
                if not fields_chess[next_row_str][next_col_letter]["figure"] or fields_chess[next_row_str][next_col_letter]["owner"] != player_code:
                    moves.append((next_row_str, next_col_letter))

    print(moves)
    return moves



def is_valid_move(move, fields_chess, current_player_turn, player_code, pl1codewhite , pl2codeblack):
    start, end = move
    start_row, start_col = str(start[1]), start[0]
    end_row, end_col = str(end[1]), end[0]
    print(start_row, start_col)

    if str(start_row) == 'a' or str(start_row) == 'b' or str(start_row) == 'c' or str(start_row) == 'e' or str(start_row) == 'd' or str(start_row) == 'f' or str(start_row) == 'e'  or str(start_row) == 'g':
        start_row, start_col = start_col, start_row
    if fields_chess[str(start_row)][start_col]["figure"] is False:
        return False, "No figure on the start cell"

    figure = fields_chess[start_row][start_col]["figure"]
    owner = fields_chess[start_row][start_col]["owner"]
    figure_type = fields_chess[start_row][start_col]["type"]


    if player_code == pl1codewhite:
        my_color = "white"
    elif player_code == pl2codeblack:
         my_color = "black"
    else:
         return False, "Wrong player code"

    if owner != my_color:
        return False, "It's not your figure"

    if current_player_turn != (0 if owner == "white" else 1):
        return False, "It's not your turn"

    available_moves = get_available_moves(figure_type, start_row, start_col, player_code, fields_chess, pl1codewhite, pl2codeblack)

    if figure_type == 'king':
        for move in available_moves:
            if is_in_check(fields_chess, move[1], current_player_turn, player_code, pl1codewhite , pl2codeblack) == False:
                return False, 'You have a mate.'

        if is_in_check(fields_chess, (end_row, end_col), current_player_turn, player_code, pl1codewhite , pl2codeblack) == True:
            return False, 'The king is in check in this move. You cant move here.'

    if (end_row, end_col) in available_moves:
        return True, update_board(fields_chess, start, end)

    return False, "Invalid move"

def is_in_check(fields_chess, my_pos, current_player_turn, player_code, pl1codewhite , pl2codeblack):
    opponent = "black" if fields_chess[my_pos[0]][my_pos[1]]['type'] == "white" else "white"
    print(my_pos[0], my_pos[1])
    for r in range(1, 7):
        r = str(r)
        for c in {'a', 'b', 'c', 'd', 'e', 'f', 'g'}:
            print(r, c)
            if fields_chess[r][c]["figure"] and fields_chess[r][c]["owner"] == opponent and fields_chess[r][c]['type'] != "king":
                if is_valid_move((r + c, my_pos[0] + my_pos[1]), fields_chess, current_player_turn, player_code, pl1codewhite, pl2codeblack):
                    return True
    return False

@api_view(['POST'])
def postData(request):
    game = get_object_or_404(ChessGame, game_code=request.data["game_code"])
    serializer = ChessGameSerializerPost(game, data=request.data)
    move = (request.data["start"], request.data["end"])
    print(move, game.fields_chess, game.current_player_turn, request.data["player_code"])

    if serializer.is_valid():
        move = (request.data["start"], request.data["end"])
        is_valid, result = is_valid_move(move, game.fields_chess, game.current_player_turn, request.data["player_code"], game.player_1_code, game.player_2_code)



        if not is_valid:
            return Response({"detail": result}, status=400)

        game.fields_chess = result
        game.current_player_turn = 1 - game.current_player_turn
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)



@api_view(['GET'])
def getData(request):
    game_code = request.data.get('game_code')
    if game_code:
        chess = ChessGame.objects.filter(game_code=game_code)
        if chess.exists():
            serializer = ChessGameSerializer(chess, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Game not found."}, status=404)
    else:
        return Response({"detail": "game_code parameter is required."}, status=400)


@api_view(['POST'])
def postData(request):
    game = get_object_or_404(ChessGame, game_code=request.data["game_code"])
    serializer = ChessGameSerializerPost(game, data=request.data)

    if serializer.is_valid():
        move = (request.data["start"], request.data["end"])
        is_valid, result = is_valid_move(move, game.fields_chess, game.current_player_turn, request.data["player_code"], game.player_1_code, game.player_2_code)

        if not is_valid:
            return Response({"detail": result}, status=400)

        game.fields_chess = result
        game.current_player_turn = 1 - game.current_player_turn
        serializer.save()
        return Response({"detail": result}, status=200)

    return Response(serializer.errors, status=400)
