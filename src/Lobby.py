import argparse, retro, os, time
from enum import Enum
from Discretizer import StreetFighter2Discretizer

# Used incase too many players are added to the lobby
class Lobby_Full_Exception(Exception):
    pass

# determines how many players the lobby will request moves from before updating the game state
class Lobby_Modes(Enum):
    SINGLE_PLAYER = 1
    TWO_PLAYER = 2

class Lobby():
    """A class that handles all of the necessary book keeping for running the gym environment.
       A number of players are added and a game state is selected and the lobby will handle
       piping in the player moves and keeping track of some relevant game information.
    """

    ### Static Variables 

    # Variables relating to monitoring state and contorls
    NO_ACTION = 0
    MOVEMENT_BUTTONS = ['LEFT', 'RIGHT', 'DOWN', 'UP']
    ACTION_BUTTONS = ['X', 'Y', 'Z', 'A', 'B', 'C']
    ROUND_TIMER_NOT_STARTED = 39208
    STANDING_STATUS = 512
    CROUCHING_STATUS = 514
    JUMPING_STATUS = 516
    ACTIONABLE_STATUSES = [STANDING_STATUS, CROUCHING_STATUS, JUMPING_STATUS]

    # Variables keeping track of the delay between these movement inputs and
    # when the next button inputs are picked ups
    JUMP_LAG = 4

    FRAME_RATE = 1 / 115                                                                           # The time between frames if real time is enabled

    ### End of static variables 

    ### Static Methods

    def getStates():
        """Static method that gets and returns a list of all the save state names that can be loaded

        Parameters
        ----------
        None

        ReturnsStreetFighter2Discretizer
        -------
        states
            A list of strings where each string is the name of a different save state
        """
        files = os.listdir('../StreetFighterIISpecialChampionEdition-Genesis')
        states = [file.split('.')[0] for file in files if file.split('.')[1] == 'state']
        return states

    ### End of static methods

    def __init__(self, game= 'StreetFighterIISpecialChampionEdition-Genesis', render= False, mode= Lobby_Modes.SINGLE_PLAYER):
        """Initializes the agent and the underlying neural network

        Parameters
        ----------
        game
            A String of the game the lobby will be making an environment of, defaults to StreetFighterIISpecialChampionEdition-Genesis

        render
            A boolean flag that specifies whether or not to visually render the game while a match is being played

        mode
            An enum type that describes whether this lobby is for single player or two player matches

        Returns
        -------
        None
        """
        self.game = game
        self.render = render
        self.mode = mode
        self.clearLobby()

    def initEnvironment(self, state):
        """Initializes a game environment that the Agent can play a save state in

        Parameters
        ----------
        state
            A string of the name of the save state to load into the environment

        Returns
        -------
        None
        """
        self.environment = retro.make(game= self.game, state= state, players= self.mode.value)
        self.environment = StreetFighter2Discretizer(self.environment)
        self.environment.reset()                                                               
        self.lastObservation, _, _, self.lastInfo = self.environment.step(Lobby.NO_ACTION)                   # The initial observation and state info are gathered by doing nothing the first frame and viewing the return data
        self.lastAction, self.frameInputs = 0, [Lobby.NO_ACTION]
        self.currentJumpFrame = 0
        self.done = False
        while not self.isActionableState(self.lastInfo, Lobby.NO_ACTION):
            self.lastObservation, _, _, self.lastInfo = self.environment.step(Lobby.NO_ACTION)

    def addPlayer(self, newPlayer):
        """Adds a new player to the player list of active players in this lobby
           will throw a Lobby_Full_Exception if the lobby is full

        Parameters
        ----------
        newPlayer
            An agent object that will be added to the lobby and moves will be requested from when the lobby starts

        Returns
        -------
        None
        """
        for playerNum, player in enumerate(self.players):
            if player is None:
                self.players[playerNum] = newPlayer
                return

        raise Lobby_Full_Exception("Lobby has already reached the maximum number of players")

    def clearLobby(self):
        """Clears the players currently inside the lobby's play queue

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.players = [None] * self.mode.value

    def isActionableState(self, info, action = 0):
        """Determines if the Agent has control over the game in it's current state(the Agent is in hit stun, ending lag, etc.)

        Parameters
        ----------
        info
            The RAM info of the current game state the Agent is presented with as a dictionary of keyworded values from Data.json

        action
            The last action taken by the Agent

        Returns
        -------
        isActionable
            A boolean variable describing whether the Agent has control over the given state of the game
        """
        action = self.environment.get_action_meaning(action)
        if info['round_timer'] == Lobby.ROUND_TIMER_NOT_STARTED:                                                       
            return False
        elif info['status'] == Lobby.JUMPING_STATUS and self.currentJumpFrame <= Lobby.JUMP_LAG:
            self.currentJumpFrame += 1
            return False
        elif info['status'] == Lobby.JUMPING_STATUS and any([button in action for button in Lobby.ACTION_BUTTONS]):   # Have to manually track if we are in a jumping attack
            return False
        elif info['status'] not in Lobby.ACTIONABLE_STATUSES:                                                         # Standing, Crouching, or Jumping 
             return False
        else:
            if info['status'] != Lobby.JUMPING_STATUS and self.currentJumpFrame > 0: self.currentJumpFrame = 0 
            return True

    def play(self, state):
        """The Agent will load the specified save state and play through it until finished, recording the fight for training

        Parameters
        ----------
        state
            A string of the name of the save state the Agent will be playing

        Returns
        -------
        None
        """
        self.initEnvironment(state)
        while not self.done:

            # action is an iterable object that contains an input buffer representing frame by frame inputs
            # the lobby will run through these inputs and enter each one on the appropriate frames
            self.lastAction, self.frameInputs = self.players[0].getMove(self.lastObservation, self.lastInfo)

            # Fully execute frame object and then wait for next actionable state
            self.lastReward = 0
            info, obs = self.enterFrameInputs()
            info, obs = self.waitForNextActionableState(info, obs)

            # Record Results
            self.players[0].recordStep((self.lastObservation, self.lastInfo, self.lastAction, self.lastReward, obs, info, self.done))
            self.lastObservation, self.lastInfo = [obs, info]                   # Overwrite after recording step so Agent remembers the previous state that led to this one
        
        self.environment.close()
        if self.render: self.environment.viewer.close()

    def enterFrameInputs(self):
        """Enter each of the frame inputs in the input buffer inside the last action object supplied by the Agent

        Parameters
        ----------
        None

        Returns
        -------
        info
            The ram information received from the emulator after the last frame input has been entered    

        obs
            The image buffer data received from the emulator after entering all input frames
        """
        for frame in self.frameInputs:
            obs, tempReward, self.done, info = self.environment.step(frame)
            if self.done: return info, obs
            if self.render: 
                self.environment.render()
                time.sleep(Lobby.FRAME_RATE)
            self.lastReward += tempReward
        return info, obs

    def waitForNextActionableState(self, info, obs):
        """Wait for the next game state where the Agent can make an action

        Parameters
        ----------
        info
            The ram info received from the emulator of the last frame of the game

        obs
            The image buffer received from the emulator starting the frame after that last set of inputs
            
        Returns
        -------
        info
            The ram info received from the emulator after finally getting to an actionable state

        obs
            The image buffer data received from the emulator after finally getting to an actionable state

        """
        while not self.isActionableState(info, action= self.frameInputs[-1]):
            obs, tempReward, self.done, info = self.environment.step(Lobby.NO_ACTION)
            if self.done: return info, obs
            if self.render: self.environment.render()
            if self.render:
                self.environment.render()
                time.sleep(Lobby.FRAME_RATE)
            self.lastReward += tempReward
        return info, obs

    def executeTrainingRun(self, review= True, episodes= 1):
        """The lobby will load each of the saved states to generate data for the agent to train on
            Note: This will only work for single player mode

        Parameters
        ----------
        review
            A boolean variable that tells the Agent whether or not it should train after running through all the save states, true means train

        episodes
            An integer that represents the number of game play episodes to go through before training, once through the roster is one episode

        Returns
        -------
        None
        """
        for episodeNumber in range(episodes):
            print('Starting episode', episodeNumber)
            for state in Lobby.getStates():
                self.play(state= state)
            
            if self.players[0].__class__.__name__ != "Agent" and review == True: 
                self.players[0].reviewFight()


# Makes an example lobby and has a random agent play through an example training run
if __name__ == "__main__":
    testLobby = Lobby(render= True)
    from Agent import Agent
    agent = Agent()
    testLobby.addPlayer(agent)
    testLobby.executeTrainingRun()