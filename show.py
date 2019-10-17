import os
from tests.translucent_event_log_new.algo.discover_automaton import utils
from pm4py.algo.discovery.alpha import factory as alpha_miner
from tests.translucent_event_log_new.objects.tel.tel import Event as tel_event
from tests.translucent_event_log_new.algo.discover_petrinet import state_based_region as sb
from pm4py.visualization.transition_system import factory as vis_factory
from pm4py.visualization.petrinet import factory as petri_vis_factory
from pm4py.evaluation import factory as evaluation_factory
from pm4py.statistics.traces.log import case_statistics
from pm4py.algo.discovery.transition_system.parameters import *
from tests.translucent_event_log_new.algo.discover_petrinet import inductive_revise
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory


def evaluation(net, im, fm, log):
    '''
    calculate fitness, precision, simplicity, generalization for petri net
    :param net:
    :param im:
    :param fm:
    :param log:
    :return:
    '''
    result = evaluation_factory.apply(log, net, im, fm)
    #to calculate alignment based fitness
    # fitness = replay_factory.apply(log, net, im, fm, variant="alignments")
    # result['fitness'] = fitness

    return result


def stat(log):
    '''
    Shows statistical information of log
    :param log: input log
    :return: stat_dict(# of events, # of variants, # of cases)
    '''
    a = case_statistics.get_variant_statistics(log)
    num_event = 0
    for trace in log:
        num_event += len(trace)

    stat_dict = {}
    stat_dict['events'] = num_event
    stat_dict['variants'] = len(a)
    stat_dict['cases'] = len(log)

    return stat_dict


def show(model, tel, file_name, parameters):
    '''
    Show model and its quality measures
    :param model: model type (transition system, state based region, inductive miner, alpha miner)
    :param tel: input log
    :param file_name: img file name to show model
    :param parameters: parmater for transition system (afreq, sfreq)
    :return:
    '''

    tel_flag = False
    if isinstance(tel[0][0], tel_event):
        tel_flag = True



    if model in ['ts', 'sbr']:
        if tel_flag:
            output_file_path = os.path.join("static", "images", file_name[:file_name.find('.')] + '_' + model + '_' +
                                         str(parameters['afreq_thresh']) + '_' + str(parameters['sfreq_thresh'])+".png")
        else:
            output_file_path = os.path.join("static", "images", "2" + "_" +  file_name[:file_name.find('.')] + '_' + model + '_' +
                                         str(parameters[PARAM_KEY_DIRECTION]) + '_' + str(parameters[PARAM_KEY_WINDOW])+ "_" + str(parameters[PARAM_KEY_VIEW]) + ".png")

        auto = utils.discover_annotated_automaton(tel, parameters=parameters)

        max_thresh = {}
        max_afreq = 0
        max_sfreq = 0

        if tel_flag:
            for trans in auto.transitions:
                max_afreq = max(max_afreq, trans.afreq)
            for state in auto.states:
                max_sfreq = max(max_sfreq, state.sfreq)
        max_thresh['afreq'] = max_afreq
        max_thresh['sfreq'] = max_sfreq

        if model == 'ts':
            result = {}
            gviz = vis_factory.apply(auto)
            vis_factory.save(gviz, output_file_path)
            result['num of transitions'] = len(auto.transitions)
            result['num of states'] = len(auto.states)

        else:
            net, im, fm = sb.petri_net_synthesis(auto)
            gviz = petri_vis_factory.apply(net, im, fm)
            petri_vis_factory.save(gviz, output_file_path)
            result = evaluation(net, im, fm, tel)

    else:
        if tel_flag:
            output_file_path = os.path.join("static", "images", file_name[:file_name.find('.')] + '_' + model + '_' + ".png")
        else:
            output_file_path = os.path.join("static", "images", "2"+
                                            file_name[:file_name.find('.')] + '_' + model + '_' + ".png")

        if model == 'alpha':
            net, im, fm = alpha_miner.apply(tel)
            gviz = petri_vis_factory.apply(net, im, fm)
            petri_vis_factory.save(gviz, output_file_path)
            result = evaluation(net, im, fm, tel)

        else:
            dfg = dfg_factory.apply(tel)
            if tel_flag:
                dfg_tel = inductive_revise.get_dfg_graph_trans(tel)
                dfg = dfg_tel + dfg

            gviz = dfg_vis_factory.apply(dfg, log=tel)
            dfg_vis_factory.save(gviz, output_file_path)
            result = None

        #chaged
        # input_file_path = os.path.join("input_data", "running_alpha_1000_tel.xes")
        # logg = xes_importer.apply(input_file_path)
        # result = evaluation(net, im, fm, logg)
        #changed

        max_thresh = None

    return output_file_path, result, max_thresh


def show_model(model, tel, file_name, parameters):
    '''
    Show one model (show model)
    :param model:
    :param tel:
    :param file_name:
    :return:
    '''

    statis = stat(tel)

    output_file_path, result, max_thresh = show(model, tel, file_name, parameters)

    return output_file_path, result, max_thresh, statis


def compare_model(model, file_name, tel, log, parameters, parameters_2):
    '''
    Show two models (compare model)
    :param model:
    :param file_name:
    :param tel:
    :param log:
    :param parameters:
    :return:
    '''
    statis = stat(tel)
    output_file_path, result, max_thresh = show(model, tel, file_name, parameters)
    output_file_path_2, result_2, _ = show(model, log, file_name, parameters_2)

    return output_file_path, output_file_path_2, result, result_2, max_thresh, statis