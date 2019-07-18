from django.shortcuts import render
import mme.status.report
from mme.status.configer import mme_list


def index(request):
    unit_statics = []
    col = []
    status=[]
    ab_count = 0
    i = 0
    task_list = mme.status.report.report_api()
    for task in task_list:
        for r in task.results:
            if type(r.stats).__name__ == 'dict':
                unit_statics.append(mme_list[i])
                unit_statics.append(r.stats['WO-EX'])
                unit_statics.append(r.stats['SP-EX'])
                unit_statics.append(r.stats['Other'])
                status.append(r.status)
                col.append(unit_statics)
                unit_statics = []
                ab_count = r.stats['Other'] + ab_count
                i=i + 1
    return render(request, 'index.html', {'col': col, 'abc': ab_count,'status':status})

def cpu_statics(request):
    render(request,'mme_report_HZMME48BNK.html')
