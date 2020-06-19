# Getting Started

This readme will take you through how to get this repo up and running with the example agents, make your own test agents, and also how to create your own save states to test your agents on. 

---
## Installing Dependancies

This code only works with Python 3.6 or later. Before trying to install dependencies it is recommend to open the terminal and run:  
`sudo apt-get update`  
`sudo apt-get upgrade`  
`sudo -H pip3 install --upgrade pip`  

To download the necessary dependencies after cloning the repo call:
`pip3 install -r requirements.txt`

This should be called in the top level directory of the repo. This will install the following libraries you will need to create game environments that serve as a wrapper abstracting the interface between your agent and the underlying emulator:

-gym  
-gym-retro   
-tensorflow   
-keras   

These libraries can sometimes have serious issues installing themselves or their dependencies on a windows machine. It is recommended to work on Linux. The server we will be training on runs Linux and all libraries plus code have been confirmed to work on Ubuntu's latest stable distribution.

---
## Preparing the Game Files 

After the dependencies have been installed the necessary game files, all zipped inside of the **StreetFighterIISpecialChampionEdition-Genesis** directory, can be setup. The game files need to be copied into the actual game data files inside the installation of the retro library on your local machine. This location can be found by running the following lines in the command line:  

`python3`  
`import retro`  
`print(retro.__file__)`    

That should return the path to where the retro __init__.py script is stored. One level up from that should be the data folder. Inside there should be the stable folder. Copy the **StreetFighterIISpecialChampionEdition-Genesis** folder that is in the top level of the repo here. Inside the folder should be the following files:

-rom.md    
-rom.sha    
-scenario.json  
-data.json  
-metadata.json  
-reward_script.lua   
-Several .state files with each having the name of a specific fighter from the game  

With that the game files should be correctly set up and you should be able to run a test agent. 

---
## The first test run

To double check that the game files were properly set up the example agent can be run. cd into the src directory. Then either run the following command on your terminal:

`python3 Agent.py -r`

Or you can open Agent.py and execute it from your preferred IDE of choice by supplying the -r flag during execution flag. Without that flag the Agent will play the games however they will not render and you will not be able to watch it. When running on the server via an ssh shell it is important to leave this flag off as an error will be thrown when trying to render. This is Agent that essentially button mashes. It does a random move every frame update despite what is going on in the game. If everything was installed correctly it should simply one by one open up each save state in the game directory and run through the fights set up for it. This will involve a small window popping up showing the game running at a very high speed. Once the fight is over a new window should open up with the next fight. Once all fights are over the program should kill itself and close all windows.

---
## How to make an agent

To make your own agent it is recommended to make a class that inherits from Agent.py. Agent.py contains several useful helper functions that allow you to:

-Find and loop through every save state  
-Handle opening and cleaning up of the gym environment  
-Recording data during the fights
-And even training the agent after the fights

Some of these methods aren't filled in but the overall framework in place makes it easy to drop in your own versions of the getMove, train, and initialize network functions such that there is little work outside of network design that has to be done to get your agent up and running. The goal is to create a streamlined platform to rapidly prototype, train, and deploy new agents instead of starting for scratch every time. As well enforcing the interface for the agent class allows for high level software to be developed that can import various user created agents without fear of breaking due to interface issues. 

### Agent class

There are four main functions that need to be implemented in order to create a new intelligent agent.

-getMove  
-initializeNetwork  
-prepareMemoryForTraining  
-trainNetwork

Each section below gives a description of the interface required for each function and it's purpose. Further documentation can be seen inside the code of Agent.py

#### getMove

Get move simply returns a multivariate array of the action space of the game. A one in a given index represents the button corresponding to that index being pressed, a zero means the button is not pressed. This way multiple buttons can be pushed in one move and special moves can be preformed. This function must take in the observation and info about the current state. The observation is the contents of each pixel of the game screen and info is a dictionary containing key word mapped variables as specified in data.json. The indices correspond to Up, Down, Left, Right, A, B, X, Y, L, R.

#### initializeNetwork

initializeNetwork does whatever under the hood set up needs to be done to either create a network from scratch, if the load flag is supplied when initializing an Agent then a pretrained model will be loaded instead and this function does not need to be implemented. It does not take in any parameters but its expected to return the model desired for the Agent.

#### prepareMemoryForTraining

As the Agent plays it records the events during a fight. It records observation, state, action, reward, next observation, next state reward sequences. Each index in the memory buffer of the Agent demonstrates a state the Agent was presented with, the action it took, the next state the action led to, the reward the Agent received for that action, and a flag specifying if that game instance is finished. State and next state are both dictionaries containing the RAM data of the game at those times as specified in Data.json. The action is an array that represents a sampling of the action space as presented by the Agent where a one represents a given button being pressed and a zero is that button not being pressed. And finally Done is a boolean flag where True means the current game instance is over. Is expected to return an array containing the full set of prepared training data. The elements of these steps may change over time but their indices are stored in a set of static variables in Agent.py as follows:

-OBSERVATION_INDEX   
-STATE_INDEX   
-ACTION_INDEX   
-REWARD_INDEX   
-NEXT_OBSERVATION_INDEX   
-NEXT_STATE_INDEX   
-DONE_INDEX   

A child class can access them by calling {class_name}.{variable_name}. Indexing into a step to get the next observation from the DeepQAgent for example would look like:

`step[DeepQAgent.NEXT_OBSERVATION_INDEX]`

#### trainNetwork

Takes in the prepared training data and the current model and runs a desired amount of training epochs on it. The trained model is then returned once training is finished.

---

### Training Checkpoints

A training episode consists of one play through of each save state in the game folder. Once the episode is complete training will be run and after the trained and updated model is returned a checkpoint will be made by Agent.py in order to save the model for later use. As well custom training logs will be made for each unique class that is training that will show the training error of the Agent as it is learning. These logs and models are stored in the logs and models directories respectively and are formatted as models/{class_name}{Log} and logs/{class_name}{Model}. Note that the formatting is based on the class name and so only one instance of a model for each unique class can be stored as of now.

### Watch Agent

Watch Agent is a basic script that allows the user to load in a pretrained Agent and visualize it playing the game. It is useful to use this in conjunction with checkpoints in order to pause an Agent between episodes and view it's progress to understand if it's headed in the right direction and that things are working correctly.

## Json Files

There are three json files that the gym environment reads in order to setup the high level "rules" of the emulation. These files are metadata.json, data.json, and scenario.json. 

### Metadata.json

The metadata.json file holds high level global information about the game environment. For now this simply tells the environment the default save state that the game ROM should launch in if none has been selected. 

### Data.json

The data.json file is an abstraction of the games ram into callable variables with specified data types that the environment, user, and environment.json files can interact with. A complete list of named variables and their corresponding addresses in memory can be found listed in the file itself. If a publicly available RAM dump for a game can not be found finding new variables on your own is an involved process and requires monitoring RAM and downloading the bizhawk emulator. Bizhawk is an emulator used for developing tool assisted speedruns and has a wide selection of tools for RAM snooping. This video is a good reference for learning how to snoop RAM:

https://www.youtube.com/watch?v=zsPLCIAJE5o&t=900s

### Scenario.json

Scenario.json specifies several conditions over which that define the goal of the simulation or specify what criteria the agent will be judged on for rewards. The main specifications are the reward function and the done flag. The reward function for the StreetFighterAgents is seperated into it's own lua script to make designing a more complex reward function easier. The script can be imported and pointed to for use by gym-retro's environment for it's reward function by including the code snippet in scenario.json as follows:

```

"reward": {
        "script": "lua:calculate_reward"
    },
"scripts": [
        "reward_script.lua"
    ],

```

#### Reward Function

The reward function specifies what variables make up the reward function and what weights are assigned, whether that be positive or negative, to each variable. After each action is taken by an agent a reward calculated by this function is returned to the agent. This is then recorded and stored for later training after all fights in an epoch are finished. For now the default reward function utilizes the agent's score, agent's health, the enemy health, the number of rounds the agent has won, and the number of rounds the enemy has won. 

#### Done

Done is a flag that signifies whether the current environment has completed. Currently Done is set if the enemy or the agent get two round wins, which in game is what determines if a match is over. So once the match is over the agent moves onto the next save state.

---
## Generating New Save States

Save states are generated by a user actually saving their games state while playing in an emulator. In order to make new save states to contribute to the variety of matches your agent will play in you have to actually play the Street Fighter ROM up until the point you want the agent to start at. 

### Installing the Emulator

Retroarch is the emulator that is needed to generate the correct save states under the hood. It can be installed at:  
https://www.retroarch.com/?page=platforms


### Preparing the Cores

Retroarch needs a core of the architecture it is trying to simulate. The Street Fighter ROM we are working with is for the Sega Genisis. Retro actually has a built in core that can be copy and pasted into Retroarchs core folder and this is their recommended installation method. However finding the retroarch installation folder can be difficult and so can finding the cores in the Retro library. Instead open up Retroarch and go into Load Core. Inside Load Core scroll down and select download core. Scroll way down until you see genesis_plus_gx_libretro.so.zip and install it. Now go back to the main menu and select Load Content. Navigate to the Street Fighter folder at the top level of the repo and load the rom.md file. From here the game should load up correctly.

### Saving states

F2 is the shortcut key that saves the current state of the game. The state is saved to the currently selected game state slot. This starts at slot zero and can be incremented with the F6 key and decremented with the F7 key. When a fight is about to start that you want to create a state for hit F2. Then I would recommend incrementing the save slot by pressing F6 so that if you try to save another state you don't accidentally overwrite the last state you saved. There are 8 slots in total. By pressing F5 and going to view->settings-Directory you can control where the save states are stored. The states will be saved with the extension of 'state' plus the number of the save slot it was saved in. To prep these for usage cleave off the number at the end of each extension and rename each file to the name of the fighter that the agent will be going up against plus some other context information if necessary. Then move these ROMS into the game files inside of retro like when preparing the game files after the initial cloning of the repo. Once inside that repo each state should be zipped independently of one another. Once this happens the extension will now be .zip, remove this from the extension so that the extension still remains .state. The states are now ready to be loaded by the agent. Every time you load up the emulator decrement all the way back to zero again. 

---
## Example Implemented Agents

### DeepQAgent

DeepQAgent is an implementation of the DeepQ reinforcement algorithm for playing StreetFighter using policy gradients, a dense reward function, and greedy exploration controlled by an epsilon value that decreases as the model is trained. Each action the Agent takes during a fight is rewarded after a change in time in order to see what effect the move had on the fight outcome. When the model is first initialized it plays completely randomly in order to kick start rapid greedy exploration. As the model trains epsilon slowly decreases until the model begins to take over now that it has watched random play for a while and hopefully picked up some techniques. Below is a description the implementation of each of the abstract functions required for a child class. The observation of the current state is not actually used in training as building a network to do feature extraction for each stage and fighter combination from image data would be incredibly hard. That information is thrown away and instead only the RAM data is used to train.

#### Get Move

 The RAM data of the current state is converted into a feature vector by the helper function prepareNetworkInputs. Several parts of the RAM data such as the enemy character, player and enemy_state, and more are one hot encoded so that mutual independence is established. This leads to a feature vector containing 30 elements that is fed into the network. The output of the network decides what move the Agent will take from a preset move list where the move is then mapped to a set of inputs via a look up table and fed into the environment. The activation function of the output layer is a softmax function that assigns a probability to each possible move. These probabilities all sum to one and the move with the highest probability is picked as the action the Agent will undertake. However whenever a move is requested by the Agent a random number is generated, if this number is below the epsilon value, which ranges from 0 to 1 and decreases over time towards a lower bound during training, a random move is picked instead. This forces exploration of new strategies by the Agent. However this exploration is not informed by any model the Agent has and so is simply random greedy exploration. 

#### initializeNetwork

The input layer is the size of the info about the state space that is created in prepareNetworkInputs when converting the RAM info of the current state into a feature vector. There are 5 hidden layers all with linear activations. The output layer is the size of the predefined user action space. Note that this is not the same as the action space of the game. The action space of the game is the number of buttons the Agent can possibly press, however to assist the Agent a predefined set of button inputs for specific moves and combos have been established to chose from. So the output of the network is the size of the predefined set of moves. The output activation function is softmax so that each predefined move is assigned a probability by the network that all sum to one. 

#### preprareMemoryForTraining

Each time step from the training game memory has the RAM data from the game converted into a 30 element feature vector described in the top of the section. That is the only preparation needed. The states where the Agent is locked in hit stun or is in the middle of a move could be filtered out but as their reward is zero they will not effect the training weights. However they do slow down the training time so future updates will most likely filter them out for performance's sake. The observation, next_state, and done flag are thrown out in this model for simplicities sake. However they will be utilized in future updates.

#### trainNetwork

For training the method of policy gradients is used. A dense reward function has been designed so that the Agent can be given frequent rewards for using good moves. Policy gradients essentially uses the reward for each state, action, new state sequence as the gradient for training our network. The gradient vector then has the index of the move chosen set to the reward and all other indices are left zero. So the network is either trained to pick solely that move more or less in that state depending on the reward, but other moves are not penalized. 

---
## References:
https://github.com/openai/retro/issues/33 (outdated but helpful)   
https://medium.com/aureliantactics/integrating-new-games-into-retro-gym-12b237d3ed75 (Very helpful for writing the json files) 
https://github.com/keon/deep-q-learning (Someones basic implementation of DeepQ in python) 

https://www.youtube.com/watch?v=JgvyzIkgxF0 (reinforcement learning intro video)   
https://www.youtube.com/watch?v=0Ey02HT_1Ho (more advanced techniques)   
http://karpathy.github.io/2016/05/31/rl/ (good article on basic reinforcement learning)   
https://towardsdatascience.com/reinforcement-learning-lets-teach-a-taxi-cab-how-to-drive-4fd1a0d00529 (article on deep q learning for learning atari games)   
