from referee import Action, SpawnAction, SpreadAction, HexPos, HexDir

class BoardState:
    # a list of all coordinates on the hex board (with a range and domain of 0 to 7)
    grid_coords = [(r, q) for r in range(0, 7) for q in range(0, 7)]


    def __init__(self, board, history, depth, agentColor):
        '''board is a dictionary of (r, q) coordinates and (p, k) cell states'''
        self.board = board
        self.history = history
        self.depth = depth
        self.agentColor = agentColor
        # The set of visited states is only stored in the root node. Note that 'visited' states means a node that has had its children generated
        self.visited_states = set()


    def get_spreadmoves(self):
        '''Return a list of all possible spreadmoves from the current board state'''
        spreadmoves = []
        for ((x, y), (player, k)) in self.board.items():
            if (player == self.agentColor):
                spreadmoves += self.generate_spreadmoves(x, y)
        return spreadmoves
    
    def get_spawnmoves(self):
        '''Return a list of all possible spawnmoves from the current board state'''
        spawnmoves = []
        for coord in self.grid_coords:
            if coord not in self.board:
                spawnmoves.append(SpawnAction(HexPos(coord[0], coord[1])))
        return spawnmoves

    def generate_spreadmoves(self, x, y):
        """
        Returns a list of all possible moves for a given tile, ie. is of form [(r,q,dr,dq)].
        Basically just generates 6 moves for each hexagonal direction
        """
        moves = []
        for dir in HexDir:
            moves.append(SpreadAction(HexPos(x, y), dir))
        return moves

    def update_history(self, move):
        '''Update the history of the board state with the given move'''
        self.history.append(move)
    
    def is_valid_gamestate(self):
        '''Validate the board state, ensuring the total power of all tiles does not exceed 49'''
        total_power = self.get_total_power(self.board)
        if total_power > 49:
            return False
        if self.depth > 343:
            return False
        return True
    
    def get_total_power(board):
        '''Get the total power of all tiles on the board'''
        total_power = 0
        for ((r, q), (player, k)) in board.items():
            total_power += k
        return total_power
        
    def get_f_score(self):
        '''get f score: f = g + h'''
        return self.get_path_cost() + self.simple_heuristic_3()
    
    def get_board_net_score(self, board):
        '''get the net score of a given board. This is the difference between the player power and opponent power
        Note that a board parameter is required as this function may be used to calculate the net score of a potential board, and not always the present board'''

        return self.get_my_power(board) - self.get_opp_power(board)
    
    def calculate_move_impact(self, move):
        '''Calculate the net gain/loss of a given move'''
        return self.get_board_net_score(self.get_new_boardstate(move)) - self.get_board_net_score(self.board)
    
    def update_boardstate(self, move, playerColour):
        """
        Given a move, update the boardState with the move, using get_new_boardstate
        """
        self.board = self.get_new_boardstate(move)
        self.depth += 1

    
    def get_new_boardstate(self, move, playerColour):
        '''Get the new board state after a given move'''
        match move:
            case SpawnAction(cell):
                new_board = self.board.copy()
                new_board[(cell.r, cell.q)] = (playerColour, 1)
                return new_board
            
            case SpreadAction(cell, direction):
                cell_power_count = 1
                new_board = self.board.copy()
                match direction:
                    case HexDir.DownRight:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the down right direction
                            existing_power = new_board[(cell.r, cell.q + cell_power_count)][1]

                            if (existing_power < 6):
                                new_board[(cell.r, cell.q + cell_power_count)] = (playerColour, existing_power + 1)

                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r, cell.q + cell_power_count))

                            cell_power_count += 1
                            return new_board
                        
                    case HexDir.Down:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the down direction
                            existing_power = new_board[(cell.r - cell_power_count, cell.q + cell_power_count)][1]

                            if (existing_power < 6):
                                new_board[(cell.r - cell_power_count, cell.q + cell_power_count)] = (playerColour, existing_power + 1)

                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r - cell_power_count, cell.q + cell_power_count))

                            cell_power_count += 1
                            return new_board
                        
                    case HexDir.DownLeft:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the down left direction
                            existing_power = new_board[(cell.r - cell_power_count, cell.q)][1]

                            if (existing_power < 6):
                                new_board[(cell.r - cell_power_count, cell.q)] = (playerColour, existing_power + 1)

                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r - cell_power_count, cell.q))

                            cell_power_count += 1
                            return new_board
                        
                    case HexDir.UpLeft:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the up left direction
                            existing_power = new_board[(cell.r, cell.q - cell_power_count)][1]

                            if (existing_power < 6):
                                new_board[(cell.r, cell.q - cell_power_count)] = (playerColour, existing_power + 1)
                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r, cell.q - cell_power_count))

                            cell_power_count += 1
                            return new_board
                        
                    case HexDir.Up:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the up direction
                            existing_power = new_board[(cell.r + cell_power_count, cell.q - cell_power_count)][1]

                            if (existing_power < 6):
                                new_board[(cell.r + cell_power_count, cell.q - cell_power_count)] = (playerColour, existing_power + 1)

                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r + cell_power_count, cell.q - cell_power_count))

                            cell_power_count += 1
                            return new_board
                        
                    case HexDir.UpRight:
                        while cell_power_count <= self.board[(cell.r, cell.q)][1]:
                            # place a new tile in the up right direction
                            existing_power = new_board[(cell.r + cell_power_count, cell.q)][1]

                            if (existing_power < 6):
                                new_board[(cell.r + cell_power_count, cell.q)] = (playerColour, existing_power + 1)
                            
                            else:
                                # if the tile is at max power, it will be emptied, ie. removed from the board
                                new_board.pop((cell.r + cell_power_count, cell.q))
                                
                            cell_power_count += 1
                            return new_board
                        

    def simple_heuristic(self):
        '''simple heuristic 1. Counts how many blue tiles are on the board'''
        blue_power = 2 * len(self.get_blue_tiles())
        return blue_power
    
    def simple_heuristic_2(self):
        '''simple heuristic 2. This takes into account the linear groupings of blue tiles. E.g. if there are adjacent blue tiles in a row
            or column, it will be more likely that they will be taken in the same spread action
            This heuristic totals the blue tiles, and subtracts the number of blue tiles that are in a linear grouping'''
        blue_power = len(self.get_blue_tiles())
        blue_power -= self.get_linear_blue_groupings()
        return blue_power
    
    def simple_heuristic_3(self):
        '''simple heuristic 3. This finds the distance between the closest red and blue tiles'''
        running_total = 0
        if (len(self.get_blue_tiles()) == 0):
            return 0
        
        # this is a list of all used red tiles in computing closest red tile to each blue tile.
        # this is kept unique to ensure the heuristic is more accurate
        used_red_tiles = []
        for blue_tile in self.get_blue_tiles():
            running_total += self.get_distance_to_closest_red_tile(blue_tile, used_red_tiles)
        return running_total

    def get_linear_blue_groupings(self):
        '''Function which counts how many blue tiles are in a linear grouping. E.g. if there are adjacent blue tiles in a row
            Used in heuristic 2'''
        linear_groupings = set()
        tiles = {"r": [], "b": []}

        # Build a split dictionary of all red and blue tiles
        for ((r, q), (player, k)) in self.board.items():
            tiles[player].append((r, q))

        # Check if each blue tile is adjacent to any other blue tile
        for (r1, q1) in tiles["b"]:
            for (r2, q2) in tiles["b"]:
                if self.tiles_are_adjacent(r1, q1, r2, q2):
                    linear_groupings.add((r1, q1))
                    linear_groupings.add((r2, q2))
        return len(linear_groupings)
    
    def get_distance_to_closest_red_tile(self, blue_tile, used_red_tiles):
        '''Function which returns the distance to the closest red tile for a given blue tile
        Used in heuristic 3'''
        min_dist = 7
        for (r, q), (player, k) in self.get_red_tiles():
            dr, dq = self.get_r_q_distances_between_two_tiles(blue_tile[0][0], blue_tile[0][1], r, q)
            if dr + dq < min_dist and (r, q) not in used_red_tiles:
                min_dist = dr + dq
                used_red_tiles.append((r, q))
        return min_dist
    
    def get_r_q_distances_between_two_tiles(self, r1, q1, r2, q2):
        '''Get the (r, q) distances between two tiles on the board, accounting for wrapping around the edges'''
        dr = abs(r1 - r2)
        dq = abs(q1 - q2)
        if dr > 3:
            dr = 7 - dr
        if dq > 3:
            dq = 7 - dq
        return dr, dq

    def distance_between_closest_two_tiles(self):
        '''Get the minimum distance between any two red and blue tiles on the board'''
        min_dist_r = 7
        min_dist_q = 7
        tiles = {"r": [], "b": []}
        for ((r, q), (player, k)) in self.board.items():
            tiles[player].append((r, q))
        for (r1, q1) in tiles["r"]:
            for (r2, q2) in tiles["b"]:
                dr, dq = self.get_r_q_distances_between_two_tiles(r1, q1, r2, q2)
                if dr < min_dist_r:
                    min_dist_r = dr
                if dq < min_dist_q:
                    min_dist_q = dq

        # Return the square root of the sum of the squares of the minimum distances between red and blue tiles
        return (min_dist_r ** 2 + min_dist_q ** 2) ** 0.5
    
    def get_my_power(self, board):
        '''Get the combined power of all player tiles on the board
        This also requires a board parameter as often it is used for potential boards, and not the present board'''
        my_power = 0
        for ((r, q), (player, k)) in board.items():
            if player == self.agentColor:
                my_power += k
        return my_power
    
    def get_my_tiles(self):
        '''Gets all the player tiles on the given board'''
        my_tiles = []
        for ((r, q), (player, k)) in self.board.items():
            if player == self.agentColor:
                my_tiles.append(((r, q), (player, k)))
        return my_tiles
    
    def get_opp_tiles(self, board):
        '''Gets all the opp tiles on the given board parameter'''
        opp_tiles = []
        for ((r, q), (player, k)) in board.items():
            if player != self.agentColor:
                opp_tiles.append(((r, q), (player, k)))
        return opp_tiles
    
    def tiles_are_adjacent(self, r1, q1, r2, q2):
        '''Check if two tiles are adjacent to each other'''
        dr, dq = self.get_r_q_distances_between_two_tiles(r1, q1, r2, q2)
        if dr <= 1 and dq <= 1:
            return True
        return False
    
    def red_tiles_are_adjacent_to_blue_tiles(self):
        '''Check if any of the red tiles on the board are adjacent to any of the blue tiles on the board'''
        tiles = {"r": [], "b": []}
        for ((r, q), (player, k)) in self.board.items():
            tiles[player].append((r, q))
        for (r1, q1) in tiles["r"]:
            for (r2, q2) in tiles["b"]:
                if self.tiles_are_adjacent(r1, q1, r2, q2):
                    return True
        return False

    def red_power_higher_than_parent(self):
        '''Determine if the red power of this boardstate is higher than the red power of the parent state'''
        this_boardstate_red_power = self.get_red_power()
        parent_boardstate_red_power = self.parent.get_red_power()
        if this_boardstate_red_power > parent_boardstate_red_power:
            return True
        return False