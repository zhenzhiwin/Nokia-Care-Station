#! coding: utf-8
"""smartchecks是执行检查的主控制脚本。它的主要功能是完成以下各项操作或依次执行
所有操作：
1. 读入检查任务的相关信息
2. 生成并初始化检查任务
3. 调用collector登录到网元并收集数据
4. 调用parser对采集到的数据（log文件）进行检查及分析，并将检查结果保存到。
5. 调用reporter将检查结果按照模板生成对应的报告。

CLI Usage:

   smartcheck <check_task_config> <collect|parse|report>

"""
import sys
import pickle

from libs.task import TaskControler, CheckTask
from libs.collector import Collector
from libs.utils import get_logfile, get_checkitems, read_task_conf, EZLogger
from mme.status import checkers

logger = EZLogger(level='INFO')

TASK_LIST_DATAFILE = ["tasklist.data"]

def _print_check_status(task):
    print(f"Executing:{task}")
    print(f"Results: {task.results}")

def run_parser(taskconf):
    logger.info("Start parsing the log...")

    for task in taskconf.task_list:
        task.parse_log()
        _print_check_status(task)

    _parser = taskconf.ParserConfig
    with open(_parser.task_list_datafile, 'wb+') as fp:
        fp.write(pickle.dumps(taskconf.task_list))

    logger.debug("save the ResultInfo to '%s'" % _parser.task_list_datafile)

    return taskconf.task_list

def run_collector(taskconf):
    logger.info("Start collecting log from NE...")
    for task in taskconf.task_list:      
        task.collect_log()

    return conf.task_list

def run_reporter(taskconf):
    """run reportor to output the report and data.
    """
    logger.info("Start generating report")

    _parser = taskconf.ParserConfig
    try:
        with open(_parser.task_list_datafile, 'rb') as fp:
            tasklist = pickle.load(fp)
    except FileNotFoundError as err:
        logger.error(err)
        return

    for task in tasklist:
        task.make_report(taskconf.ReporterConfig)
        
def init_task_list(confile):
    """
    """
    conf = read_task_conf(confile)
    conf.filename = confile
    #!!! 下面语句从checkers读入相关的检查项，不妥。需要优化，根据配置文件导入

    parser = conf.ParserConfig
    checkitems = get_checkitems(checkers, parser.checkitem_namelist)
    
    if not hasattr(parser, 'task_list_datafile'):
        parser.task_list_datafile = confile.replace("conf","data")


    task_list = []
    ## 初始化每个网元的检查任务TaskControler
    for host in conf.NeInfo.ne_list:
        task = CheckTask(name=conf.task_name, hostname=host, ne_type=conf.NeInfo.ne_type)
        # 指定对应的log文件
        task.logfile = get_logfile(host, conf.CollectorConfig.logfile_path)
        task.checkitem_list = checkitems
        task_list.append(task)    

    conf.set('task_list', task_list)

    return conf

def check_wrong_cmd(cmdlist, available_cmds):
    for cmd in cmdlist:
        if cmd not in available_cmds:
            raise ValueError("Wrong Command: '%s'" % cmd)
    return None

def controler(taskconf, command_list):
    """根据命令行参数，执行相应的操作
    """
    opt_list = { "collect" : run_collector,
                 "parse"   : run_parser,
                 "report"  : run_reporter,
                 "all"     : None,
                }

    try:
        check_wrong_cmd(command_list, opt_list.keys())
    except ValueError as err:
        logger.error("%s, available: 'collect, parse, report'" % err)
        exit(1)

    if command_list[0] == "all":
        command_list = ['collect','parse','report']

    for cmd in command_list:
        opt_list[cmd](taskconf)
    
    return 

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(__doc__)
        exit(1)

    confile, commandstr = sys.argv[1:]
    conf = init_task_list(confile)

    if hasattr(conf, 'log_level'):
        logger.set_level(conf.log_level)

    command_list = commandstr.split(',')

    controler(conf, command_list)

