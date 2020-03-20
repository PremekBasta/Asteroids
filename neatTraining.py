import neat
import os
from enviroment import *
from agents import *
from multiprocessing import *


def simulate_one_game(index, env, agent_one, agent_two, return_vals):

    game_over = False
    state = env.reset()
    #global semi_result
    while game_over == False:
        actions_one = agent_one.choose_actions(state)
        actions_two = agent_two.choose_actions(state)


        step_count, (game_over, rocket_one_won), state, (reward_one, reward_two) = env.next_step(actions_one, actions_two)



    #semi_result[index-1] = step_count - agent_one.penalty
    #print(semi_result)
    #return step_count


    result = step_count

    if agent_one.defense_count == 0:
        result = result - 500
    result = result + agent_one.defense_count
    agent_one.defense_count = 0

    if agent_one.attack_count == 0:
        result = result - 500
    result = result + agent_one.attack_count
    agent_one.attack_count = 0

    if agent_one.evasion_count == 0:
        result = result - 1000
    result = result + agent_one.evasion_count
    agent_one.evasion_count = 0

    if agent_one.stop_count == 0:
        result = result - 500
    agent_one.stop_count = 0

    if rocket_one_won:
        result = result + 2000
    else:
        result = result - 1000

    return_vals[index] = result
    return result

def fitness(net):
    env = Enviroment()
    agent_one = Neat_agent(1, net)
    agent_two = Stable_defensive_agent(2)
    ret_vals = [0]
    result = simulate_one_game(0, env, agent_one, agent_two, ret_vals)
    return result

def parallel_fitness(net, num_cores):

    manager = Manager()
    return_vals = manager.dict()
    agents_one = [Neat_agent(1,net) for i in range(num_cores)]
    agents_two = [Stable_defensive_agent for i in range(num_cores)]
    envs = [Enviroment() for i in range(num_cores)]
    processes = [Process(target=simulate_one_game, args=(i, envs[i], agents_one[i], agents_two[i], return_vals)) for i in range(num_cores)]

    for i in range(num_cores):
        processes[i].start()
    for i in range(num_cores):
        processes[i].join()
    result = sum(return_vals.values()) // num_cores
    return result,



def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = fitness(net)
        #genome.fitness = parallel_fitness(net, 4)


def run(config_file, episodes_num):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, episodes_num)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


    #visualize.draw_net(config, winner, True, node_names=node_names)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    run(config_path,10)