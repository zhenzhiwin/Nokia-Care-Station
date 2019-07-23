from django.shortcuts import render
from mme.status.configer import mme_list
from mme.status.checkers import FNS_unit_presentation, FNS_alarm_presentation, presentation


def index(request):
    f_u_p = FNS_unit_presentation()
    f_a_p = FNS_alarm_presentation()
    presentation(f_u_p, f_a_p)
    return render(request, 'index.html',
                  {'col': f_u_p.row_presentation,
                   'abc': f_u_p.abnormal_count,
                   'al_stat':f_a_p
                              })

# def unit_statics(request):
#     task_list = mme.status.report.report_api()
#     render(request, 'unitstat.html',{'task_list':task_list})
