import copy
import random
import sqlite3
import time
#pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q", king = "K" and empty = "E"
#turn = W for White and B for black (capital letters only)
#Move = [a,b,c,d] piece in [a,b] moves to [c,d] / in case of five elements, the last will indicate the piece of pawn 
#promotion.
#MateIn = White moves to Mate. If 60, it's a draw. If 100 it's still undefined. If >=0 and <=59, it is a "Mate In x".
#Capital letters for White
#Castle and en-passant moves not implemented in this code
def IsABlackPiece(x):
    if (x == "p"): return True
    if (x == "n"): return True
    if (x == "b"): return True
    if (x == "r"): return True
    if (x == "q"): return True
    if (x == "k"): return True
    return False
def IsAWhitePiece(x):
    if (x == "P"): return True
    if (x == "N"): return True
    if (x == "B"): return True
    if (x == "R"): return True
    if (x == "Q"): return True
    if (x == "K"): return True
    return False
def MapAttacksBlack(board):
    # Attacked by White and Black
    AttackedByBlack = [[False for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if (board[i][j] == "p"):
                # on edge
                if (j == 0):
                    AttackedByBlack[i - 1][j + 1] = True
                    continue
                if (j == 7):
                    AttackedByBlack[i - 1][j - 1] = True
                    continue
                # not on edge
                AttackedByBlack[i - 1][j - 1] = True
                AttackedByBlack[i - 1][j + 1] = True
            if (board[i][j] == "n"):
                di = [-2, -1, 1, 2, 2, 1, -1, -2]
                dj = [1, 2, 2, 1, -1, -2, -2, -1]
                for k in range(8):
                    if (0 <= i + di[k] <= 7 and 0 <= j + dj[k] <= 7):
                        AttackedByBlack[i + di[k]][j + dj[k]] = True
            if (board[i][j] == "b"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (di == 0 or dj == 0): continue  # diagonal moves only
                        for k in range(1, 10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByBlack[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "r"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (not (di == 0 or dj == 0)): continue  # straight moves only
                        if (di == 0 and dj == 0): continue
                        for k in range(1, 10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByBlack[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "q"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        # mighty queen moving all directions
                        if (di == 0 and dj == 0):    continue
                        for k in range(1, 10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByBlack[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "k"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (di == 0 and dj == 0): continue
                        # humble king moving all directions, but once
                        new_i = i + di
                        new_j = j + dj
                        if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): continue
                        AttackedByBlack[new_i][new_j] = True
    return AttackedByBlack
def MapAttacksWhite(board):
    # Attacked by White and Black
    AttackedByWhite = [[False for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if (board[i][j] == "P"):
                # on edge
                if (j == 0):
                    AttackedByWhite[i + 1][j + 1] = True
                    continue
                if (j == 7):
                    AttackedByWhite[i + 1][j - 1] = True
                    continue
                # not on edge
                AttackedByWhite[i + 1][j - 1] = True
                AttackedByWhite[i + 1][j + 1] = True
            if (board[i][j] == "N"):
                di = [-2, -1, 1, 2, 2, 1, -1, -2]
                dj = [1, 2, 2, 1, -1, -2, -2, -1]
                for k in range(8):
                    if (0 <= i + di[k] <= 7 and 0 <= j + dj[k] <= 7):
                        AttackedByWhite[i + di[k]][j + dj[k]] = True
            if (board[i][j] == "B"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (di == 0 or dj == 0): continue  # diagonal moves only
                        for k in range(1,10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByWhite[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "R"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if (not (di == 0 or dj == 0)): continue  # straight moves only
                        if (di == 0 and dj == 0): continue
                        for k in range(1,10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByWhite[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "Q"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        # mighty queen moving all directions
                        if(di == 0 and dj == 0):    continue
                        for k in range(1,10):
                            new_i = i + di * k
                            new_j = j + dj * k
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                            AttackedByWhite[new_i][new_j] = True
                            if (board[new_i][new_j] != "E"): break
            if (board[i][j] == "K"):
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if(di == 0 and dj == 0): continue
                        # humble king moving all directions, but once
                        new_i = i + di
                        new_j = j + dj
                        if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): continue
                        AttackedByWhite[new_i][new_j] = True
    return AttackedByWhite
def PossibleMoves(board, turn):
    if(turn == "W"):
        MechanicalMoves = []
        #At first, mechanical moves are considered only, i.e., no king's saftey verification
        for i in range(8):
            for j in range(8):
                if (board[i][j] == "P"):
                    #Advancing from second rank
                    if (i == 1 and board[i + 1][j] == "E" and board[i + 2][j] == "E"): MechanicalMoves.append([i, j, i + 2, j])
                    if (i == 1 and board[i + 1][j] == "E"): MechanicalMoves.append([i, j, i + 1, j])
                    #Advancing from seventh rank - promotion!
                    if (i == 6 and board[i + 1][j] == "E"):
                        MechanicalMoves.append([i, j, i + 1, j,"N"])
                        MechanicalMoves.append([i, j, i + 1, j,"B"])
                        MechanicalMoves.append([i, j, i + 1, j,"R"])
                        MechanicalMoves.append([i, j, i + 1, j,"Q"])
                    #Advancing from any other rank
                    if (2 <= i <= 5 and board[i + 1][j] == "E"): MechanicalMoves.append([i, j, i + 1, j])
                    #Left Capturing from seventh rank
                    if (i == 6 and j > 0 and IsABlackPiece(board[i+1][j-1])):
                        MechanicalMoves.append([i, j, i + 1, j - 1, "N"])
                        MechanicalMoves.append([i, j, i + 1, j - 1, "B"])
                        MechanicalMoves.append([i, j, i + 1, j - 1, "R"])
                        MechanicalMoves.append([i, j, i + 1, j - 1, "Q"])
                    #Right Capturing from seventh rank
                    if (i == 6 and j < 7 and IsABlackPiece(board[i + 1][j + 1])):
                        MechanicalMoves.append([i, j, i + 1, j + 1, "N"])
                        MechanicalMoves.append([i, j, i + 1, j + 1, "B"])
                        MechanicalMoves.append([i, j, i + 1, j + 1, "R"])
                        MechanicalMoves.append([i, j, i + 1, j + 1, "Q"])
                    # Left Capturing from any rank
                    if (i < 6 and j > 0 and IsABlackPiece(board[i + 1][j - 1])):
                        MechanicalMoves.append([i, j, i + 1, j - 1])
                    # Right Capturing from any rank
                    if (i < 6 and j < 7 and IsABlackPiece(board[i + 1][j + 1])):
                        MechanicalMoves.append([i, j, i + 1, j + 1])
                if (board[i][j] == "N"):
                    di = [-2, -1, 1, 2, 2, 1, -1, -2]
                    dj = [1, 2, 2, 1, -1, -2, -2, -1]
                    for k in range(8):
                        if (not(0 <= i + di[k] <= 7 and 0 <= j + dj[k] <= 7)): continue
                        if (board[i + di[k]][j + dj[k]] == "E" or IsABlackPiece(board[i + di[k]][j + dj[k]])):
                            MechanicalMoves.append([i, j, i + di[k],j  + dj[k]])
                if (board[i][j] == "B"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (di == 0 or dj == 0): continue  # diagonal moves only
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if(IsABlackPiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "R"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (not (di == 0 or dj == 0)): continue  # straight moves only
                            if (di == 0 and dj == 0): continue
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if (IsABlackPiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "Q"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            # mighty queen moving all directions
                            if (di == 0 and dj == 0):    continue
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if (IsABlackPiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "K"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (di == 0 and dj == 0): continue
                            # humble king moving all directions, but once
                            new_i = i + di
                            new_j = j + dj
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): continue
                            if (board[new_i][new_j] == "E" or IsABlackPiece(board[new_i][new_j])):
                                MechanicalMoves.append([i, j, new_i, new_j])
        #Validate each Mechanical Moves by verifying king's safety
        PossibleMoves = []
        for move in MechanicalMoves:
            NewBoard = copy.deepcopy(board)
            a = move[0]
            b = move[1]
            c = move[2]
            d = move[3]
            NewBoard[c][d] = NewBoard[a][b]
            NewBoard[a][b] = "E"
            if(len(move) == 5): NewBoard[c][d] = move[4] #promotion
            Attacked = MapAttacksBlack(NewBoard)
            #Find King
            found = False
            for i in range(8):
                for j in range(8):
                    if(NewBoard[i][j] == "K"):
                        found = True
                        King_i = i
                        King_j = j
                        break
                    if(found): break
            #If king attacked, continue
            if(Attacked[King_i][King_j]): continue
            #Safe to add to possible moves
            PossibleMoves.append(move)
        #Is the king in check?
        Attacked = MapAttacksBlack(board)
        found = False
        for i in range(8):
            for j in range(8):
                if (board[i][j] == "K"):
                    found = True
                    King_i = i
                    King_j = j
                    break
                if (found): break
        KingInCheck = Attacked[King_i][King_j]
        #Verify if this position is a stalemate draw
        if (len(PossibleMoves) == 0 and not(KingInCheck)): PossibleMoves = "DRAW"
        #Verify if Black wins by check mate
        if (len(PossibleMoves) == 0 and KingInCheck): PossibleMoves = "BLACK WINS - MATE"
    else:
        MechanicalMoves = []
        # At first, mechanical moves are considered only, i.e., no king's saftey verification
        for i in range(8):
            for j in range(8):
                if (board[i][j] == "p"):
                    # Advancing from second rank
                    if (i == 6 and board[i - 1][j] == "E" and board[i - 2][j] == "E"): MechanicalMoves.append([i, j, i + 2, j])
                    if (i == 6 and board[i - 1][j] == "E"): MechanicalMoves.append([i, j, i + 1, j])
                    # Advancing from seventh rank - promotion!
                    if (i == 1 and board[i - 1][j] == "E"):
                        MechanicalMoves.append([i, j, i - 1, j, "N"])
                        MechanicalMoves.append([i, j, i - 1, j, "B"])
                        MechanicalMoves.append([i, j, i - 1, j, "R"])
                        MechanicalMoves.append([i, j, i - 1, j, "Q"])
                    # Advancing from any other rank
                    if (2 <= i <= 5 and board[i - 1][j] == "E"): MechanicalMoves.append([i, j, i - 1, j])
                    # Left Capturing from seventh rank
                    if (i == 1 and j > 0 and IsAWhitePiece(board[i - 1][j - 1])):
                        MechanicalMoves.append([i, j, i - 1, j - 1, "N"])
                        MechanicalMoves.append([i, j, i - 1, j - 1, "B"])
                        MechanicalMoves.append([i, j, i - 1, j - 1, "R"])
                        MechanicalMoves.append([i, j, i - 1, j - 1, "Q"])
                    # Right Capturing from seventh rank
                    if (i == 1 and j < 7 and IsAWhitePiece(board[i + 1][j + 1])):
                        MechanicalMoves.append([i, j, i - 1, j + 1, "N"])
                        MechanicalMoves.append([i, j, i - 1, j + 1, "B"])
                        MechanicalMoves.append([i, j, i - 1, j + 1, "R"])
                        MechanicalMoves.append([i, j, i - 1, j + 1, "Q"])
                    # Left Capturing from any rank
                    if (i > 1 and j > 0 and IsAWhitePiece(board[i - 1][j - 1])):
                        MechanicalMoves.append([i, j, i - 1, j - 1])
                    # Right Capturing from any rank
                    if (i > 1 and j < 7 and IsAWhitePiece(board[i - 1][j + 1])):
                        MechanicalMoves.append([i, j, i - 1, j + 1])
                if (board[i][j] == "n"): #*** continue
                    di = [-2, -1, 1, 2, 2, 1, -1, -2]
                    dj = [1, 2, 2, 1, -1, -2, -2, -1]
                    for k in range(8):
                        if (not (0 <= i + di[k] <= 7 and 0 <= j + dj[k] <= 7)): continue
                        if (board[i + di[k]][j + dj[k]] == "E" or IsAWhitePiece(board[i + di[k]][j + dj[k]])):
                            MechanicalMoves.append([i, j, i + di[k], j + dj[k]])
                if (board[i][j] == "b"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (di == 0 or dj == 0): continue  # diagonal moves only
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if (IsAWhitePiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "r"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (not (di == 0 or dj == 0)): continue  # straight moves only
                            if (di == 0 and dj == 0): continue
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if (IsAWhitePiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "q"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            # mighty queen moving all directions
                            if (di == 0 and dj == 0):    continue
                            for k in range(1, 10):
                                new_i = i + di * k
                                new_j = j + dj * k
                                if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): break
                                if (board[new_i][new_j] == "E"):
                                    MechanicalMoves.append([i, j, new_i, new_j])
                                    continue
                                if (IsAWhitePiece(board[new_i][new_j])): MechanicalMoves.append([i, j, new_i, new_j])
                                break
                if (board[i][j] == "k"):
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if (di == 0 and dj == 0): continue
                            # humble king moving all directions, but once
                            new_i = i + di
                            new_j = j + dj
                            if (not (0 <= new_i <= 7 and 0 <= new_j <= 7)): continue
                            if (board[new_i][new_j] == "E" or IsAWhitePiece(board[new_i][new_j])):
                                MechanicalMoves.append([i, j, new_i, new_j])
        # Validate each Mechanical Moves by verifying king's safety
        PossibleMoves = []
        for move in MechanicalMoves:
            NewBoard = copy.deepcopy(board)
            a = move[0]
            b = move[1]
            c = move[2]
            d = move[3]
            NewBoard[c][d] = NewBoard[a][b]
            NewBoard[a][b] = "E"
            if (len(move) == 5): NewBoard[c][d] = move[4]  # promotion
            Attacked = MapAttacksWhite(NewBoard)
            # Find King
            found = False
            for i in range(8):
                for j in range(8):
                    if (NewBoard[i][j] == "k"):
                        found = True
                        King_i = i
                        King_j = j
                        break
                    if (found): break
            # If king attacked, continue
            if (Attacked[King_i][King_j]): continue
            # Safe to add to possible moves
            PossibleMoves.append(move)
        # Is the king in check?
        Attacked = MapAttacksWhite(board)
        found = False
        for i in range(8):
            for j in range(8):
                if (board[i][j] == "k"):
                    found = True
                    King_i = i
                    King_j = j
                    break
                if (found): break
        KingInCheck = Attacked[King_i][King_j]
        # Verify if this position is a stalemate draw
        if (len(PossibleMoves) == 0 and not (KingInCheck)): PossibleMoves = "DRAW"
        # Verify if Black wins by check mate
        if (len(PossibleMoves) == 0 and KingInCheck): PossibleMoves = "WHITE WINS - MATE"
    return PossibleMoves
def Step1_ListValidPosition(turn):
    global conn
    #List all valid position off the analysed case and store then in a database
    #Initiate database
    cur = conn.cursor()
    if (turn == "W"):
        cur.execute('''CREATE TABLE PositionsBlackToPlay (
                        IdentifierNumber PRIMARY KEY,
                        MateIn TINYINT,
                        Destinations TEXT
                        )''')
        conn.commit()
        cur.execute('''CREATE TABLE PositionsWhiteToPlay (
                        IdentifierNumber PRIMARY KEY,
                        MateIn TINYINT,
                        Destinations TEXT
                        )''')
        conn.commit()
    #Try all combinations of positions
    aux = [-1,0,0,0,0,0,0,0]
    done = -1
    TotalFound = 0
    DrawFound = 0
    MateFound = 0
    init = time.time()
    while(True):
        #Monitor Progress
        done += 1
        if (done % 10 ** 3 == 1):
            print("Done: {:.4f}% TotalFound: {} DrawFound: {} MateFound: {} Time: {:.4f}s".format(
                100 * done / (8 ** 8), TotalFound, DrawFound, MateFound, time.time() - init))
            init = time.time()
            conn.commit()
        #Increment
        WeAreDone = False
        for i in range(8):
            aux[i] += 1
            if (aux[i] == 8):
                if (i == 7):
                    WeAreDone = True
                    break
                aux[i] = 0
            else:
                break
        if (WeAreDone): break
        # Continue if bishop in black square
        if ((aux[6] % 2 == 0) and (aux[7] % 2 == 1)): continue
        if ((aux[6] % 2 == 1) and (aux[7] % 2 == 0)): continue
        # Continue if pieces overlap
        if (aux[0] == aux[2] and aux[1] == aux[3]): continue
        if (aux[0] == aux[4] and aux[1] == aux[5]): continue
        if (aux[0] == aux[6] and aux[1] == aux[7]): continue
        if (aux[2] == aux[4] and aux[3] == aux[5]): continue
        if (aux[2] == aux[6] and aux[3] == aux[7]): continue
        if (aux[4] == aux[6] and aux[5] == aux[7]): continue
        # Kings too close
        ProblemHere = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (aux[0] == aux[2] + i and aux[1] == aux[3] + j): ProblemHere = True
        if (ProblemHere): continue
        # Fill the board
        board = [["E" for _ in range(8)] for _ in range(8)]
        board[aux[0]][aux[1]] = 'K'
        board[aux[2]][aux[3]] = 'k'
        board[aux[4]][aux[5]] = 'N'
        board[aux[6]][aux[7]] = 'B'
        #Black king attacked by White during White' turn
        if(turn == "W"):
            Attacked = MapAttacksWhite(board)
            BlackKingInDanger = False
            for i in range(8):
                for j in range(8):
                    if(board[i][j] == "k" and Attacked[i][j]):
                        BlackKingInDanger = True
            if (BlackKingInDanger): continue
        #We have a valid position - build identifier
        TotalFound += 1
        factor = 1
        MyIdentifier = 0
        for i in range(8):
            MyIdentifier += aux[i] * factor
            factor *= 16
        #Check all future positions
        Destinations = ""
        PossibleMovesArray = PossibleMoves(board,turn)
        #Is it a draw?
        if(PossibleMovesArray == "DRAW"):
            cur.executemany("INSERT INTO PositionsBlackToPlay VALUES (?,?,?)", [(MyIdentifier, 60, "")])
            DrawFound += 1
            continue
        #Is it a mate?
        if (PossibleMovesArray == "WHITE WINS - MATE"):
            cur.executemany("INSERT INTO PositionsBlackToPlay VALUES (?,?,?)", [(MyIdentifier, 0, "")])
            MateFound += 1
            continue
        #If we got here, some moves are available
        for move in PossibleMovesArray:
            NewAux = copy.deepcopy(aux)
            if (NewAux[0] == move[0] and NewAux[1] == move[1]):
                NewAux[0] = move[2]
                NewAux[1] = move[3]
            if (NewAux[2] == move[0] and NewAux[3] == move[1]):
                NewAux[2] = move[2]
                NewAux[3] = move[3]
            if (NewAux[4] == move[0] and NewAux[5] == move[1]):
                NewAux[4] = move[2]
                NewAux[5] = move[3]
            if (NewAux[6] == move[0] and NewAux[7] == move[1]):
                NewAux[6] = move[2]
                NewAux[7] = move[3]
            factor = 1
            NewIdentifier = 0
            for i in range(8):
                NewIdentifier += NewAux[i] * factor
                factor *= 16
            Destinations += str(NewIdentifier) + "#"
        #Write to database
        if (turn == "W"):
            cur.executemany("INSERT INTO PositionsWhiteToPlay VALUES (?,?,?)", [(MyIdentifier, 100,Destinations)])
        else:
            cur.executemany("INSERT INTO PositionsBlackToPlay VALUES (?,?,?)", [(MyIdentifier, 100,Destinations)])
    print("Final--> TotalFound: {} DrawFound: {} MateFound: {}".format(TotalFound, DrawFound, MateFound))
    conn.commit()
def Step2_ListDrawsByBlackCapture():
    global conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM PositionsBlackToPlay")
    done = -1
    DrawsFound = 0
    init = time.time()
    for Position in cur:
        done += 1
        if (done % 1000 == 1):
            print("Done: {:.4f}% DrawFound: {} time: {:.4f}s".format(100 * done / 6830292,DrawsFound, time.time() - init))
            conn.commit()
            init = time.time()
        if(Position[1] != 100): continue
        #Calculate Board
        IdentifierNumber = int(Position[0])
        MyAux = [0 for _ in range(8)]
        for i in range(8):
            MyAux[i] = int(IdentifierNumber % 16)
            IdentifierNumber -= MyAux[i]
            IdentifierNumber /= 16
        IdentifierNumber = int(Position[0])
        board = [["E" for _ in range(8)] for _ in range(8)]
        board[MyAux[0]][MyAux[1]] = 'K'
        board[MyAux[2]][MyAux[3]] = 'k'
        board[MyAux[4]][MyAux[5]] = 'N'
        board[MyAux[6]][MyAux[7]] = 'B'
        AttacksBlack = MapAttacksBlack(board)
        AttacksWhite = MapAttacksWhite(board)
        DrawByCapture = False
        if (AttacksBlack[MyAux[6]][MyAux[7]] and not (AttacksWhite[MyAux[6]][MyAux[7]])): DrawByCapture = True
        if (AttacksBlack[MyAux[4]][MyAux[5]] and not (AttacksWhite[MyAux[4]][MyAux[5]])): DrawByCapture = True
        if (DrawByCapture):
            conn.execute("UPDATE PositionsBlackToPlay SET MateIn = 60 WHERE IdentifierNumber = {}".format(IdentifierNumber))
            DrawsFound += 1
    print("Finish --> Found {} Draws".format(DrawsFound))
    conn.commit()
def Step3_LookAtNextPositions(turn):
    global conn
    cur = conn.cursor()
    cur2 = conn.cursor()
    if (turn == "B"): cur.execute("SELECT * FROM PositionsBlackToPlay")
    if (turn == "W"): cur.execute("SELECT * FROM PositionsWhiteToPlay")
    if (turn == "B"): TotalPositions = 6830292
    if (turn == "W"): TotalPositions = 5437752
    done = -1
    DrawsFound = 0
    MatesFound = [0 for _ in range(60)]
    UndefFound = 0
    NewDraw = 0
    NewMate = 0
    init = time.time()
    for Position in cur:
        #Monitor Progress
        done += 1
        if (done % 1000 == 1):
            print("Done: {:.4f}% DrawsFound: {} MatesFound: {} in {:.4f}s"
                  .format(100 * done / TotalPositions, NewDraw, NewMate, time.time() - init))
            init = time.time()
            conn.commit()
        #Process
        if(Position[1] == 60):
            DrawsFound += 1
            continue
        if (0 <= Position[1] <= 59):
            MatesFound[Position[1]] += 1
            continue
        #Initiate Flags
        AllMates = True
        SomeMate = False
        AllDraws = True
        SomeDraw = False
        GreatestMateIn = -10
        SmallestMateIn = 100
        Destinations = Position[2]
        Destinations = Destinations.split("#")
        Destinations.pop()
        for DestPosition in Destinations:
            if (turn == "B"):
                cur2.execute("SELECT * FROM PositionsWhiteToPlay WHERE IdentifierNumber = {}".format(int(DestPosition)))
            if (turn == "W"):
                cur2.execute("SELECT * FROM PositionsBlackToPlay WHERE IdentifierNumber = {}".format(int(DestPosition)))
            NextMateIn = cur2.fetchall()
            NextMateIn = NextMateIn[0][1]
            #Update Flags
            if (NextMateIn == 60):
                SomeDraw = True
            else:
                AllDraws = False
            if (0 <= NextMateIn <= 59):
                SomeMate = True
            else:
                AllMates = False
            #Update Greatest and Smallest
            if (NextMateIn < SmallestMateIn): SmallestMateIn = NextMateIn
            if (NextMateIn > GreatestMateIn): GreatestMateIn = NextMateIn
        #Verify if new status (MateIn) was found
        if (turn == "W"):
            if (SomeMate):
                cur2.execute(
                    "UPDATE PositionsWhiteToPlay SET MateIn = {} WHERE IdentifierNumber = {}"
                        .format(SmallestMateIn + 1, Position[0]))
                NewMate += 1
                MatesFound [SmallestMateIn + 1] += 1
                continue
            if (AllDraws):
                cur2.execute(
                    "UPDATE PositionsWhiteToPlay SET MateIn = {} WHERE IdentifierNumber = {}"
                        .format(60, Position[0]))
                DrawsFound += 1
                NewDraw += 1
                continue
        if (turn == "B"):
            if (SomeDraw):
                cur2.execute(
                    "UPDATE PositionsBlackToPlay SET MateIn = {} WHERE IdentifierNumber = {}"
                        .format(60, Position[0]))
                DrawsFound += 1
                NewDraw += 1
                continue
            if (AllMates):
                cur2.execute(
                    "UPDATE PositionsBlackToPlay SET MateIn = {} WHERE IdentifierNumber = {}"
                        .format(GreatestMateIn, Position[0]))
                NewMate += 1
                MatesFound[GreatestMateIn] += 1
                continue
        UndefFound += 1
    conn.commit()
    print("Finished NewDrawsFound: {} NewMatesFound: {}".format(NewDraw, NewMate))
    f = open("{}_LOG.txt".format(int(time.time())),"w")
    if (turn == "W"): f.write("White to Play\n")
    if (turn == "B"): f.write("Black to Play\n")
    f.write("New Draws Found:       {}\n".format(NewDraw))
    f.write("New Mates Found:       {}\n".format(NewMate))
    f.write("Total Draws Found:     {}\n".format(DrawsFound))
    f.write("Total Undefined Found: {}\n".format(UndefFound))
    for i in range(10):
        f.write("MateIn0{} Found:   {}\n".format(i,MatesFound[i]))
    for i in range(10,60):
        f.write("MateIn{} Found:    {}\n".format(i,MatesFound[i]))
    f.close()


conn = sqlite3.connect('Database.db')
#TestOnly()
#Step1_ListValidPosition("W")
#Step1_ListValidPosition("B")
#Step2_ListDrawsByBlackCapture()
for _ in range(15): #one cycle took approximatly 40 min
    Step3_LookAtNextPositions("W")
    Step3_LookAtNextPositions("B")
conn.close()
exit(0)

