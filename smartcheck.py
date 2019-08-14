#! coding: utf-8
"""这是一个执行smartcheck的主控制脚本。它的是：
1. 读入检查任务的相关信息
2. 生成并初始化检查任务
3. 调用collector登录到网元并收集数据（未实现）
3. 调用run_parser执行各个检查项
4. 将检查结果输出到stdin/pickle/

CLI Usage:

   smartcheck <check_task_config> <collect|parse|report>

"""
from libs.task import TaskControler, CheckTask
from libs.collector import Collector
from libs.utils import get_logfile, get_checkitems, read_task_conf, EZLogger
from mme.status import checkers

logger = EZLogger(level='DEBUG', logname="smartcheck")

def _print_check_status(task):
    print(f"Executing:{task}")
    print(f"Results: {task.results}")

def run_parser(task_list):
    logger.info("Start parsing the log...")
    for task in task_list:
        task.parse_log()
        _print_check_status(task)

    return task_list

def run_collector(task_list):
    logger.info("Start collecting log from NE...")
    for task in task_list:
        task.collect_log('collector')

    return task_list

def run_reporter(tasklist):
    """run reportor to output the report and data.
    """
    logger.info("Start generating report")
    run_parser(tasklist)
    for task in tasklist:
        content = task.report()
        print("".join(content))

def init_task_list(confile):
    conf = read_task_conf(confile)

    #!!! 下面语句从checkers读入相关的检查项，不妥。需要优化，根据配置文件导入
    checkitems = get_checkitems(checkers, conf.checkitem_namelist)
    
    task_list = []
    ## 初始化每个网元的检查任务TaskControler
    for host in conf.ne_list:
        task = CheckTask(name=conf.task_name, hostname=host) 
        # 指定对应的log文件
        task.logfile = get_logfile(host, conf.logfile_path)
        task.checkitem_list = checkitems
        task_list.append(task)    

    return task_list

def controler(task_list, command):
    """
    """
    func_list = { "collect" : run_collector,
                 "parse"   : run_parser,
                 "report"  : run_reporter,
                }

    if command in func_list:
        func_list[command](task_list)
    else:
        logger.error("Unknown command: %s, available: 'collect, parse, report'" % command)


if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(__doc__)
        exit(1)

    confile, command = sys.argv[1:]
    task_list = init_task_list(confile)
    
    controler(task_list, command)

