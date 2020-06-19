import gym
env = gym.make('LunarLander-v2')
env.reset()

for _ in range(30):
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample())
    if done == True:
        break
 
env.close()
