from translucent_event_log.objects.tel.importer.xes import utils as xes_utils
from translucent_event_log.objects.tel.importer.xes import iterparse_tel
from translucent_event_log.objects.tel.utils import tel_set_enabled


def xes_import(input_file_path):
    #make xes file into tel object
    tel = iterparse_tel.import_tel(input_file_path)
    xes_utils.set_enabled(tel)
    return tel


def tel_import(input_file_path):
    #make xes++ file into tel object
    log = iterparse_tel.import_tel(input_file_path)
    tel = tel_set_enabled(log)
    return tel