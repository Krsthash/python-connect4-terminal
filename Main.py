#!/usr/bin/env python3
from curses import textpad
import gameLogic
import curses

class Board():
    def __init__(self, y, x, player):
        self.player = player  # Default first player goes first
        self.y = y
        self.x = x
        self.cursorPos = 0
        self.board = gameLogic.Game(y, x)
        self.win = curses.newwin(self.y + 2, self.x + 2, 2, 2)
        self.cursor_win = curses.newwin(1, self.x * 2 + 2, 2, 2)
    
    def drawBoard(self):
        # Drawing the game map on the screen
        for y in range(len(self.board.map)):
            for x in range(len(self.board.map[y])):
                if self.board.map[y][x] == 0:
                    self.win.addstr(y + 1, x, "⚪")
                elif self.board.map[y][x] == 1:
                    self.win.addstr(y + 1, x, "⚫", curses.color_pair(1))
                else:
                    self.win.addstr(y + 1, x, "⚫", curses.color_pair(2))

        self.win.refresh()

    def drawCursor(self):
        self.cursor_win.clear()
        if self.player == 1:
            self.cursor_win.addch(0, self.cursorPos, "⬇", curses.color_pair(1))
        else:
            self.cursor_win.addch(0, self.cursorPos, "⬇", curses.color_pair(2))
        self.cursor_win.refresh()

class InfoLine:
    def __init__(self, screen, y):
        self.maxy, self.maxx = screen.getmaxyx()
        self.y = y
        self.win = curses.newwin(1, self.maxx, self.y, 0)
    
    def write(self, text, colourtag = 3):
        self.win.addstr(0, 0, text + " " * (self.maxx - len(text) - 1), curses.color_pair(colourtag))
        self.win.refresh()


def draw_custom(stdscr, selected, enter, custom_opts):
    maxy, maxx = stdscr.getmaxyx()
    opts = ["-Width:", "-Height:", "-Player:", "Save"]
    win4 = curses.newwin(10, 30, (maxy // 2) - 5, (maxx // 2) - 15)
    textpad.rectangle(win4, 0, 0, 8, 29)
    win4.addstr(0, 2, "Options")
    win4.addstr(1, 1, "Custom size:")
    for idx, opt in enumerate(opts):
        if idx == selected:
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
            win4.attron(curses.color_pair(4))
            if idx != 3:
                win4.addstr(idx + 2, 1, str(opt) + f" {custom_opts[idx]}")
            else:
                win4.addstr(idx + 2, 1, str(opt))
            win4.attroff(curses.color_pair(4))
        else:
            if idx != 3:
                win4.addstr(idx + 2, 1, str(opt) + f" {custom_opts[idx]}")
            else:
                win4.addstr(idx + 2, 1, str(opt))
    if enter:
        curses.echo()
        s = ""
        while not s.isnumeric():
            win4.addstr(selected + 2, len(opts[selected]) + 2, "   ")
            s = str(win4.getstr(selected + 2, len(opts[selected]) + 2, 3).decode("utf-8"))
            stdscr.refresh()
        curses.noecho()
        return s
    win4.refresh()


def options(stdscr):
    global height
    global width
    global player
    selected = 0
    custom_opts = [7, 6, 0]
    while True:
        draw_custom(stdscr, selected, False, custom_opts)
        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected < 3:
            selected += 1
            draw_custom(stdscr, selected, False, custom_opts)
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1
            draw_custom(stdscr, selected, False, custom_opts)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if selected == 0:
                custom_opts[selected] = int(draw_custom(stdscr, selected, True, custom_opts))
            elif selected == 1:
                custom_opts[selected] = int(draw_custom(stdscr, selected, True, custom_opts))
            elif selected == 2:
                custom_opts[selected] = int(draw_custom(stdscr, selected, True, custom_opts))
            else:
                width = custom_opts[0]
                height = custom_opts[1]
                player = custom_opts[2]
                break


def main(stdscr):
    header = InfoLine(stdscr, 0)
    footer = InfoLine(stdscr, stdscr.getmaxyx()[0] - 1)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Player 1 colour
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Player 2 colour
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)  # Header/Footer colour
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Win colour
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)  # Error/Draw colour

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    game = Board(height, width, player)
    footer.write(f"Game started.")
    stdscr.refresh()

    while True:  # Game mainloop
        game.drawBoard()
        game.drawCursor()
        header.write(f"Terminal Connect Four  -  Size: {width}x{height}")
        footer.write(f"Player {game.player}'s turn...  |  [n] - New game    [q] - Quit    [o] - Options")
        stdscr.refresh()
        keyPressed = stdscr.getch()

        if keyPressed == ord("q"):
            return 1
        elif keyPressed == ord("o"):
            options(stdscr)
            stdscr.clear()
            stdscr.refresh()
        elif keyPressed == ord("n"):
            return 0
        elif keyPressed == curses.KEY_LEFT:
            if game.cursorPos > 1:
                game.cursorPos -= 2
        elif keyPressed == curses.KEY_RIGHT:
            if game.cursorPos <= game.x * 2 - 4:
                game.cursorPos += 2
        elif keyPressed == curses.KEY_ENTER or keyPressed == 10 or keyPressed == 13:
            drop = game.board.drop(game.player, game.cursorPos // 2)
            game.drawBoard()
            game.drawCursor()
            stdscr.refresh()
            win_check = game.board.piece_win_check(game.player)
            if win_check == True:
                header.write(f"Terminal Connect Four  -  Size: {height}x{width}", 4)
                winFooter = InfoLine(stdscr, stdscr.getmaxyx()[0] - 5)
                winFooter.write(f"Game has finished, player {game.player} won. Press any key to start a new game...", 4)
                footer.write(f"Player {game.player} won the game!  |  [n] - New game    [q] - Quit    [o] - Options", 4)
                stdscr.getch()
                return 0
            elif win_check == -1:
                header.write(f"Terminal Connect Four  -  Size: {height}x{width}", 4)
                winFooter = InfoLine(stdscr, stdscr.getmaxyx()[0] - 5)
                winFooter.write(f"Game has finished, it's a draw. Press any key to start a new game...", 5)
                footer.write(f"The board is full!  |  [n] - New game    [q] - Quit    [o] - Options", 5)
                stdscr.getch()
                return 0
            if drop != False:
                if game.player == 1: game.player = 2
                else: game.player = 1
        game.drawCursor()

if __name__ == '__main__':
    # Default map size for a new game (6x7)
    height = 6
    width = 7
    player = 1
    q = 0
    while q != 1:  # When the quit signal gets sent, quit.
        q = curses.wrapper(main)
