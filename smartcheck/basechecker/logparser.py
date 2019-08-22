#! coding: utf8
"""此模块主要实现利用TextFSM来实现对log文件的分析并提取相关的数据。

FsmParser   TextFsm分析类

Usage:
   parser = FsmParser('path/to/fsm_template_file')
   data = parser.parse(logfile)     #从log文件里提取数据
   data = parser.parse(loglines)    #从文本列表里提取数据

   data为一个列表，每个元素为一个字典。

"""
import os
import re
import logging
from .textfsm import TextFSM

class FsmParser(object):
    """A log parser using the FSM template.
    """
    def __init__(self, fsm_file=None):
        self.fsm = None
        if fsm_file:
            self.load_template(fsm_file)
    
        
    def load_template(self, fsm_file):
        """load FSM template and generate a textfsm parser.
        """
        with open(fsm_file) as fp:
            self.fsm = TextFSM(fp)

        return self.fsm
    
    def parse(self, logfile=None, logbuf=None):
        """Return a list of dict of row.
        """
        if logfile:
            with open(logfile) as fp:
                logtext = fp.read()
        elif logbuf:
            logtext = "".join(logbuf)
            #print(logtext)
        else:
            return None
            
        self.fsm.Reset()
        rows = self.fsm.ParseText(logtext)
        return [dict(zip(self.fsm.header,row)) for row in rows]
        