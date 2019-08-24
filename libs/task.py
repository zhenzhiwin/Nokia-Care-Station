#! coding: utf-8

import os
import json
import time
import logging

from .utils import read_task_conf, get_checkitems
from .configreader import ConfigObject
from .basechecker.resultinfo import ResultInfo
from .basechecker.checkitem import exec_checkitem
from .reporter import reporter_factory
from .collector import Collector

logger = logging.getLogger('task')

class TaskControler(object):
    """not implement
    """
    def __init__(self, confile, checker_module):
        conf = read_task_conf(confile)

        #!!! 下面语句从checkers读入相关的检查项，不妥。需要优化，根据配置文件导入
        checkitems = get_checkitems(checker_module, conf.checkitem_namelist)
        
        self.task_list = []
        ## 初始化每个网元的检查任务TaskControler
        for host in conf.ne_list:
            task = CheckTask(name="TestTask", hostname=host) 
            # 指定对应的log文件
            task.logfile = get_logfile(host, conf.logfile_path)
            task.checkitem_list = checkitems
            self.task_list.append(task)    

        return task_list

    def run(self, command):
        available_cmds = ['collect', 'parse', 'report']
        if command not in available_cmds:
            raise ValueError("unknown command: %s, available: %s" % (command, available_cmds))

        for task in self.task_list:
            task.run(command)
                  
class CheckTask(object):
    def __init__(self, ne_type=None, hostname=None, name=None, checkitems=None, logfile=None):
        self.name = name
        self.ne_type = ne_type
        self.hostname = hostname
        self.logfile = logfile
        self.task_time = None
        self.checkitem_list = []
        self.status = 'UNKNOWN'

        self.results = []

    def init(self, confile):
        """init the task with the configuration file 'confile'
        """
        conf = ConfigObject(confile)

        for key in ['task_name', 'ne_type', 'ne_list']:
            if hasattr(conf, key):
                self.__dict__[key] = conf.get(key)
                conf.remove(key)
        
        self.conf = conf    
        
        if self.conf.get('checkitem_namelist'):
            self.checkitem_list = get_checkitems(conf.checkitem_namelist)       

        return self.conf

    def collect_log(self):
        """收集网元信息及检查项命令信息，并执行收集log的动作
        """
        collector = Collector(self.ne_type, self.hostname)
        cmdlist=collector.get_cmd_list(self.checkitem_list)
        collector.run(self.hostname, cmdlist)

    def parse_log(self, checkitems=None, logfile=None):
        """execute the checkitem one by one with logfile.
        """
        if not checkitems:
            checkitems = self.checkitem_list

        if not logfile:
            logfile = self.logfile

        self.datetime = time.ctime()

        for itemclass in checkitems:
            item = itemclass()
            self.results.append(exec_checkitem(item, logfile))

        return self

    def make_report(self, conf):
        """
        """
        try:
            rpt = reporter_factory(conf)
            rpt.make(self)
        except ValueError as err:
            logger.error(err)

        return None

    def info(self):
        return self.__dict__

    def __repr__(self):
        return "CheckTask<name={name},host={hostname}>".format(**self.__dict__)

def format_result(result, detail=False):
    if not detail:
        result.__dict__.pop('data')

    return result.to_json(indent=2)


