import calendar
from cachecontrol.heuristics import BaseHeuristic
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate
import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache


class CustomHeuristic(BaseHeuristic):

    def __init__(self, days: float = ...):
        self.days = days

    def update_headers(self, response):
        date = parsedate(response.headers['date'])
        expires = datetime(*date[:6]) + timedelta(days=self.days)
        # print(formatdate(calendar.timegm(expires.timetuple())))
        return {
            'expires': formatdate(calendar.timegm(expires.timetuple())),
            'cache-control': 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg


class CacheControlHelper(object):

    def __init__(self):
        self.sess = CacheControl(requests.session(), heuristic=CustomHeuristic(days=30), cache=FileCache('.web_cache'))
        self.exceptions = requests.exceptions

    def get(self, url, params=None, timeout=120, cookies=None, headers={'Accept': 'application/json'}):
        if cookies:
            return self.sess.get(url, params=params, timeout=timeout, cookies=cookies, headers=headers)
        else:
            return self.sess.get(url, params=params, timeout=timeout, headers=headers)

    def post(self, url, data, timeout=120, headers={'Accept': 'application/json'}):
        return self.sess.post(url, data=data, timeout=timeout, headers=headers)
