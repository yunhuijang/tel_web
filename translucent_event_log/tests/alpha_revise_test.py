
import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from translucent_event_log.algo.discover_petrinet import alpha_revise
from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
from translucent_event_log.objects.tel.importer.xes import iterparse_tel
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.evaluation import factory as eval_factory
from pm4py.visualization.petrinet import factory as vis_factory

os.chdir('C:\\Users\\yunhui\\PycharmProjects\\tel_web\\input_data')

input_file_path_list = os.listdir(os.getcwd())
for input_file_path in input_file_path_list:
    log = xes_importer.apply(input_file_path)
    tel = iterparse_tel.import_tel(input_file_path)
    xes_utils.set_enabled(tel)
    n, im, fm = alpha_miner.apply(log)
    net, initial_marking, final_marking = alpha_revise.trans_alpha(tel)
    print("log")
    print(eval_factory.apply(log, n, im, fm))
    print("tel")
    print(eval_factory.apply(tel, net, initial_marking, final_marking))
    print(" ")










