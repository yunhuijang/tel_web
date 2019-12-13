from pm4py.algo.discovery.transition_system import factory as trans_factory
from pm4py.objects.log.importer.xes import factory as xes_importer
import os
from translucent_event_log.algo.discover_petrinet import state_based_region as sb
from pm4py.visualization.petrinet import factory as vis_factory

from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
from translucent_event_log.objects.tel.importer.xes import iterparse_tel
from translucent_event_log.objects.tel.utils import tel_set_enabled
from pm4py.objects.log.exporter.xes import factory as xes_exporter

os.chdir('C:\\Users\\yunhui\\PycharmProjects\\tel_web')

def xes_import(input_file_path):
    #make xes file into tel object
    tel = iterparse_tel.import_tel(input_file_path)
    xes_utils.set_enabled(tel)
    return tel

tel = xes_import(os.path.join("input_data", "roadtraffic100traces.xes"))
xes_exporter.apply(tel, "road100_tel.xes")