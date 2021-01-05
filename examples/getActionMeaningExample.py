import retro

def main(game= 'StreetFighterIISpecialChampionEdition-Genesis',  state= "chunli"):
    env = retro.make(game= game, state= state)
    obs = env.reset()
    spaceSize = len(env.action_space.sample())
    for i in range(spaceSize):
        action = [0] * spaceSize
        action[i] = 1
        print("The action", action, " represents:", env.get_action_meaning(action))
    env.close()

if __name__ == "__main__":
    main()