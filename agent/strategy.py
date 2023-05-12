# A file where we define the strategies for our agent as classes.
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from .agentboard import BoardState

import random

class ParentStrategy:
    """
    A parent class for all strategies. Note that this class is not intended to be used directly.
    """
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the strategy.
        """
        self._color = color
        
    def action(self, board: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        pass

class RandomStrategy(ParentStrategy):
    """
    A strategy that makes a random move.
    """
    def action(self, board: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        pass

class OneMoveStrategy(ParentStrategy):
    """
    A strategy that makes a move with no look-ahead. Makes the move with the best immediate outcome.
    """
    def action(self, boardSt: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # OneMoveStrategy prioritises spread moves, choosing the spreadmove with the highest net gain.
        best_move = None
        best_gain = 0
        
        for spread in boardSt.get_spreadmoves(self._color):
            spread_gain = boardSt.calculate_move_impact(spread, self._color)
            if spread_gain > best_gain:
                best_move = spread
                best_gain = spread_gain
            elif best_move is None:
                best_move = spread
                best_gain = spread_gain

        # If the best spread move has net gain =< 1, and total board power < 48, it will spawn a cell next to an opponent cell with the highest power.
        best_opp_adjacent = 0
        if boardSt.get_total_power(boardSt.board) < 48 and best_gain <= 1:

            for spawn in boardSt.get_spawnmoves():
                opp_adjacent = boardSt.get_highest_opp_tile_adjacent(boardSt.board, self._color, spawn.cell)
                if opp_adjacent > best_opp_adjacent:
                    best_move = spawn
                    best_gain = 1
                    best_opp_adjacent = opp_adjacent
                elif best_move is None:
                    best_move = spawn
                    best_gain = 1
        
        boardSt = boardSt.get_new_boardstate(best_move, self._color)
        return best_move
    
class OneMoveStrategy2(ParentStrategy):
    """
    A strategy that makes a move with no look-ahead. Makes the move with the best immediate outcome.
    Different from OneMoveStrategy in that it will prioritise decreasing opponent power, not just increasing net gain.
    """
    def action(self, boardSt: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        

        # OneMoveStrategy prioritises spread moves, choosing the spreadmove with the highest net gain.
        best_move = None
        best_gain = 0
        
        for spread in boardSt.get_spreadmoves(self._color):
            # Firstly, check if spread move results in winning the game.
            if (boardSt.check_if_win(self._color, boardSt.get_new_boardstate(spread, self._color))):
                return spread
            # Otherwise, calculate the move that results in the biggest decrease in net opponent power.
            spread_gain = - (boardSt.calculate_move_opp_impact(spread, self._color))
            if spread_gain > best_gain:
                best_move = spread
                best_gain = spread_gain
            elif best_move is None:
                best_move = spread
                best_gain = spread_gain

        # If the best spread move has net gain =< 1, and total board power < 48, it will spawn a cell next to an opponent cell with the highest power.
        best_opp_adjacent = 0
        if boardSt.get_total_power(boardSt.board) < 48 and best_gain < 1:

            for spawn in boardSt.get_spawnmoves():
                opp_adjacent = boardSt.get_highest_opp_tile_adjacent(boardSt.board, self._color, spawn.cell)
                if opp_adjacent > best_opp_adjacent:
                    best_move = spawn
                    best_gain = 1
                    best_opp_adjacent = opp_adjacent
                elif best_move is None:
                    best_move = spawn
                    best_gain = 1
        return best_move

class TwoMoveStrategy(ParentStrategy):
    """
    Strategy that makes a move with one look-ahead. Makes the move with the best outcome after the next move.
    Predicts opponent's move using OneMoveStrategy.
    """
    def action(self, boardSt: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # TwoMoveStrategy prioritises spread moves, choosing the spreadmove with the highest net gain.
        best_move = None
        best_gain = 0
        running_gain = 0
        best_opp_move = None

        # Create a new OneMoveStrategy object to predict opponent's move.
        opp_strategy = OneMoveStrategy2(self._color.opponent, **referee)

        # Create a new OneMoveStrategy object to find the best move after the opponent's predicted move.
        next_turn_strategy = OneMoveStrategy2(self._color, **referee)

        # Iterate through all possible moves. Find the move with the highest net gain after the opponent's move.
        for spread in boardSt.get_spreadmoves(self._color):
            # Create a copy of the boardstate and calculate the net gain of the spread move.

            copyBoard = boardSt.copy()
            running_gain = copyBoard.calculate_move_impact(spread, self._color)
            copyBoard.board = copyBoard.get_new_boardstate(spread, self._color)

            # Check if spread move results in winning the game.
            if (copyBoard.check_if_win(self._color, copyBoard.board)):
                return spread
            
            # Predict opponent's move and calculate the net gain of the opponent's move.
            opp_move = opp_strategy.action(copyBoard, **referee)
            running_gain += copyBoard.calculate_move_impact(opp_move, self._color.opponent)
            copyBoard.board = copyBoard.get_new_boardstate(opp_move, self._color.opponent)

            # Ensure that we aren't trying to play from a game that has already been lost.
            # However, if the only possible move is a losing move, we will play it.
            # This 'last resort' case in is in the specific instance that a spawn move is not possible, 
            # and the only spread move possible is a losing move.
            if (copyBoard.check_if_win(self._color.opponent, copyBoard.board)):
                last_resort = spread
                continue

            # Then, find the spread move with the highest gain after the opponent's move.
            next_move = next_turn_strategy.action(copyBoard, **referee)
            running_gain += copyBoard.calculate_move_impact(next_move, self._color)
            copyBoard.board = copyBoard.get_new_boardstate(next_move, self._color)

            if running_gain > best_gain:
                best_move = spread
                best_gain = running_gain
                best_opp_move = opp_move
            elif best_move is None:
                best_move = spread
                best_gain = running_gain
                best_opp_move = opp_move


        # If the  total board power < 48, iterate through possible spawn moves to see if there is a spawn move that will result in the highest net gain after the opponent's move.
        if boardSt.get_total_power(boardSt.board) < 48:
            for spawn in boardSt.get_spawnmoves():
                # Create a copy of the boardstate and calculate the net gain of the spawn move.
                copyBoard = boardSt.copy()
                copyBoard.board = copyBoard.get_new_boardstate(spawn, self._color)
                running_gain = 1

                # Predict opponent's move and calculate the net gain of the opponent's move.
                opp_move = opp_strategy.action(copyBoard, **referee)
                running_gain += copyBoard.calculate_move_impact(opp_move, self._color.opponent)
                copyBoard.board = copyBoard.get_new_boardstate(opp_move, self._color.opponent)

                # delete this
                opp_copyBoard = copyBoard.board
                
                # Ensure that we aren't trying to play from a game that has already been lost.
                if (copyBoard.check_if_win(self._color.opponent, copyBoard.board)):
                    continue

                # Then, find the spread move with the highest gain after the opponent's move.
                next_move = next_turn_strategy.action(copyBoard, **referee)
                running_gain += copyBoard.calculate_move_impact(next_move, self._color)
                copyBoard.board = copyBoard.get_new_boardstate(next_move, self._color)
                
                if running_gain > best_gain:
                    best_move = spawn
                    best_gain = running_gain
                    best_opp_move = opp_move
                elif best_move is None:
                    best_move = spawn
                    best_gain = running_gain
                    best_opp_move = opp_move

        if best_move is None:
            return last_resort
        
        return best_move
    
class RandomStrategy(ParentStrategy):
    """
    A random strategy that makes a move with no look-ahead. 
    Randomly chooses to either place a tile or take a spread action.
    """
    def action(self, boardSt: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """

        # If it's the first turn, place a random tile. 
        if boardSt.get_total_power(boardSt.board) <= 1:
            coords_to_potentially_spawn_a_tile = boardSt.get_spawnmoves()
            return random.choice(coords_to_potentially_spawn_a_tile)
        
        # If the total board power <= 48, randomly choose to either place a tile or take a spread action.
        elif boardSt.get_total_power(boardSt.board) <= 48:
            if random.randint(0,1) == 0:
                coords_to_potentially_spawn_a_tile = boardSt.get_spawnmoves()
                return random.choice(coords_to_potentially_spawn_a_tile)
            else:
                potential_spreadmoves = boardSt.get_spreadmoves(self._color)
                # print(f"potential_spreadmoves: {potential_spreadmoves}")
                return random.choice(potential_spreadmoves)
            
class AlphaBetaStrategy(ParentStrategy):
    """
    A strategy that uses alpha-beta pruning to look ahead 2 turns. 
    """
    def action(self, boardSt: BoardState, **referee: dict) -> Action:
        """
        Return the next action to take.
        """

        