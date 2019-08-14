#! coding: utf8
"""此模块包含检查项基类的实现。

BaseCheckItem   检查项的基类。所有具体的检查项都继承于这个基类。 检查项子类主要实现check_status方法
                并返回ResultInfo类列表。

"""
import os
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
                # print("start mark found! {}".format(line))
                flag = True
                continue
            if line.startswith(end_mark) and flag:
                # print("end mark found! {}".format(line))
                break
            if flag:
                buf.append(line)
    return buf


def exec_checkitem(item, logfile):
    hostname = os.path.basename(logfile).split('.')[0]
    item.init_parser()
    blk = item.extract_log(logfile)
    result = item.check_status(blk)

    if not result.hostname:
        result.hostname = hostname

    return result


class BaseCheckItem(object):
    """Base Class for StatusChecker
    all the status checker should be the subClass of this.
    """
    check_cmd = ''
    base_path = ''
    fsm_template_name = ''

    log_delimit_mark = "==={}"

    def __init__(self):
        self.status_data = None
        self.parser = None
        self.logfile = None
        self.start_mark = None
        self.end_mark = None
        self.logblock = None

        self.results = None

        self.info = {}
        self.init_info()

    def init_info(self):
        doclines = self.__doc__.split("\n")
        self.info['name'] = doclines[0]
        self.info['description'] = "".join(doclines[1:])

    def extract_log(self, logfile):
        buf = []
        start_mark = self.log_delimit_mark.format(self.check_cmd)
        end_mark = "COMMAND EXECUTED"
        self.logblock = extract_textblock(logfile, start_mark, end_mark)

        return self.logblock

    def init_parser(self, fsm_file=None, template_dir=None):
        if not fsm_file:
            fsm_file = self.fsm_template_name

        if not template_dir:
            template_dir = self.base_path
        self.fsm_file = os.path.join(template_dir, 'fsm_templates', fsm_file)
        # print('fsm_file:%s' % self.fsm_file)
        self.fsm_parser = FsmParser(self.fsm_file)

    def check_status(self):
        raise NotImplementError

    def __repr__(self):
        return self.__class__.__name__


class BasePresentation(object):
    """Base Class for Presentation
    all the presentation should be the subClass of this.
    """

    def __init__(self):
        self.abnormal_count = 0
        self.data=[]
        self.row_presentation = []
        # self.init_info()
        self.info = {}

    # def init_info(self):
    #     doclines = self.__doc__.split()
    #     self.info['name'] = doclines[0]
    #     self.info['description'] = "".join(doclines[1:])

    def __repr__(self):
        return self.__class__.__name__
