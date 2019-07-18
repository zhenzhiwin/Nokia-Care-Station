#! coding: utf8
"""此模块包含检查项基类的实现。

BaseCheckItem   检查项的基类。所有具体的检查项都继承于这个基类。 检查项子类主要实现check_status方法
                并返回ResultInfo类列表。
ResultInfo      保存检查结果和相关信息的类，用于传递信息给其他模块。比如reportor模块

"""
import os
import json
import time
import logging
from libs.basechecker.logparser import FsmParser


def extract_textblock(logfile, start_mark, end_mark=None):
    """extract the text block from the logfile.
    params:
      logfile,      full path name of the logfile.
      start_mark,   the start mark indicate the start of the block.
      end_mark,     the end mark indicate the end of the block. if it's None.
                    means same as start_mark.
    """
    if not end_mark:
        end_mark = start_mark
        
    buf = []
    with open(logfile) as fp:
        flag = False
        for line in fp.readlines():
            if line.startswith(start_mark):
                #print("start mark found! {}".format(line))
                flag = True
                continue
            if line.startswith(end_mark) and flag:
                #print("end mark found! {}".format(line))
                break
            if flag:
                buf.append(line)
    return buf    

def exec_task():
    results = []
    task.datetime = time.ctime()
    logfile = task.logfile
    for itemclass in task.checkitems:
        item = itemclass()
        #print(item, logfile)
        results.append(exec_checkitem(item, logfile))

    task.results = results
    
    return task

def exec_checkitem(item, logfile):
    hostname = os.path.basename(logfile).split('.')[0]
    item.init_parser()
    blk = item.extract_log(logfile)
    result = item.check_status(blk)

    if not result.hostname:
        result.hostname = hostname

    return result

class ResultInfo(object):
    """Class for storing the info of check result.
    
  参数说明：
    hostname:       网元名称
    name:           检查结果名称。如：MME单元状态检查
    status:         检查结果的状态。有三个状态：UNKNOWN，PASSED，FAILED
    description:    检查结果的详细描述。如：检查mme所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元的数量
    info:           有关检查结果的附加说明。
    error:          如果检查出错，相关的错误信息将存放在此

    """
    def __init__(self, **kwargs):
        self.hostname = kwargs.get('hostname','')
        self.name = kwargs.get('name','')     
        self.description = kwargs.get('description','')        
        self.status = 'UNKNOWN'                     
                       
        self.info = ''                              
        self.error = ''                             
        
    def to_json(self, indent=None):
        """translate the result data to json format.
        """
        return json.dumps(self.__dict__, indent=indent)

    def __repr__(self):
        return "ResultInfo({hostname},{name})".format(**self.__dict__)
        
class BaseCheckItem(object):
    """Base Class for StatusChecker
    all the status checker should be the subClass of this.
    """
    check_cmd = ''
    base_path = ''
    fsm_template_name = "flexins_doi.fsm"
    
    log_delimit_mark = "==={}"
    
    def __init__(self):
        self.status_data = None
        self.parser = None
        self.logfile = None
        self.start_mark = None
        self.end_mark = None
        self.logblock =None
        
        self.results = None

        self.info = {}
        self.init_info()

    def init_info(self):
        doclines = self.__doc__.split()
        self.info['name'] = doclines[0]
        self.info['description'] = "".join(doclines[1:])

    def extract_log(self, logfile):
        buf = []
        start_mark=self.log_delimit_mark.format(self.check_cmd)
        end_mark = "COMMAND EXECUTED"
        self.logblock = extract_textblock(logfile, start_mark, end_mark)
                
        return self.logblock
    
    def init_parser(self, fsm_file=None, template_dir=None):
        if not fsm_file:
            fsm_file = self.fsm_template_name
        
        if not template_dir:
            template_dir = self.base_path
        
        self.fsm_file = os.path.join(template_dir,'fsm_templates',fsm_file)
        #print('fsm_file:%s' % self.fsm_file)
        self.fsm_parser = FsmParser(self.fsm_file)
        
    def __repr__(self):
        return self.__class__.__name__
