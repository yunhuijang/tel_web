from translucent_event_log.objects.tel.importer.xes.iterparse_tel import import_tel
import os
from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
import csv
from translucent_event_log.algo.discover_automaton import utils
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.evaluation import factory as evaluation_factory
from translucent_event_log.algo.discover_petrinet import state_based_region as sb
from pm4py.objects.petri import check_soundness
from pm4py.evaluation.replay_fitness import factory as replay_factory

os.chdir('C:\\Users\\yunhui\\PycharmProjects\\tel_web')

input_file_path_list = []
input_file_path_list.append(os.path.join("input_data", "roadtraffic100traces.xes"))
input_file_path_list.append(os.path.join("input_data", "event_log-1266-small-orders-complete.xes"))
input_file_path_list.append(os.path.join("input_data", "reviewing_with_fewer_errors_and_more_data-complete.xes"))

with open('output.csv', 'w', newline='') as f:
    wr = csv.writer(f, delimiter=',')
    wr.writerow(['option', '# of trans', '# of states', 'soundness', 'fitness', 'align_fitness', 'precision', 'simplicity', 'generalization', 'fl-score', '4-avg' ])

    for i in range(len(input_file_path_list)):
        print(" ")
        print("event log: ", i)
        tel = import_tel(input_file_path_list[i])
        log = xes_importer.apply(input_file_path_list[i])
        xes_utils.set_enabled(tel)

        log_param_list = [None, {'view': 'set'}, {'view': 'multiset'},
                          {'window' :3}, {'window': 3, 'view': 'set'}, {'window': 3, 'view': 'multiset'},
                          {'direction': 'backward'}, {'direction': 'backward', 'view': 'set'}, {'direction': 'backward', 'view': 'multiset'},
                          {'window': 3, 'direction': 'backward'}, {'window': 3, 'direction': 'backward', 'view': 'set'},
                          {'window': 3, 'direction': 'backward', 'view': 'multiset'}]
        print("log")
        for j in log_param_list:
            print(j)
            auto_log = utils.discover_annotated_automaton(log, j)
            net_log, im_log, fm_log = sb.petri_net_synthesis(auto_log)
            print("# of trans: ", len(auto_log.transitions))
            print("# of states: ", len(auto_log.states))
            ev = evaluation_factory.apply(log, net_log, im_log, fm_log)
            ev['fitness'] = ev['fitness']['averageFitness']
            print("fitness: ", round(ev['fitness']['averageFitness'], 2))
            print("precision: ", round(ev['precision'], 2))
            print("simplicity: ", round(ev['simplicity'], 2))
            print("generalization: ", round(ev['generalization'], 2))
            soundness_log = check_soundness.check_petri_wfnet_and_soundness(net_log)
            if soundness_log:
                fitness = replay_factory.apply(log, net_log, im_log, fm_log)
                ev['align_fitness'] = fitness['averageFitness']
            else:
                ev['align_fitness'] = -1
            wr.writerow([j, len(auto_log.transitions), len(auto_log.states), soundness_log, round(ev['fitness'], 2),
                         round(ev['align_fitness'], 2),
                         round(ev['precision'], 2), round(ev['simplicity'], 2), round(ev['generalization'], 2)],
                        round(ev['fscore'], 2), round(ev['metricsAverageWeight'], 2))
            print(" ")

        auto_tel = utils.discover_annotated_automaton(tel)
        max_afreq = 1
        max_sfreq = 1
        for transition in auto_tel.transitions:
            max_afreq = max(max_afreq, transition.afreq)
        for state in auto_tel.states:
            max_sfreq = max(max_sfreq, state.sfreq)

        tel_param_list = [None, {'afreq_thresh': max_afreq * 0.1}, {'afreq_thresh': max_afreq * 0.2}, {'afreq_thresh': max_afreq * 0.5},
                          {'sfreq_thresh': max_sfreq * 0.1}, {'sfreq_thresh': max_sfreq * 0.2}, {'sfreq_thresh': max_sfreq * 0.5}]
        for k in tel_param_list:
            print(k)
            auto_tell = utils.discover_annotated_automaton(tel, parameters=k)
            net_tel, im_tel, fm_tel = sb.petri_net_synthesis(auto_tell)
            print("# of trans: ", len(auto_tell.transitions))
            print("# of states: ", len(auto_tell.states))
            ev_tel = evaluation_factory.apply(tel, net_tel, im_tel, fm_tel)
            ev_tel['fitness'] = ev_tel['fitness']['averageFitness']
            print("fitness: ", round(ev_tel['fitness'], 2))
            print("precision: ", round(ev_tel['precision'], 2))
            print("simplicity: ", round(ev_tel['simplicity'], 2))
            print("generalization: ", round(ev_tel['generalization'], 2))
            soundness_tel = check_soundness.check_petri_wfnet_and_soundness(net_tel)
            if soundness_tel:
                fitness = replay_factory.apply(tel, net_tel, im_tel, fm_tel)
                ev_tel['align_fitness'] = fitness['averageFitness']
            else:
                ev_tel['align_fitness'] = -1
            wr.writerow([k, len(auto_tell.transitions), len(auto_tell.states), soundness_tel, round(ev_tel['fitness'], 2),
                        round(ev_tel['align_fitness'], 2), round(ev_tel['precision'], 2), round(ev_tel['simplicity'], 2), round(ev_tel['generalization'], 2)],
                        round(ev_tel['fscore'], 2), round(ev_tel['metricsAverageWeight'], 2))
            print(" ")
