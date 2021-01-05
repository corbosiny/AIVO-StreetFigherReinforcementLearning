import argparse, retro, threading, os, numpy, time, random
from collections import deque

from tensorflow.python import keras
from keras.models import load_model

from DefaultMoveList import Moves

class Agent():
    """ Abstract class that user created Agents should inherit from.
        Contains helper functions for launching training environments and generating training data sets.
    """

    # Global constants keeping track of some input lag for some directional movements
    # Moves following these inputs will not be picked up unless input after the lag

    # The indices representing what each index in a training point represent
    OBSERVATION_INDEX = 0                                                                          # The current display image of the game state
    STATE_INDEX = 1                                                                                # The state the agent was presented with    
    ACTION_INDEX = 2                                                                               # The action the agent took
    REWARD_INDEX = 3                                                                               # The reward the agent received for that action
    NEXT_OBSERVATION_INDEX = 4                                                                     # The current display image of the new state the action led to
    NEXT_STATE_INDEX = 5                                                                           # The next state that the action led to
    DONE_INDEX = 6                                                                                 # A flag signifying if the game is over

    MAX_DATA_LENGTH = 50000                                                                        # Max number of decision frames the Agent can remember from a fight, average is about 2000 per fight

    DEFAULT_MODELS_DIR_PATH = '../local_models'               # Default path to the dir where the trained models are saved for later access
    DEFAULT_MODELS_SUB_DIR = '{0}_models'                     # Models are further organized into subdirectories to avoid checkpoint overwrites by this naming scheme
    DEFAULT_LOGS_DIR_PATH = '../local_logs'                   # Default path to the dir where training logs are saved for user review

    ### End of static variables 

    ### Object methods

    def __init__(self, load= False, name= None, moveList= Moves):
        """Initializes the agent and the underlying neural network
        Parameters
        ----------
        load
            A boolean flag that specifies whether to initialize the model from scratch or load in a pretrained model
        name
            A string representing the name of the model that will be used when saving the model and the training logs
            Defaults to the class name if none are provided
        moveList
            An enum class that contains all of the allowed moves the Agent can perform
        Returns
        -------
        None
        """
        if name is None: self.name = self.__class__.__name__
        else: self.name = name
        self.prepareForNextFight()
        self.moveList = moveList

        if self.__class__.__name__ != "Agent":
            self.model = self.initializeNetwork()    								            # Only invoked in child subclasses, Agent has no network
            if load: self.loadModel()

    def prepareForNextFight(self):
        """Clears the memory of the fighter so it can prepare to record the next fight"""
        self.memory = deque(maxlen= Agent.MAX_DATA_LENGTH)                                     # Double ended queue that stores states during the game

    def getRandomMove(self, info):
        """Returns a random set of button inputs
        Parameters
        ----------
        info
            Metadata dictionary about the current game state from the RAM
        Returns
        -------
        moveName.value
            An integer representing the move from the move list that was selected
        frameInputs
            A set of frame inputs where each number corresponds to a set of button inputs in the action space.
        """ 
        moveName = random.choice(list(self.moveList))                                          # Take random sample of all the button press inputs the Agent could make
        frameInputs = self.convertMoveToFrameInputs(moveName, info)                                                   
        return moveName.value, frameInputs                                

    def convertMoveToFrameInputs(self, move, info):
        """Converts the desired move into a series of frame inputs in order to acomplish that move
        Parameters
        ----------
        move
            enum type named after the move to be performed
            is used as the key into the move to inputs dic
        info
            Metadata dictionary about the current game state from the RAM
        Returns
        -------
        frameInputs
            An iterable frame inputs object containing the frame by frame input buffer for the move
        """
        frameInputs = self.moveList.getMoveInputs(move)
        frameInputs = self.formatInputsForDirection(move, frameInputs, info)
        return frameInputs

    def formatInputsForDirection(self, move, frameInputs, info):
        """Converts special move directional inputs to account for the player direction so they properly execute
        Parameters
        ----------
        move
            enum type named after the move to be performed
            is used as the key into the move to inputs dic
        frameInputs
            An array containing the series of frame inputs for the desired move
            In the case of a special move it has two sets of possible inputs
        info
            Information about the current game state we will pull the player
            and opponent position from 
        Returns
        -------
        frameInputs
            An iterable frame inputs object containing the frame by frame input buffer for the move
        """
        if not self.moveList.isDirectionalMove(move):
            return frameInputs

        if info['x_position'] < info['enemy_x_position']:
            return frameInputs[0]
        else:
            return frameInputs[1]

        return frameInputs

    def recordStep(self, step):
        """Records the last observation, action, reward and the resultant observation about the environment for later training
        Parameters
        ----------
        step
            A tuple containing the following elements:
            observation
                The current display image in the form of a 2D array containing RGB values of each pixel
            state
                The state the Agent was presented with before it took an action.
                A dictionary containing tagged RAM data
            lastAction
                Integer representing the last move from the move list the Agent chose to pick
            reward
                The reward the agent received for taking that action
            nextObservation
                The resultant display image in the form of a 2D array containing RGB values of each pixel
            nextState
                The state that the chosen action led to
            done
                Whether or not the new state marks the completion of the emulation
        Returns
        -------
        None
        """
        self.memory.append(step) # Steps are stored as tuples to avoid unintended changes

    def reviewFight(self):
        """The Agent goes over the data collected from it's last fight, prepares it, and then runs through one epoch of training on the data"""
        data = self.prepareMemoryForTraining(self.memory)
        self.model = self.trainNetwork(data, self.model)   		                           # Only invoked in child subclasses, Agent does not learn
        self.saveModel()
        self.prepareForNextFight()

    def saveModel(self):
        """Saves the currently trained model in the default naming convention ../models/{Class_Name}Model
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        totalDirPath = os.path.join(Agent.DEFAULT_MODELS_DIR_PATH, Agent.DEFAULT_MODELS_SUB_DIR.format(self.name))
        self.model.save_weights(os.path.join(totalDirPath, self.getModelName()))
        with open(os.path.join(Agent.DEFAULT_LOGS_DIR_PATH, self.getLogsName()), 'a+') as file:
            try:
                file.write(str(sum(self.lossHistory.losses) / len(self.lossHistory.losses)))
                file.write('\n')
            except:
                pass # No losses to report yet

    def loadModel(self):
        """Loads in pretrained model object ../models/{Class_Name}Model
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        print('Model successfully loaded')
        totalDirPath = os.path.join(Agent.DEFAULT_MODELS_DIR_PATH, Agent.DEFAULT_MODELS_SUB_DIR.format(self.name))
        self.model.load_weights(os.path.join(totalDirPath, self.getModelName()))

    def getModelName(self):
        """Returns the formatted model name for the current model"""
        return  self.name + "Model"

    def getLogsName(self):
        """Returns the formatted log name for the current model"""
        return self.name + "Logs"

    ### End of object methods

    ### Abstract methods for the child Agent to implement
    def getMove(self, obs, info):
        """Returns a set of button inputs generated by the Agent's network after looking at the current observation
        Parameters
        ----------
        obs
            The observation of the current environment, 2D numpy array of pixel values
        info
            An array of information about the current environment, like player health, enemy health, matches won, and matches lost, etc.
            A full list of info can be found in data.json
        Returns
        -------
        move
            Integer representing the move that was selected from the move list
        frameInputs
            A set of frame inputs where each number corresponds to a set of button inputs in the action space.
        """
        move, frameInputs = self.getRandomMove(info)
        return move, frameInputs

    def initializeNetwork(self):
        """To be implemented in child class, should initialize or load in the Agent's neural network
        
        Parameters
        ----------
        None
        Returns
        -------
        model
            A newly initialized model that the Agent will use when generating moves
        """
        raise NotImplementedError("Implement this is in the inherited agent")
    
    def prepareMemoryForTraining(self, memory):
        """To be implemented in child class, should prepare the recorded fight sequences into training data
        
        Parameters
        ----------
        memory
            A 2D array where each index is a recording of a state, action, new state, and reward sequence
            See readme for more details
        Returns
        -------
        data
            The prepared training data
        """
        raise NotImplementedError("Implement this is in the inherited agent")

    def trainNetwork(self, data, model):
        """To be implemented in child class, Runs through a training epoch reviewing the training data and returns the trained model
        Parameters
        ----------
        data
            The training data for the model
        
        model
            The model for the function to train
        Returns
        -------
        model
            The now trained and hopefully improved model
        """
        raise NotImplementedError("Implement this is in the inherited agent")

    ### End of Abstract methods


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processes agent parameters.')
    parser.add_argument('-r', '--render', action= 'store_true', help= 'Boolean flag for if the user wants the game environment to render during play')
    args = parser.parse_args()
    from Lobby import Lobby
    testLobby = Lobby(render= args.render)
    agent = Agent()
    testLobby.addPlayer(agent)
    testLobby.executeTrainingRun()