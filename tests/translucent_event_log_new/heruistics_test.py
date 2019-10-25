
import os

from pm4py.objects.log.importer.xes import factory as xes_importer
from tests.translucent_event_log_new.objects.tel.importer.xes import utils as xes_utils
from tests.translucent_event_log_new.objects.tel.importer.xes import iterparse_tel
from pm4py.objects.log.exporter.xes import factory as xes_exporter

input_file_path = os.path.join("input_data", "event_log-1266-small-orders-complete.xes")
log = xes_importer.apply(input_file_path)
tel = iterparse_tel.import_tel(input_file_path)
xes_utils.set_enabled(tel)

for trace in tel:
    for event in trace:
        print(event['concept:name'])
        print(event['enabled'])









