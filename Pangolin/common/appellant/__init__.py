import json
from .Headers import Headers
from .ReplaceMsg import ReplaceMsg
from .RequestAPI import RequestAPI


class OutObj:

    def __init__(self, trans_name=None, request=None, response=None, data=None):
        self.trans_name = trans_name
        self.request = request
        self.response = response
        self.data = data
        self.resq = dict()
        self.data_format()

    def data_format(self):
        try:
            if isinstance(self.request, str):
                self.request = json.loads(self.request)

            if isinstance(self.response, str):
                self.response = json.loads(self.response)

            if isinstance(self.data, str):
                self.data = json.loads(self.data)

            self.resq.update({
                "request": self.request,
                "response": self.response
            })

        except:
            pass

        # finally:   todo 对返回的xml做格式化处理
        #     if isinstance(self.request, html):
        #         self.request = json.loads(self.request)
