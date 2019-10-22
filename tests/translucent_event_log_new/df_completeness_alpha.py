from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
import os
from tests.translucent_event_log_new.algo.discover_petrinet import inductive_revise
from pm4py.objects.log.util import sampling
from tests.translucent_event_log_new.objects.tel.importer.xes import utils as xes_utils
from pm4py.algo.filtering.log.start_activities.start_activities_filter import get_start_activities
from pm4py.algo.filtering.log.end_activities.end_activities_filter import get_end_activities

alpha_avg = []
alpha_num = []

for tree in range(1,11):
    tel_tree_num = 0
    log_tree_num = 0
    print(tree)
    tree_avg_tel = 0
    tree_avg_log = 0
    for sam in range(1,11):
        print(sam)

        path = os.path.join("input_data", "df_complete_logs", "%d_1000_%d.xes" %(tree, sam))
        log = xes_importer.apply(path)
        dfg_org = dfg_factory.apply(log)
        start_act = set(get_start_activities(log).keys())
        end_act = set(get_end_activities(log).keys())

        alpha_path = os.path.join("input_data", "df_complete_logs", "df_complete_alpha", "%d_alpha_%d.xes" %(tree, sam))
        alpha_log = xes_importer.apply(alpha_path)

        num = len(dfg_org.keys())
        score_tel = 0
        su_tel = 0
        for k in range(10):
            for n in range(1,1000):
                sampled_log = sampling.sample_log(alpha_log, no_traces=n)
                dfg_log = dfg_factory.apply(sampled_log)

                yes_dfg = 0

                for i in dfg_org.keys():
                    if i in dfg_log.keys():
                       yes_dfg += 1

                if num == yes_dfg:
                    if start_act == set(get_start_activities(sampled_log).keys()) and end_act == set(get_end_activities(sampled_log).keys()):
                        print("alpha df-complete")
                        print(n)
                        score_tel += n
                        su_tel += 1
                        break
        if su_tel > 0:
            score_tel = score_tel / su_tel
            tel_tree_num +=1
        else:
            score_tel = 0
        print("%d %d alpha avg"%(tree, sam))
        print(score_tel)
        tree_avg_tel += score_tel

    if tel_tree_num > 0:
        tree_avg_tel /= tel_tree_num
    else:
        tree_avg_tel = 0
    alpha_avg.append(tree_avg_tel)
    alpha_num.append(tel_tree_num)
    print("%d_tel"%tree)
    print(tree_avg_tel)
    print(tel_tree_num)

for i in alpha_avg:
    print(i)

