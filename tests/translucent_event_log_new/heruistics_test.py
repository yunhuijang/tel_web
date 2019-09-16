
import os
from pm4py.objects.log.importer.xes import factory as xes_importer
from tests.translucent_event_log_new.objects.tel.importer.xes import utils as xes_utils
from tests.translucent_event_log_new.objects.tel.importer.xes import iterparse_tel
from pm4py.objects.log.exporter.xes import factory as xes_exporter

input_file_path = os.path.join("input_data", "test_logs" , "running_100_remove_10.xes")
log = xes_importer.apply(input_file_path)
tel = iterparse_tel.import_tel(input_file_path)
xes_utils.set_enabled(tel)

output_path = os.path.join("input_data", "test_logs", "running_100_remove_10_tel.xes")
xes_exporter.export_log(tel, output_path)









