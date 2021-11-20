class Game():
    def __init__(self, mapY: int, mapX: int):
        # Previous move positions (used to calculate if the game has been won)
        self.last_pY = 0
        self.last_pX = 0

        self.mapY = mapY
        self.mapX = mapX
        # Creating the 2d array game map
        self.map = []
        for i in range(mapY):
            self.map.append([])
            for _ in range(mapX):
                self.map[i].append(0)

    def drop(self, player: int, row: int):
        """
        Function used to control the dropping of pieces into the board
        """

        if self.map[0][row] != 0:
            return False
        for i in range(self.mapY):
            if self.map[i][row] != 0:
                self.map[i-1][row] = player
                self.last_pY = i-1
                self.last_pX = row
                self.last_player = player
                return True
        self.last_pY = self.mapY-1
        self.last_pX = row
        self.last_player = player
        self.map[self.mapY-1][row] = player

    def piece_win_check(self, player):
        """
        After each turn, this function should run, checking if the game has been won.
        """
        map_full = True
        for y in range(len(self.map)):
            if map_full == False:
                break
            for x in range(len(self.map[y])):
                if self.map[y][x] == 0:
                    map_full = False
                    break
        if map_full:
            return -1

        touching = 0
        # Checking the y axis for any connected pieces
        for i in range(self.mapY):
            if self.map[i][self.last_pX] == player:
                touching += 1
            else:
                touching = 0  # The next piece is not the player's piece, resets the connected counter to 0
            if touching >= 4:
                return True  # Player won
            

        touching = 0
        # Checking the x axis for any connected pieces
        for i in range(self.mapX):
            if self.map[self.last_pY][i] == player:
                touching += 1
            else:
                touching = 0  # The next piece is not the player's piece, resets the connected counter to 0
            if touching >= 4:
                return True  # Player wins if 4 pieces are touching!

        touching = 0
        # Checking if there are any connected pieces on the first diagonal [\]
        if self.last_pY < self.last_pX:
            # finding the starting coordinates of the diagonal (first triangle)
            dY = 0
            dX = self.last_pX - self.last_pY
        else:
            # (first triangle)
            dX = 0
            dY = self.last_pY - self.last_pX

        i = 0
        while dY + i != self.mapY and dX + i != self.mapX:  # loop through all tiles until we hit an edge
            if self.map[dY + i][dX + i] == player:
                touching += 1
            else:
                touching = 0
            if touching >= 4:
                return True
            i += 1


        touching = 0
        # Checking if there are any connected pieces on the second diagonal [/]
        p2X = (self.mapX - 1) - self.last_pX  # X coordinates relative to the right edge (top right 0, 0)
        
        if p2X < self.last_pY:
            d2X = self.mapX - 1 # 0
            d2Y = self.last_pY - p2X
        else:
            d2Y = 0
            d2X = self.last_pX + self.last_pY

        i = 0
        while d2Y + i != self.mapY and d2X - i != -1:
            if self.map[d2Y + i][d2X - i] == player:
                touching += 1
            else:
                touching = 0
            if touching >= 4:
                return True
            i += 1

