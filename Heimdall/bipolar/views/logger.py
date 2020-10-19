import json
import datetime
import pytz

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from bipolar.models import Log

@csrf_exempt
def login(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        m = datetime.datetime.strptime(data["month"], "%b").month
        t = data["time"].split(':')
        d = datetime.datetime(timezone.now().year, m, int(data["date"]), int(t[0]), int(t[1]), int(t[2]))
        log = Log(time=d, host=data["host"], user=data["user"], ip=data["ip"], port=data["port"], activity=True)
        log.save()

        return HttpResponse("Logged")
    else:
        return HttpResponseBadRequest("Only POST request allowed")
        

@csrf_exempt
def logout(request):
    if(request.method == "POST"):
        data = json.loads(request.body)
        m = datetime.datetime.strptime(data["month"], "%b").month
        t = data["time"].split(':')
        d = datetime.datetime(timezone.now().year, m, int(data["date"]), int(t[0]), int(t[1]), int(t[2]))
        log = Log(time=d, host=data["host"], user=data["user"], ip=data["ip"], port=data["port"], activity=False)
        log.save()

        return HttpResponse("Logged")
    else:
        return HttpResponseBadRequest("Only POST request allowed")