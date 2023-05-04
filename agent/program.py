# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

import strategy
import agentboard

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
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
        
        # Initialise the strategy. This will be the only line you need to change for child Agents.
        self.strategy = strategy.ParentStrategy(color, **referee)

        # Initialise the board
        self.board = agentboard.BoardState({}, [], 0, self._color)


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        return self.strategy.action(**referee)

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass

class OneMoveAgent(Agent):
    """ 
    An agent that makes a move with no look-ahead. Makes the move with the best immediate outcome.
    Uses inheritance to inherit the action method from the Agent class.
    """
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        super().__init__(color, **referee)

        # Initialise the strategy
        self.strategy = strategy.OneMoveStrategy(color, **referee)
    
    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        return self.strategy.action(**referee)
    
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        return
