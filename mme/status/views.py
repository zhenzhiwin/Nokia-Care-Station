#! coding: utf-8
from smartcheck.reportviews import BasePresentation
from smartcheck.utils import get_pickle_data


class FNS_unit_presentation(BasePresentation):
    """MME单元检查呈现类
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()
        # self.abnormal_count=0


class FNS_alarm_presentation(BasePresentation):
    """MME告警检查呈现类
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()
        # self.notice_level = []
        # self.warning_level = []
        # self.critical_level = []
        self.key_alarms = []
        self.chart_data = ''
        self.summary = []
        self.ne_list = []


class FNS_interface_presentation(BasePresentation):
    """MME 接口呈现类
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()


class taskinfo_presentation(BasePresentation):
    """TASKINO呈现类,目前暂时用于时间戳，后续可丰富本信息
    继承BasePresentation
    """

    def __init__(self):
        super().__init__()
        self.timestamp = ''
        self.datfile_list = []


def presentation(f_u_p, f_a_p, taskinfo, if_p, conf):
    i = 0
    unit_statics = []
    datafile_list = []
    with open(conf.ParserConfig.task_list_datafile + '/lastest.pointer', 'r') as datafile:
        task_list = get_pickle_data(datafile.read())
    with open(conf.ParserConfig.task_list_datafile + '/data.list', 'r') as list:
        for line in list.readlines():
            if len(line) > 1:
                datafile_list.append(line.strip())
        taskinfo.datafile_list = datafile_list
    for t in task_list[0].results:
        if t.name == 'TASKINFO':
            taskinfo.timestamp = t.data[0]['timestamp']
            break
    for task in task_list:
        if_stats = []
        gr_flag_per_mme = True
        for r in task.results:
            if r.name == 'MME单元状态检查':
                unit_statics.append(conf.NeInfo.ne_list[i])
                unit_statics.append(r.stats['WO-EX'])
                unit_statics.append(r.stats['SP-EX'])
                unit_statics.append(r.stats['Other'])
                if r.status == 'OK':
                    unit_statics.append(True)
                else:
                    unit_statics.append(False)
                f_u_p.abnormal_count = r.stats['Other'] + f_u_p.abnormal_count
                i = i + 1
            if r.name == 'MME单元CPU负荷检查':
                if r.status == 'OK':
                    unit_statics[4] = unit_statics[4] and True
                else:
                    unit_statics[4] = unit_statics[4] and False
                unit_statics.append(len(r.stats))
                unit_statics[4], unit_statics[5] = unit_statics[5], unit_statics[4]
                f_u_p.row_presentation.append(unit_statics)
                unit_statics = []
                f_u_p.abnormal_count = f_u_p.abnormal_count + len(r.stats)
            if r.name == 'MME告警检查':
                alist = []
                adict = {}
                summary = []
                # alarm_statics.append(r.hostname)
                # n_c = 0
                # w_c = 0
                key_counter = 0
                for a in r.data:
                    # if a['alarmid']:
                    info = a['alarmid'].strip() + '----' + a['alarmtext'].strip()
                    alist.append(info)
                    if a['alarmid'].strip() in conf.OptimizedFilter.MME_key_alarm_dict:
                        a['info'] = conf.OptimizedFilter.MME_key_alarm_dict[a['alarmid']]
                        f_a_p.key_alarms.append(a)
                        key_counter += 1
                    # if a['level'] == '*':
                    #     args[1].notice_level.append(a)
                    #     n_c += 1
                    # if a['level'] == '**':
                    #     args[1].warning_level.append(a)
                    #     w_c += 1
                    # if a['level'] == '***':
                    #     args[1].critical_level.append(a)
                    #     c_c += 1
                aset = set(alist)
                for info in aset:
                    adict.update({info: alist.count(info)})
                for ak, av in adict.items():
                    summary.append(ak + ',当前数量:' + str(av) + '条')

                # alarm_statics.append(n_c)
                # alarm_statics.append(w_c)
                # alarm_statics.append(c_c)
                f_a_p.chart_data += a['host'] + str(key_counter)
                # args[1].row_presentation.append(alarm_statics)
                f_a_p.summary.append({r.hostname: summary})
                f_a_p.ne_list.append(r.hostname)
            #
            # if r.name == 'MME历史告警':
            #     alarm_history = []
            #     alarm_history.append(r.hostname)
            #     n_c = 0
            #     w_c = 0
            #     c_c = 0
            #     for a in r.data:
            #         if a['level'] == '*':
            #             args[2].notice_level.append(a)
            #             n_c += 1
            #         if a['level'] == '**':
            #             args[2].warning_level.append(a)
            #             w_c += 1
            #         if a['level'] == '***':
            #             args[2].critical_level.append(a)
            #             c_c += 1
            #     alarm_history.append(n_c)
            #     alarm_history.append(w_c)
            #     alarm_history.append(c_c)
            #     args[2].chart_data += r.hostname + str(w_c + c_c)
            #     args[2].row_presentation.append(alarm_history)
            if r.name == 'MMESGS状态检查':
                status_per_mme = True
                for stats in r.data:
                    if stats['linkstatus'] != 'UP' or stats['mode'] != 'WORKING':
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMESLS状态检查':
                status_per_mme = True
                for stats in r.data:
                    if stats['STATE'] != 'UP' or stats['S_STATE'] != 'UP':
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMESZ状态检查':
                status_per_mme = True
                for stats in r.data:
                    if stats['STATUS'] != 'CONNECTED':
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMES6A/SLG状态检查':
                status_per_mme = True
                for stats in r.data:
                    if stats['CONN_STATUS'] != 'CONNECTED':
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMEGA状态信息':
                status_per_mme = True
                for stats in r.data:
                    if stats['adminstate'] != '1 UNLOCKED' or stats['operstatus'].strip() != '1 OPERATIONAL':
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMESV状态检查':
                status_per_mme = True
                for stats in r.data:
                    if stats['mode'] not in ['NORMAL', 'DEFAULT']:
                        status_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(status_per_mme)
            if r.name == 'MMEGr状态信息':
                for stats in r.data:
                    if stats['LINKSTATE'] != 'AV-EX':
                        gr_flag_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
            if r.name == 'MMEGrsub状态信息':
                for stats in r.data:
                    if stats['STATE'] != 'AV' or stats['STATE_LSTP'] != 'AV-EX':
                        gr_flag_per_mme = False
                        if_p.abnormal_count = if_p.abnormal_count + 1
                if_stats.append(gr_flag_per_mme)
        if_stats.insert(0, task.hostname)
        if_p.row_presentation.append(if_stats)
    # args[1].chart_data = args[1].chart_data + '!' + args[2].chart_data

    # conf = init_task_list('mme_task.conf')
    # controler(conf, ['parse','report'])
    # return args

# def history_presentation(*args, **kwargs):
#     i = 0
#     unit_statics = []
#     datafile_list = []
#     conf = kwargs.get('conf')
#     tasklist = get_pickle_data(args[4])
#     _parser = conf.ParserConfig
#     for task in tasklist:
#         task.make_report(conf.ReporterConfig)
#     with open(conf.ParserConfig.task_list_datafile + '/data.list', 'r') as list:
#         for line in list.readlines():
#             if len(line) > 1:
#                 datafile_list.append(line.strip())
#         args[3].datafile_list = datafile_list
#     for t in tasklist[0].results:
#         if t.name == 'TASKINFO':
#             # print(t.data[0]['timestamp'])
#             args[3].timestamp = t.data[0]['timestamp']
#             break
#     # print(task_list[0].results[7].data[0]['timestamp'])
#     for task in tasklist:
#         if_stats = []
#         gr_flag_per_mme = True
#         for r in task.results:
#             if r.name == 'MME单元状态检查':
#                 unit_statics.append(conf.NeInfo.ne_list[i])
#                 unit_statics.append(r.stats['WO-EX'])
#                 unit_statics.append(r.stats['SP-EX'])
#                 unit_statics.append(r.stats['Other'])
#                 if r.status == 'OK':
#                     unit_statics.append(True)
#                 else:
#                     unit_statics.append(False)
#                 args[0].abnormal_count = r.stats['Other'] + args[0].abnormal_count
#                 i = i + 1
#             if r.name == 'MME单元CPU负荷检查':
#                 if r.status == 'OK':
#                     unit_statics[4] = unit_statics[4] and True
#                 else:
#                     unit_statics[4] = unit_statics[4] and False
#                 unit_statics.append(len(r.stats))
#                 unit_statics[4], unit_statics[5] = unit_statics[5], unit_statics[4]
#                 args[0].row_presentation.append(unit_statics)
#                 unit_statics = []
#                 args[0].abnormal_count = args[0].abnormal_count + len(r.stats)
#             if r.name == 'MME告警检查':
#                 alarm_statics = []
#                 alist = []
#                 adict = {}
#                 summary = []
#                 alarm_statics.append(r.hostname)
#                 n_c = 0
#                 w_c = 0
#                 c_c = 0
#                 for a in r.data:
#                     if a['alarmid']:
#                         info = a['alarmid'].strip() + '----' + a['alarmtext'].strip()
#                         alist.append(info)
#                         if a['level'] == '*':
#                             args[1].notice_level.append(a)
#                             n_c += 1
#                         if a['level'] == '**':
#                             args[1].warning_level.append(a)
#                             w_c += 1
#                         if a['level'] == '***':
#                             args[1].critical_level.append(a)
#                             c_c += 1
#                 aset = set(alist)
#                 for info in aset:
#                     adict.update({info: alist.count(info)})
#                 for ak, av in adict.items():
#                     summary.append(ak + ',当前数量:' + str(av) + '条')
#                 alarm_statics.append(n_c)
#                 alarm_statics.append(w_c)
#                 alarm_statics.append(c_c)
#                 args[1].chart_data += a['host'] + str(w_c + c_c)
#                 args[1].row_presentation.append(alarm_statics)
#                 args[1].summary.append({r.hostname: summary})
#                 args[1].ne_list.append(r.hostname)
#             if r.name == 'MME历史告警':
#                 alarm_history = []
#                 alarm_history.append(r.hostname)
#                 n_c = 0
#                 w_c = 0
#                 c_c = 0
#                 for a in r.data:
#                     if a['level'] == '*':
#                         args[2].notice_level.append(a)
#                         n_c += 1
#                     if a['level'] == '**':
#                         args[2].warning_level.append(a)
#                         w_c += 1
#                     if a['level'] == '***':
#                         args[2].critical_level.append(a)
#                         c_c += 1
#                 alarm_history.append(n_c)
#                 alarm_history.append(w_c)
#                 alarm_history.append(c_c)
#                 args[2].chart_data += r.hostname + str(w_c + c_c)
#                 args[2].row_presentation.append(alarm_history)
#             if r.name == 'MMESGS状态检查':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['linkstatus'] != 'UP' or stats['mode'] != 'WORKING':
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMESLS状态检查':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['STATE'] != 'UP' or stats['S_STATE'] != 'UP':
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMESZ状态检查':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['STATUS'] != 'CONNECTED':
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMES6A/SLG状态检查':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['CONN_STATUS'] != 'CONNECTED':
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMEGA状态信息':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['adminstate'] != '1 UNLOCKED' or stats['operstatus'].strip() != '1 OPERATIONAL':
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMESV状态检查':
#                 status_per_mme = True
#                 for stats in r.data:
#                     if stats['mode'] not in ['NORMAL', 'DEFAULT']:
#                         status_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(status_per_mme)
#             if r.name == 'MMEGr状态信息':
#                 for stats in r.data:
#                     if stats['LINKSTATE'] != 'AV-EX':
#                         gr_flag_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#             if r.name == 'MMEGrsub状态信息':
#                 for stats in r.data:
#                     if stats['STATE'] != 'AV' or stats['STATE_LSTP'] != 'AV-EX':
#                         gr_flag_per_mme = False
#                         args[5].abnormal_count = args[5].abnormal_count + 1
#                 if_stats.append(gr_flag_per_mme)
#         if_stats.insert(0, task.hostname)
#         args[5].row_presentation.append(if_stats)
#     args[1].chart_data = args[1].chart_data + '!' + args[2].chart_data
