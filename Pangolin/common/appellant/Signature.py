"""
-------------------------------------------------
        Author :    albertz.yang
        contact:    albertz.yang@poloniex.com
      File Name：   Signature
           date：   2022/3/22 6:57 下午
   Description :
-------------------------------------------------
   Change Activity:
                   2022/3/22:
-------------------------------------------------
"""

import hashlib
import urllib
import urllib.parse
import time
import hmac
import base64
import json, re


class Signature:
    """
    Desc：创建签名
    """

    def __init__(self, apikey=None, keySecret=None, password=None, **kwargs):
        self.__apikey = apikey
        self.__keySecret = keySecret
        self.__password = password
        self.__time = int(time.time() * 1000)
        # 将时间戳转为毫秒，需要参与签名

    def create_sign(self, params: dict, method, path, system):
        timestamp = self.__time
        sign_params = self.get_spot_sign_params(params, method, path, timestamp) \
            if system.upper() == "SPOT" else \
            self.get_future_sign_params(params, method, path, timestamp)
        # print(encode_params)
        sign_params = sign_params.encode(encoding="UTF8")

        print(f"----{system}系统签名参数---", sign_params)
        keySecret = self.__keySecret.encode(encoding="UTF8")
        # print("---私钥---", keySecret)
        digest = hmac.new(
            keySecret,
            sign_params,
            digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        # print("---生成的签名---", signature)

        return signature, timestamp

    def get_spot_sign_params(self, params: dict, method, path, timestamp):
        """获取spot系统签名参数"""
        if method not in ["post", "delete", "put"]:
            params.update({"signTimestamp": timestamp})
            sorted_params = sorted(
                params.items(),
                key=lambda d: d[0],
                reverse=False)
            if method in ["ws", "wss"]:
                path = "/ws"
                method = "get"
                sorted_params = {"signTimestamp": timestamp}
            encode_params = urllib.parse.urlencode(sorted_params)

        elif re.compile(r"\d+").findall(path) and not params:
            encode_params = f"signTimestamp={timestamp}"
        else:
            encode_params = f"requestBody={json.dumps(params)}&signTimestamp={timestamp}"

        sign_params_first = [method.upper(), path, encode_params]
        sign_params_second = "\n".join(sign_params_first)

        return sign_params_second

    def get_future_sign_params(self, params, method, path, timestamp):
        """获取期货系统签名参数"""
        body = ""
        if not params:
            pass
        elif method.lower() in ["post"]:
            body = json.dumps(params)
        elif method.lower() in ["delete", "get"]:
            params = [f'{key}={value}' for key, value in params.items()]
            params = '&'.join(params)
            path += '?' + params

        str_to_sign = str(timestamp) + method.upper() + path + body
        return str_to_sign


