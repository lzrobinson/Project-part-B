# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

from agent.agentboard import BoardState
from agent.strategy import ParentStrategy, OneMoveStrategy2, TwoMoveStrategy, RandomStrategy, AlphaBetaStrategy


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    """
    A parent class for all agents. Note that this class is not intended to be used directly.
    """
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        
        # Initialise the strategy. This will be the only line you need to change for child Agents.
        self.strategy = AlphaBetaStrategy(color, **referee)

        # Initialise the board
        self.board = BoardState({}, [], 0, self._color)


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        action = self.strategy.action(self.board, **referee)
        return action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self.board.update_boardstate(action, color)

class AlphaBetaAgent(Agent):
    """ 
    An agent that makes a random move with no look-ahead. 
    Uses inheritance to inherit the action method from the Agent class.
    """
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        super().__init__(color, **referee)

        # Initialise the strategy
        self.strategy = AlphaBetaStrategy(color, **referee)