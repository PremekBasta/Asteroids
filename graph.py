import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    rewards = []
    with open("LL_DQ_stable_deffensive_opponent/10000_base_action_DQ_stable_deffensive_opponent_2.txt", mode="r") as f:
        for count, line in enumerate(f, start=0):
            if (count + 0) % 4 == 0:
                splits = line.split()
                print(splits[5])
                rewards.append(int(splits[5]))

        print(len(rewards))
        averaged_rewards = []

        average_batch_count = 200
        for i in range(0, len(rewards), average_batch_count):
            averaged_rewards.append(np.average(rewards[i:i+average_batch_count]))
        #print(averaged_rewards)

        plt.figure(figsize=(12,8))
        plt.plot(averaged_rewards, "-")
        plt.ylabel('Reward')
        plt.xlabel('Episode')
        plt.show()