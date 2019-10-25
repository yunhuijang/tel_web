from tests.translucent_event_log_new.objects.tel.tel import Event
from pm4py.algo.discovery.heuristics import factory as heuristics_miner
from tests.translucent_event_log_new.objects.tel.importer.xes import utils
from pm4py.objects.petri import semantics
from pm4py.visualization.heuristics_net import factory as hn_vis_factory

def and_set(log, window = 1):

    and_dict = {}

    for trace in log:
        for i in range(len(trace)):
            if trace[i]['concept:name'] not in and_dict.keys():
                and_dict[trace[i]['concept:name']] = set()
            for j in range(1, window+1):
                if i+j > len(trace) - 1:
                    and_dict[trace[i]['concept:name']].add(trace[i-j]['concept:name'])
                elif i-j < 0:
                    and_dict[trace[i]['concept:name']].add(trace[i+j]['concept:name'])
                else:
                    and_dict[trace[i]['concept:name']].add(trace[i - j]['concept:name'])
                    and_dict[trace[i]['concept:name']].add(trace[i + j]['concept:name'])

    return and_dict

def find_input(log, timewindow = 4, parameters = None):
    '''
    Finds input binding and output binding for each activity

    :param log: input log
    :param timewindow: size for binding (default = 4)
    :param parameters: parameter for heuristic miner (same with heuristic miner's parameters)

    :return: input_dict, (dictionary for input binding for each activity)
    '''
    heu_net = heuristics_miner.apply_heu(log, parameters)

    input_cand = {}

    for act, values in heu_net.nodes.items():
        input_cand[act] = set()
        for t in values.input_connections:
            input_cand[act].add(t.node_name)

    input_dict = {}

    for act in heu_net.nodes:
        input_dict[act] = set()

    for act in input_cand:
        input = set()
        for trace in log:
            for event_index, event in enumerate(trace):
                if event["concept:name"] == act:
                    index = event_index
                    for ev in trace[max(index - timewindow, 0):index]:
                        if ev["concept:name"] in input_cand[act]:
                            input.add(ev["concept:name"])
                    if len(input) > 0:
                        input_dict[act].add(frozenset(input))
                    input = set()

    for key, value in input_dict.items():
        if key in heu_net.start_activities[0].keys():
            value.add(frozenset())

    return input_dict


def set_enabled(tel, and_window = 1):
    '''
    Sets enabled for each event in heuristic manner

    :param tel: input log

    '''


    in_ = utils.find_input(tel)
    and_dict = and_set(tel, and_window) #and: can happen together (not concurrent)

    start_act = set()
    for trace in tel:
        start_act.add(trace[0]['concept:name']) #make start activity list

    # pair = set()
    # for act in in_:
    #     for actt in in_:
    #         if in_[act] == in_[actt] and act != actt:
    #             pair.add((act, actt)) #find activity pair that have same input condition

    for trace in tel:
        case_id = trace.attributes['concept:name']
        en = []
        left = []
        input = []
        output = []
        en.append(frozenset(start_act)) #first' activity's enabled: start_act list

        for event_index, event in enumerate(trace):
            event['enabled'] = en[event_index]
            ss = set()
            act = event['concept:name']

            if event_index > 0:
                try:
                    for k in sorted(in_[act]):
                        if len(k) > 0 and k.issubset(input[event_index-1]): # current activity's input condition is subset of last input
                            input[event_index-1] = input[event_index-1] - k
                            break
                except KeyError:
                    pass

            and_ = and_dict[act]
            ss.add(act)
            if event_index == 0: #for first activity
                input.append(ss)
            else:
                input.append(ss.union(input[event_index - 1])) #input
            # left_set = set()
            # if event_index >=1:
            #     if output_ex[case_id][event_index-1].issubset(en[event_index]):
            #         left_set = output_ex[case_id][event_index-1]

            left_set = en[event_index]

            remove_set = set()
            for s in left_set:
                if s not in and_: #concurrent activity (cannot happen together)
                    remove_set.add(s)

            # parallel = set()
            # for pa in pair:
            #     if act == pa[0]:
            #         parallel.add(pa[1]) #if it has same input condition with other activity, they are removed together from enabled list

            left.append(left_set - ss - remove_set)
            o = set()
            for e in in_:
                for k in in_[e]:
                    if k.issubset(input[event_index]) and len(k) > 0:
                        ee = set()
                        ee.add(e)
                        o = o.union(ee)

            output.append(o) #activity generated by current event

            en.append(frozenset(output[event_index] | left[event_index])) #enabled = output union left

def log_to_tel(net, initial_marking, final_marking, tel):
    '''
    set enabled into the log based on replaying on net

    Parameters
    ----------
    :param net: petri net
    :param log: tel object

    Returns
    --------
    translucent event log
    '''

    for trace in tel:
        m = initial_marking
        for event in trace:
            act = event['concept:name']

            for trans in net.transitions:
                if act == trans.label:
                    t = trans
                    break

            en = semantics.enabled_transitions(net, m)
            event.set_enabled(frozenset(en))
            if m == final_marking:
                break
            m = semantics.execute(t, net, m)  # find enabled activity

    return tel