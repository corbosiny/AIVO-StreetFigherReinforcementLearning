import retro

def main(game= 'StreetFighterIISpecialChampionEdition-Genesis',  state= "chunli"):
    env = retro.make(game= game, state= state)
    env.reset()
    while True:
        env.render()
        userInput = input("Enter a set of moves in the action space {0}:".format(env.action_space))
        try:
            separateInputs = userInput.split(',')
            action = [int(value) for value in separateInputs]
        except:
            action = [0] * len(env.action_space.sample())
        _, _, done, _ = env.step(action)
        if done:
            env.reset()
    env.close()

if __name__ == "__main__": 
    main()
