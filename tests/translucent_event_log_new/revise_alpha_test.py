
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as vis_factory
from tests.translucent_event_log_new.algo.discover_petrinet.alpha_revise import trans_alpha
from tests.translucent_event_log_new.objects.tel.importer.xes import utils as xes_utils
from tests.translucent_event_log_new.objects.tel.importer.xes import iterparse_tel
import os

from pm4py.objects.log.importer.xes import factory as xes_importer


input_file_path = os.path.join("input_data", "event_log-1266-small-orders-complete.xes")
log = xes_importer.apply(input_file_path)
tel = iterparse_tel.import_tel(input_file_path)
xes_utils.set_enabled(tel)

net, im, fm = trans_alpha(tel)
nett, imm, fmm = alpha_miner.apply(log)

gviz = vis_factory.apply(net, im, fm)
gvizz = vis_factory.apply(nett, imm, fmm)
vis_factory.view(gviz)
vis_factory.view(gvizz)

