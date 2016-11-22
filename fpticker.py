import re
from pyquery import PyQuery
from sseclient import SSEClient
import requests


class SSEClientError(RuntimeError):
    pass


class ForexFP(object):
    MAIN_URL = "http://jq.forexpf.ru"
    QUOTES = "html/htmlquotes/site.jsp"

    def __init__(self):
        d = PyQuery(url="%s/%s" % (ForexFP.URL))
        m = re.match(r".*SID=(?P<SID>\w+)&.*", d('iframe').attr('src'))
        sid = m.group('SID')
        sid = "fvIf5SWR"
        sse_url = "http://jq.forexpf.ru/html/htmlquotes/qsse?msg=1;SID=%s" % sid

try:
    messages = SSEClient(sse_url)
except requests.exceptions.HTTPError as e:
    raise SSEClientError("SSE not initialized: %s" % e)

for msg in messages:
    data = msg.dump()
    print(data)


