# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements Backgammon for the purposes of developing an AI
#          agent for ME344: Introduction to building High Performance
#          Computing clusters, at Stanford Summer Session 2024.

# IMPORTS ------------------------------------------------------------ #

from copy import deepcopy
from queue import LifoQueue
import random
from ExtendedFormGame.template import GameState, GameRules, Action
from backgammon_tree import PlayNode
import numpy as np

# CONSTANTS ---------------------------------------------------------- #

MIN_FACE_VALUE:int = 1
MAX_FACE_VALUE:int = 6
NUM_BACKGAMMON_AGENTS:int = 2
BLACK_ID:int = 0
WHITE_ID:int = 1
BLACK_HOME_POINT:int = 25
BLACK_HOME_BORDER:int = 19
WHITE_HOME_POINT:int = 0
WHITE_HOME_BORDER:int = 6
INIT_BOARD_CONFIG = [(1,2), (12,5), (17,3), (19,5)]
DOUBLES_MULTIPLIER:int = 4
CHECKERS_BLOCKED:int = 2
# Board States
ON_BAR:int = -1
NORMAL:int = 0
BEAR_OFF:int = 1
# Endgame scores
LOSING_SCORE:int = 0
WINNING_SCORE:int = 1

# CLASS DEF ---------------------------------------------------------- #

class BackgammonState(GameState):
    
    def __init__(self,
                 num_agents:int =NUM_BACKGAMMON_AGENTS,
                 agent_id:int =BLACK_ID) -> None:
        """__init__
        Initialise an instance of BackgammonState class using a modified
        version of the representation proposed by Lishout, Chaslot, and
        Uiterwijk.

        References List:
            Van Lishout, François & Chaslot, Guillaume & Uiterwijk, Jos.
            (2007). Monte-Carlo tree search in backgammon. Computer
            Games Workshop.

        Args:
            num_agents (int, optional): Number of agents in the game.
            Defaults to 2.
            STARTING_AGENT_ID (int, optional): Starting Agent ID.
            Defaults to BLACK_ID.

        """
        # Assert expected input from Game builder.
        assert (num_agents == 2)
        assert (agent_id == 0)

        # Initialise GameState attributes.
        self.num_agents = num_agents
        self.current_agent_id = agent_id

        # Initialise the board state attributes.
        self.points_content = [0] * 26
        self.black_checkers = []
        self.white_checkers = []
        for point, num_checkers in INIT_BOARD_CONFIG:
            # Black Setup
            self.points_content[point] = num_checkers
            self.black_checkers.append(point)
            # White Setup
            self.points_content[BLACK_HOME_POINT - point] = -num_checkers
            self.white_checkers = [BLACK_HOME_POINT - point] + self.white_checkers
        self.black_checkers_taken = 0
        self.white_checkers_taken = 0

        # Initialise the dice attributes.
        self.dice = [random.randint(MIN_FACE_VALUE, MAX_FACE_VALUE),
                     random.randint(MIN_FACE_VALUE, MAX_FACE_VALUE)]
    
    def __str__(self) -> str:
        output: str = ""
        tmp_points_content = deepcopy(self.points_content)
        
        # Write board labels.
        for i in range(len(self.points_content)):
            output += str(i) + " "
        output += "\n"
        
        # Write pieces.
        not_all_zero: bool = True
        while (not_all_zero):
            not_all_zero = False
            for i in range(len(tmp_points_content)):
                if tmp_points_content[i] > 0:
                    output += "B "
                    tmp_points_content[i] -= 1
                    not_all_zero = True
                elif tmp_points_content[i] < 0:
                    output += "W "
                    tmp_points_content[i] += 1
                    not_all_zero = True
                else:
                    output += "  " # White space.
                if i >= 9:
                    output += " "
            output += "\n"
        
        # Print taken.
        output += ("TAKEN: B" + str(self.black_checkers_taken) +
                   " W" + str(self.white_checkers_taken) + "\n")

        # Print dice.
        output += str("DICE: "+str(self.dice[0])+" "+str(self.dice[1]))
        return output

    def roll(self) -> None:
        """roll
        Roll the dice to generate a new set of two dice representation.
        """

        self.dice = [random.randint(MIN_FACE_VALUE, MAX_FACE_VALUE),
                     random.randint(MIN_FACE_VALUE, MAX_FACE_VALUE)]
        
        return None


class BackgammonRules(GameRules):
    
    def __init__(self):
        """__init__
        Initialise an instance of GameRules class.
        """
        super().__init__(NUM_BACKGAMMON_AGENTS)

    def initial_game_state(self) -> BackgammonState:
        """initial_game_state
        Returns the intial game state for the games rules.

        Returns:
            BackgammonState: An instance of BackgammonState class.
        """
        return BackgammonState(self.num_agents)

    def get_legal_actions(self, game_state:BackgammonState,
                          agent_id:int) -> list[Action]:
        """get_legal_actions
        Returns a list of Action instances that are legal for Agent ID
        in a given GameState using the approach proposed by Berliner.

        References List:
            Hans J. Berliner (1977) BKG -- A Program that plays
            Backgammon. Carnegie-Mellon University.

        Args:
            game_state (BackgammonState): BackgammonState s.
            agent_id (int): Agent ID.

        Returns:
            list[Action]: List of Action instances that are valid in
            BackgammonState s.
        """
        # Validate dice to determine available moves.
        [dice_a, dice_b] = game_state.dice
        faces = []
        if dice_a == dice_b:
            faces = [dice_a] * DOUBLES_MULTIPLIER
        else:
            faces = game_state.dice
        # Rules require that if only one move can be played, it is done
        # with the largest rolled face. As such, each play sequence,
        # will be generated with this property in mind.
        faces.sort(reverse=True)

        # TECH DEBT: This shuold go to a log file!
        print(game_state)
        if game_state.current_agent_id == BLACK_ID:
            print("TURN "+str(self.action_counter)+": BLACK")
        else:
            print("TURN "+str(self.action_counter)+": WHITE")

        # Generate play sequences.
        root = PlayNode(None, game_state)
        self._generate_play_tree(root, faces)
        if len(faces) != DOUBLES_MULTIPLIER:
            faces.sort()
            self._generate_play_tree(root, faces)

        # Extract play sequences using DFS
        return self._extract_actions(root)
    
    def _extract_actions(self, root:PlayNode) -> list[tuple]:
        """_extract_actions
        DFS of play tree to extract valid action sequences.

        Args:
            root (PlayNode): Root node of play tree.

        Returns:
            list[tuple]: _description_
        """

        # Initialise stack.
        stack = LifoQueue(maxsize=0)
        stack.put((root, []))

        # Perform DFS extraction
        return self._extract_play_tree_dfs(stack, [])


    def _extract_play_tree_dfs(self, stack:LifoQueue, actions:list) -> list:
        """_extract_play_tree_dfs

        Args:
            stack (LifoQueue): Stack for DFS.
            actions (list): Set of extracted actions.

        Returns:
            list: Extracted actions.
        """
        # Extract next element in stack.
        node, sequence = stack.get()

        # Evaluate end condition.
        if len(node.children) == 0:
            actions.append(sequence)
            return actions

        # Update stack with next depth of nodes.
        for child in node.children:
            new_sequence = deepcopy(sequence)
            new_sequence.append(child.move)
            stack.put((child, new_sequence))
            # Continue DFS.
            self._extract_play_tree_dfs(stack, actions)
        
        return actions
        

    def _generate_play_tree(self, root:PlayNode, faces:list[int]) -> None:
        """_generate_play_tree

        Args:
            root (PlayNode): Node of a tree that stores the play
            sequences.
            faces (list[int]): List of faces to be used in play
            sequence.
        """

        # Validate exit condition: no more faces to consider.
        if len(faces) == 0:
            return root
        
        # Validate board state
        board_state = self._evaluate_board_state(root.state)
        if board_state == ON_BAR:
            
            # Determine move.
            if root.state.current_agent_id == BLACK_ID:
                move = (WHITE_HOME_POINT,
                        WHITE_HOME_POINT + faces[0],
                        faces[0])
            else:
                move = (BLACK_HOME_POINT,
                        BLACK_HOME_POINT - faces[0],
                        faces[0])
                
            if self._evaluate_valid_move(root.state, move):
                # Generate new state after applying move.
                game_state_prime = self._update_game_state(deepcopy(root.state), move)
                # Create a new search state node storing next state, and move applied to get it there.
                node_prime = PlayNode(root, game_state_prime, move)
                # Add new search state node to set of children.
                root.children.append(node_prime)
                # Recursive call on new search state node with unsused faces.
                self._generate_play_tree(node_prime, faces[1:])

        elif board_state == BEAR_OFF:
            
            if root.state.current_agent_id == BLACK_ID:
                
                # Determine move.
                for point in root.state.black_checkers:
                    move = (point,
                            min(point + faces[0], BLACK_HOME_POINT),
                            faces[0])
                    
                    if self._evaluate_valid_bear_off(root.state, move):
                        # Generate new state after applying move.
                        game_state_prime = self._update_game_state(deepcopy(root.state), move)
                        # Create a new search state node storing next state, and move applied to get it there.
                        node_prime = PlayNode(root, game_state_prime, move)
                        # Add new search state node to set of children.
                        root.children.append(node_prime)
                        # Recursive call on new search state node with unsused faces.
                        self._generate_play_tree(node_prime, faces[1:])
                    
            else:

                # Determine move.
                for point in root.state.white_checkers:
                    move = (point,
                            max(point - faces[0], WHITE_HOME_POINT),
                            faces[0])
                    
                    if self._evaluate_valid_bear_off(root.state, move):
                        # Generate new state after applying move.
                        game_state_prime = self._update_game_state(deepcopy(root.state), move)
                        # Create a new search state node storing next state, and move applied to get it there.
                        node_prime = PlayNode(root, game_state_prime, move)
                        # Add new search state node to set of children.
                        root.children.append(node_prime)
                        # Recursive call on new search state node with unsused faces.
                        self._generate_play_tree(node_prime, faces[1:])

        elif board_state == NORMAL:
            
            if root.state.current_agent_id == BLACK_ID:
                
                # Determine move.
                for point in root.state.black_checkers:
                    move = (point,
                            min(point + faces[0], BLACK_HOME_POINT),
                            faces[0])
                    
                    if self._evaluate_valid_move(root.state, move):
                        # Generate new state after applying move.
                        game_state_prime = self._update_game_state(deepcopy(root.state), move)
                        # Create a new search state node storing next state, and move applied to get it there.
                        node_prime = PlayNode(root, game_state_prime, move)
                        # Add new search state node to set of children.
                        root.children.append(node_prime)
                        # Recursive call on new search state node with unsused faces.
                        self._generate_play_tree(node_prime, faces[1:])
                    
            else:

                # Determine move.
                for point in root.state.white_checkers:
                    move = (point,
                            max(point - faces[0], WHITE_HOME_POINT),
                            faces[0])
                    
                    if self._evaluate_valid_move(root.state, move):
                        # Generate new state after applying move.
                        game_state_prime = self._update_game_state(deepcopy(root.state), move)
                        # Create a new search state node storing next state, and move applied to get it there.
                        node_prime = PlayNode(root, game_state_prime, move)
                        # Add new search state node to set of children.
                        root.children.append(node_prime)
                        # Recursive call on new search state node with unsused faces.
                        self._generate_play_tree(node_prime, faces[1:])

    def _evaluate_valid_move(self, game_state:BackgammonState,
                             move:tuple) -> bool:
        """_evaluate_valid_move
        Returns a boolean indicating whether the move is valid for the
        board state in ON_BAR or NORMAL board states.

        Valid move if to_point is not blocked by opposing checkers,
        assuming the following:
        - The board is in ON_BAR or NORMAL board states.
        - The from_point is held by the current ID.
        - The move is a valid face for the current BackgammonState.

        Args:
            game_state (BackgammonState): Gamestate s.
            move (tuple): Three tuple detailing fromPoint, toPoint, and
            face value of a move.

        Returns:
            bool: True if valid, False otherwise.
        """
        (from_point, to_point, face) = move

        # Check if attempting to bear off.
        if (abs(to_point - from_point) != face):
            return False

        if (game_state.current_agent_id == BLACK_ID
            and game_state.points_content[to_point] > -CHECKERS_BLOCKED):
            # Piece moving from bar.
            if (from_point == WHITE_HOME_POINT
                  and game_state.black_checkers_taken > 0):
                return True
            # Piece moving from board.
            elif (to_point != BLACK_HOME_POINT):
                assert(from_point in set(game_state.black_checkers))
                return True
            else:
                return False
            
        elif (game_state.current_agent_id == WHITE_ID
              and game_state.points_content[to_point] < CHECKERS_BLOCKED):
            # Piece moving from bar.
            if (from_point == BLACK_HOME_POINT
                  and game_state.white_checkers_taken > 0):
                return True
            # Piece moving from board.
            elif (to_point != WHITE_HOME_POINT):
                assert(from_point in set(game_state.white_checkers))
                return True
            else:
                return False
            
        else:
            return False
    
    def _evaluate_valid_bear_off(self, game_state:BackgammonState,
                                 move:tuple) -> bool:
        """_evaluate_valid_bear_off
        Returns a boolean indicating whether the move is valid for the
        board state in the BEAR_OFF board state.

        Valid move if the move is:
        - an exact bear-off, or
        - when a larger number is rolled, the furthest piece is
        born-off,
        - or is a valid move.

        assuming the following:
        - The board is in BEAR_OFF board state.
        - The from_point is held by the current ID.
        - The move is a valid face for the current BackgammonState.

        Args:
            game_state (BackgammonState): Gamestate s.
            move (tuple): Three tuple detailing fromPoint, toPoint, and
            face value of a move.

        Returns:
            bool: True if valid, False otherwise.
        """
        
        (from_point, to_point, face) = move

        if (game_state.current_agent_id == BLACK_ID):
            # Move piece to home point.
            if (to_point == BLACK_HOME_POINT and 
                abs(to_point - from_point) == face):
                return True
            
            # Move the furthest piece to home point with an overshoot.
            elif (to_point == BLACK_HOME_POINT and
                  abs(to_point - from_point) < face and
                  game_state.black_checkers[0] == from_point):
                return True
            
            # Determine if otherwise a valid normal state move. (e.g.
            # with a face of two, move a checker from point 4 to
            # point 2.)
            else:
                return self._evaluate_valid_move(game_state, move)

        elif (game_state.current_agent_id == WHITE_ID):
            # Move piece to home point.
            if (to_point == WHITE_HOME_POINT and 
                abs(to_point - from_point) == face):
                return True
            
            # Move the furthest piece to home point with an overshoot.
            elif (to_point == WHITE_HOME_POINT and
                  abs(to_point - from_point) < face and
                  game_state.white_checkers[0] == from_point):
                return True
            
            # Determine if otherwise a valid normal state move. (e.g.
            # with a face of two, move a checker from point 4 to
            # point 2.)
            else:
                return self._evaluate_valid_move(game_state, move)

    def _evaluate_board_state(self, game_state:BackgammonState) -> int:
        """_evaluate_board_state
        Returns an integer indicating what class of state the board is
        in.

        Args:
            game_state (BackgammonState): Game state s.

        Returns:
            int: Class of board state
        """

        if game_state.current_agent_id == BLACK_ID:
            if game_state.black_checkers_taken >= 1:
                # Taken black pieces on bar.
                return ON_BAR
            elif game_state.black_checkers[0] >= BLACK_HOME_BORDER:
                # All black pieces in black home board.
                assert (game_state.black_checkers_taken < 1)
                return BEAR_OFF
            else:
                return NORMAL
        else:
            if game_state.white_checkers_taken >= 1:
                # Taken white pieces on bar.
                return ON_BAR
            elif game_state.white_checkers[0] <= WHITE_HOME_BORDER:
                # All white pieces in white home board.
                assert (game_state.white_checkers_taken < 1)
                return BEAR_OFF
            else:
                return NORMAL
    
    def generate_successor(self, game_state: BackgammonState,
                           action:list[tuple],
                           agent_id:int) -> BackgammonState:
        """generate_successor
        Returns the successive GameState s' for applying Action a on 
        Agent agent_id in GameState s.

        Args:
            game_state (GameState): GameState s.
            action (list[tuple]): List of move tuples.
            agent_id (int): Agent ID.

        Returns:
            GameState: GameState s'.
        """
        # Assert that action is being applied to the correct agent.
        assert(agent_id == game_state.current_agent_id)

        game_state_prime:BackgammonState = deepcopy(game_state)

        # Update board state
        for move in action:
            game_state_prime = self._update_game_state(game_state_prime,
                                                       move)

        # Roll dice.
        game_state_prime.roll()

        # Update game state id.
        if game_state.current_agent_id == BLACK_ID:
            game_state_prime.current_agent_id = WHITE_ID
        else:
            game_state_prime.current_agent_id = BLACK_ID

        return game_state_prime

    
    def _update_game_state(self, game_state:BackgammonState,
                           move:tuple) -> BackgammonState:
        """_update_game_state
        Returns an updated game state s' after applying move m in game
        state s in place.

        Assumptions: The provided move is a valid move in the current
        board state.

        Args:
            game_state (BackgammonState): BackgammonState, s.
            move (tuple): Three tuple of a valid move, m.

        Returns:
            BackgammonState: BackgammonState, s'.
        """

        (from_point, to_point, _) = move

        if game_state.current_agent_id == BLACK_ID:
            # Pick up checker.
            if from_point == WHITE_HOME_POINT:
                game_state.black_checkers_taken -= 1
            else:
                assert (game_state.points_content[from_point] > 0)
                game_state.points_content[from_point] -= 1
                if game_state.points_content[from_point] == 0:
                    game_state.black_checkers.remove(from_point)
            
            
            # Put down checker.
            assert (game_state.points_content[to_point] > -CHECKERS_BLOCKED)
            if game_state.points_content[to_point] > 0:
                # Existing point.
                game_state.points_content[to_point] += 1
            elif game_state.points_content[to_point] == 0:
                # New point acquired.
                game_state.points_content[to_point] = 1
                game_state.black_checkers.append(to_point)
                game_state.black_checkers.sort()
            elif game_state.points_content[to_point] < 0:
                # Take piece.
                game_state.points_content[to_point] = 1
                game_state.black_checkers.append(to_point)
                game_state.black_checkers.sort()
                game_state.white_checkers.remove(to_point)
                game_state.white_checkers.sort(reverse=True)
                game_state.white_checkers_taken += 1
        
        elif game_state.current_agent_id == WHITE_ID:
            # Pick up checker.
            if from_point == BLACK_HOME_POINT:
                game_state.white_checkers_taken -= 1
            else:
                assert (game_state.points_content[from_point] < 0)
                game_state.points_content[from_point] += 1
                if game_state.points_content[from_point] == 0:
                    game_state.white_checkers.remove(from_point)

            # Put down checker.
            assert (game_state.points_content[to_point] < CHECKERS_BLOCKED)
            if game_state.points_content[to_point] < 0:
                # Existing point.
                game_state.points_content[to_point] -= 1

            elif game_state.points_content[to_point] == 0:
                # New point acquired.
                game_state.points_content[to_point] = -1
                game_state.white_checkers.append(to_point)
                game_state.white_checkers.sort(reverse=True) 

            elif game_state.points_content[to_point] > 0:
                # Take piece.
                game_state.points_content[to_point] = -1
                game_state.white_checkers.append(to_point)
                game_state.white_checkers.sort(reverse=True) 
                game_state.black_checkers.remove(to_point)
                game_state.black_checkers.sort()
                game_state.black_checkers_taken += 1
        
        return game_state
        

    def calculate_score(self, game_state:BackgammonState,
                        agent_id:int) -> int:
        """calculate_score
        Returns the pip score for agent ID in BackgammonState s.

        Args:
            game_state (BackgammonState): BackgammonState s.
            agent_id (int): Agent ID.

        Returns:
            int: Integer representing the agent's score.
        """
        pip_score = 0
        if (agent_id == BLACK_ID):
            for point in game_state.black_checkers:
                pip_score += (game_state.points_content[point] *
                              abs(BLACK_HOME_POINT - point))
        elif (agent_id == WHITE_ID):
            for point in game_state.white_checkers:
                pip_score -= (game_state.points_content[point] *
                              abs(WHITE_HOME_POINT - point))

        return pip_score

    def calculate_endgame_score(self, game_state:GameState,
                                agent_id:int) -> int:
        """calculate_endgame_score
        Returns the score for agent ID in GameState s, where s is an
        endgame state.

        Args:
            game_state (GameState): GameState s.
            agent_id (int): Agent ID.

        Returns:
            int: Integer representing the agent's score.
        """
        # TECH DEBT: We would update the game here, to include the
        # doubling cube in the game for the final game score.
        
        if self.calculate_score(game_state, agent_id) > 0:
            return LOSING_SCORE
        else:
            # Player must have won, with a pip value of 0, as PIP value
            # is bound to positive integers.
            return WINNING_SCORE

    def game_ends(self, game_state:BackgammonState) -> bool:
        """game_ends
        Returns whether the game ends in BackgammonState.

        Args:
            game_state (BackgammonState): BackgammonState s.
        
        Returns:
            bool: Boolean indicating the completion of the game.
        """
        if (len(game_state.black_checkers) == 1 and
            game_state.black_checkers[0] == BLACK_HOME_POINT and
            game_state.black_checkers_taken == 0):
            # Black has moved all pieces to its home position.
            return True
        elif (len(game_state.white_checkers) == 1 and
                game_state.white_checkers[0] == WHITE_HOME_POINT and
                game_state.white_checkers_taken == 0):
                # White has moved all pieces to its home position.
                return True
        else:
            return False

class BackgammonAction(Action):
    pass

# FUNC DEF ----------------------------------------------------------- #

def generate_td_gammon_vector(game_state:BackgammonState) -> np.array:
    """generate_td_gammon_vector
    Turn a BackgammonState object into a vector representation used in
    the TD-gammon technique outlined in Tesaruo's paper.

    Reference List:
        Tesauro, G. (1995). Temporal difference learning and TD-Gammon.
        Communications of the ACM, 38(3), 58-68.

    Args:
        game_state (BackgammonState): BackgammonState s.

    Returns:
        np.array: Vector representation of game state.
    """

    # Determine agent vectors.
    black_vector = []
    white_vector = []
    blank_vector = [0] * 4
    for i in range(1, 25):
        point = game_state.points_content[i]
        if point > 0:
            # Black owned point.
            if point < 4:
                point_vec = [1 for x in range(point)] + [0 for x in range(abs(point-4))]
            else:
                point_vec = [1,1,1, ((point-3)/2)]

            black_vector += point_vec
            white_vector += blank_vector
        elif point < 0:
            # White owned point.
            if point > -4:
                point_vec = [1 for x in range(abs(point))] + [0 for x in range(abs(abs(point)-4))]
            else:
                point_vec = [1,1,1, ((abs(point)-3)/2)]

            white_vector += point_vec
            black_vector += blank_vector
        else:
            # Empty point.
            black_vector += blank_vector
            white_vector += blank_vector
    
    vector:list = black_vector + white_vector
    
    # Pieces on bar.
    vector.append((game_state.black_checkers_taken / 2))
    vector.append((game_state.white_checkers_taken / 2))

    # Pieces removed.
    vector.append(abs(game_state.points_content[BLACK_HOME_POINT]) / 2)
    vector.append(abs(game_state.points_content[WHITE_HOME_POINT]) / 2)

    # Agents turn.
    vector.append((1 if game_state.current_agent_id == BLACK_ID else 0))
    vector.append((1 if game_state.current_agent_id == WHITE_ID else 0))

    return np.array(vector)

# END ---------------------------------------------------------------- #