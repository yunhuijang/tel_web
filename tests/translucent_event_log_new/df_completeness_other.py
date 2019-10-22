from pm4py.objects.log.importer.xes import factory as xes_importer
import os
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.simulation.playout import factory as sim_factory
from tests.translucent_event_log_new.algo.discover_petrinet import state_based_region as sb
from pm4py.algo.discovery.transition_system import factory as trans_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.algo.filtering.log.start_activities.start_activities_filter import get_start_activities
from pm4py.algo.filtering.log.end_activities.end_activities_filter import get_end_activities
from pm4py.objects.log.util import sampling
from pm4py.algo.discovery.heuristics import factory as heu_factory

model = "heu"
result_avg = []
result_num = []

print(model)

tree = 5
tree_num = 0
tree_avg = 0
print(tree)
for sam in range(1,11):
    print(sam)
    input_file_path = os.path.join("input_data", "df_complete_logs", "%d_1000_%d.xes"%(tree, sam))
    log = xes_importer.apply(input_file_path)
    dfg_org = dfg_factory.apply(log)
    start_act = set(get_start_activities(log).keys())
    end_act = set(get_end_activities(log).keys())
    #make petri net for simulation
    net, im, fm = heu_factory.apply(log)

    num = len(dfg_org.keys())
    sim_log = sim_factory.apply(net, im, parameters={'maxTraceLength':20, 'noTraces':1000})
    dfg_algo = dfg_factory.apply(log)
    start_act_algo = set(get_start_activities(sim_log).keys())
    end_act_algo = set(get_end_activities(sim_log).keys())

    score = 0
    su = 0

    for k in range(10):
        for n in range(1, 1000):
            sampled_log = sampling.sample_log(sim_log, no_traces=n)
            dfg_log = dfg_factory.apply(sampled_log)

            yes_dfg = 0

            for i in dfg_org.keys():
                if i in dfg_log.keys():
                    yes_dfg += 1

            if num == yes_dfg:
                if start_act == set(get_start_activities(sampled_log).keys()) and end_act == set(
                        get_end_activities(sampled_log).keys()):
                    print("%s df-complete"%model)
                    print(n)
                    score += n
                    su += 1
                    break
    if su > 0:
        score = score / su
        tree_num += 1
    else:
        score_tel = 0
    print("%d %d %s avg" % (tree, sam, model))
    print(score)
    tree_avg += score

if tree_num > 0:
    tree_avg /= tree_num
else:
    tree_avg = 0
result_avg.append(tree_avg)
result_num.append(tree_num)

print("%d_%s" %(tree, model))
print(tree_avg)
print(tree_num)

print("result")
print(model)

i = 0
print(i)
print(result_num[i])
print(result_avg[i])


