
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
test_log = xes_importer.apply(input_file_path)

for j in [3,5,10]:
    for i in range(10):
        sample_log = sampling.sample(test_log, n=j)
        path = os.path.join("input_data", "test_logs", "Sepsis_%d_tel_%d" %(j, i))
        xes_exporter.apply(sample_log, path)

for j in [3,5,10]:
    print(j)
    for i in range(10):
        file = os.path.join("input_data", "test_logs", "Sepsis_%d_tel_%d" %(j, i))
        log = xes_importer.apply(file)
        tel = iterparse_tel.import_tel(file)
        tel = tel_set_enabled(tel)
        net, im, fm = inductive_miner.apply(log)
        nett, imm, fmm = inductive_miner.apply(tel)
        result_log = evaluation_factory.apply(test_log, net, im, fm)
        result_tel = evaluation_factory.apply(test_log, nett, imm, fmm)
        print(result_log)
        print(result_tel)
        print(" ")
