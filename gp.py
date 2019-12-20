from deap import gp, creator, base, tools, algorithms
from enviroment import Enviroment
from agents import *
import operator
import matplotlib.pyplot as plt
import pydot
from IPython.display import Image
from enum import Enum
from multiprocessing import Process

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
    return ActionEnum.ATTACK

def ret_deffense():
    return ActionEnum.DEFFENSE

def ret_evade():
    return ActionEnum.EVASION


def return_individual():
    func = toolbox.compile(expr = "if_then_else(compare(mul(compare(compare(mul(add(5, compare(-1, 100)), compare(3, 0)), mul(compare(False, ARG0), compare(ARG2, compare(3, 10)))), mul(compare(mul(1, 0), add(5, True)), add(mul(True, add(mul(3, ARG0), add(ARG1, add(5, 3)))), compare(3, 5)))), compare(compare(add(compare(mul(5, mul(False, compare(1, add(False, 100)))), ARG2), compare(mul(1, ARG2), ARG0)), mul(mul(3, ARG0), compare(-1, ARG1))), compare(mul(compare(mul(False, ARG0), mul(compare(5, ARG0), ARG2)), mul(True, True)), compare(add(True, -1), mul(ARG2, mul(3, -1)))))), mul(add(compare(add(compare(mul(False, True), 1), add(False, 10)), mul(compare(5, add(5, -1)), add(0, 10))), add(compare(compare(mul(-1, 100), ARG0), compare(100, 5)), compare(mul(ARG2, add(1, 3)), compare(0, mul(100, compare(mul(False, ARG1), compare(0, ARG0))))))), compare(add(compare(mul(mul(mul(100, 5), compare(compare(ARG0, mul(-1, 10)), compare(mul(5, ARG1), compare(10, -1)))), mul(3, 3)), mul(0, False)), mul(compare(10, add(100, mul(10, ARG0))), compare(3, False))), compare(mul(add(-1, 5), compare(ARG0, 0)), mul(add(ARG0, 3), compare(ARG1, mul(3, ARG0))))))), if_then_else(compare(add(compare(compare(compare(ARG2, -1), compare(1, -1)), compare(compare(-1, 100), add(compare(3, 1), 0))), mul(add(mul(ARG2, 100), compare(compare(100, ARG0), True)), mul(add(100, 3), add(ARG2, 10)))), add(add(mul(compare(False, ARG2), mul(100, 3)), mul(add(ARG1, mul(mul(True, ARG1), 1)), mul(ARG0, 5))), mul(mul(compare(ARG0, ARG1), add(False, True)), compare(mul(ARG2, compare(compare(ARG1, ARG1), 1)), mul(add(ARG0, 1), ARG2))))), if_then_else(compare(mul(compare(compare(3, ARG2), compare(10, 3)), mul(compare(compare(ARG1, mul(-1, add(add(-1, 10), add(5, 5)))), 3), compare(5, ARG0))), mul(add(compare(ARG1, ARG2), add(10, False)), add(compare(True, 100), add(1, -1)))), if_then_else(compare(compare(mul(True, 100), mul(ARG2, add(ARG1, compare(10, 10)))), mul(compare(-1, compare(ARG1, mul(True, add(100, ARG1)))), add(1, mul(compare(compare(3, 3), compare(compare(ARG2, -1), ARG2)), 3)))), if_then_else(compare(compare(0, 0), compare(-1, 10)), if_then_else(compare(add(10, compare(1, ARG1)), compare(ARG0, ARG1)), if_then_else(True, ret_evade, if_then_else(False, ret_attack, ret_attack)), if_then_else(True, ret_attack, if_then_else(compare(add(add(3, 5), True), 3), ret_attack, if_then_else(compare(compare(True, 0), compare(1, ARG1)), if_then_else(compare(False, False), if_then_else(True, ret_deffense, ret_deffense), if_then_else(True, ret_attack, ret_evade)), if_then_else(compare(False, 10), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_deffense, ret_deffense)))))), if_then_else(compare(True, 5), if_then_else(False, ret_attack, ret_evade), if_then_else(compare(add(-1, True), 1), if_then_else(False, ret_deffense, if_then_else(False, if_then_else(True, ret_evade, ret_deffense), ret_evade)), ret_attack))), if_then_else(compare(compare(ARG2, ARG2), add(0, False)), if_then_else(compare(True, 5), if_then_else(False, ret_attack, ret_deffense), if_then_else(False, ret_deffense, ret_attack)), if_then_else(compare(1, True), if_then_else(False, ret_evade, ret_evade), if_then_else(True, ret_attack, ret_attack)))), if_then_else(compare(compare(mul(False, 3), compare(3, 10)), compare(add(add(ARG1, ARG1), add(-1, 0)), add(mul(100, ARG2), add(5, ARG0)))), if_then_else(compare(add(ARG0, -1), mul(100, mul(ARG2, 1))), if_then_else(compare(ARG0, ARG2), ret_deffense, if_then_else(False, ret_deffense, if_then_else(compare(0, ARG2), ret_attack, ret_deffense))), if_then_else(compare(10, -1), if_then_else(compare(compare(-1, compare(ARG0, ARG0)), ARG2), if_then_else(True, ret_deffense, ret_attack), ret_evade), if_then_else(True, ret_evade, ret_deffense))), if_then_else(compare(compare(5, ARG2), mul(100, 100)), if_then_else(compare(mul(-1, 0), True), if_then_else(True, ret_deffense, ret_attack), if_then_else(True, ret_deffense, ret_evade)), if_then_else(compare(10, 1), if_then_else(compare(ARG2, False), ret_deffense, ret_evade), if_then_else(False, ret_evade, if_then_else(compare(mul(10, ARG2), 100), ret_evade, if_then_else(False, ret_deffense, ret_attack))))))), if_then_else(compare(compare(mul(add(10, 1), add(10, 1)), mul(mul(ARG1, 5), add(0, ARG1))), compare(add(add(1, ARG2), compare(True, 100)), add(mul(True, False), mul(ARG2, 0)))), if_then_else(compare(add(add(True, 100), mul(add(100, compare(ARG2, compare(ARG1, True))), 0)), mul(mul(add(False, 1), True), compare(10, 10))), if_then_else(compare(compare(True, compare(ARG2, 3)), add(3, 10)), if_then_else(compare(False, True), if_then_else(compare(3, 1), ret_deffense, ret_attack), if_then_else(False, ret_evade, ret_evade)), ret_evade), if_then_else(compare(compare(ARG0, 0), compare(3, add(ARG1, 100))), if_then_else(compare(0, 100), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_deffense, ret_evade)), if_then_else(compare(False, 5), if_then_else(True, ret_attack, ret_attack), if_then_else(compare(3, 0), ret_deffense, ret_attack)))), if_then_else(compare(add(compare(1, 100), add(-1, compare(10, 3))), add(compare(mul(100, False), True), compare(3, 1))), if_then_else(compare(mul(False, ARG1), compare(ARG1, True)), if_then_else(compare(100, ARG0), if_then_else(False, ret_attack, ret_evade), if_then_else(True, ret_attack, ret_evade)), if_then_else(compare(1, 100), if_then_else(True, ret_deffense, ret_deffense), if_then_else(True, ret_deffense, if_then_else(False, ret_attack, ret_evade)))), if_then_else(compare(add(True, mul(5, add(3, ARG1))), compare(compare(mul(False, False), -1), 100)), if_then_else(compare(False, add(0, 10)), if_then_else(False, ret_attack, ret_evade), if_then_else(False, ret_attack, ret_attack)), if_then_else(compare(add(0, compare(100, 1)), ARG1), if_then_else(compare(100, 10), ret_evade, ret_deffense), if_then_else(True, ret_attack, ret_deffense)))))), if_then_else(compare(add(compare(mul(compare(compare(0, mul(True, 1)), ARG0), add(-1, 3)), add(compare(100, True), add(ARG1, True))), compare(add(add(5, ARG1), mul(100, False)), mul(compare(-1, False), compare(ARG2, mul(ARG0, 100))))), mul(compare(compare(compare(ARG2, mul(add(0, 1), compare(compare(ARG2, add(-1, -1)), compare(ARG1, 1)))), add(add(ARG2, 1), False)), add(mul(True, True), mul(0, ARG2))), compare(compare(mul(1, ARG2), mul(-1, 10)), compare(compare(0, 5), compare(mul(ARG0, 1), add(False, add(mul(100, compare(0, -1)), 5))))))), if_then_else(compare(compare(compare(compare(True, 10), add(10, 3)), add(compare(True, True), add(add(1, mul(False, ARG1)), add(100, compare(ARG2, compare(ARG1, True)))))), mul(add(mul(10, -1), mul(add(10, ARG0), -1)), compare(mul(10, add(-1, add(1, ARG2))), mul(5, 10)))), if_then_else(compare(compare(add(3, ARG2), mul(1, 5)), mul(add(100, True), mul(5, -1))), if_then_else(compare(compare(True, compare(mul(-1, True), 100)), mul(-1, -1)), if_then_else(compare(0, False), if_then_else(False, ret_attack, ret_evade), if_then_else(compare(10, mul(10, ARG2)), if_then_else(False, ret_evade, if_then_else(False, ret_evade, ret_attack)), ret_evade)), if_then_else(compare(100, ARG2), if_then_else(True, if_then_else(True, if_then_else(True, ret_deffense, ret_evade), ret_attack), ret_deffense), if_then_else(True, ret_attack, if_then_else(compare(-1, -1), ret_attack, ret_evade)))), if_then_else(compare(mul(100, ARG2), compare(compare(ARG1, add(1, 1)), ARG1)), if_then_else(compare(100, 3), if_then_else(False, ret_attack, ret_evade), if_then_else(False, ret_deffense, if_then_else(False, ret_evade, ret_deffense))), if_then_else(compare(0, add(ARG0, 3)), if_then_else(False, ret_deffense, if_then_else(compare(3, 5), ret_attack, if_then_else(False, ret_deffense, ret_deffense))), if_then_else(False, ret_attack, ret_attack)))), if_then_else(compare(mul(add(add(add(add(5, 100), 3), mul(100, 10)), compare(3, True)), compare(100, ARG0)), compare(compare(True, 5), mul(ARG0, True))), if_then_else(compare(mul(-1, 5), mul(3, 10)), if_then_else(compare(10, True), if_then_else(False, ret_attack, ret_attack), if_then_else(False, ret_deffense, if_then_else(False, ret_evade, ret_attack))), if_then_else(compare(1, True), if_then_else(True, ret_evade, ret_attack), if_then_else(True, ret_evade, if_then_else(False, ret_attack, ret_deffense)))), if_then_else(compare(compare(5, compare(ARG1, 3)), mul(0, False)), if_then_else(compare(True, ARG0), if_then_else(False, ret_evade, ret_deffense), if_then_else(False, if_then_else(True, if_then_else(False, ret_attack, ret_deffense), ret_evade), ret_evade)), if_then_else(compare(5, 10), if_then_else(False, if_then_else(True, ret_attack, ret_attack), if_then_else(compare(ARG1, 0), ret_evade, if_then_else(False, if_then_else(True, ret_deffense, ret_deffense), ret_attack))), if_then_else(False, ret_attack, ret_deffense))))), if_then_else(compare(add(ARG0, mul(add(3, compare(ARG2, -1)), mul(False, mul(ARG1, False)))), compare(mul(compare(add(1, False), 100), mul(ARG1, 0)), mul(mul(-1, 1), mul(add(mul(mul(add(5, 3), False), 10), False), -1)))), if_then_else(compare(mul(compare(0, 1), add(3, 0)), mul(compare(True, 10), compare(ARG1, -1))), if_then_else(compare(add(ARG1, ARG1), compare(mul(compare(False, 5), False), ARG1)), if_then_else(compare(1, compare(True, False)), if_then_else(False, if_then_else(False, if_then_else(True, ret_deffense, if_then_else(compare(-1, ARG0), ret_deffense, ret_deffense)), ret_deffense), ret_evade), if_then_else(False, if_then_else(False, ret_deffense, ret_deffense), ret_deffense)), ret_deffense), if_then_else(compare(compare(3, False), mul(-1, False)), if_then_else(compare(10, ARG0), if_then_else(False, ret_deffense, ret_deffense), if_then_else(True, ret_deffense, if_then_else(True, ret_deffense, ret_evade))), if_then_else(compare(0, add(mul(False, True), True)), if_then_else(compare(ARG0, ARG1), ret_attack, ret_evade), if_then_else(True, ret_evade, ret_attack)))), if_then_else(compare(compare(100, -1), add(compare(3, 3), mul(-1, 5))), if_then_else(compare(add(5, mul(mul(3, 0), 100)), add(-1, mul(-1, compare(5, add(mul(ARG1, True), ARG0))))), if_then_else(compare(-1, 10), if_then_else(True, ret_deffense, if_then_else(False, ret_attack, if_then_else(True, ret_attack, ret_evade))), if_then_else(False, ret_evade, ret_attack)), if_then_else(compare(ARG2, True), if_then_else(True, ret_attack, ret_attack), if_then_else(True, if_then_else(True, ret_deffense, if_then_else(compare(-1, ARG0), ret_deffense, ret_deffense)), ret_attack))), if_then_else(compare(mul(100, 1), compare(3, 10)), if_then_else(compare(5, 100), if_then_else(True, ret_attack, if_then_else(compare(ARG0, ARG2), ret_evade, ret_attack)), if_then_else(True, if_then_else(compare(False, 100), ret_attack, ret_evade), ret_evade)), if_then_else(compare(5, compare(10, False)), if_then_else(True, ret_attack, ret_attack), if_then_else(True, ret_deffense, ret_deffense)))))))")
    return func





env1 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
env2 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
env3 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
agent1_two = Stable_defensive_agent(2)
agent2_two = Stable_defensive_agent(2)
agent3_two = Stable_defensive_agent(2)
semi_result = [0,0,0]

def simulate_one_game(index, env, agent_one, agent_two):
    game_over = False
    state = env.reset()
    agent_one_actions = []
    agent_two_actions = []
    while game_over == False:
        actions_two = agent_two.choose_actions(state, agent_one_actions)
        actions_one = agent_one.choose_actions(state, agent_two_actions)

        step_count, (game_over, rocketOne_health, rocketTwo_health), state, agent_one_actions, agent_two_actions = env.next_step(actions_one, actions_two)

    semi_result[index-1] = step_count - agent_one.penalty


def paralel_fitness(ind):
    func = toolbox.compile(expr=ind)
    agent1_one = Genetic_agent(1, func)
    agent2_one = Genetic_agent(1, func)
    agent3_one = Genetic_agent(1, func)

    p1 = Process(target=simulate_one_game, args=(1, env1, agent1_one, agent1_one,))
    p2 = Process(target=simulate_one_game, args=(2, env2, agent2_one, agent2_one,))
    p3 = Process(target=simulate_one_game, args=(3, env3, agent3_one, agent3_one,))
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    return sum(semi_result)



def fitness(ind):
    # return 100,
    func = toolbox.compile(expr=ind)
    agent_one = Genetic_agent(env1.screen, 1, func)
    result = 0
    games_count = 1
    for i in range(games_count):
        game_over = False
        state = env1.reset()
        agent_one_actions = []
        agent_two_actions = []
        while game_over == False:
            # events = pygame.event.get(pygame.KEYDOWN)
            # all_keys = pygame.key.get_pressed()
            actions_two = agent1_two.choose_actions(state, agent_one_actions)
            actions_one = agent_one.choose_actions(state, agent_two_actions)

            step_count, (game_over, rocketOne_health, rocketTwo_health), state, agent_one_actions, agent_two_actions = env1.next_step(actions_one, actions_two)

        result = result + step_count
        if agent_one.attack_count == 0:
            result = result - 500
        if agent_one.evasion_count == 0:
            result = result - 500

    return (result // games_count) - agent_one.penalty,

class Bool(object): pass

pset = gp.PrimitiveSetTyped("main", [int, int, int], ActionEnum)
pset.addPrimitive(if_then_else, [Bool, ActionEnum, ActionEnum], ActionEnum)
pset.addPrimitive(compare, [int, int], Bool)
pset.addPrimitive(operator.mul, [int, int], int)
pset.addPrimitive(operator.add, [int, int], int)
# pset.addPrimitive(operator.and_,[bool,bool], bool)
pset.addTerminal(100, int)
pset.addTerminal(10, int)
pset.addTerminal(5, int)
pset.addTerminal(3, int)
pset.addTerminal(1, int)
pset.addTerminal(-1, int)
pset.addTerminal(0, int)
pset.addTerminal(ret_attack, ActionEnum)
pset.addTerminal(ret_deffense, ActionEnum)
pset.addTerminal(ret_evade, ActionEnum)
# pset.addTerminal(ActionEnum.ATTACK ,ActionEnum)
# pset.addTerminal(ActionEnum.DEFFENSE,ActionEnum)
# pset.addTerminal(ActionEnum.EVASION,ActionEnum)
# pset.addTerminal(True, bool)
pset.addTerminal(False, Bool)


creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, type_=ActionEnum, min_=7, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

toolbox.register("evaluate", fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

pop = toolbox.population(n=6)
hof = tools.HallOfFame(5)

stats_fit = tools.Statistics(lambda ind: ind.fitness.values[0])
stats_size = tools.Statistics(len)
mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
mstats.register("avg", np.mean)
mstats.register("std", np.std)
mstats.register("min", np.min)
mstats.register("max", np.max)

if __name__ == "__main__":
    # pass
    paralel_fitness(toolbox.individual())
    # print(toolbox.individual())
    # pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 10, stats=mstats, halloffame=hof, verbose=True)
    # print(f"hof[0]: {hof[0]}")
    # print(f"hof[1]: {hof[1]}")
    # print(f"hof[2]: {hof[2]}")
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