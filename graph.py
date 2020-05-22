import matplotlib.pyplot as plt
import numpy as np

def plot_multi_bar():
    averaged_actions1 = [5.25500000e+02, 7.54333333e+02, 8.33333333e-02, 0.00000000e+00]
    averaged_actions2 = [558.5       , 444.91666667,  24.58333333,   0.        ]
    #plans = ["Rotace \nvlevlo", "Rotace \nvpravo", "Akcelerace", "Střela", "Rozdvojovací \nstřela", "Prázdná \nakce"]
    plans = ["Útok", "Obrana", "Úhyb", "Zastavení"]

    ind = np.arange(4)
    width = 0.27

    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, averaged_actions1, width, color='r')
    rects2 = ax.bar(ind+width, averaged_actions2, width, color='g')

    ax.set_ylabel("Počet vybrání plánu")
    ax.set_xticks(ind+width)
    ax.set_xticklabels(plans, rotation=90)
    ax.legend((rects1[0], rects2[0]),('agent z experimentu č.2', 'agent z experimentu č.5'))

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.title("Průměrný počet kroků hry: 1694.5\nVýsledek: 10:2")
    #plt.suptitle("Výsledek: 10:8")
    plt.show()


    axs = plt.subplot(111)
    axs.bar(averaged_actions1, height=[10, 15, 20])
    axs.bar(averaged_actions2, y=10)

    plt.xlabel("common X")
    plt.ylabel("common Y")
    # plt.figure(figsize=(18, 6))
    # axs[0].bar(plans, averaged_actions1)
    # axs[0].set(ylabel = 'Počet vybrání akce')

    # axs[1].bar(plans, averaged_actions2)
    # axs[1].set(xlabel = "Akce", ylabel='Počet vybrání akce')

    plt.show()



def plot_games_times():
    times = []
    lengths = []
    with open("Recalculaction_of_plans.txt", mode="r") as f:
        #for count, line in enumerate(f, start=0):
        #    splits = line.split()
        #    times.append(float(splits[1]))
        #    lengths.append(float(splits[2]))

        print(times)
        print(lengths)




        #averaged_plans = [60.5,1885,15.6,20.8]
        #plans = ["Útok", "Obrana", "Úhyb", "Zastavevní"]

        averaged_actions = [1260.3, 0.2, 10.5, 0.1, 221.6, 0.3]
        plans = ["Rotace \nvlevlo", "Rotace \nvpravo", "Akcelerace", "Střela", "Rozdvojovací \nstřela",
                 "Prázdná \nakce"]

        plt.figure(figsize=(8, 6))
        plt.title("Průměrný počet kroků hry: 1493")
        plt.suptitle("Výsledek: 0:10")
        plt.bar(plans,averaged_actions)
        #plt.ylabel('Reward')
        #plt.xticks(rotation="vertical")
        plt.xlabel('Elementární akce')
        plt.ylabel("Počet vybrání akce ")

        plt.show()


def plot_results_of_games():
    rewards = []
    with open("HL_DQ/extended_model_training_3001.txt", mode="r") as f:
        for count, line in enumerate(f, start=0):
            if (count + 0) % 3 == 0:
                splits = line.split()
                print(splits[1])
                rewards.append(int(splits[1]))

        print(len(rewards))
        averaged_rewards = []

        average_batch_count = 1
        for i in range(0, len(rewards), average_batch_count):
            averaged_rewards.append(np.average(rewards[i:i + average_batch_count]))
        # print(averaged_rewards)

        plt.figure(figsize=(12, 8))
        plt.plot(averaged_rewards, "o")
        plt.title("Průběh trénování")
        plt.ylabel('Výsledná odměna')
        plt.xlabel('Zahraná hra')
        #plt.xticks(range(0,3000,500))
        plt.show()

if __name__ == "__main__":
    #plot_games_times()
    plot_multi_bar()

