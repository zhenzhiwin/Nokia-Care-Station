from django.shortcuts import render
from mme.status.views import FNS_unit_presentation, FNS_alarm_presentation, presentation
from smartcheck.utils import read_task_conf

task_conf = read_task_conf('mme_task.conf')

def index(request):
    f_u_p = FNS_unit_presentation()
    f_a_p = FNS_alarm_presentation()
    f_a_h = FNS_alarm_presentation()

    presentation(f_u_p, f_a_p, f_a_h, conf=task_conf)

    return render(request, 'index.html',
                  {'col': f_u_p.row_presentation,
                   'abc': f_u_p.abnormal_count,
                   'al_stat': f_a_p,
                   'al_hist': f_a_h
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
