from DeepQAgent import *

"""Makes a DeepQ Agent and runs it through one fight for each character in the roster so the user can view it"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Processes agent parameters.')
    parser.add_argument('-n', '--name', type= str, default= None, help= 'Name of the instance that will be used when saving the model or it\'s training logs')
    args = parser.parse_args()
    qAgent = DeepQAgent(load= True, epsilon= 0, name= args.name)

    from Lobby import Lobby
    testLobby = Lobby(render= True)
    testLobby.addPlayer(qAgent)
    testLobby.executeTrainingRun(review= False)
