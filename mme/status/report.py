#! coding: utf8
import os
import time
import json
import logging
import codecs
from jinja2 import Environment, FileSystemLoader
from .configer import mme_list
from .configer import BASE_PATH, HTML_REPORT_PATH


def save_report(hostname, html):
    filename = "mme_report_%s.html" % hostname
    output_file = os.path.join(HTML_REPORT_PATH, filename)
    with open(output_file,'w+', encoding='utf8') as fp:
        fp.write(html)

    return output_file

def make_report(env, template_name, **kwargs):
    tmpl = env.get_template(template_name)
    html = tmpl.render(**kwargs)

    return html

def reformat_data(data):
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

def report_api():
    from .checkers import run_task
    from .configer import mme_list

    template_dir = os.path.join(BASE_PATH, 'html_templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    task_list=[]
    for host in mme_list:
        task = run_task(hostname=host)
        task.results = reformat_data(task.results)
        task_list.append(task)
        u_con_list=range(0,11)
        html = make_report(env, 'mme_report.html', task=task,hostlist=mme_list,u_con_list=u_con_list)
        if len(html)>0:
            saved_filename=save_report(task.hostname, html)
            #print("report was saved to %s" % saved_filename)

    return task_list