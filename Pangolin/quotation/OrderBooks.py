"""
-------------------------------------------------
        Author :    albertz.king
        contact:    albertz.king@bitget.com
      File Name：   OrderBooks.py
           date：   2023/12/1
   Description :  铺单
-------------------------------------------------
   Change Activity:
                   2023/12/01 22:06:
-------------------------------------------------
"""
import math, time
from decimal import Decimal
from threading import Thread
from common.constants import Constants
from common.GetDictData import GetDictData as Gda
from common.TransAdapter import TranAdapter as Router


class OrderBooks:

    def __init__(self):
        pass

    @classmethod
    def drape_order_book(cls, env=None, system=None, symbol=None,
                         times=1, quantity=0, notch=100, **kwargs):
        """
            铺单
        :param env: 环境
        :param system: 交易类型
        :param symbol: 币对
        :param times: 铺单次数
        :param quantity: 每档委托数量
        :param notch: 买卖方各档位
        :return:
        """
        curr_price = cls().__get_trade_price(env, system, symbol)
        if isinstance(curr_price, dict):
            return curr_price
        config = cls().__get_symbol_price_scale(env, system, symbol)
        if not isinstance(config, dict):
            return {
                "code": "20002",
                "data": [],
                "msg": config
            }
        else:
            min_amount = config["min_amount"]
            quantity_scale = config["quantity_scale"]
            quantity = math.ceil(Decimal(str(quantity)) / Decimal(str(1 / (10 ** quantity_scale)))) * Decimal(str(1 / (10 ** quantity_scale)))
            min_count = math.ceil(min_amount / curr_price / Decimal(str(1 / (10 ** quantity_scale)))) * Decimal(str(1 / (10 ** quantity_scale)))
            quantity = Decimal(str(max(min_count, quantity)))
        while times:
            buy = cls().__place_order(env, system, symbol, curr_price, config["price_scale"], quantity, notch, "buy")
            sell = cls().__place_order(env, system, symbol, curr_price, config["price_scale"], quantity, notch, "sell")
            times -= 1

    def __place_order(self, env, system, symbol, curr_price, scale, quantity, notch, direction):

        while notch:
            req_data = {
                "symbol": symbol,
                "side": direction,
                "orderType": "limit",
                "force": "gtc",
                "price": curr_price,
                "size": quantity,
                "clientOid": f"{str(time.time() * 10 ** 6)[:13]}"
            }
            res = Router.common_send(req_data, "place")
            assert Gda.get_single_value('code', res.response) == "00000", \
                Gda.get_single_value('message', res.response)
            if direction == "buy":
                curr_price -= scale
            else:
                curr_price += scale
            notch -= 1

    def __get_trade_price(self, env, system, symbol):
        """获取最新成交价"""
        req_data = {
            "symbol": symbol,
        }
        res = Router.common_send(req_data, "ticker")
        if Gda.get_single_value("code", res.response) != "00000":
            return res.response
        curr_price = Decimal(str(Gda.get_single_value("lastPr", res)))

        return curr_price

    def __get_symbol_price_scale(self, env, system, symbol):
        """获取币对价格精度和最小挂单数量"""
        req_data = {
            "env": env,
            "system": system,
            "symbol": symbol,
        }
        res = Router.common_send(req_data, "symbol")
        if Gda.get_single_value("code", res) != "00000":
            return Gda.get_single_value("msg", res)
        price_scale = Decimal(str(Gda.get_single_value("pricePrecision", res)
                                  if system == "spot" else
                                  Gda.get_single_value("pricePlace", res)))
        min_amount = Decimal(str(Gda.get_single_value("minTradeUSDT", res)
                                   if system == "spot" else
                                   Gda.get_single_value("minTradeUSDT", res)))
        quantity_scale = Decimal(str(Gda.get_single_value("quantityPrecision", res)
                                     if system == "spot" else
                                     Gda.get_single_value("volumePlace", res)))

        return {
            "min_amount": min_amount,
            "price_scale": price_scale,
            "quantity_scale": quantity_scale,
        }


if __name__ == '__main__':
    print(OrderBooks().drape_order_book("dev", "spot", "BCHUSDT"))
