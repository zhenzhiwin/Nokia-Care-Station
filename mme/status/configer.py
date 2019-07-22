#! coding: utf8
import os

BASE_PATH = os.path.split(os.path.abspath(__file__))[0]

##log文件保存路径
# LOGFILE_PATH = "/tmp/cache/"
LOGFILE_PATH = os.path.abspath(os.path.join(os.getcwd(), "../smartcare/log"))  # window目录

# 静态html报告保存路径
# HTML_REPORT_PATH = "/opt/smartcare/reports"
HTML_REPORT_PATH = os.path.abspath(os.path.join(os.getcwd(), "../smartcare/templates"))

checking_rules = {
    'cpuload': [25, 80, 90],
    'alarmlevel':['*','**','***']
}

mme_list = [
    "HZMME45BNK",
    "HZMME46BNK",
    "HZMME47BNK",
    "HZMME48BNK",
    "HZMME49BNK",
    "HZMME50BNK",
    "HZMME51BNK",
    "HZMME52BNK",
    "HZMME53BNK",
    "HZMME54BNK",
    "HZMME55BNK",
    "HZMME56BNK",
    "HZMME57BNK",
    "HZMME72BNK",
    "HZMME73BNK",
    "HZMME89BNK",
    "HZMME105BNK",
    "HZMME106BNK",
]
