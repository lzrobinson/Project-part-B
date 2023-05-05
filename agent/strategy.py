# A file where we define the strategies for our agent as classes.
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from .agentboard import BoardState

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

        for spread in boardSt.get_spreadmoves():
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
            print("gets here1")
            #for spawn in boardSt.get_spawnmoves():
                #print("spawn cell val: " + str(spawn.cell.r) + ", " + str(spawn.cell.q))

            for spawn in boardSt.get_spawnmoves():
                opp_adjacent = boardSt.get_highest_opp_tile_adjacent(boardSt.board, spawn.cell)
                if opp_adjacent > best_opp_adjacent:
                    best_move = spawn
                    best_gain = 1
                    best_opp_adjacent = opp_adjacent
                elif best_move is None:
                    best_move = spawn
                    best_gain = 1
        
        boardSt = boardSt.get_new_boardstate(best_move, self._color)
        return best_move