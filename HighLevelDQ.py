import os
from multiprocessing import *
from filelock import FileLock
from datetime import datetime
from enviroment import *
from agents import *

class Model_holder():
    def __init__(self, get_queue, post_queues, num_inputs, num_outputs, batch_size = 32, num_batches = 64, model = None):
        self.get_queue = get_queue
        self.post_queues = post_queues
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.eps = 1.0
        self.eps_decay = 0.9985
        self.gamma = 0.95
        self.exp_buffer = []
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.buffer_size = 5000
        if model is None:
            self.model = self.build_model()
        else:
            self.model = model


    def build_model(self):
        self.model = tf.keras.models.Sequential([tf.keras.layers.Dense(24, activation=tf.nn.relu, input_dim=self.num_inputs),
                                                 tf.keras.layers.Dense(24, activation=tf.nn.relu),
                                                 tf.keras.layers.Dense(self.num_outputs, activation='linear')])
        opt = tf.keras.optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=opt, loss='mse')

    def choose_action_plan_index(self, state):
        if np.random.uniform() < self.eps:
            val = np.random.randint(self.num_outputs)
            #self.history[val] += 1
            return val
        else:
            val = np.argmax(self.model.predict(state)[0])
            #self.history[val] += 1
            return val

    def start_processing_queue(self):
        while True:
            state, process_num = self.get_queue.get()
            if state is None:
                continue
            action_index = self.choose_action_plan_index(state)
            self.post_queues[process_num].put(action_index)

    def train(self, input_buffers):
        for buffer in input_buffers:
            #self.exp_buffer = self.exp_buffer + buffer
            for item in buffer:
                self.exp_buffer.append(item)


        if (len(self.exp_buffer) <= self.batch_size):
            return

        for _ in range(self.num_batches):
            batch = random.sample(self.exp_buffer, self.batch_size)
            states = np.array([s for (s, _, _, _, _) in batch])
            print(states)
            next_states = np.array([ns for (_, _, _, ns, _) in batch])
            print(next_states)
            states = states.reshape((-1, self.num_inputs))
            next_states = next_states.reshape((-1, self.num_inputs))
            pred = self.model.predict(states)
            next_pred = self.model.predict(next_states)
            # spocitame cilove hodnoty
            for i, (s, a, r, ns, go) in enumerate(batch):
                pred[i][a] = r
                if not go:
                    pred[i][a] = r + self.gamma*np.amax(next_pred[i])

            self.model.fit(states, pred, epochs=1, verbose=0)
        if self.eps > 0.01:
            self.eps = self.eps*self.eps_decay




def simulate_one_game(index, env, agent_one, agent_two, episode_num, exp_buffers, post_queue, get_queues, file):
    rewards = []
    state = env.reset()
    agent_one.history = [0,0,0,0]
    transformed_state, action_plans = agent_one.get_state_info(state)
    transformed_state = np.reshape(transformed_state, newshape=(1, -1))
    game_over = False
    R = 0
    while not game_over:
        old_transformed_state = transformed_state

        post_queue.put((transformed_state, index))
        #action_plan_index = agent_one.choose_action_plan_index(transformed_state)
        action_plan_index = get_queues[index].get()
        while action_plan_index is None:
            action_plan_index = get_queues.get()

        actions_one = agent_one.get_action_from_action_plan(action_plan_index, action_plans)

        actions_two = agent_two.choose_actions(state, [])

        step_count, (game_over, rocket_one_won), state, (reward_one, reward_two) = env.next_step(actions_one, actions_two)
        if game_over:
            if rocket_one_won:
                reward_one += 2000
            else:
                reward_one += -1000

        transformed_state, action_plans = agent_one.get_state_info(state)
        transformed_state = np.reshape(transformed_state, newshape=(1, -1))

        R += reward_one
        agent_one.record_experience(
            (old_transformed_state, action_plan_index, reward_one, transformed_state, game_over))
    exp_buffers[index] = agent_one.exp_buffer
    print(f"episode: {episode_num}, index: {index} finished")
    #agent_one.train()

    #print(f"episode_num: {episode_num}, thread_num: {index}, reward: {R}, history: {agent_one.history}")
    #with FileLock("myfile.txt.lock"):
    #    file.write("#, " + str(episode_num) + ", " + str(index) + ", " + str(R) + "\n")
    #    file.write(str(agent_one.history) + "\n\n")
    #    file.flush()
    #semi_result[index-1] = step_count - agent_one.penalty
    #print(semi_result)
    #return step_count
    #return_vals[index] = result
    #return

def train_parallel(num_cores = 4, num_episodes = 200):


    processes = []
    manager = Manager()

    model_holder_queue = manager.Queue(maxsize=100)
    agent_queues = []
    for i in range(num_cores-1):
        agent_queues.append(manager.Queue())

    exp_buffers = manager.list()
    for i in range(num_cores):
        exp_buffers.append(manager.list())
    model_holder = Model_holder(model_holder_queue, agent_queues, num_inputs=4, num_outputs=4)


    agents_one = [None for i in range(num_cores-1)]
    agents_two = [Stable_defensive_agent(2) for i in range(num_cores-1)]
    envs = [Enviroment() for i in range(num_cores-1)]

    agents_one[0] = DQAgent(player_number=1, num_inputs=4, num_outputs=4, model=None)
    for i in range(1, num_cores-1):
        agents_one[i] = DQAgent(player_number=1, num_inputs=4, num_outputs=4, model=None)


    with open("model_multiprocessing_training.txt", "w+") as f:
        for episode_num in range(num_episodes):
            processes.append(Process(target=model_holder.start_processing_queue))
            for i in range(num_cores-1):
                processes.append(
                    Process(target=simulate_one_game, args=(i, envs[i], agents_one[i], agents_two[i], episode_num,
                                                            exp_buffers, model_holder_queue, agent_queues, f)))



            for i in range(num_cores):
                processes[i].start()
            for i in range(1, num_cores):
                processes[i].join()

            processes[0].kill()
            processes[0].join()

            for i in range(num_cores):
                print(f"process {i} is alive: {processes[i].is_alive()}")

            model_holder.train(exp_buffers)



            #agents_one[0].train(exp_buffers[0])
            #exp_buffers[0] = []
            processes = []

        #result = sum(return_vals.values()) // 6
        #return result,

def train_single_thread(num_episodes):
    with open("model_training_2000", "w+") as f:
        agent_one = DQAgent(player_number=1, num_inputs=4, num_outputs=4)
        agent_two = Stable_defensive_agent(2)
        env = Enviroment()
        for i in range(num_episodes):
            rewards = []
            agent_one.history = [0, 0, 0, 0]
            state = env.reset()
            transformed_state, action_plans = agent_one.get_state_info(state)
            transformed_state = np.reshape(transformed_state, newshape=(1, -1))
            game_over = False
            R = 0
            while not game_over:
                old_transformed_state = transformed_state
                action_plan_index = agent_one.choose_action_plan_index(transformed_state)
                actions_one = agent_one.get_action_from_action_plan(action_plan_index, action_plans)

                actions_two = agent_two.choose_actions(state, [])

                step_count, (game_over, rocket_one_won), state, reward = env.next_step(actions_one, actions_two)
                if not game_over:
                    reward += 1

                else:
                    if rocket_one_won:
                        reward += 2000
                    else:
                        reward += -1000

                transformed_state, action_plans = agent_one.get_state_info(state)
                transformed_state = np.reshape(transformed_state, newshape=(1, -1))

                R += reward

                agent_one.record_experience(
                    (old_transformed_state, action_plan_index, reward, transformed_state, game_over))
            agent_one.train()

            # rewards.append(R)
            print(i, R)
            f.write(str(i) + " " + str(R) + "\n")
            print(agent_one.history)
            f.write(str(agent_one.history))
            f.write('\n\n')
    agent_one.model.save(os.path.dirname(os.path.realpath(__file__)) + "/model_single_2000")
    f.close()





if __name__ == '__main__':
    print(datetime.now())
    #train_single_thread(2000)
    train_parallel(4,100)
    print(datetime.now())