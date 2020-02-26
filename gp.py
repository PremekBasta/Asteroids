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
    func = toolbox.compile(expr = "if_then_else(compare(mul(add(mul(mul(add(1, 5), mul(-1, 3)), mul(mul(1, 5), add(ARG1, 5))), mul(add(add(ARG1, ARG1), add(ARG0, ARG1)), add(add(5, ARG2), mul(ARG2, ARG1)))), mul(add(add(add(-1, -1), mul(5, ARG1)), add(add(0, 100), add(3, 5))), add(add(mul(ARG2, 3), add(5, 5)), add(mul(100, 5), add(1, 3))))), mul(add(add(mul(add(ARG1, -1), mul(ARG2, -1)), mul(add(ARG1, 100), mul(ARG1, ARG0))), add(add(add(1, ARG2), add(100, 1)), mul(add(ARG1, ARG2), mul(ARG1, 10)))), add(add(add(add(100, ARG2), add(0, 5)), mul(add(5, 3), mul(100, 10))), mul(add(mul(100, ARG0), mul(-1, ARG0)), add(add(100, 5), add(ARG2, 3)))))), if_then_else(compare(mul(mul(add(mul(ARG1, -1), add(5, 10)), mul(add(0, ARG0), mul(ARG2, -1))), add(add(mul(ARG2, 100), mul(1, ARG1)), add(mul(-1, -1), add(5, 100)))), mul(add(add(add(ARG2, ARG2), add(3, 3)), mul(add(1, 10), mul(3, ARG0))), add(add(add(10, 1), add(ARG0, ARG0)), mul(mul(100, 1), add(100, 5))))), if_then_else(compare(mul(add(add(ARG0, 3), add(1, ARG0)), mul(mul(0, 10), add(5, 3))), mul(mul(mul(0, ARG2), mul(ARG0, 1)), add(add(0, 10), mul(1, 3)))), if_then_else(compare(mul(mul(100, 1), add(1, 10)), add(add(10, 0), add(ARG1, ARG1))), if_then_else(compare(mul(ARG1, ARG1), mul(ARG1, ARG2)), if_then_else(compare(ARG1, -1), if_then_else(False, ret_attack, ret_attack), if_then_else(False, ret_deffense, ret_stop)), if_then_else(compare(-1, ARG1), if_then_else(False, ret_attack, ret_deffense), if_then_else(False, ret_attack, ret_stop))), if_then_else(compare(add(0, ARG2), add(100, 0)), if_then_else(compare(5, ARG0), if_then_else(False, ret_stop, ret_deffense), if_then_else(False, ret_stop, ret_deffense)), if_then_else(compare(ARG0, 5), if_then_else(False, ret_stop, ret_evade), if_then_else(False, ret_deffense, ret_evade)))), ret_attack), if_then_else(compare(add(add(add(ARG2, 10), mul(1, 1)), add(mul(ARG2, 5), add(100, 5))), add(mul(add(ARG0, ARG0), mul(1, 3)), mul(mul(5, 3), add(-1, 5)))), if_then_else(compare(mul(mul(1, 5), add(0, 3)), mul(mul(0, 1), add(1, 3))), if_then_else(compare(add(ARG0, ARG0), mul(0, 0)), if_then_else(False, if_then_else(False, ret_stop, ret_evade), if_then_else(False, ret_attack, ret_deffense)), if_then_else(compare(0, 0), if_then_else(False, ret_attack, ret_deffense), if_then_else(False, ret_evade, ret_evade))), if_then_else(compare(mul(100, 3), add(100, 3)), if_then_else(compare(100, -1), if_then_else(False, ret_stop, ret_deffense), if_then_else(False, ret_attack, ret_evade)), if_then_else(compare(100, ARG2), if_then_else(False, ret_evade, ret_deffense), if_then_else(False, ret_evade, ret_evade)))), if_then_else(compare(mul(add(ARG0, 10), add(10, 1)), mul(add(add(ARG2, ARG2), mul(1, 10)), mul(ARG0, 1))), if_then_else(compare(mul(ARG1, 0), mul(1, 10)), if_then_else(compare(10, ARG2), if_then_else(False, ret_stop, ret_deffense), if_then_else(False, ret_evade, ret_evade)), if_then_else(compare(100, -1), if_then_else(False, ret_attack, ret_attack), if_then_else(False, ret_stop, ret_attack))), if_then_else(compare(mul(5, ARG2), mul(10, 1)), if_then_else(compare(ARG2, 0), if_then_else(False, ret_stop, ret_stop), if_then_else(False, ret_evade, ret_deffense)), if_then_else(compare(5, 100), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_stop, ret_deffense)))))), if_then_else(compare(add(mul(mul(mul(5, ARG2), add(10, ARG1)), mul(add(-1, ARG1), add(ARG1, -1))), add(add(mul(1, 1), mul(ARG2, 100)), add(add(100, 10), mul(5, 1)))), mul(mul(add(mul(ARG1, ARG2), mul(0, 1)), add(add(0, 5), mul(ARG1, ARG0))), add(add(mul(5, 0), mul(1, 3)), mul(mul(ARG2, 5), add(ARG0, 0))))), if_then_else(compare(add(mul(add(ARG2, 10), add(ARG0, 1)), mul(add(100, 100), mul(ARG2, ARG1))), mul(mul(add(ARG1, -1), add(10, -1)), add(mul(1, 5), add(10, 10)))), if_then_else(compare(add(add(0, 10), add(ARG1, 100)), add(mul(ARG2, 100), mul(-1, 1))), if_then_else(compare(add(-1, ARG1), mul(10, ARG2)), if_then_else(compare(5, 0), ret_stop, if_then_else(False, ret_attack, ret_stop)), if_then_else(compare(ARG1, 10), if_then_else(False, ret_evade, ret_attack), if_then_else(False, ret_attack, ret_deffense))), if_then_else(compare(ARG1, 100), if_then_else(False, ret_evade, ret_deffense), if_then_else(False, ret_evade, ret_stop))), if_then_else(compare(mul(add(1, ARG0), add(ARG0, 100)), add(add(10, ARG0), add(ARG1, 5))), if_then_else(compare(mul(ARG1, -1), mul(100, -1)), if_then_else(compare(5, ARG2), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_deffense, ret_deffense)), if_then_else(compare(3, ARG1), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_stop, ret_deffense))), if_then_else(compare(add(3, 1), mul(ARG0, 1)), if_then_else(compare(1, 10), if_then_else(False, ret_evade, ret_evade), if_then_else(False, ret_stop, ret_deffense)), if_then_else(compare(ARG2, 100), if_then_else(False, if_then_else(compare(mul(ARG0, ARG1), mul(0, 10)), if_then_else(compare(ARG1, ARG1), if_then_else(False, ret_stop, ret_evade), if_then_else(False, ret_deffense, ret_attack)), if_then_else(compare(ARG1, 10), if_then_else(False, ret_stop, ret_stop), if_then_else(False, ret_evade, ret_evade))), ret_attack), if_then_else(False, ret_evade, ret_evade))))), if_then_else(compare(add(add(add(100, 3), add(3, ARG1)), mul(add(ARG2, ARG1), mul(100, 1))), mul(mul(mul(10, ARG2), mul(-1, ARG2)), mul(mul(-1, ARG1), add(1, 5)))), if_then_else(compare(mul(mul(1, 100), mul(0, ARG1)), add(mul(1, ARG0), mul(0, ARG0))), if_then_else(compare(mul(5, 0), add(3, 10)), if_then_else(compare(5, 5), if_then_else(False, ret_deffense, ret_evade), if_then_else(False, ret_attack, ret_stop)), if_then_else(compare(ARG0, ARG1), if_then_else(False, ret_evade, ret_attack), if_then_else(False, ret_attack, ret_deffense))), if_then_else(compare(add(ARG2, 10), mul(3, 5)), if_then_else(compare(-1, ARG1), if_then_else(False, ret_evade, ret_stop), if_then_else(False, ret_evade, ret_stop)), if_then_else(compare(-1, 3), if_then_else(False, ret_attack, ret_evade), if_then_else(False, ret_deffense, ret_attack)))), if_then_else(compare(mul(add(0, 10), mul(-1, 10)), mul(mul(5, 0), mul(100, 5))), if_then_else(compare(mul(ARG0, ARG1), mul(0, 10)), if_then_else(compare(ARG1, ARG1), if_then_else(False, ret_stop, ret_evade), if_then_else(False, ret_deffense, ret_attack)), if_then_else(compare(ARG1, 10), if_then_else(False, ret_stop, ret_stop), if_then_else(False, ret_evade, ret_evade))), if_then_else(compare(mul(100, -1), add(0, 100)), if_then_else(compare(ARG0, 3), if_then_else(False, ret_deffense, ret_attack), if_then_else(False, ret_attack, ret_deffense)), if_then_else(compare(100, 5), if_then_else(False, ret_attack, ret_deffense), if_then_else(False, ret_deffense, ret_stop)))))))")
    return func




envs = [Enviroment() for i in range(6)]
agents_one = [None for i in range(6)]
agents_two = [Stable_defensive_agent(2) for i in range(6)]
funcs = [None for i in range(6)]

env1 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
env2 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
env3 = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
agent1_two = Stable_defensive_agent(2)
agent2_two = Stable_defensive_agent(2)
agent3_two = Stable_defensive_agent(2)
semi_result = [0,0,0,0,0,0,0]



def simulate_one_game(index, env, agent_one, agent_two, return_vals):

    game_over = False
    state = env.reset()
    agent_one_actions = []
    agent_two_actions = []
    global semi_result
    while game_over == False:
        actions_two = agent_two.choose_actions(state, agent_one_actions)
        actions_one = agent_one.choose_actions(state, agent_two_actions)

        step_count, (game_over, rocket_one_won), state, agent_one_actions, agent_two_actions = env.next_step(actions_one, actions_two)


    print(step_count)

    semi_result[index-1] = step_count - agent_one.penalty
    print(semi_result)
    return step_count


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
    return



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


    func1 = toolbox.compile(expr=ind)
    func2 = toolbox.compile(expr=ind)
    func3 = toolbox.compile(expr=ind)
    agent1_one = Genetic_agent(1, func1)
    agent2_one = Genetic_agent(1, func2)
    agent3_one = Genetic_agent(1, func3)



    p1 = Process(target=simulate_one_game, args=(1, env1, agent1_one, agent1_two))
    p2 = Process(target=simulate_one_game, args=(2, env2, agent2_one, agent2_two))
    p3 = Process(target=simulate_one_game, args=(3, env3, agent3_one, agent3_two))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    global semi_result

    print(semi_result)
    
    print("finished")

    # result = pool.amap(simulate_one_game, [1,2,3], [env1, env2, env3], [agent1_one, agent2_one, agent3_one], [agent1_two, agent2_two, agent3_two])
    #while not result.ready():
    #    print(result.ready())
    #    time.sleep(0.01)
    # a = 50
    # a,b,c = result.get()

# p1 = Process(target=simulate_one_game, args=(1, env1, agent1_one, agent1_two,))
    # p2 = Process(target=simulate_one_game, args=(2, env2, agent2_one, agent2_two,))
    # p3 = Process(target=simulate_one_game, args=(3, env3, agent3_one, agent3_two,))
    # p1.start()
    # p2.start()
    # p3.start()
    #
    # p1.join()
    # p2.join()
    # p3.join()
    #
    # return sum(semi_result)

    for i in range(len(processes)):
        processes[i].start()
    for i in range(len(processes)):
        processes[i].join()
    result = sum(return_vals.values()) // 6
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

            step_count, (game_over, agent_one_won), state, agent_one_actions, agent_two_actions = env1.next_step(actions_one, actions_two)

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

pset = gp.PrimitiveSetTyped("main", [int, int, int], ActionPlanEnum)
pset.addPrimitive(if_then_else, [Bool, ActionPlanEnum, ActionPlanEnum], ActionPlanEnum)
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
pset.addTerminal(ret_attack, ActionPlanEnum)
pset.addTerminal(ret_deffense, ActionPlanEnum)
pset.addTerminal(ret_evade, ActionPlanEnum)
pset.addTerminal(ret_stop, ActionPlanEnum)
# pset.addTerminal(ActionPlanEnum.ATTACK ,ActionPlanEnum)
# pset.addTerminal(ActionPlanEnum.DEFFENSE,ActionPlanEnum)
# pset.addTerminal(ActionPlanEnum.EVASION,ActionPlanEnum)
# pset.addTerminal(True, bool)
pset.addTerminal(False, Bool)


creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, type_=ActionPlanEnum, min_=7, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

toolbox.register("evaluate", paralel_fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


pop = toolbox.population(n=15)
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
    # pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 250, stats=mstats, halloffame=hof, verbose=True)
    # print(f"hof[0]: {hof[0]}")
    # print(f"hof[1]: {hof[1]}")
    # print(f"hof[2]: {hof[2]}")
    # print(f"hof[3]: {hof[3]}")
    # print(f"hof[4]: {hof[4]}")

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