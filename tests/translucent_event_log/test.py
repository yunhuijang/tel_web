from tests.translucent_event_log.algo.discovery.state_based_region_theory import state_based_region_theory as state_region
from tests.translucent_event_log.objects.tel.importer.xes.iterparse_tel import import_tel
import os
from tests.translucent_event_log.objects.tel.importer.xes.utils import log_to_tel
from pm4py.algo.discovery.alpha import factory as alpha_miner
from tests.translucent_event_log.objects.tel import utils
from pm4py.visualization.transition_system import factory as vis_factory
from itertools import combinations

input_file_path = os.path.join("input_data", "running-example.xes")
log = import_tel(input_file_path)
nett, initial_marking, final_marking = alpha_miner.apply(log)

tel = log_to_tel(nett, initial_marking, final_marking, log)
auto = utils.discover_annotated_automaton(tel)

gviz = vis_factory.apply(auto)
vis_factory.view(gviz)









