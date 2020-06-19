import retro

def main(game= 'StreetFighterIISpecialChampionEdition-Genesis',  state= "chunli"):
    env = retro.make(game= game, state= state)
    obs = env.reset()
    while True:
        env.render()
        userInput = input("Enter a set of moves in the action space {0}:".format(env.action_space))
        separateInputs = userInput.split(',')
        action = [int(value) for value in separateInputs]
        obs, rew, done, info = env.step(action)
        if done:
            obs = env.reset()
    env.close()

if __name__ == "__main__":
    main()
