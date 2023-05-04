# A file where we define the strategies for our agent as classes.
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from agent import agentboard

class ParentStrategy:
    """
    A parent class for all strategies. Note that this class is not intended to be used directly.
    """
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the strategy.
        """
        self._color = color
        
    def action(**referee: dict) -> Action:
        """
        Return the next action to take.
        """
        pass

class RandomStrategy(ParentStrategy):
    """
    A strategy that makes a random move.
    """
    def action(**referee: dict) -> Action:
        """
        Return the next action to take.
        """
        pass

class OneMoveStrategy(ParentStrategy):
    """
    A strategy that makes a move with no look-ahead. Makes the move with the best immediate outcome.
    """
    def action(**referee: dict) -> Action:
        """
        Return the next action to take.
        """