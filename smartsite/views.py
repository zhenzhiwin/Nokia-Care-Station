from django.shortcuts import render
import mme.status.report
from mme.status.configer import mme_list


def index(request):
    unit_statics = []
    alarm_statics=[]
    col = []
    ab_count = 0
    alarm_count=0
    i = 0
    task_list = mme.status.report.report_api()
    for task in task_list:
        for r in task.results:
            if r.name== 'MME单元状态检查':
                unit_statics.append(mme_list[i])
                unit_statics.append(r.stats['WO-EX'])
                unit_statics.append(r.stats['SP-EX'])
                unit_statics.append(r.stats['Other'])
                if r.status == 'OK':
                    unit_statics.append(True)
                else:
                    unit_statics.append(False)
                ab_count = r.stats['Other'] + ab_count
                i = i + 1
            if r.name=='MME单元CPU负荷检查':
                if r.status == 'OK':
                    unit_statics[4] = unit_statics[4] and True
                else:
                    unit_statics[4] = unit_statics[4] and False
                unit_statics.append(len(r.stats))
                unit_statics[4], unit_statics[5] = unit_statics[5], unit_statics[4]
                col.append(unit_statics)
                unit_statics = []
                ab_count = ab_count + len(r.stats)
            if r.name=='MME告警检查':
                alarm_count=alarm_count+len(r.stats)

    return render(request, 'index.html', {'col': col, 'abc': ab_count,'alc':alarm_count})


# def unit_statics(request):
#     task_list = mme.status.report.report_api()
#     render(request, 'unitstat.html',{'task_list':task_list})
