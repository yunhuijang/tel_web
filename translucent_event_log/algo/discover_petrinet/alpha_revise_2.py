import time
from pm4py.objects.log.util import xes as xes_util
from pm4py.algo.discovery.alpha.data_structures import alpha_classic_abstraction
from pm4py.algo.discovery.dfg.versions import native as dfg_inst
from pm4py.objects import petri
from pm4py.algo.discovery.alpha.versions import classic
from pm4py.objects.petri.petrinet import Marking
from pm4py.algo.discovery.alpha.utils import endpoints
from pm4py import util as pm_util


def trans_alpha(log, parameters=None):
    dfg = {k: v for k, v in dfg_inst.apply(log).items() if v > 0}
    if parameters is None:
        parameters = {}
    if pm_util.constants.PARAMETER_CONSTANT_ACTIVITY_KEY not in parameters:
            parameters[pm_util.constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = xes_util.DEFAULT_NAME_KEY
    start_activities = endpoints.derive_start_activities_from_log(log, parameters[
            pm_util.constants.PARAMETER_CONSTANT_ACTIVITY_KEY])
    end_activities = endpoints.derive_end_activities_from_log(log, parameters[
            pm_util.constants.PARAMETER_CONSTANT_ACTIVITY_KEY])

    labels = set()
    for el in dfg:
        labels.add(el[0])
        labels.add(el[1])
    for a in start_activities:
        labels.add(a)
    for a in end_activities:
        labels.add(a)
    labels = list(labels)

    alpha_abstraction = alpha_classic_abstraction.ClassicAlphaAbstraction(start_activities, end_activities, dfg)

    pairs = list(map(lambda p: ({p[0]}, {p[1]}),
                     filter(lambda p: classic.__initial_filter(alpha_abstraction.parallel_relation, p),
                            alpha_abstraction.causal_relation)))
    #this part added
    parallel_set = alpha_abstraction.parallel_relation
    loop_cand_set = set()
    for rel in parallel_set.copy():
        not_loop_flag = False
        pre_act = rel[0]
        post_act = rel[1]
        for trace in log:
            for i in range(len(trace)-1):
                if trace[i]['concept:name'] == pre_act and trace[i+1]['concept:name'] == post_act:
                    pre_en = trace[i]['enabled']
                    if post_act in pre_en: #not loop
                        not_loop_flag = True
                        break
                    else: #loop
                        continue
            break
        if not not_loop_flag:
            loop_cand_set.add((pre_act, post_act))
    loop_set = set()
    for loop_cand in loop_cand_set:
        if loop_cand[::-1] in loop_cand_set and loop_cand[0] != loop_cand[1]:
            loop_set.add(loop_cand)

    #find loops based on enabling information
    #this part added
    for i in range(0, len(pairs)):
        t1 = pairs[i]
        for j in range(i, len(pairs)):
            t2 = pairs[j]
            if t1 != t2:
                if t1[0].issubset(t2[0]) or t1[1].issubset(t2[1]):
                    if not (classic.__check_is_unrelated(alpha_abstraction.parallel_relation, alpha_abstraction.causal_relation,t1[0], t2[0])
                            or classic.__check_is_unrelated(alpha_abstraction.parallel_relation, alpha_abstraction.causal_relation, t1[1], t2[1])):
                        new_alpha_pair = (t1[0] | t2[0], t1[1] | t2[1])
                        if new_alpha_pair not in pairs:
                            pairs.append((t1[0] | t2[0], t1[1] | t2[1]))

    internal_places = filter(lambda p: classic.__pair_maximizer(pairs, p), pairs)
    net = petri.petrinet.PetriNet('alpha_classic_net_' + str(time.time()))
    label_transition_dict = {}

    for i in range(0, len(labels)):
        label_transition_dict[labels[i]] = petri.petrinet.PetriNet.Transition(labels[i], labels[i])
        net.transitions.add(label_transition_dict[labels[i]])

    for pair in internal_places:
        place = petri.petrinet.PetriNet.Place(str(pair))
        net.places.add(place)

        for in_arc in pair[0]:
            petri.utils.add_arc_from_to(label_transition_dict[in_arc], place, net)
        for out_arc in pair[1]:
            petri.utils.add_arc_from_to(place, label_transition_dict[out_arc], net)

    src = classic.__add_source(net, alpha_abstraction.start_activities, label_transition_dict)
    sink = classic.__add_sink(net, alpha_abstraction.end_activities, label_transition_dict)

    loop_tail_set = set()
    for t in label_transition_dict.values(): #check if two-length-loop
        if len(t.in_arcs) == 0 and len(t.out_arcs) ==0:
            loop_tail_set.add(t)

    for loop_tail in loop_tail_set:
        if loop_set is not None:
            loop_body = None
            for loop in loop_set:
                if loop[0] == loop_tail.name:
                    loop_body = label_transition_dict[loop[1]]
            if loop_body is not None:
                for place in net.places:
                    for in_arc in place.in_arcs:
                        if in_arc.source == loop_body:
                            petri.utils.add_arc_from_to(place, label_transition_dict[loop_tail.name], net)
                            break
                    for out_arc in place.out_arcs:
                        if out_arc.target == loop_body:
                            petri.utils.add_arc_from_to(label_transition_dict[loop_tail.name], place, net)

    return net, Marking({src: 1}), Marking({sink: 1})