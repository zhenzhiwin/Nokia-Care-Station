#! coding: utf-8
"""Helper function for smartcheck.
"""
import os
import logging
import pickle

from .configreader import ConfigObject


def read_task_conf(confile):
    return ConfigObject(confile)


def get_logfile(hostname, logfile_path, logfile_pattern="%s.stats"):
    return os.path.join(logfile_path, logfile_pattern % hostname)


def get_checkitems(module, checkitem_namelist):
    checkitems = []
    for name in checkitem_namelist:
        checkitem = getattr(module, name, None)
        if checkitem:
            checkitems.append(checkitem)
            # print("Checkitem: {}".format(checkitem))

    return checkitems


def get_pickle_data(datafile):
    """read and return the tasklist info saved in pickle file.
    return None if anything wrong.
    """
    try:
        with open(datafile, 'rb') as fp:
            tasklist = pickle.load(fp)
    except FileNotFoundError as err:
        # logger.error(err)
        return None

    return tasklist


class EZLogger(object):
    '''
    一个简单的日志系统， 既能把日志输出到控制台， 同时写入日志文件

    logger = EzLogger(loglevel=1, logger="fox",logfile='log.txt')

    '''

    def __init__(self, level, logname=None, logfile=None, format=None):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        self.log_format = format or '%(asctime)s[%(levelname)s][%(name)s:%(lineno)s],%(message)s'
        self.level = level or logging.DEBUG
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        # 创建一个logger
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(self.level)

        # 定义handler的输出格式
        # formatter = logging.Formatter(self.log_format)

        # 创建一个handler，用于输出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(self.log_format, datefmt=self.datefmt))
        # 给logger添加handler
        self.logger.addHandler(console)

        # 创建一个handler，用于写入日志文件
        # if logfile:
        #     set_logfile(logfile)

    def set_level(self, loglevel, handler=None):
        if not handler:
            self.logger.setLevel(loglevel)
        else:
            handler.setLevel(loglevel)

    def set_format(self, logformat, datefmt=None):
        if not datefmt:
            datefmt = self.datefmt

        console_handler = self.logger.handlers[0]
        console_handler.setFormat(logging.Formatter(logformat, datefmt=datefmt))

    def set_logfile(self, logfile):
        fh = logging.FileHandler(logfile)
        fh.setLevel(self.level)
        fh.setFormatter(self.log_format)
        self.logger.addHandler(fh)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)
