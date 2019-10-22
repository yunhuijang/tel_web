from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
import os
from tests.translucent_event_log_new.algo.discover_petrinet import inductive_revise
from pm4py.objects.log.util import sampling
from tests.translucent_event_log_new.objects.tel.importer.xes import utils as xes_utils
from pm4py.algo.filtering.log.start_activities.start_activities_filter import get_start_activities
from pm4py.algo.filtering.log.end_activities.end_activities_filter import get_end_activities

tel_avg = []
log_avg = []
tel_num = 0
log_num = 0
tree = 10
tel_tree_num = 0
log_tree_num = 0
print(tree)
tree_avg_tel = 0
tree_avg_log = 0
for sam in range(1,11):
    print(sam)

    path = os.path.join("input_data", "df_complete_logs", "%d_1000_%d.xes" %(tree, sam))
    log = xes_importer.apply(path)
    tel = xes_importer.apply(path)
    xes_utils.set_enabled(tel)
    dfg_100 = dfg_factory.apply(log)
    start_act = set(get_start_activities(log).keys())
    end_act = set(get_end_activities(log).keys())

    result_norm = []
    result_tel = []

    num = len(dfg_100.keys())
    score_tel = 0
    score_log = 0
    su_tel = 0
    su_log = 0
    for k in range(10):
        for n in range(1,1000):
            sampled_tel = sampling.sample_log(tel, no_traces = n)
            dfg_log = dfg_factory.apply(sampled_tel)
            dfg_tel = inductive_revise.get_dfg_graph_trans(sampled_tel)
            dfg = dfg_log + dfg_tel

            yes_dfg = 0

            for i in dfg_100.keys():
                if i in dfg_tel.keys():
                   yes_dfg += 1

            if num == yes_dfg:
                if start_act == set(get_start_activities(sampled_tel).keys()) and end_act == set(get_end_activities(sampled_tel).keys()):
                    print("tel df-complete")
                    print(n)
                    score_tel += n
                    su_tel += 1
                    break
    if su_tel > 0:
        score_tel = score_tel / su_tel
        tel_tree_num +=1
    else:
        score_tel = 0
    print("%d %d tel avg"%(tree, sam))
    print(score_tel)
    tel_num += tel_tree_num
    tree_avg_tel += score_tel

    for k in range(10):
        for n in range(1,1000):
            sampled_log = sampling.sample_log(log, no_traces = n)
            dfg_log = dfg_factory.apply(sampled_log)
            yes_norm = 0
            for i in dfg_100.keys():
                if i in dfg_log.keys():
                    yes_norm += 1

            if num == yes_norm:
                if start_act == set(get_start_activities(sampled_log).keys()) and end_act == set(get_end_activities(sampled_log).keys()):
                    print("log df-complete")
                    print(n)
                    score_log += n
                    su_log += 1
                    break
    if su_log > 0:
        score_log = score_log / su_log
        log_tree_num +=1
    else:
        score_log = 0
    print("%d %d log avg" % (tree, sam))
    print(score_log)
    tree_avg_log += score_log

if tel_tree_num > 0:
    tree_avg_tel /= tel_tree_num
else:
    tree_avg_tel = 0
tel_avg.append(tree_avg_tel)
print("%d_tel"%tree)
print(tree_avg_tel)
print(tel_tree_num)

if log_tree_num > 0:
    tree_avg_log /= log_tree_num
else:
    tree_avg_log = 0
log_avg.append(tree_avg_log)
print("%d_log"%tree)
print(tree_avg_log)
print(log_tree_num)

for i in tel_avg:
    print(i)

for j in log_avg:
    print(j)

