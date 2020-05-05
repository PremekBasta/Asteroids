from enviroment import *
from agents import *


class DQAgent:
    def __init__(self, num_inputs, num_outputs, batch_size = 32, num_batches = 16):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.eps = 1.0
        self.eps_decay = 0.995
        self.gamma = 0.95
        self.exp_buffer = []
        self.build_model()

    # vytvari model Q-site
    def build_model(self):
        self.model = tf.keras.models.Sequential([tf.keras.layers.Dense(24, activation=tf.nn.relu, input_dim=self.num_inputs, name='dense_1'),
                                                 tf.keras.layers.Dense(24, activation=tf.nn.relu, name = 'dense_02'),
                                                 tf.keras.layers.Dense(self.num_outputs, activation='linear')])
        opt = tf.keras.optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=opt, loss='mse')

    # vraci akci agenta - pokud trenujeme tak epsilon-greedy, jinak nejlepsi podle site
    def action(self, state, train=False):
        if train and np.random.uniform() < self.eps:
            return np.random.randint(self.num_outputs)
        else:
            return np.argmax(self.model.predict(state)[0])

    # ulozeni informaci do experience bufferus
    def record_experience(self, exp):
        self.exp_buffer.append(exp)
        if len(self.exp_buffer) > 2000:
            self.exp_buffer = self.exp_buffer[-2000:]

    # trenovani z bufferu
    def train(self):
        if (len(self.exp_buffer) <= self.batch_size):
            return

        for _ in range(self.num_batches):
            batch = random.sample(self.exp_buffer, self.batch_size)
            states = np.array([s for (s, _, _, _, _) in batch])
            next_states = np.array([ns for (_, _, _, ns, _) in batch])
            states = states.reshape((-1, self.num_inputs))
            next_states = next_states.reshape((-1, self.num_inputs))
            pred = self.model.predict(states)
            next_pred = self.model.predict(next_states)
            # spocitame cilove hodnoty
            for i, (s, a, r, ns, d) in enumerate(batch):
                pred[i][a] = r
                if not d:
                    pred[i][a] = r + self.gamma*np.amax(next_pred[i])

            self.model.fit(states, pred, epochs=1, verbose=0)
        # snizime epsilon pro epsilon-greedy strategii
        if self.eps > 0.01:
            self.eps = self.eps*self.eps_decay


if __name__ == "__main__":
    # vytvorime agenta (4 vstupy, 2 akce)
    agent = DQAgent(4, 2)
    env = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)



    # spustime trenovani na 1000 epizodach prostredi
    rewards = []
    for i in range(1000):
        obs = env.reset()
        obs = np.reshape(obs, newshape=(1, -1))
        done = False
        R = 0
        t = 0
        while not done:
            old_state = obs
            action = agent.action(obs, train=True)
            obs, r, done, _ = env.step(action)
            R += r
            t += 1
            r = r if not done else 10
            obs = np.reshape(obs, newshape=(1, -1))
            agent.record_experience((old_state, action, r, obs, done))
        agent.train()

        rewards.append(R)
        print(i, R)