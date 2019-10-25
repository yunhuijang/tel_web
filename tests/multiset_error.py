from pm4py.visualization.transition_system import factory as trans_factory
from pm4py.algo.discovery.transition_system import factory as trans_miner
from pm4py.objects.log.importer.xes import factory as xes_importer
import os

file_path = os.path.join("translucent_event_log_new", "input_data", "running-example.xes")

log = xes_importer.apply(file_path)
ts = trans_miner.apply(log, parameters={'view': 'multiset'})
tss = trans_miner.apply(log, parameters={'view': "set"})
gvizz = trans_factory.apply(tss)
trans_factory.view(gvizz)
gviz = trans_factory.apply(ts)
trans_factory.view(gviz)
