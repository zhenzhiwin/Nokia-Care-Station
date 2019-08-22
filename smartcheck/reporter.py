#! coding: utf-8

import os
import logging

class Reporter(object):
    """
    """
    def __init__(self):
        pass

    def make(self, task, tempalte=None):
        content = []
        content.append("\n===== Result for host: %s =====" % task.hostname)
        for result in task.results:
            content.append("\n-- CheckItem: %s" % result.name)
            content.append("\n-- ResultInfo: {}".format(result.to_json(indent=2)))

        return content        