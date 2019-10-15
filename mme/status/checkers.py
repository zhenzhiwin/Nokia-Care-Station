#! coding: utf8

import os, IPy

from smartcheck.basechecker.checkitem import BaseCheckItem, exec_checkitem
from smartcheck.basechecker.resultinfo import ResultInfo
from smartcheck.utils import read_task_conf

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


class TaskInfo(BaseCheckItem):
    """TASKINFO
    there basic info of the task.
    """
    check_cmd = "TASKINFO"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "taskinfo.fsm"

    def check_status(self, logbuf=None):
        data = self.fsm_parser.parse(logbuf=logbuf)
        # print(data)
        if data:
            self.info['status'] = "PASSED"

        results = ResultInfo(**self.info)
        results.data = data

        return results


class FlexinsUnitStatus(BaseCheckItem):
    """MME单元状态检查
    检查MME所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元详情
    """

    check_cmd = "ZUSI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
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
        # print(results.stats)
        results.data = self.status_data
        results.info = info
        # print(results.data)
        return results


class FlexinsCpuloadStatus(BaseCheckItem):
    """MME单元CPU负荷检查
    检查mme所有单元的CPU负荷，输出单元的负荷信息。如果有单元负荷大于checking_rules的规定，则输出Failed。
    data={'cpuload': {'mmdu-0': 10,'mmdu-1': 2}}
    """
    check_cmd = "ZDOI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_doi.fsm"

    # 检查的规则和阀值（另外定义在单独的一个文件更合适）
    checking_rules = {
        'cpuload': [60, 80, 90],
    }

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        hostname = self.status_data[0]['host']
        results = ResultInfo(**self.info)
        overload_units = []
        for s in self.status_data:
            if int(s['cpuload']) > self.checking_rules['cpuload'][0]:
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
        conf = read_task_conf("mme_task.conf")  # 从这里读取不是很妥，还需考虑配置文件的提取
        ip_filter_list = conf.OptimizedFilter.MME_unavailable_alarm_filer_list
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        results.data = []
        if self.status_data:
            for r in self.status_data:
                if r['alarmid'] == '3450':
                    ip = '%d.%d.%d.%d' % (
                    int(r['hexinfo'][3:5], 16), int(r['hexinfo'][6:8], 16), int(r['hexinfo'][9:11], 16),
                    int(r['hexinfo'][12:14], 16),)
                    for filter in ip_filter_list:
                        if ip in IPy.IP(filter):
                            results.data.append(r)
                elif r['alarmid'] == '3717':
                    ip=r['hexinfo'][:r['hexinfo'].find('FF')-1]
                    for filter in ip_filter_list:
                        if ip in IPy.IP(filter):
                            results.data.append(r)
                else:
                    results.data.append(r)
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
        conf = read_task_conf("mme_task.conf")  # 从这里读取不是很妥，还需考虑配置文件的提取
        ip_filter_list = conf.OptimizedFilter.MME_unavailable_alarm_filer_list
        results.data = []

        if self.status_data:
            for r in self.status_data:
                if r['alarmid'] == '3450':
                    ip = '%d.%d.%d.%d' % (
                    int(r['hexinfo'][3:5], 16), int(r['hexinfo'][6:8], 16), int(r['hexinfo'][9:11], 16),
                    int(r['hexinfo'][12:14], 16),)
                    for filter in ip_filter_list:
                        if ip in IPy.IP(filter):
                            results.data.append(r)
                elif r['alarmid'] == '3717':
                    ip=r['hexinfo'][:r['hexinfo'].find('FF')-1]
                    for filter in ip_filter_list:
                        if ip in IPy.IP(filter):
                            results.data.append(r)
                else:
                    results.data.append(r)
        else:
            results.data = []
        return results


'''自己添加'''
'''ZBIV:INT;'''


class FlexinsSgsStatus(BaseCheckItem):
    """MMESGS状态检查
    输出MME SGS 链路情况，链路状态。
    """
    check_cmd = "ZBIV:INT"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_biv.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []

        return results


class FlexinsSlsStatus(BaseCheckItem):
    """MMESLS状态检查
    输出MME SLS 链路情况，链路状态。
    """
    check_cmd = "ZBIS:INT"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_bis.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []

        return results


class FlexinsSvStatus(BaseCheckItem):
    """MMESV状态检查
    输出MME SV 链路情况，链路状态。
    """
    check_cmd = "ZBIR:INT"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_bir.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        return results


class FlexinsSzStatus(BaseCheckItem):
    """MMESZ状态检查
    输出MME SZ 链路情况，链路状态。
    """
    check_cmd = "ZBIU:INTBS"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_biu.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []

        return results


class FlexinsS6aStatus(BaseCheckItem):
    """MMES6A/SLG状态检查
    输出MME S6A/SLG 链路情况，链路状态。
    """
    check_cmd = "ZOHI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_ohi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []

        return results


# '''ZB6I::RT=SUM'''
#
#
# class FlexinsS1Connect(BaseCheckItem):
#     """MME S1链路 连接ENB数和断站数
#     输出MME S1 连接数。
#     """
#     check_cmd = "ZB6I::RT=SUM"
#     base_path = os.path.split(os.path.abspath(__file__))[0]
#     fsm_template_name = "flexins_b6i.fsm"
#
#     def check_status(self, logbuf):
#         self.status_data = self.fsm_parser.parse(logbuf=logbuf)
#         results = ResultInfo(**self.info)
#         if self.status_data:
#             results.data = self.status_data
#         else:
#             results.data = []
#
#         return results


# '''ZBMI'''


# class FlexinsUser4g(BaseCheckItem):
#     """MME 4g user链路 状态信息
#     输出MME 4g user 链路情况，链路状态。
#     """
#     check_cmd = "ZBMI"
#     base_path = os.path.split(os.path.abspath(__file__))[0]
#     fsm_template_name = "flexins_bmi.fsm"
#
#     def check_status(self, logbuf):
#         self.status_data = self.fsm_parser.parse(logbuf=logbuf)
#         results = ResultInfo(**self.info)
#         if self.status_data:
#             results.data = self.status_data
#         else:
#             results.data = []
#         # print(results.data)
#         return results


'''ZGHI'''


class Flexinsgacdr(BaseCheckItem):
    """MMEGA状态信息
    输出MME 与CG国漫话单 链路情况，链路状态。
    """
    check_cmd = "ZGHI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_ghi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        # print(results.data)
        return results


class FlexinsGrlink(BaseCheckItem):
    """MMEGr状态信息
    输出MMEGr链路状态。
    """
    check_cmd = "ZNLI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_nli.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        # print(results.data)
        return results


class FlexinsGrsublink(BaseCheckItem):
    """MMEGrsub状态信息
    输出MMEGr子系统链路状态。
    """
    check_cmd = "ZNHI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_nhi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        # print(results.data)
        return results
# '''ZW7I'''
#
#
# class Flexinsstatuscode(BaseCheckItem):
#     """MME 直接查询code对应的 信息
#     输出MME 直接查询code对应的 信息
#     """
#     check_cmd = "ZW7I:UCAP"
#     base_path = os.path.split(os.path.abspath(__file__))[0]
#     fsm_template_name = "flexins_w7i.fsm"
#
#     def check_status(self, logbuf):
#         self.status_data = self.fsm_parser.parse(logbuf=logbuf)
#         results = ResultInfo(**self.info)
#         if self.status_data:
#             results.data = self.status_data
#         else:
#             results.data = []
#         # print(results.data)
#         return results
