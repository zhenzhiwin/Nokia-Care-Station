#! coding: utf8

import os

from smartcheck.basechecker.checkitem import BaseCheckItem, exec_checkitem
from smartcheck.basechecker.resultinfo import ResultInfo

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
        print(data)
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
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        alarmlevel_high = []
        results = ResultInfo(**self.info)
        if self.status_data:
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


'''自己添加'''
'''ZBIV:INT;'''


class FlexinsSgsStatus(BaseCheckItem):
    """MME SGS链路 状态信息
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


'''ZB6I::RT=SUM'''


class FlexinsS1Connect(BaseCheckItem):
    """MME S1链路 连接ENB数和断站数
    输出MME S1 连接数。
    """
    check_cmd = "ZB6I::RT=SUM"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_b6i.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []

        return results


'''ZBMI'''


class FlexinsUser4g(BaseCheckItem):
    """MME 4g user链路 状态信息
    输出MME 4g user 链路情况，链路状态。
    """
    check_cmd = "ZBMI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_bmi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        # print(results.data)
        return results


'''ZGHI'''


class Flexinsgacdr(BaseCheckItem):
    """MME 与CG国漫话单链路 状态信息
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


class Flexinssgwlink(BaseCheckItem):
    """MME 与SGW 链路 状态信息
    输出MME 与SGW 链路状态。
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


'''ZW7I'''


class Flexinsstatuscode(BaseCheckItem):
    """MME 直接查询code对应的 信息
    输出MME 直接查询code对应的 信息
    """
    check_cmd = "ZW7I:UCAP"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_w7i.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        results = ResultInfo(**self.info)
        if self.status_data:
            results.data = self.status_data
        else:
            results.data = []
        # print(results.data)
        return results
