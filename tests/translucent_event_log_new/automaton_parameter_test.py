from tests.translucent_event_log.objects.tel.importer.xes.iterparse_tel import import_tel
import os

from tests.translucent_event_log_new.objects.tel.utils import tel_set_enabled
from pm4py.visualization.transition_system import factory as vis_factory
from tests.translucent_event_log_new.algo.discover_automaton import utils


input_file_path = os.path.join("input_data","test_logs", "running_10000_tel.xes")
log = import_tel(input_file_path)
tel = tel_set_enabled(log)

auto = utils.discover_annotated_automaton(tel)
gviz = vis_factory.apply(auto)
vis_factory.view(gviz) #show automaton

#
# auto = utils.discover_annotated_automaton(tel, parameters={'sfreq_thresh' : 5, 'afreq_thresh' : 2})
#
# gviz = vis_factory.apply(auto)
# vis_factory.view(gviz) #show automaton
