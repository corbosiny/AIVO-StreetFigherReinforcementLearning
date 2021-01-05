import retro

def main(game= 'StreetFighterIISpecialChampionEdition-Genesis',  state= "chunli"):
    env = retro.make(game= game, state= state)
    obs = env.reset()
    while True:
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()
    env.close()

if __name__ == "__main__":
    main()
