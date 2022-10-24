import random
from time import sleep
from playsound import playsound
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy

# sign variable to decide the turn of which player
sign = 0

# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]


# check if match is over
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


# Configure text on button while playing with another player
def get_text(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            board[i][j] = "X"
            button[i][j].config(text='X')
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
        else:
            board[i][j] = "O"
            button[i][j].config(text='O')
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
        sign += 1
        playsound('sound/click.wav')
    if winner(board, "X"):
        playsound('sound/success.wav')
        gb.destroy()
        box = messagebox.showinfo("Winner", "Player 1 won the match")
    elif winner(board, "O"):
        playsound('sound/success.wav')
        gb.destroy()
        box = messagebox.showinfo("Winner", "Player 2 won the match")
    elif(isfull()):
        playsound('sound/gameover.wav')
        gb.destroy()
        box = messagebox.showinfo("Tie Game", "Tie Game")


# Check if the player can push the button or not
def isfree(i, j):
    return board[i][j] == " "


# Check the board is full or not
def isfull():
    flag = True
    for i in board:
        if(i.count(' ') > 0):
            flag = False
    return flag


# Create the GUI of game board for play along with another player
def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(game_board, bd=5, command=get_t, height=3, width=6, font="arial 20 bold",
                                  bg="#237543", fg="white", activebackground="#237543", activeforeground="white")
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# Decide the next move of system
def pc():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner)-1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge)-1)
            return edge[move]


# Configure text on button while playing with system
def get_text_pc(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        button[i][j].config(text=board[i][j])
        sign += 1
        if sign % 2 == 1:
            playsound('sound/click.wav')
    x = True
    if winner(board, "X"):
        playsound('sound/success.wav')
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Player won the match")
    elif winner(board, "O"):
        playsound('sound/gameover.wav')
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Computer won the match")
    elif(isfull()):
        playsound('sound/gameover.wav')
        gb.destroy()
        x = False
        box = messagebox.showinfo("Tie Game", "Tie Game")
    if(x):
        if sign % 2 != 0:
            move = pc()
            button[move[0]][move[1]].config(state=DISABLED)
            get_text_pc(move[0], move[1], gb, l1, l2)


# Create the GUI of game board for play along with system
def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=3, width=6, font="arial 20 bold", bg="#237543", fg="white", activebackground="#237543", activeforeground="white")
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# Initialize the game board to play with system
def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.geometry("380x420+500+0")
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player 1 : X", width=12,
                padx=5, pady=5, font="arial 12 bold")

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Computer : O",
                width=12, state=DISABLED, padx=5, pady=5, font="arial 12 bold")

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)


# Initialize the game board to play with another player
def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.geometry("380x420+500+0")
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player 1 : X", width=12,
                padx=5, pady=5, font="arial 12 bold")

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Player 2 : O",
                width=12, state=DISABLED, padx=5, pady=5, font="arial 12 bold")

    l2.grid(row=2, column=1)
    gameboard_pl(game_board, l1, l2)


# main function
def play():
    root = Tk()
    root.geometry("500x500+500+0")
    root.title("Tic Tac Toe")
    wpc = partial(withpc, root)
    wpl = partial(withplayer, root)

    head = Label(root, text="Welcome to tic-tac-toe", bg="#237543",
                 fg="white", width=500, font='monospace 25 bold', bd=4)
    lf = LabelFrame(root, text="Choose play mode", bd=2,
                    relief=GROOVE, font="monospace 15 bold", padx=50, pady=20)
    lf.place(x=10, y=70, height=420, width=475)

    B1 = Button(lf, text="Single Player", command=wpc,
                activeforeground='white',
                activebackground="#25a000", bg="#237543",
                fg="white", width=500, bd=5, padx=10, pady=10, font="arial 15 bold")

    B2 = Button(lf, text="Multi Player", command=wpl, activeforeground='white',
                activebackground="#25a000", bg="#237543",
                fg="white", width=500, bd=5, padx=10, pady=10, font="arial 15 bold")

    B3 = Button(lf, text="Exit", command=root.quit, activeforeground='white',
                activebackground="#25a000", bg="#237543",
                fg="white", width=500, bd=5, padx=10, pady=10, font="arial 15 bold")
    head.pack(side='top')
    B1.pack(side='top')
    B2.pack(side='top')
    B3.pack(side='top')
    root.mainloop()


# Call main function
if __name__ == '__main__':
    play()
