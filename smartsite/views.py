from django.shortcuts import render
from mme.status.views import FNS_unit_presentation, FNS_alarm_presentation, taskinfo_presentation, presentation, \
    history_presentation, FNS_interface_presentation
from smartcheck.utils import read_task_conf
from smtchk import controler, init_task_list

task_conf = read_task_conf('mme_task.conf')


def index(request):
    f_u_p = FNS_unit_presentation()
    f_a_p = FNS_alarm_presentation()
    f_a_h = FNS_alarm_presentation()
    taskinfo = taskinfo_presentation()
    if_p = FNS_interface_presentation()
    presentation(f_u_p, f_a_p, f_a_h, taskinfo, if_p, conf=task_conf)
    return render(request, 'index.html',
                  {'col': f_u_p.row_presentation,
                   'abc': f_u_p.abnormal_count,
                   'al_stat': f_a_p,
                   'al_hist': f_a_h,
                   'timestamp': taskinfo.timestamp,
                   'datafile_list': taskinfo.datafile_list,
                   'if_p': if_p
                   })


def unit_statics(request):
    url = str(request)[str(request).find('mme'):-2]
    return render(request, url)


def alarm_statics(request):
    url = str(request)[str(request).find('alarms'):-2]
    return render(request, url)


def alarmhist_stat(request):
    url = str(request)[str(request).find('alarmh'):-2]
    return render(request, url)


def if_stat(request):
    url = str(request)[str(request).find('if'):-2]
    return render(request, url)


def fresh_trigger(request):
    controler(init_task_list('mme_task.conf'), ['parse', 'report'])
    f_u_p = FNS_unit_presentation()
    f_a_p = FNS_alarm_presentation()
    f_a_h = FNS_alarm_presentation()
    taskinfo = taskinfo_presentation()
    if_p = FNS_interface_presentation()

    presentation(f_u_p, f_a_p, f_a_h, taskinfo, if_p, conf=task_conf)
    return render(request, 'index.html',
                  {'col': f_u_p.row_presentation,
                   'abc': f_u_p.abnormal_count,
                   'al_stat': f_a_p,
                   'al_hist': f_a_h,
                   'timestamp': taskinfo.timestamp,
                   'datafile_list': taskinfo.datafile_list,
                   'if_p': if_p
                   })


def datafile_selection(request):
    f_u_p = FNS_unit_presentation()
    f_a_p = FNS_alarm_presentation()
    f_a_h = FNS_alarm_presentation()
    taskinfo = taskinfo_presentation()
    if_p = FNS_interface_presentation()
    datafile = task_conf.ParserConfig.task_list_datafile + '/data.' + str(request)[
                                                                      str(request).find('For') + 3:-7].replace('%20',
                                                                                                               ' ').strip()
    history_presentation(f_u_p, f_a_p, f_a_h, taskinfo, datafile, if_p, conf=task_conf)
    return render(request, 'index.html',
                  {'col': f_u_p.row_presentation,
                   'abc': f_u_p.abnormal_count,
                   'al_stat': f_a_p,
                   'al_hist': f_a_h,
                   'timestamp': taskinfo.timestamp,
                   'datafile_list': taskinfo.datafile_list,
                   'if_p': if_p
                   })
