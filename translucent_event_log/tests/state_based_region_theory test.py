
from translucent_event_log.objects.tel.importer.xes.iterparse_tel import import_tel
import os
from translucent_event_log.objects.tel.importer.xes.utils import log_to_tel
from translucent_event_log.objects.tel.utils import tel_set_enabled
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as vis_factory
from pm4py.visualization.transition_system import factory as trans_vis_factory
from pm4py.algo.discovery.transition_system import factory as trans_factory
from translucent_event_log.objects.tel import utils
from translucent_event_log.algo.discover_petrinet import state_based_region as sb

input_file_path = os.path.join("input_data","test_logs","running_10_tel.xes")
log = import_tel(input_file_path)
tel = tel_set_enabled(log)


auto = utils.discover_annotated_automaton(tel)
gviz = trans_vis_factory.apply(auto)
trans_vis_factory.view(gviz) #show automaton

auto_2 = trans_factory.apply(log)

nett, im, fm = sb.petri_net_synthesis(auto)
net, i, f = sb.petri_net_synthesis(auto_2)
#
gviz = vis_factory.apply(nett, im, fm)
vis_factory.view(gviz)

# gviz = vis_factory.apply(net, i, f)
# vis_factory.view(gviz)