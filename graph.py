import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    rewards = []
    with open("2462_sensor_4inputs_data.txt", mode="r") as f:
        for count, line in enumerate(f, start=0):
            if count % 2 == 0:
                splits = line.split()
                print(splits[1])
                rewards.append(int(splits[1]))

        print(len(rewards))
        averaged_rewards = []

        for i in range(0, len(rewards), 20):
            averaged_rewards.append(np.average(rewards[i:i+20]))
        #print(averaged_rewards)

        plt.figure(figsize=(12,8))
        #plt.plot(rewards, "ro")
        plt.plot(averaged_rewards, "-")
        plt.ylabel('Reward')
        plt.xlabel('Episode')
        #plt.yticks()
        plt.show()
        #plt.savefig("1250-rewarasdds.png")