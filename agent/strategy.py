# A file where we define the strategies for our agent as classes.
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from agent import agentboard

class RandomStrategy():
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

class OneMoveStrategy():
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the strategy.
        """
        self._color = color
        
    def action(**referee: dict) -> Action:
        """
        Return the next action to take.
        """