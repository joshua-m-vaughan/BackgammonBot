# INFORMATION -------------------------------------------------------- #

# Author:  Code leveraged from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements template classes for game state, actions, game
#          rules, and agents.

# IMPORTS ------------------------------------------------------------ #

from . import utils
import random

# CONSTANTS ---------------------------------------------------------- #


# CLASS DEF ---------------------------------------------------------- #

class GameState():
    def __init__(self, num_agents: int, agent_id: int) -> None:
        pass

class Action():
    pass

class GameRules:
    def __init__(self, num_agents: int = 2) -> None:
        """__init__
        Initialise an instance of GameRules class.

        Args:
            num_agents (int, optional): Number of agents in the game.
            Defaults to 2.
        """
        self.current_agent_id: int = 0
        self.num_agents: int = num_agents
        self.current_game_state: GameState = self.initial_game_state()
        self.action_counter: int = 0

    def initial_game_state(self) -> GameState:
        """initial_game_state
        Returns the intial game state for the games rules.

        Returns:
            GameState: An instance of GameState class.
        """
        utils.raiseNotDefined()
        return 0

    def generate_successor(self, game_state: GameState,
                           action:Action, agent_id:int) -> GameState:
        """generate_successor
        Returns the successive GameState s' for applying Action a on 
        Agent agent_id in GameState s.

        Args:
            game_state (GameState): GameState s.
            action (Action): Action a.
            agent_id (int): Agent ID.

        Returns:
            GameState: GameState s'.
        """
        utils.raiseNotDefined()
        return 0

    def get_next_agent_id(self) -> int:
        """get_next_agent_id
        Returns the Agent ID of the agent whose turn is next.

        Returns:
            int: Agent ID
        """
        return (self.current_agent_id + 1) % self.num_agents

    def get_legal_actions(self, game_state:GameState,
                          agent_id:int) -> list[Action]:
        """get_legal_actions
        Returns a list of Action instances that are legal for Agent ID
        in a given GameState.

        Args:
            game_state (GameState): GameState s.
            agent_id (int): Agent ID.

        Returns:
            list[Action]: List of Action instances that are valid in
            GameState s.
        """
        utils.raiseNotDefined()
        return []

    def calculate_score(self, game_state:GameState,
                        agent_id:int) -> int:
        """calculate_score
        Returns the score for agent ID in GameState s.

        Args:
            game_state (GameState): GameState s.
            agent_id (int): Agent ID.

        Returns:
            int: Integer representing the agent's score.
        """
        utils.raiseNotDefined()
        return 0

    def game_ends(self, game_state:GameState) -> bool:
        """game_ends
        Returns whether the game ends in GameState.

        Args:
            game_state (GameState): GameState s.
        
        Returns:
            bool: Boolean indicating the completion of the game.
        """
        utils.raiseNotDefined()
        return False

    def update(self, action:Action) -> None:
        """update
        In-place update of GameState s to GameState s', by applying
        Action a.

        Args:
            action (Action): Action a.
        """

        temp_state = self.current_game_state
        self.current_game_state = self.generate_successor(temp_state,
                                                          action,
                                                          self.current_agent_id)
        self.current_agent_id = self.get_next_agent_id()
        self.action_counter += 1
        
        return None

    def get_current_agent_id(self) -> int:
        """get_current_agent_id

        Returns:
            int: Current agent ID.
        """
        return self.current_agent_id
    
class Agent():
    def __init__(self, id):
        self.id = id
 
    def select_action(self, game_state:GameState,
                      actions:list[Action]) -> Action:
        """select_action
        Given a set of available actions for the agent to execute, and
        a copy of the current game state (including that of the agent),
        select one of the actions to execute.

        Args:
            game_state (GameState): Instance of GameState.
            actions (list[Action]): List of Action instances.

        Returns:
            Action: Selected action instance.
        """
        return random.choice(actions)

# END ---------------------------------------------------------------- #