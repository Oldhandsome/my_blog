from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import time
from django.http import JsonResponse


class MyThrottle(MiddlewareMixin):
    # 限流的类型
    scope = settings.THROTTLE_RATES.get('middle')
    ACCESS_IPADDR = {}

    def process_request(self, request):
        access_limit = settings.ACCESS_LIMITION
        ip = request.META.get("REMOTE_ADDR")
        if ip not in access_limit:
            if ip not in self.ACCESS_IPADDR:
                self.ACCESS_IPADDR[ip] = []
            history = self.ACCESS_IPADDR[ip]
            now = time.time()
            # 列表的弹出 是在尾部
            while history and now - history[-1] > 60:
                history.pop()
            history.insert(0, now)
            if len(history) > self.scope:
                return JsonResponse({'code': 2000, 'data': None, 'message': '您的访问过于频繁'})
