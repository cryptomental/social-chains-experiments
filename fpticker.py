import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from sseclient import SSEClient


class SSEClientError(RuntimeError):
    pass


class ForexFP(object):
    URL = "http://jq.forexpf.ru/html/htmlquotes/"
    JSP_PAGE = "site.jsp"

    INDEXES_CFD = ["DJIA", "SP500", "NASD_COMP", "NASD100", "FTSE100",
                   "DAX", "AEX" "CAC40", "SMI", "RTST", "USD_INDEX"]
    STOCKS = ["GAZ_ADR", "GMK_ADR", "LUK_ADR", "ROS_ADR", "RTK_ADR",
              "SNG_ADR", "TAT_ADR", "VTB_ADR"]
    METALS = ["GOLD", "SILVER", "PLATINUM", "PALLADIUM", "ALUM",
              "COPPER", "NICKEL", "BRENT", "LIGHT"]
    RUB = ["USDRUB", "EURRUB"]
    MINI = ["NASDAQ", "SnP500"],
    CURRENCY_CFD = ["AUD/JPY", "AUD/USD", "CAD/JPY", "CHF/JPY",
                    "EUR/AUD", "EUR/CAD", "EUR/CHF", "EUR/GBP",
                    "EUR/JPY", "EUR/USD", "GBP/CHF", "GBP/JPY",
                    "GBP/USD", "USD/CAD", "USD/CHF", "USD/JPY"]
    CURRENCY_FUTURES = ["AUD_FUT", "CAD_FUT", "CHF_FUT", "EUR_FUT",
                        "GBP_FUT", "JPY_FUT"]
    INDEX_FUTURES = ["DJIA_FUT", "SP500_FUT", "NASD100_FUT", "NIK_FUT"]

    def __init__(self, sub=RUB):
        self.session = requests.session()
        s = self.session.get("%s/%s" % (ForexFP.URL, ForexFP.JSP_PAGE))

        dom = BeautifulSoup(s.text, "lxml")
        m = re.match(r".*SID=(?P<SID>\w+)&.*", dom.find("iframe")["src"])
        self.sid = m.group('SID')
        self.__subscribe(sub)

        sse_url = "%sqsse?msg=1;SID=%s" % (ForexFP.URL, self.sid)
        try:
            self.sse = SSEClient(sse_url, session=self.session)
        except HTTPError as e:
            raise SSEClientError("SSE error: %s" % e)

    def __subscribe(self, instruments):
        """
        Subscribe to FPForex financial instruments.
        This is achieved by sending a formatted POST query
        ForexFP.URL/q URL.

        :param instruments: list of instruments to subscribe to.
        :type instruments: list
        :return: -
        """
        sub = ""
        for instrument in instruments:
            sub += "S=" + instrument + ";"
        self.session.post("%s/q" % ForexFP.URL,
                          data="1;SID=%s;B=;A=;NCH=;NCHP=;%s\n" % (self.sid,
                                                                   sub))

    def stream_raw(self):
        """
        Stream subscribed instruments in raw format as received
        by SSE client.

        :return: -
        """
        for msg in self.sse:
            print(msg.data)

    def stream(self):
        """
        Stream subscribed data as dictionaries.

        :return: -
        """
        for msg in self.sse:
            it = iter(msg.data.replace("=", ";").split(";")[1:])
            print(dict(zip(it, it)))


if __name__ == "__main__":
    sub = ForexFP.STOCKS + ForexFP.METALS
    fp = ForexFP(sub)
    fp.stream()
