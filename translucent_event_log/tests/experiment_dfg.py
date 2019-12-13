from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.dfg import factory as dfg_factory
import os
from translucent_event_log.algo.discover_petrinet import inductive_revise
from pm4py.objects.log.util import sampling
from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
from pm4py.algo.filtering.log.start_activities.start_activities_filter import get_start_activities
from pm4py.algo.filtering.log.end_activities.end_activities_filter import get_end_activities

tel_dict = {}
log_dict = {}
sum_dict = {}

tel_num = 0
log_num = 0
sum_num = 0
for tree in range(2,11):
    whole_tel_num = 0
    whole_log_num = 0
    whole_sum_num = 0
    tel_tree_num = 0
    log_tree_num = 0
    sum_tree_num = 0
    print(tree)
    tree_avg_tel = 0
    tree_avg_log = 0
    tree_avg_sum = 0
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
        score_sum = 0
        su_tel = 0
        su_log = 0
        su_sum = 0
        for k in range(10):
            found_tel = False
            found_log = False
            found_sum = False
            for n in range(1,1000):
                sampled_tel = sampling.sample_log(tel, no_traces = n)
                dfg_log = dfg_factory.apply(sampled_tel)
                dfg_tel = inductive_revise.get_dfg_graph_trans(sampled_tel)
                dfg = dfg_log + dfg_tel

                flag = (start_act == set(get_start_activities(sampled_tel).keys()) and end_act == set(get_end_activities(sampled_tel).keys()))

                yes_tel = 0
                yes_norm = 0
                yes_sum = 0

                for i in dfg_100.keys():
                    if i in dfg_tel.keys():
                        yes_tel += 1
                    if i in dfg_log.keys():
                        yes_norm +=1
                    if i in dfg.keys():
                        yes_sum +=1

                if flag:
                    if num == yes_tel and not found_tel:
                        print("tel df-complete")
                        print(n)
                        score_tel += n
                        su_tel += 1
                        found_tel = True

                    if num == yes_norm and not found_log:
                        print("log df-complete")
                        print(n)
                        score_log += n
                        su_log +=1
                        found_log = True

                    if num == yes_sum and not found_sum:
                        print("sum df-complete")
                        print(n)
                        score_sum +=n
                        su_sum +=1
                        found_sum = True
                    if found_log and found_sum and found_tel:
                        break

        if su_tel > 0:
            whole_tel_num += score_tel
            score_tel = score_tel / su_tel
            tel_tree_num += su_tel
        else:
            score_tel = 0
        print("%d %d tel avg"%(tree, sam))
        print(score_tel)
        print(tel_tree_num)

        if su_log > 0:
            whole_log_num += score_log
            score_log = score_log / su_log
            log_tree_num += su_log
        else:
            score_log = 0
        print("%d %d log avg"%(tree, sam))
        print(score_log)
        print(log_tree_num)

        if su_sum > 0:
            whole_sum_num += score_sum
            score_sum = score_sum / su_sum
            sum_tree_num += su_sum
        else:
            score_sum = 0
        print("%d %d sum avg"%(tree, sam))
        print(score_sum)
        print(sum_tree_num)

    print("%d_tel"%tree)
    tree_avg_tel = whole_tel_num / tel_tree_num
    print(tree_avg_tel)
    print(tel_tree_num)
    tel_dict[tree] = {'len': 0, 'perc':0}
    tel_dict[tree]['len'] = tree_avg_tel
    tel_dict[tree]['perc'] = tel_tree_num

    print("%d_log"%tree)
    tree_avg_log = whole_log_num / log_tree_num
    print(tree_avg_log)
    print(log_tree_num)
    log_dict[tree] = {'len': 0, 'perc':0}
    log_dict[tree]['len'] = tree_avg_log
    log_dict[tree]['perc'] = log_tree_num

    print("%d_sum"%tree)
    tree_avg_sum = whole_sum_num / sum_tree_num
    print(tree_avg_sum)
    print(sum_tree_num)
    sum_dict[tree] = {'len': 0, 'perc':0}
    sum_dict[tree]['len'] = tree_avg_sum
    sum_dict[tree]['perc'] = sum_tree_num

print("tel")
print(tel_dict)
print("log")
print(log_dict)
print("sum")
print(sum_dict)