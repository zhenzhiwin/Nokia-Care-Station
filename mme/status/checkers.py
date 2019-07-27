#! coding: utf8
import os
import json
import time
import logging
from mme.status.configer import mme_list
from libs.basechecker.checkitem import BaseCheckItem, ResultInfo, BasePresentation
from libs.basechecker.checkitem import exec_checkitem
from .report import report_api
from .configer import BASE_PATH, LOGFILE_PATH
from .configer import checking_rules


class FlexinsUnitStatus(BaseCheckItem):
    """MME单元状态检查
    检查MME所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元详情
    """

    check_cmd = "ZUSI"
    base_path = BASE_PATH
    fsm_template_name = "flexins_usi.fsm"

    def check_status(self, logbuf=None):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        hostname = self.status_data[0]['host']
        self.info['hostname'] = hostname
        results = ResultInfo(**self.info)
        unit_status = []
        info = []
        stats = {'WO-EX': 0, 'SP-EX': 0, 'Other': 0}
        for s in self.status_data:
            if s['unit'] and s['status'] not in ['WO-EX', 'SP-EX']:
                unit_status.append(False)
                stats['Other'] += 1
                info.append(s)
            elif s['status']:
                stats[s['status']] += 1
        # print(stats)
        results.status = all(unit_status) and "OK" or "NOK"
        results.stats = stats
        results.data = self.status_data
        results.info = info
        # print(results.info)
        return results


class FlexinsCpuloadStatus(BaseCheckItem):
    """MME单元CPU负荷检查
    检查mme所有单元的CPU负荷，输出单元的负荷信息。如果有单元负荷大于25%，则输出Failed。
    data={'cpuload': {'mmdu-0': 10,'mmdu-1': 2}}
    """
    check_cmd = "ZDOI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_doi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        hostname = self.status_data[0]['host']
        results = ResultInfo(**self.info)
        overload_units = []
        for s in self.status_data:
            if int(s['cpuload']) > checking_rules['cpuload'][0]:
                # results.status = 'NOK'
                overload_units.append(s)

        results.status = (len(overload_units) == 0) and "OK" or "NOK"
        results.stats = overload_units
        results.data = self.status_data
        # print(results.stats)
        return results


class FlexinsAlarmStatus(BaseCheckItem):
    """MME告警检查
    检查mme所有告警情况，输出单元告警信息。如果有告警级别较高的告警，则输出警示。
    """
    check_cmd = "ZAHO"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_aho.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        alarmlevel_high = []
        results = ResultInfo(**self.info)
        if self.status_data:
            #     for s in self.status_data:
            #         if int(len(s['level'])) > len(checking_rules['alarmlevel'][1]):
            #             alarmlevel_high.append(s)
            #
            #     results.status = (len(alarmlevel_high) == 0) and "alarm_ok" or "alarm_nok"
            #     results.stats = alarmlevel_high
            results.data = self.status_data
        else:
            results.data = []
        return results


class FlexinsAlarmHistory(BaseCheckItem):
    """MME历史告警
    输出mm历史告警情况，单元信息。
    """
    check_cmd = "ZAHP"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_ahp.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        return results


class CheckTask(object):
    def __init__(self, hostname=None, name=None, checkitems=None, logfile=None):
        self.name = name
        self.hostname = hostname
        self.logfile = logfile
        self.task_time = None
        self.checkitems_list = None
        self.status = 'UNKNOWN'

        self.checkitems = []
        self.results = []

    def execute(self, checkitems, logfile=None):
        if not logfile:
            logfile = "%s.stats" % self.hostname
            logfile = os.path.join(LOGFILE_PATH, logfile)

        # results = []
        self.datetime = time.ctime()

        for itemclass in checkitems:
            item = itemclass()
            self.results.append(exec_checkitem(item, logfile))

        return self

    def info(self):
        return self.__dict__


def print_task_result(result, detail=False):
    if not detail:
        result.__dict__.pop('data')

    print(result.to_json(indent=2))


def run_task(hostname=None, logfile=None):
    task = CheckTask(hostname=hostname)
    checkitems = [FlexinsUnitStatus, FlexinsCpuloadStatus, FlexinsAlarmStatus, FlexinsAlarmHistory]
    task.execute(checkitems)
    return task


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


def presentation(*args):
    i = 0
    unit_statics = []
    task_list = report_api()

    for task in task_list:
        for r in task.results:
            if r.name == 'MME单元状态检查':
                unit_statics.append(mme_list[i])
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


if __name__ == "__main__":
    from .configer import mme_list

    # print(mme_list)
    task = run_task(hostname="HZMME89BNK")
    # print("Task: {hostname}, {datetime},{status}".format(**task.info()))
    # print("Result: {}".format(task.results))
