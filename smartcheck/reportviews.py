#! coding: utf-8

class BasePresentation(object):
    """Base Class for Presentation
    all the presentation should be the subClass of this.
    """

    def __init__(self):
        self.abnormal_count = 0
        self.data = []
        self.row_presentation = []
        # self.init_info()
        self.info = {}

    # def init_info(self):
    #     doclines = self.__doc__.split()
    #     self.info['name'] = doclines[0]
    #     self.info['description'] = "".join(doclines[1:])

    def __repr__(self):
        return self.__class__.__name__
