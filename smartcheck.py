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
import pickle

from smartcheck.task import TaskControler, CheckTask
from smartcheck.utils import get_logfile, get_checkitems, read_task_conf, EZLogger
from mme.status import checkers

logger = EZLogger(level='DEBUG', logname="smartcheck")

TASK_LIST_DATAFILE = ["tasklist.data"]


def _print_check_status(task):
    print(f"Executing:{task}")
    print(f"Results: {task.results}")


def run_parser(task_list):
    logger.info("Start parsing the log...")
    for task in task_list:
        task.parse_log()
        _print_check_status(task)

    with open(TASK_LIST_DATAFILE[0], 'wb+') as fp:
        fp.write(pickle.dumps(task_list))

    return task_list


def run_collector(task_list):
    logger.info("Start collecting log from NE...")
    for task in task_list:
        task.collect_log()

    return task_list


def run_reporter(tasklist=None):
    """run reportor to output the report and data.
    """
    logger.info("Start generating report")

    try:
        with open(TASK_LIST_DATAFILE[0], 'rb') as fp:
            tasklist = pickle.load(fp)
    except FileNotFoundError as err:
        logger.error(err)
        return

    for task in tasklist:
        content = task.report()
        print("".join(content))


def init_task_list(confile):
    conf = read_task_conf(confile)
    conf.filename = confile
    # !!! 下面语句从checkers读入相关的检查项，不妥。需要优化，根据配置文件导入
    checkitems = get_checkitems(checkers, conf.checkitem_namelist)
    TASK_LIST_DATAFILE[0] = confile.replace("conf", "data")

    task_list = []
    ## 初始化每个网元的检查任务TaskControler
    for host in conf.ne_list:
        task = CheckTask(name=conf.task_name, hostname=host, ne_type=conf.ne_type)
        # 指定对应的log文件
        task.logfile = get_logfile(host, conf.logfile_path)
        task.checkitem_list = checkitems
        task_list.append(task)

    return task_list


def check_wrong_cmd(cmdlist, available_cmds):
    for cmd in cmdlist:
        if cmd not in available_cmds:
            raise ValueError("Wrong Command: '%s'" % cmd)
    return None


def controler(task_list, command_list):
    """根据命令行参数，执行相应的操作
    """
    opt_list = {"collect": run_collector,
                "parse": run_parser,
                "report": run_reporter,
                "all": None,
                }

    try:
        check_wrong_cmd(command_list, opt_list.keys())
    except ValueError as err:
        logger.error("%s, available: 'collect, parse, report'" % err)
        exit(1)

    if command_list[0] == "all":
        command_list = ['collect', 'parse', 'report']

    for cmd in command_list:
        opt_list[cmd](task_list)

    return


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(__doc__)
        exit(1)

    confile, commandstr = sys.argv[1:]
    task_list = init_task_list(confile)

    command_list = commandstr.split(',')

    controler(task_list, command_list)
