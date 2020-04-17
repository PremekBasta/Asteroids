from deap import gp, creator, base, tools, algorithms
from enviroment import Enviroment
from agents import *
import operator
import matplotlib.pyplot as plt
import pydot
from IPython.display import Image
from enum import Enum
from multiprocessing import *
import dill
from pathos.multiprocessing import ProcessingPool


#zobrazeni jedince jako stromu
def plot_tree(tree):
    nodes, edges, labels = gp.graph(tree)
    nodesDot = list(map(lambda x: pydot.Node(x, label=str(labels.get(x))),nodes))

    g = pydot.Dot(graph_type='graph')
    for node in nodesDot:
        g.add_node(node)
    for f,t in edges:
        edge = pydot.Edge(nodesDot[f], nodesDot[t])
        g.add_edge(edge)

    return g.create_png()

def if_then_else(input, output1, output2):
    return output1 if input else output2

def compare(val1, val2):
    return val1 > val2

def ret_attack():
    return ActionPlanEnum.ATTACK

def ret_deffense():
    return ActionPlanEnum.DEFFENSE

def ret_evade():
    return ActionPlanEnum.EVASION

def ret_stop():
    return ActionPlanEnum.STOP


def return_individual():
    func = toolbox.compile(expr = "if_then_else(compare(add(3, add(add(mul(ARG2, -1), add(mul(mul(mul(mul(mul(add(add(5, 10), add(ARG0, ARG2)), mul(mul(1, ARG1), add(0, ARG0))), mul(add(ARG1, 3), mul(0, 0))), ARG0), mul(mul(10, ARG2), ARG3)), mul(mul(3, 1), mul(add(3, 10), -1))), mul(mul(mul(mul(ARG2, ARG1), add(ARG3, add(mul(3, 1), add(5, 0)))), 5), add(add(add(mul(1, 0), add(ARG2, 1)), mul(3, ARG0)), add(3, 10))))), mul(add(add(add(mul(100, 1), add(100, 1)), add(mul(-1, -1), mul(5, ARG2))), add(add(add(3, mul(add(0, -1), add(add(mul(-1, 1), ARG2), add(mul(3, add(100, -1)), add(add(1, 5), add(ARG1, 10)))))), add(ARG3, add(mul(mul(-1, -1), mul(-1, 5)), add(add(add(add(add(3, ARG1), mul(0, 3)), mul(mul(ARG0, 1), add(100, 100))), 3), mul(3, 1))))), add(ARG0, mul(mul(add(add(ARG3, 0), mul(1, 1)), 3), mul(-1, ARG1))))), mul(mul(add(add(-1, mul(mul(add(add(1, add(mul(add(ARG1, 1), mul(10, -1)), add(-1, 1))), mul(10, ARG2)), mul(add(ARG1, 3), mul(0, 0))), mul(mul(0, add(add(1, add(ARG0, 100)), mul(mul(mul(-1, ARG0), add(ARG3, ARG2)), mul(mul(ARG3, -1), add(10, ARG2))))), add(0, add(10, ARG0))))), mul(mul(add(ARG0, 1), add(ARG0, ARG3)), add(add(add(ARG1, add(add(mul(add(ARG1, ARG0), mul(5, 0)), add(add(100, ARG3), add(3, ARG3))), add(mul(ARG0, mul(ARG1, 10)), add(1, ARG1)))), add(add(mul(add(ARG3, 3), 5), ARG2), add(mul(mul(add(ARG3, 3), 5), add(100, -1)), add(add(1, 5), add(add(add(ARG2, 3), mul(10, ARG3)), 100))))), add(0, 100)))), 5), mul(mul(add(1, mul(add(5, ARG3), add(1, ARG3))), mul(5, 100)), add(ARG0, mul(ARG0, add(add(add(ARG2, 3), mul(10, ARG3)), 100)))))))), mul(add(5, 5), add(add(add(10, -1), add(10, ARG0)), mul(add(ARG2, ARG1), mul(mul(mul(mul(mul(ARG0, 100), add(ARG1, 10)), add(3, 10)), 5), add(add(add(0, 0), add(ARG0, 10)), mul(mul(100, 10), add(add(mul(-1, add(ARG3, mul(0, 3))), ARG2), add(mul(mul(add(ARG3, 3), 5), add(100, -1)), add(add(1, 5), add(add(add(ARG2, 3), mul(10, ARG3)), 100))))))))))), if_then_else(compare(mul(add(ARG0, add(mul(100, 100), mul(0, ARG0))), 5), add(mul(100, 10), mul(mul(add(add(add(ARG1, add(add(mul(add(ARG1, ARG0), mul(-1, 100)), add(add(100, add(mul(ARG0, mul(ARG1, 10)), add(1, ARG1))), add(mul(add(5, 10), add(1, ARG3)), ARG3))), mul(mul(add(ARG3, ARG0), add(1, ARG2)), add(mul(0, ARG0), mul(ARG2, ARG2))))), add(add(mul(-1, add(ARG3, mul(0, 3))), ARG2), add(mul(mul(add(ARG3, 3), 5), add(100, -1)), add(add(1, 5), add(add(add(ARG2, 3), mul(10, ARG3)), 100))))), add(add(10, -1), add(add(mul(ARG3, mul(mul(mul(ARG0, 10), mul(ARG1, ARG0)), mul(add(1, 1), add(ARG1, 10)))), mul(10, ARG1)), add(add(ARG2, 100), mul(1, ARG2))))), mul(5, 3)), add(add(add(ARG0, 1), add(1, ARG3)), mul(add(ARG1, 100), mul(ARG3, 0)))))), if_then_else(False, ret_evade, ret_evade), if_then_else(False, if_then_else(False, ret_evade, ret_evade), ret_evade)), ret_attack)")
    return func




envs = [Enviroment() for i in range(6)]
agents_one = [None for i in range(6)]
agents_two = [Stable_defensive_agent(2) for i in range(6)]
funcs = [None for i in range(6)]

env1 = Enviroment()
env2 = Enviroment()
env3 = Enviroment()
agent1_two = Stable_defensive_agent(2)
agent2_two = Stable_defensive_agent(2)
agent3_two = Stable_defensive_agent(2)
semi_result = [0,0,0,0,0,0,0]


def simulate_one_game_wins(index, env, agent_one, agent_two, return_vals):
    game_over = False
    state = env.reset()
    while game_over == False:
        actions_two = agent_two.choose_actions(state)
        actions_one = agent_one.choose_actions(state)

        step_count, (game_over, rocket_one_won), state, _ = env.next_step(actions_one, actions_two)


    if rocket_one_won:
        result = 1
        #print(f"won + {result}")
    else:
        result = 0
        #print(result)

    #print(f"[{agent_one.attack_count}, {agent_one.defense_count}, {agent_one.evasion_count}, {agent_one.stop_count}]")

    agent_one.defense_count = 0
    agent_one.attack_count = 0
    agent_one.evasion_count = 0
    agent_one.stop_count = 0

    return_vals[index] = result
    return


def simulate_one_game(index, env, agent_one, agent_two, return_vals):
    game_over = False
    state = env.reset()
    while game_over == False:
        actions_two = agent_two.choose_actions(state)
        actions_one = agent_one.choose_actions(state)

        step_count, (game_over, rocket_one_won), state, _ = env.next_step(actions_one, actions_two)

    result = step_count

    def_ratio = agent_one.defense_count / step_count
    if(def_ratio>0.9 or def_ratio<0.6):
        result = result - 1000
    if agent_one.defense_count == 0:
        result = result - 500

    attack_ratio = agent_one.attack_count / step_count
    if(attack_ratio>0.3 or attack_ratio<0.05):
        result = result - 1000

    if(agent_one.attack_count>agent_one.defense_count):
        result = result - 1000

    if agent_one.evasion_count == 0:
        result = result - 1000


    if agent_one.stop_count == 0:
        result = result - 500

    if rocket_one_won:
        result = result + 2000
        print(f"won + {result}")
    else:
        result = result - 2000
        print(result)


    print(f"[{agent_one.attack_count}, {agent_one.defense_count}, {agent_one.evasion_count}, {agent_one.stop_count}]")

    agent_one.defense_count = 0
    agent_one.attack_count = 0
    agent_one.evasion_count = 0
    agent_one.stop_count = 0

    return_vals[index] = result
    return

def paralel_fitness_wins(ind):
    global funcs
    global agents_one
    global agents_two
    global envs

    processes=[]

    manager = Manager()
    return_vals = manager.dict()

    global currentBest
    #print(currentBest)

    for i in range(6):
        #funcs[i] = toolbox.compile(expr=ind)
        agents_one[i] = Genetic_agent(1, toolbox.compile(expr=ind))
        agents_two[i] = Genetic_agent(2, toolbox.compile(expr=currentBest))

        processes.append(Process(target=simulate_one_game_wins, args=(i, envs[i], agents_one[i], agents_two[i], return_vals)))


    for i in range(len(processes)):
        processes[i].start()
    for i in range(len(processes)):
        processes[i].join()
    result = sum(return_vals.values()) / len(processes)
    print(f"sum: {result}")
    return result,


def paralel_fitness(ind):
    pool = ProcessingPool(nodes=3)
    global funcs
    global agents_one
    global agents_two
    global envs

    processes=[]

    manager = Manager()
    return_vals = manager.dict()


    for i in range(6):
        funcs[i] = toolbox.compile(expr=ind)
        agents_one[i] = Genetic_agent(1, funcs[i])
        processes.append(Process(target=simulate_one_game, args=(i, envs[i], agents_one[i], agents_two[i], return_vals)))


    for i in range(len(processes)):
        processes[i].start()
    for i in range(len(processes)):
        processes[i].join()
    result = sum(return_vals.values()) // len(processes)
    print(f"sum: {result}" + 2 * "\n")
    return result,





def fitness(ind):
    func = toolbox.compile(expr=ind)
    agent_one = Genetic_agent(1, func)
    result = 0
    games_count = 4
    for i in range(games_count):
        game_over = False
        state = env1.reset()
        agent_one_actions = []
        agent_two_actions = []
        while game_over == False:
            actions_two = agent1_two.choose_actions(state, agent_one_actions)
            actions_one = agent_one.choose_actions(state, agent_two_actions)

            step_count, (game_over, agent_one_won), state = env1.next_step(actions_one, actions_two)

        result = result + step_count

        if agent_one.defense_count == 0:
            result = result - 500
        result = result + agent_one.defense_count
        agent_one.defense_count = 0

        if agent_one.attack_count == 0:
            result = result - 500
        result = result + agent_one.attack_count
        agent_one.attack_count = 0

        if agent_one.evasion_count == 0:
            result = result - 500
        agent_one.evasion_count = 0

        if agent_one.stop_count == 0:
            result = result - 500
        agent_one.stop_count = 0

        if agent_one_won:
            result = result + 2000
        else:
            result = result - 1000


    return (result // games_count),

class Bool(object): pass

pset = gp.PrimitiveSetTyped("main", [int, int, int, int, int], ActionPlanEnum)
pset.addPrimitive(if_then_else, [Bool, ActionPlanEnum, ActionPlanEnum], ActionPlanEnum)
pset.addPrimitive(compare, [int, int], Bool)
pset.addPrimitive(operator.mul, [int, int], int)
pset.addPrimitive(operator.add, [int, int], int)
pset.addTerminal(100, int)
pset.addTerminal(10, int)
pset.addTerminal(5, int)
pset.addTerminal(3, int)
pset.addTerminal(1, int)
pset.addTerminal(-1, int)
pset.addTerminal(0, int)
pset.addTerminal(ret_attack, ActionPlanEnum)
pset.addTerminal(ret_deffense, ActionPlanEnum)
pset.addTerminal(ret_evade, ActionPlanEnum)
pset.addTerminal(ret_stop, ActionPlanEnum)
pset.addTerminal(False, Bool)


creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, type_=ActionPlanEnum, min_=7, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

toolbox.register("evaluate", paralel_fitness_wins)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


pop = toolbox.population(n=10)
hof = tools.HallOfFame(5)

stats_fit = tools.Statistics(lambda ind: ind.fitness.values[0])
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", np.mean)
mstats.register("std", np.std)
mstats.register("min", np.min)
mstats.register("max", np.max)


def varOr(population, toolbox, lambda_, cxpb, mutpb):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover, mutation **or** reproduction). The modified individuals have
    their fitness invalidated. The individuals are cloned so returned
    population is independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param lambda\_: The number of children to produce
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: The final population.

    The variation goes as follow. On each of the *lambda_* iteration, it
    selects one of the three operations; crossover, mutation or reproduction.
    In the case of a crossover, two individuals are selected at random from
    the parental population :math:`P_\mathrm{p}`, those individuals are cloned
    using the :meth:`toolbox.clone` method and then mated using the
    :meth:`toolbox.mate` method. Only the first child is appended to the
    offspring population :math:`P_\mathrm{o}`, the second child is discarded.
    In the case of a mutation, one individual is selected at random from
    :math:`P_\mathrm{p}`, it is cloned and then mutated using using the
    :meth:`toolbox.mutate` method. The resulting mutant is appended to
    :math:`P_\mathrm{o}`. In the case of a reproduction, one individual is
    selected at random from :math:`P_\mathrm{p}`, cloned and appended to
    :math:`P_\mathrm{o}`.

    This variation is named *Or* beceause an offspring will never result from
    both operations crossover and mutation. The sum of both probabilities
    shall be in :math:`[0, 1]`, the reproduction probability is
    1 - *cxpb* - *mutpb*.
    """
    assert (cxpb + mutpb) <= 1.0, (
        "The sum of the crossover and mutation probabilities must be smaller "
        "or equal to 1.0.")

    offspring = []
    for _ in range(lambda_):
        op_choice = random.random()
        if op_choice < cxpb:            # Apply crossover
            ind1, ind2 = list(map(toolbox.clone, random.sample(population, 2)))
            ind1, ind2 = toolbox.mate(ind1, ind2)
            del ind1.fitness.values
            offspring.append(ind1)
        elif op_choice < cxpb + mutpb:  # Apply mutation
            ind = toolbox.clone(random.choice(population))
            ind, = toolbox.mutate(ind)
            del ind.fitness.values
            offspring.append(ind)
        else:                           # Apply reproduction
            offspring.append(random.choice(population))

    return offspring

def varAnd(population, toolbox, cxpb, mutpb):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their
              parents.

    The variation goes as follow. First, the parental population
    :math:`P_\mathrm{p}` is duplicated using the :meth:`toolbox.clone` method
    and the result is put into the offspring population :math:`P_\mathrm{o}`.  A
    first loop over :math:`P_\mathrm{o}` is executed to mate pairs of
    consecutive individuals. According to the crossover probability *cxpb*, the
    individuals :math:`\mathbf{x}_i` and :math:`\mathbf{x}_{i+1}` are mated
    using the :meth:`toolbox.mate` method. The resulting children
    :math:`\mathbf{y}_i` and :math:`\mathbf{y}_{i+1}` replace their respective
    parents in :math:`P_\mathrm{o}`. A second loop over the resulting
    :math:`P_\mathrm{o}` is executed to mutate every individual with a
    probability *mutpb*. When an individual is mutated it replaces its not
    mutated version in :math:`P_\mathrm{o}`. The resulting :math:`P_\mathrm{o}`
    is returned.

    This variation is named *And* beceause of its propention to apply both
    crossover and mutation on the individuals. Note that both operators are
    not applied systematicaly, the resulting individuals can be generated from
    crossover only, mutation only, crossover and mutation, and reproduction
    according to the given probabilities. Both probabilities should be in
    :math:`[0, 1]`.
    """
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring

currentBest = None
BestHistory = {None}

def eaSimple(population, toolbox, cxpb, mutpb, ngen, file, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution. The
    logbook will contain the generation number, the number of evalutions for
    each generation and the statistics if a :class:`~deap.tools.Statistics` is
    given as argument. The *cxpb* and *mutpb* arguments are passed to the
    :func:`varAnd` function. The pseudocode goes as follow ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring

    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.

    .. note::

        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.

    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """
    global currentBest
    global BestHistory
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        if halloffame is not None:
            if gen % 3 == 0:
                for best_ind in halloffame:
                    if (best_ind.fitness.values[0] > 0.7):
                        if(not str(best_ind) in BestHistory):
                #if(halloffame[0].fitness.values[0] > 0.7):
                    #if(not str(currentBest) in BestHistory):
                            print("new ind")
                            #print(f"new ind: {not currentBest in BestHistory}")
                            #print(f"different: {currentBest != halloffame[0]}")
                            currentBest = best_ind
                            BestHistory.add(str(currentBest))
                            f.write(f"{gen}: \n{currentBest}\n\n")
                            print(str(currentBest))
                            invalid_ind = [ind for ind in population]
                            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                            for ind, fit in zip(invalid_ind, fitnesses):
                                ind.fitness.values = fit
                            halloffame.clear()
                            break


        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        if halloffame is not None:
            halloffame.update(population)

        #for ind in halloffame:
        #    print(ind.fitness.values[0])
        #print()

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook



if __name__ == "__main__":
    currentBest = toolbox.individual()
    # pass
    #paralel_fitness(toolbox.individual())
    # print(toolbox.individual())
    with open("GP/gp_chaning_best_with_def_auto_write_txt_16_04", "+w") as f:

        pop, log = eaSimple(pop, toolbox, 0.6, 0.2, 1000, stats=mstats, halloffame=hof, verbose=True, file=f)
        #pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 250, stats=mstats, halloffame=hof, verbose=True)
        print(f"hof[0]: {hof[0]}")
        print(f"hof[1]: {hof[1]}")
        print(f"hof[2]: {hof[2]}")
        print(f"hof[3]: {hof[3]}")
        print(f"hof[4]: {hof[4]}")

        for ind in BestHistory:
            print(ind)

    # pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 50, stats=mstats, halloffame=hof, verbose=True)
    # print(f"hof[0]: {hof[0]}")
    # print(f"hof[1]: {hof[1]}")
    # print(f"hof[2]: {hof[2]}")
    # pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 100, stats=mstats, halloffame=hof, verbose=True)
    # print(f"hof[0]: {hof[0]}")
    # print(f"hof[1]: {hof[1]}")
    # print(f"hof[2]: {hof[2]}")


# start = time.time()
# print(paralel_fitness(toolbox.individual()))
# end = time.time()
# print(end - start)


# expr = toolbox.individual()
# print(expr)
# for ind in hof:
#     print(ind)
# print(hof[0])
# print(hof[0])

# Image(plot_tree(hof[0]))
# import matplotlib.pyplot as plt
# import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout
#
#
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)
#
# g = nx.Graph()
# g.add_nodes_from(nodes)
# g.add_edges_from(edges)
# # pos = nx.graphviz_layout(g, prog="dot")
#
# nx.draw(g, pos=graphviz_layout(g), node_size=1600, cmap=plt.cm.Blues,
#         node_color=range(len(g)),
#         prog='dot')
# plt.show()
#
# # nx.draw_networkx_nodes(g, pos)
# # nx.draw_networkx_edges(g, pos)
# # nx.draw_networkx_labels(g, pos, labels)
# # plt.show()