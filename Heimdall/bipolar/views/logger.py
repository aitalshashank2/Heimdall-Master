import io
import yaml
import json
import datetime
import pytz
import hmac
import hashlib

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from bipolar.models import Log

CONFIG = "../configuration/config.yml"

with io.open(CONFIG, 'r') as stream:
    CONFIG_VARS = yaml.safe_load(stream)

SERVERSIDE_SECRET = CONFIG_VARS['SERVERSIDE']['SECRET']

@csrf_exempt
def login(request):
    
    signature = 'sha1=' + hmac.new(SERVERSIDE_SECRET.encode(), request.body, hashlib.sha1).hexdigest()

    if(request.method == "POST"):
        try:
            if(signature == request.headers["X-Bipolar-Signature"]):
                data = json.loads(request.body)
                m = datetime.datetime.strptime(data["month"], "%b").month
                t = data["time"].split(':')
                d = datetime.datetime(timezone.now().year, m, int(data["date"]), int(t[0]), int(t[1]), int(t[2]))
                log = Log(time=d, host=data["host"], user=data["user"], ip=data["ip"], port=data["port"], activity=True)
                log.save()

                return HttpResponse("Logged")
            else:
                return HttpResponseForbidden("Invalid Bipolar Signature")
        except KeyError:
            return HttpResponseForbidden("Bipolar Signature Missing")
    else:
        return HttpResponseBadRequest("Only POST request allowed")
        

@csrf_exempt
def logout(request):

    signature = 'sha1=' + hmac.new(SERVERSIDE_SECRET.encode(), request.body, hashlib.sha1).hexdigest()

    if(request.method == "POST"):
        try:
            if(signature == request.headers["X-Bipolar-Signature"]):
                data = json.loads(request.body)
                m = datetime.datetime.strptime(data["month"], "%b").month
                t = data["time"].split(':')
                d = datetime.datetime(timezone.now().year, m, int(data["date"]), int(t[0]), int(t[1]), int(t[2]))
                log = Log(time=d, host=data["host"], user=data["user"], ip=data["ip"], port=data["port"], activity=False)
                log.save()

                return HttpResponse("Logged")
            else:
                return HttpResponseForbidden("Invalid Bipolar Signature")
        except KeyError:
            return HttpResponseForbidden("Bipolar Signature Missing")
    else:
        return HttpResponseBadRequest("Only POST request allowed")