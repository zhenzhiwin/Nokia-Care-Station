#! coding: utf-8

import os

from smartcheck.reportviews import BasePresentation
from smartcheck.utils import get_pickle_data

class FNS_unit_presentation(BasePresentation):
    """MME单元检查呈现类
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()
        # self.abnormal_count=0


class FNS_alarm_presentation(BasePresentation):
    """MME告警检查呈现类
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()
        self.notice_level = []
        self.warning_level = []
        self.critical_level = []
        self.chart_data = ''

def presentation(*args, **kwargs):
    i = 0
    unit_statics = []
    conf = kwargs.get('conf')
    task_list = get_pickle_data(conf.ParserConfig.task_list_datafile)

    for task in task_list:
        for r in task.results:
            if r.name == 'MME单元状态检查':
                unit_statics.append(conf.NeInfo.ne_list[i])
                unit_statics.append(r.stats['WO-EX'])
                unit_statics.append(r.stats['SP-EX'])
                unit_statics.append(r.stats['Other'])
                if r.status == 'OK':
                    unit_statics.append(True)
                else:
                    unit_statics.append(False)
                args[0].abnormal_count = r.stats['Other'] + args[0].abnormal_count
                i = i + 1
            if r.name == 'MME单元CPU负荷检查':
                if r.status == 'OK':
                    unit_statics[4] = unit_statics[4] and True
                else:
                    unit_statics[4] = unit_statics[4] and False
                unit_statics.append(len(r.stats))
                unit_statics[4], unit_statics[5] = unit_statics[5], unit_statics[4]
                args[0].row_presentation.append(unit_statics)
                unit_statics = []
                args[0].abnormal_count = args[0].abnormal_count + len(r.stats)
            if r.name == 'MME告警检查':
                alarm_statics = []
                alarm_statics.append(r.hostname)
                n_c = 0
                w_c = 0
                c_c = 0
                for a in r.data:
                    if a['level'] == '*':
                        args[1].notice_level.append(a)
                        n_c += 1
                    if a['level'] == '**':
                        args[1].warning_level.append(a)
                        w_c += 1
                    if a['level'] == '***':
                        args[1].critical_level.append(a)
                        c_c += 1
                alarm_statics.append(n_c)
                alarm_statics.append(w_c)
                alarm_statics.append(c_c)
                args[1].chart_data += a['host'] + str(w_c+c_c)
                args[1].row_presentation.append(alarm_statics)


            if r.name == 'MME历史告警':
                alarm_history = []
                alarm_history.append(r.hostname)
                n_c = 0
                w_c = 0
                c_c = 0
                for a in r.data:
                    if a['level'] == '*':
                        args[2].notice_level.append(a)
                        n_c += 1
                    if a['level'] == '**':
                        args[2].warning_level.append(a)
                        w_c += 1
                    if a['level'] == '***':
                        args[2].critical_level.append(a)
                        c_c += 1
                alarm_history.append(n_c)
                alarm_history.append(w_c)
                alarm_history.append(c_c)
                args[2].chart_data += a['host'] + str(w_c+c_c)
                args[2].row_presentation.append(alarm_history)
    args[1].chart_data = args[1].chart_data + '!' + args[2].chart_data
    return args


