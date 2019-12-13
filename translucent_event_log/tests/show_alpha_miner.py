from translucent_event_log.objects.tel.importer.xes.iterparse_tel import import_tel
import os
from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
import csv
from translucent_event_log.algo.discover_automaton import utils
from pm4py.objects.log.importer.xes import factory as xes_importer
from translucent_event_log.algo.discover_petrinet import state_based_region as sb
from pm4py.objects.petri import check_soundness

os.chdir('C:\\Users\\yunhui\\PycharmProjects\\tel_web')

input_file_path = os.path.join("input_data","reviewing_with_fewer_errors_and_more_data-complete.xes")

tel = import_tel(input_file_path)
log = xes_importer.apply(input_file_path)
xes_utils.set_enabled(tel)

auto_log = utils.discover_annotated_automaton(log)
auto_tel = utils.discover_annotated_automaton(tel)
net_log, im_log, fm_log = sb.petri_net_synthesis(auto_log)
net_tel, im_tel, fm_tel = sb.petri_net_synthesis(auto_tel)
print(check_soundness.check_petri_wfnet_and_soundness(net_log))
print(check_soundness.check_petri_wfnet_and_soundness(net_tel))

