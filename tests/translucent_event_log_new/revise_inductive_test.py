
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.importer.xes import factory as xes_importer
import os
from tests.translucent_event_log_new.objects.tel.utils import tel_set_enabled
from tests.translucent_event_log_new.objects.tel.importer.xes import iterparse_tel
from tests.translucent_event_log_new.objects.tel.utils import tel_set_enabled
from pm4py.objects.log.util import sampling
from pm4py.evaluation import factory as evaluation_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter

#make sample df_complete_logs
input_file_path = os.path.join("input_data", "test_logs", "Sepsis_tel.xes")
log = xes_importer.apply(input_file_path)
net, im, fm = inductive_miner.apply(log)
result = evaluation_factory.apply(log, net, im, fm)
print(result)