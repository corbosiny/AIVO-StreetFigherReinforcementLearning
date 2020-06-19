# Source Code

This directory contains all of the source code pertaining to the project.

## Main Source Code

### Agent

This file contains all of the backend code for interfacing with the retro environment, storing data, and managing training over several training episodes. All other agents inherit from this code and must implement four abstract methods in order to keep with the desired interface for an Agent. More can be read in the "How to make an Agent" section of the main README in the top level directory. Running this by itself will open up a fight with each character among the Street Fighter 2 roster and will play randomly against them. The Agent was designed to not have to know anything about the game or the type of model it is training so the game that this is working with or model the user implements are free to be changed at any state of development.

### DeepQAgent

A DeepQ Reinforcement learning model implemented using a dense reward function and policy gradients for training.

## Helper Scripts

### LossHistory

A class used to store the training error logs after each training episode as consistent with the typical keras log format. 

### watchAgent

A helper script that when run loads in a desired network and lets the user visualize how well the network is running on some test save states. 
