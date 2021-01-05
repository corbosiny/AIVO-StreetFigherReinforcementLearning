# Source Code
This directory contains all of the source code pertaining to the project.

### Lobby.py
This class handles all of the interfacing with the retro environment, storing data, and managing training over several training episodes. This class acts as a training environment that agents can enter and request different save states to train on before leaving. The lobby acts similar to an open game lobby for any online video game.

### Agent.py
This class acts as a skeletal interface for all other Agents to inherit from and also implements some backend helper functions to get other Agents started. All children classes must implement four abstract methods in order to keep with the desired interface for an Agent. More can be read in the "How to make an Agent" section of the main README in the top level directory. Running this by itself will open up a fight with each character among the Street Fighter 2 roster and will play randomly against them. The Agent was designed to not have to know anything about the game or the type of model it is training so the game that this is working with or model the user implements are free to be changed at any state of development.

### DeepQAgent.py
A DeepQ Reinforcement learning model implemented using a dense reward function and policy gradients for training.

### Discretizer.py
Custom wrapping around the input space of the environment to turn inputs into human readable button descriptions.

### DefaultMoveList.py
The dictionary that maps move selections to multiframe input sets for the Agent to preform on the emulator

### LossHistory.py
A class used to store the training error logs after each training episode as consistent with the typical keras log format. 

### watchAgent.py
A helper script that when run loads in a desired network and lets the user visualize how well the network is running on some test save states. 
