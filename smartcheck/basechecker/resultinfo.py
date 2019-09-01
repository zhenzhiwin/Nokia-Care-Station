#! coding: utf-8
"""此模块包含检查项基类的实现。
ResultInfo      保存检查结果和相关信息的类，用于传递信息给其他模块。比如reportor模块

"""

import json

class ResultInfo(object):
    """Class for storing the info of check result.
    
  参数说明：
    hostname:       网元名称
    name:           检查结果名称。如：MME单元状态检查
    status:         检查结果的状态。有三个状态：UNKNOWN，PASSED，FAILED
    description:    检查结果的详细描述。如：检查mme所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元的数量
    info:           有关检查结果的附加说明。
    error:          如果检查出错，相关的错误信息将存放在此
    data:           保存log分析所提取的全部数据。

    """

    def __init__(self, **kwargs):
        self.hostname = kwargs.get('hostname', '')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.status = kwargs.get('status','UNKNOWN')
        self.stats=kwargs.get('stats')
        self.data=kwargs.get('data')
        self.info = ''
        self.error = ''
        

    def to_json(self, indent=None):
        """translate the result data to json format.
        """
        return json.dumps(self.__dict__, indent=indent)

    def __repr__(self):
        return "ResultInfo({hostname},{name})".format(**self.__dict__)