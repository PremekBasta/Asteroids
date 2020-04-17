import matplotlib.pyplot as plt
import numpy as np


def plot_games_times():
    times = []
    lengths = []
    with open("Recalculaction_of_plans", mode="r") as f:
        #for count, line in enumerate(f, start=0):
        #    splits = line.split()
        #    times.append(float(splits[1]))
        #    lengths.append(float(splits[2]))

        print(times)
        print(lengths)

        #fix, axs = plt.subplots(2)
        #axs[0].plot(times)
        #axs[0].set(ylabel = 'Čas hry v sekundách')

        #axs[1].plot(lengths)
        #axs[1].set(xlabel='Počet pasivních kroků', ylabel='Počet kroků hry')

        #plt.show()

        averaged_plans = [1379.6,0.7,9.1,0.5,259.2,0.2]
        plans = ["Rotace \nvlevlo", "Rotace \nvpravo", "Akcelerace", "Střela", "Rozdvojovací \nstřela", "Prázdná \nakce"]

        plt.figure(figsize=(8,6))
        plt.title("Průměrný počet kroků hry: 1649.3")
        plt.suptitle("Výsledek: 0:10")
        plt.bar(plans,averaged_plans)
        #plt.ylabel('Reward')
        #plt.xticks(rotation="vertical")
        plt.xlabel('Akční plán')

        plt.show()


def plot_results_of_games():
    rewards = []
    with open("LL_DQ_stable_deffensive_opponent/10000_base_action_DQ_stable_deffensive_opponent_2.txt", mode="r") as f:
        for count, line in enumerate(f, start=0):
            if (count + 0) % 4 == 0:
                splits = line.split()
                print(splits[5])
                rewards.append(int(splits[5]))

        print(len(rewards))
        averaged_rewards = []

        average_batch_count = 500
        for i in range(0, len(rewards), average_batch_count):
            averaged_rewards.append(np.average(rewards[i:i + average_batch_count]))
        # print(averaged_rewards)

        plt.figure(figsize=(12, 8))
        plt.plot(averaged_rewards, "-")
        plt.ylabel('Reward')
        plt.xlabel('Episode')
        plt.show()

if __name__ == "__main__":
    plot_games_times()

