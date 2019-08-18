#! coding: utf-8
""" log example:
===ZDOI:;===
LOADING PROGRAM VERSION 3.47-0
PROCESSOR TIME USAGE

UNIT:                      OMU-0     

SUPERVISION OF CPU
TIME USAGE ALLOWED:               YES
SUPERVISION OF CPU
LOAD ALLOWED:                     YES
LOAD PERCENT:                       0
CALLS FOR CRRQ:                     0
CLOCK FREQUENCY (MHZ):           1600
PROCESSOR TIME USAGE

UNIT:                      MCHU-1    

SUPERVISION OF CPU
TIME USAGE ALLOWED:               YES
SUPERVISION OF CPU
LOAD ALLOWED:                     YES
LOAD PERCENT:                       0
CALLS FOR CRRQ:                     1
CLOCK FREQUENCY (MHZ):           1600
PROCESSOR TIME USAGE

UNIT:                      GBU-0     

SUPERVISION OF CPU
TIME USAGE ALLOWED:                NO
SUPERVISION OF CPU
LOAD ALLOWED:                     YES
LOAD PERCENT:                       0
CALLS FOR CRRQ:                     0
CLOCK FREQUENCY (MHZ):           1600
PROCESSOR TIME USAGE

UNIT:                      OMU-1     

SUPERVISION OF CPU
TIME USAGE ALLOWED:               YES
SUPERVISION OF CPU
LOAD ALLOWED:                     YES
LOAD PERCENT:                       0
CALLS FOR CRRQ:                     1
CLOCK FREQUENCY (MHZ):           1600
PROCESSOR TIME USAGE

COMMAND EXECUTED

"""
import os

from libs.basechecker.checkitem import BaseCheckItem, ResultInfo

class FlexinsCpuloadStatus(BaseCheckItem):
    """MME单元CPU负荷检查
    检查mme所有单元的CPU负荷，输出单元的负荷信息。如果有单元负荷大于25%，则输出Failed。
    data={'cpuload': {'mmdu-0': 10,'mmdu-1': 2}}
    """
    check_cmd = "ZDOI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_doi.fsm"

    def check_status(self, cmd_log):
        self.status_data = self.fsm_parser.parse(logbuf=cmd_log)
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
        
        return results