import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *
import time
import pandas as pd
import sqlite3

#form_class = uic.loadUiType("pytrader.ui")[0]

class TR_Practice(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        self.kiwoom.trp20002 = {'code': [], 'name': [], 'cur_price': [], 'volume': [], 'high_price': [], 'low_price': []}
        self.kiwoom.trp20006 = {'date': [], 'cur_price': [], 'volume': []}
        self.kiwoom.trp20007 = {'date': [], 'cur_price': [], 'high_price': [], 'low_price': [], 'volume': []}
        self.kiwoom.trp50036 = {'date': [], 'yesterday_end_price': [], 'gift_historic_variability': []}
        self.kiwoom.trp50037 = {'date': [], 'kospi_200_index': []}

    def business_type_juga(self):
        # market_gubun = input("market_gubun : ")
        # business_code = input("business_code : ")

        # self.kiwoom.set_input_value("시장구분", market_gubun)
        # self.kiwoom.set_input_value("업종코드", business_code)

        self.kiwoom.set_input_value("시장구분", "0")
        self.kiwoom.set_input_value("업종코드", "001")
        self.kiwoom.comm_rq_data("OPT20002_req", "OPT20002", 0, "0213")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("시장구분", "0")
            self.kiwoom.set_input_value("업종코드", "001")
            self.kiwoom.comm_rq_data("OPT20002_req", "OPT20002", 2, "0213")

        trp20002_df = pd.DataFrame(self.kiwoom.trp20002, columns = ["code", "name", "cur_price", "volume", "high_price", "low_price"], index = self.kiwoom.trp20002["code"])
        trp20002_df.to_csv('C:\\workplace\\atm_project\\tr20002.csv', encoding='ms949')
        #print(trp20002_df)
        return trp20002_df

    def business_ilbong_load(self):
        # market_gubun = input("market_gubun : ")
        # business_code = input("business_code : ")

        # self.kiwoom.set_input_value("시장구분", market_gubun)
        # self.kiwoom.set_input_value("업종코드", business_code)

        self.kiwoom.set_input_value("업종코드", "001")
        self.kiwoom.set_input_value("기준일자", "20190218")
        self.kiwoom.comm_rq_data("opt20006_req", "opt20006", 0, "0202")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("업종코드", "001")
            self.kiwoom.set_input_value("기준일자", "20190218")
            self.kiwoom.comm_rq_data("opt20006_req", "opt20006", 2, "0202")

        trp20006_df = pd.DataFrame(self.kiwoom.trp20006, columns = ["cur_price", "volume"], index = self.kiwoom.trp20006["date"])
        trp20006_df.to_csv('C:\\workplace\\atm_project\\tr20006.csv', encoding='ms949')
        #print(trp20006_df)
        return trp20006_df

    def business_jubong_load(self):
        business_code = input("business_code : ")
        standard_date = input("standard_date : ")
        #스트링 변환 넣어주기
        #상동 *2

        self.kiwoom.set_input_value("업종코드", business_code)
        self.kiwoom.set_input_value("기준일자", standard_date)
        self.kiwoom.comm_rq_data("opt20007_req", "opt20007", 0, "0202")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("업종코드", business_code)
            self.kiwoom.set_input_value("기준일자", standard_date)
            self.kiwoom.comm_rq_data("opt20007_req", "opt20007", 2, "0202")

        trp20007_df = pd.DataFrame(self.kiwoom.trp20007, columns = ["cur_price", "high_price", "low_price", "volume"], index = self.kiwoom.trp20007["date"])
        trp20007_df.to_csv('C:\\workplace\\atm_project\\tr20007.csv', encoding='ms949')
        print(trp20007_df)
        return trp20007_df

    def major_index_variability_chart(self):
        # event_code = input("event_code : ")
        # standard_date = input("standard_date : ")
        # period = input("period : ")
        # chart_gubun = input("chart_gubun : ")
        event_code = '_JP#NI225'
        standard_date = '20190220'
        period = 2
        chart_gubun = 0

        self.kiwoom.set_input_value("종목코드", str(event_code))
        self.kiwoom.set_input_value("기준일자", str(standard_date))
        self.kiwoom.set_input_value("기간", period)
        self.kiwoom.set_input_value("차트구분", chart_gubun)
        self.kiwoom.comm_rq_data("opt_50036_req", "OPT50036", 0, "0733")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", str(event_code))
            self.kiwoom.set_input_value("기준일자", str(standard_date))
            self.kiwoom.set_input_value("기간", period)
            self.kiwoom.set_input_value("차트구분", chart_gubun)
            self.kiwoom.comm_rq_data("OPT50036_req", "OPT50036", 2, "0733")

        trp50036_df = pd.DataFrame(self.kiwoom.trp50036, columns = ["date", "yesterday_end_price", "gift_historic_variability"], index = self.kiwoom.trp50036["date"])
        trp50036_df.to_csv('C:\\workplace\\atm_project\\tr50036.csv', encoding='ms949')
        print(trp50036_df)
        return trp50036_df

    def kospi200_index_load(self):
        event_code = input("event_code : ")
        standard_date = input("standard_date : ")
        event_code = str(event_code)
        standard_date = str(standard_date)

        self.kiwoom.set_input_value("종목코드", event_code)
        self.kiwoom.set_input_value("기준일자", standard_date)
        self.kiwoom.comm_rq_data("opt50037_req", "opt50037", 0, "0221")

        while self.kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            self.kiwoom.set_input_value("종목코드", event_code)
            self.kiwoom.set_input_value("기준일자", standard_date)
            self.kiwoom.comm_rq_data("opt50037_req", "opt50037", 2, "0221")

        trp50037_df = pd.DataFrame(self.kiwoom.trp50037, columns = ["kospi_200_index"], index = self.kiwoom.trp50037["date"])
        trp50037_df.to_csv('C:\\workplace\\atm_project\\tr50037.csv', encoding='ms949')
        print(trp50037_df)
        return trp50037_df

if __name__ == "__main__":
    app = QApplication(sys.argv)
    trp = TR_Practice()
    #trp.business_type_juga()
    #trp.business_ilbong_load()
    # trp.business_jubong_load()
    #trp.major_index_variability_chart()
    trp.kospi200_index_load()
    app.exec_()