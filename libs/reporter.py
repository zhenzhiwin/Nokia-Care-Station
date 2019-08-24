#! coding: utf-8

import os
import logging

logger = logging.getLogger('reporter')

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


def reporter_factory(conf):
    reporter_list = [TextReporter]

    for rpt in reporter_list:
        if rpt.__name__ == conf.reporter_name:
            return rpt(conf)

    raise ValueError("No Such Reporter: %s" % conf.report_name)
