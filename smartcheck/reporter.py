#! coding: utf-8

import os
import logging
from jinja2 import Environment, FileSystemLoader
from .utils import read_task_conf

logger = logging.getLogger('reporter')
conf = read_task_conf(os.path.abspath(os.path.join(os.getcwd(), "./mme_task.conf")))


class NoSuchReporter(Exception):
    pass


class BaseReporter(object):
    """
    """

    def __init__(self, config=None):
        self.name = ''
        self.output_path = ''

        if config:
            self.output_path = config.report_path

    def make(self, task, tempalte=None):
        raise NotImplemented


class TextReporter(BaseReporter):
    def make(self, task):
        content = []
        content.append("\n===== Result for host: %s =====" % task.hostname)
        for result in task.results:
            content.append("\n-- CheckItem: %s" % result.name)
            content.append("\n-- ResultInfo: {}".format(result.to_json(indent=2)))

        report_filename = os.path.join(self.output_path, 'text_report_%s.md' % task.hostname)
        with open(report_filename, 'w+') as fp:
            fp.writelines(content)

        logger.info(f"report was saved to:{self.output_path}")

        return content


class HtmlReporter(BaseReporter):
    def make(self, task):
        env = Environment(loader=FileSystemLoader(os.path.abspath('./mme/status/html_templates')))
        unit_html = self.make_report(env, 'mme_report.html', task=task, hostlist=conf.NeInfo.ne_list,
                                     u_con_list=range(0, 11))
        alarm_html = self.make_report(env, 'alarms_report.html', task=task, hostlist=conf.NeInfo.ne_list,
                                      u_con_list=range(0, 11))
        alarmhist_html = self.make_report(env, 'alarmhist_report.html', task=task, hostlist=conf.NeInfo.ne_list,
                                          u_con_list=range(0, 11))
        if len(unit_html) > 0:
            self.save_report(task.hostname, unit_html, 'mme_report_')
            # print("report was saved to %s" % saved_filename)
        if len(alarm_html) > 0:
            self.save_report(task.hostname, alarm_html, 'alarms_report_')
        if len(alarmhist_html) > 0:
            self.save_report(task.hostname, alarmhist_html, 'alarmhist_report_')

    def save_report(self, hostname, html, html_name):
        filename = html_name + hostname + '.html'
        output_file = os.path.join(os.path.abspath('./templates'), filename)
        with open(output_file, 'w+', encoding='utf8') as fp:
            fp.write(html)

        return output_file

    def make_report(self, env, template_name, **kwargs):
        tmpl = env.get_template(template_name)
        html = tmpl.render(**kwargs)

        return html

    def reformat_data(self, data):
        for r in data:
            if r.status.lower() == "ok":
                r.panel_status = "panel-success"
                r.status_icon = "fa-check-circle"
                r.status_color = 'green'
            else:
                r.panel_status = "panel-warning"
                r.status_icon = "fa-exclamation-circle"
                r.status_color = 'red'
        return data


def reporter_factory(conf):
    reporter_list = [TextReporter, HtmlReporter]
    rpt_list = []
    for rpt in reporter_list:
        if rpt.__name__ in conf.reporter_name:
            rpt_list.append(rpt(conf))
    return rpt_list

    raise ValueError("No Such Reporter: %s" % conf.report_name)
